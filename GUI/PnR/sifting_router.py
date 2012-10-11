#! /usr/bin/env python
from Drawing_Object import Drawing_Object
import hypernet
import pprint

class Trace_Router:
    """ Sifting Router. """

    def __init__(self):
        self.obj_dict = {}
        self.port_layer_dict = {}
        self.glue_points = {}
        self.G = None

    def set_object_dict(self, obj_dict):
        self.obj_dict = obj_dict

    def set_graph(self, g):
        self.G = g

    def run(self):
        trace_id = 0
        self._build_port_layer_dict()
        self._determine_glue_points()

        #print self.G.display()
        
        # Build up drawing objects, and their hypernets
        #  All connections with the same net name in the same layer will be
        # collated in a single Hypernet object.
        for i_layer in self.G.edges:
            track = 1
            hypernet_dict = {}
            for e in self.G.edges.get(i_layer, []):
                if e.name not in hypernet_dict:
                    name = 'hypernet_%d' %(trace_id)
                    drawobj = Drawing_Object( name=name,
                        parent=None,
                        label=e.name,
                        obj_type='hypernet' )

                    hnet = hypernet.Hypernet(e.name)
                    hnet.set_track(track)
                    drawobj.set_hypernet(hnet)

                    hypernet_dict[e.name] = hnet
                    self.obj_dict[name] = drawobj
                    track += 1
                    trace_id += 1
                else:
                    hnet = hypernet_dict[e.name]

                # add connection to hypernet
                #print "+%d : %s.%s -> %s.%s" % (i_layer, e.source, e.source_port,
                #    e.target, e.target_port )
                #print e.source
                start_point = self.glue_points[(e.source, e.source_port)]
                end_point   = self.glue_points[(e.target, e.target_port)]
                hnet.add_connection(start_point, end_point)

            assign_tracks(hypernet_dict.values())

    #
    # Drawing helper functions
    #
    def _build_port_layer_dict(self):
        """ So the layer of a port can be looked up. """
        self.port_layer_dict = {}
        for i_layer in self.G.vertices:
            for v in self.G.vertices.get(i_layer,[]):
                for port in v.get_input_ports():
                    self.port_layer_dict[(v.name, port.name)] = i_layer-1
                for port in v.get_output_ports():
                    self.port_layer_dict[(v.name, port.name)] = i_layer


    def _determine_glue_points(self):
        """ Find glue Points for pins on instantiations."""

        self.glue_points = {}
        for drawing_obj in self.obj_dict.values():
            drawing_obj.build_glue_points_dict()

            if drawing_obj.obj_type == 'hypernet':
                print "Woops - shouldn't have hypernets at this stage..."

            for pin,position in drawing_obj.glue_points.iteritems():
                self.glue_points[pin] = position

#
# Sifting functions
#
def _build_crossing_matrix(hypernets):
    crossing_matrix = {}

    # list netnames of the hyperedges in the collection
    netnames = []
    for hnet in hypernets:
        netnames.append( hnet.netname )

    # set origin of track axes so we can draw feedback nodes properly
    x_origin = 100000
    #print '-----------------------'
    for hnet in hypernets:
        if hnet.start_point[0] < x_origin:
            #print "Info (hnet %s)" % (hnet.netname ),
            #print "setting a new track origin", hnet.start_point[0]
            x_origin = hnet.start_point[0]
    for hnet in hypernets:
        hnet.x_origin = x_origin
        
    # initialise the crossing matrix. The cii = 0 is set here
    d1 = {}
    for hn in netnames:
        d1[hn] = 0
    for hn in netnames:
        crossing_matrix[hn] = dict(d1)

    # fill in the crossing matrix
    for hn1 in hypernets:
        for hn2 in hypernets:
            if hn1.netname == hn2.netname:
                continue

            # hn1 is above hn2
            hn1.set_track(1)
            hn2.set_track(2)
            crossings = hypernet.count_crossovers(hn1, hn2)
            crossing_matrix[hn1.netname][hn2.netname] = crossings

            # hn2 is above hn1
            hn1.set_track(2)
            hn2.set_track(1)
            crossings = hypernet.count_crossovers(hn1, hn2)
            crossing_matrix[hn2.netname][hn1.netname] = crossings

    return crossing_matrix

def assign_tracks(hypernets):
    """ greedy assign. """

    crossing_matrix = _build_crossing_matrix(hypernets)
    unassigned_hypernets = list(hypernets)

    for k in range( 1, len(hypernets)+1 ):
        mincost = 10e6
        for hn_i in unassigned_hypernets:
            cost = 0
            for hn_j in unassigned_hypernets:
                cost += crossing_matrix[hn_i.netname][hn_j.netname]
            if cost < mincost:
                best = hn_i
                mincost = cost

        unassigned_hypernets.remove(best)
        best.set_track(k)
