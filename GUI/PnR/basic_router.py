#! /usr/bin/env python

from Drawing_Object import Drawing_Object
import pprint

class Trace_Router:

    def __init__(self):
        self.obj_dict = {}
        self.connections = []
        self.glue_points = {}
        
    def set_object_dict(self, obj_dict):
        self.obj_dict = obj_dict
        
    def set_connections(self, conns):
        self.connections = conns

    def run(self):
        trace_id = 0
        self._determine_glue_points()
        
        for connection in self.connections:

            conn1,conn2 = connection
            #conn1 = conn1.replace('_iport.','')
            #conn1 = conn1.replace('_oport.','')                                             
            #conn2 = conn2.replace('_iport.','')
            #conn2 = conn2.replace('_oport.','')   
            print "C1:", conn1
            print "C2:", conn2
            
            # Create the flightline
            name = 'conn_%d' %(trace_id)
            drawobj = Drawing_Object( name=name,
                                      parent=None,
                                      label=conn1,
                                      obj_type='conn' )
            
            drawobj.startpt  = self.glue_points[conn1]
            drawobj.endpt    = self.glue_points[conn2]
            self.obj_dict[name] = drawobj
            trace_id += 1
            
    def _determine_glue_points(self):
        """ Find glue Points for pins on instantiations."""
        
        self.glue_points = {}
        for drawing_obj in self.obj_dict.values():
            drawing_obj.build_glue_points_dict()
            
            if drawing_obj.obj_type == 'hypernet':
                print "Woops - shouldn't have hypernets at this stage..."
             
            for pin,position in drawing_obj.glue_points.iteritems():
                self.glue_points[pin] = position

        pprint.pprint(self.glue_points)

