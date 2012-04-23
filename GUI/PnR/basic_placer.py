#! /usr/bin/env

from wx import Point
from wx import Size

X_DELTA = 40
Y_DELTA = 20

class Placer:

    def __init__(self):
        self.G = None
        self.obj_dict = None
        
    def set_graph(self, G):
        self.G = G
        
    def set_object_dict(self, obj_dict):
        self.obj_dict = obj_dict
        
    def run(self):
        next_x = 100  # allow some LHS space for port names
        layers = self.G.vertices.keys()
        layers.sort()
        for i_layer in layers:
            layer = self.G.vertices[i_layer]
            next_y = 10
            x_hist = []
            for block in layer:
                obj = self.obj_dict[block.get_name()]
                obj.SetPosition( Point(next_x, next_y) )
                
                (x,y) = obj.getSize()
                next_y += y + Y_DELTA
                x_hist.append(x)
                
            next_x += max(x_hist) + X_DELTA 
                            
    def resize_passthrus(self):
        """ Resize each of the passthrus in each layer.
        Should match the widest block in that layer
        """
        layers = self.G.vertices.keys()
        layers.sort()
        for i_layer in layers:
            layer = self.G.vertices[i_layer]
            # find widest object in the layer
            names = [ block.get_name() for block in layer ]
            widths = [ self._get_width(name) for name in names ]
            max_width = max(widths)
            
            # set all passthru objects to match widest object
            dummies = [ name for name in names if block.type == 'dummy' ]
            for dummy in dummies:
                obj = self.obj_dict[dummy]
                obj.endpt   = Point(max_width,0)

                
    def _get_width(self, name):
        """ Lookup the drawing object dict to get the width of the named object."""
        width, height = self.obj_dict[name].getSize()
        return width
             
