""" Hyperedges

We'll be using hyperedges for drawing the connections in the circuit. And
we'll use the scheme in [] to store them. 

Hyperedges are modeled as a list of hyperedge segments. For the moment, I'm 
only going deal with 1:n connections.

"""

SEPARATION = 5

class Segment(object):
    """ Hyperedge Segment Class. 
    Stores the co-ordinate of the segment, and a list of segments that
    lead out from it.
    """
    def __init__(self, point):
        self.point = point
        self.children = []

    def add_child(self, child):
        """ Add a Child Segment. """
        self.children.append(child)
        return child
        
    def get_children(self):
        """ Return a list of Segments that flow from this segment. """
        return self.children
        
        
class Hyperedge(object):
    """ Hyperedge Class.
    Modeled as a tree of hyperedge Segments starting from a root segment.
    
    Also includes one or two methods to traverse the hyperedge tree:
    * returns line segments for drawing and crossover counting
    """ 
    
    def __init__(self):
        self.netname = ''
        self.root = None
        self.track = 1
        
    def add_connection(self, start_point, end_point ):
        """ Add hyperedge segments to connect start_point to end_point. """
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
        x2, y2 = 0, y1
        
        segments = self.root.get_children()
        segments = segments[0].get_children()
        x2 = segments[0].point
        yield (x1,y1), (x2,y2)
        
        orientation = 'vertical'
        for segment in segments.get_children():
            point = self._walk_tree(segment, orientation)
            yield line
            
    def _walk_tree(self, segment, orientation):
        """ Walk the Segment tree, breadth first."""
        if segment.get_children():
            for child in segments:
                self._walk_tree(child)
        
    def __str__(self):
        """ Return a string representation of the hyperedge. """
        gen = self.ilines()
        _str = []
        for line in gen:
            _str.append(line)
            
        return '\n'.join(_str)
        
    def __repr__(self):
        return self.__str__()
        
       
