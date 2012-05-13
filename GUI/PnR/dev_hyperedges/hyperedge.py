""" Hyperedge Stuff"""

SEPARATION = 5

class Segment(object):
    def __init__(self, point):
        self.point = point
        self.children = []
        
    def add_child(self, child):
        self.children.append(child)
        return child
        
    def get_children(self):
        return self.children
        
        
class Hyperedge(object):

    def __init__(self):
        self.netname = ''
        self.root = None
        self.track = 1
        
    def add_connection(self, start_point, end_point ):
        """ """
        x1,y1 = start_point
        x2,y2 = end_point
        
        # initial point
        self.root = Segment(x1)
        tip = self.root.add_child( Segment(y1) )
        
        # vertical segment
        vertical = tip.add_child( Segment(self.track * SEPARATION) )
        
        # end point
        a = vertical.add_child(Segment(y2))
        b = a.add_child(Segment(x2))
        
    def ilines(self):
        """ Return an iterator to return the lines in the hyperedge"""
        x1 = self.root.point
        y1 = self.root.get_children()[0].point
        yield (x1,y1), (0,0)
        
    def display(self):
        gen = self.ilines()
        for line in gen:
            print line
            
        
        
     
       
