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
        for layer in self.G.vertices:
            next_y = 10
            x_hist = []
            for block in layer:
                obj = self.obj_dict[block.name]
                obj.SetPosition( Point(next_x, next_y) )
                
                (x,y) = obj.getSize()
                next_y += y + Y_DELTA
                x_hist.append(x)
                
            next_x += max(x_hist) + X_DELTA 
                            
        

