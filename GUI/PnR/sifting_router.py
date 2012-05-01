#! /usr/bin/env python
from Drawing_Object import Drawing_Object

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

        for i_layer in self.G.edges:
            track = 0
            for e in self.G.edges.get(i_layer, []):
                name = 'conn_%d' %(trace_id)
                drawobj = Drawing_Object( name=name,
                    parent=None,
                    label=e.net,
                    obj_type='hypernet' )
                    
                # Get start point
                start_point = self.glue_points[(e.source, e.source_port)]
                end_point   = self.glue_points[(e.target, e.target_port)]

                # Midway point - this is the x co-ord for the horizontal section
                drawobj.horizontal_origin = ( ( ( end_point.x - start_point.x ) / 2 ) 
                                               + start_point.x )

                drawobj.hypernet_tree = [ start_point.x, start_point.y, 
                                          0,  # horizontal section position
                                          end_point.y, end_point.x ]
                                          
                drawobj.track = track
                drawobj.update_horizontal_position()
                
                self.obj_dict[name] = drawobj
                track += 1
                trace_id += 1
                
    
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
        
