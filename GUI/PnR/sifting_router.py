#! /usr/bin/env python
from Drawing_Object import Drawing_Object
import hypernet

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

        # Build up drawing objects, and their hypernets
        #  All connections with the same net name will be collated in a
        # single Hypernet object.
        for i_layer in self.G.edges:
            track = 1
            hypernet_dict = {}
            for e in self.G.edges.get(i_layer, []):
            
                if e not in hypernet_dict:
                    name = 'conn_%d' %(trace_id)
                    drawobj = Drawing_Object( name=name,
                        parent=None,
                        label=e.net,
                        obj_type='hypernet' )
                    
                    hnet = hypernet.Hypernet(name)
                    hnet.set_track(track)
                    drawobj.set_hypernet(hnet)
                    
                    hypernet_dict[e] = hnet
                    self.obj_dict[name] = drawobj
                    track += 1                    
                    trace_id += 1
                else:
                    hnet = hypernet_dict[e]
                                        
                # add connection to hypernet
                start_point = self.glue_points[(e.source, e.source_port)]
                end_point   = self.glue_points[(e.target, e.target_port)]
                hnet.add_connection(start_point, end_point)

    
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
        
