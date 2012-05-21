""" Hyperedges

We'll be using hyperedges for drawing the connections in the circuit. For the
moment, I'm only going deal with 1:n connections.

I'll want to do a few things with a hyperedge:
* traverse it and return line segments
* tweak the co-ordinate of the vertical segment
* build a hyperedge, given some normal graph edges, or maybe target
  co-ordinates.

"""

SEPARATION = 5

        
class Hyperedge(object):
    """ Hyperedge Class.
    
    Also includes one or two methods to traverse the hyperedge tree:
    * returns line segments for drawing and crossover counting
    """ 
    
    def __init__(self):
        self.netname = ''
        self.track = 1
        
        self.start_point = None
        self.end_points = []
        self.vertical = self.track * SEPARATION
       
    def add_connection(self, start_point, end_point ):
        """ Add hyperedge to connect start_point to end_point.
        All edges for this hyperedge must have the same start point. """
        
        if self.start_point == None:
            self.start_point = start_point
        elif start_point != self.start_point:
            print "Warning: Hyperedge connection start co-ordinate doesn't match."""
            print self.start_point, start_point
            return
            
        self.end_points.append(end_point)
        
        # initial point
        
    def set_track(self, track_num):
        """ Set the track number of the vertical segment. """
        if track_num <= 0:
            print "Bad track id for vertical segment"
            return
        self.track = track_num
        
    def ilines(self):
        """ Return an iterator to return the lines in the hyperedge"""
        x_vertical = self.track * SEPARATION
        
        # 1st line is from source out to the vertical
        yield self.start_point, ( x_vertical, self.start_point[1] )
        
        # 2nd line is the vertical
        ys_vertical = list(zip(*self.end_points)[1])
        ys_vertical.append( self.start_point[1] )
        yield (x_vertical, min(ys_vertical)) , (x_vertical, max(ys_vertical))
        
        # 3rd 
        for end_point in self.end_points:
            yield (x_vertical, end_point[1]), end_point

        
    def __str__(self):
        """ Return a string representation of the hyperedge. """
        gen = self.ilines()
        _str = []
        for line in gen:
            _str.append(str(line))
            
        return '\n'.join(_str)
        
    def __repr__(self):
        return self.__str__()
  
  
def count_crossovers( hedge1, hedge2 ):
    """ Count the crossovers between two Hyperedges. 
    
    What's the brute-force algorithm? Go through each line segment of
    hyperedge 1 and check if it overlaps with each line segment of
    hyperedge 2.
    
    The lines are guaranteed to be orthogonal, are there any optimisations
    I can use, so?
    
    For the lines to cross, there has to be an overlap in the x dimensions
    and in the y dimensions, right? And the points are going to be non-negative
    integers.
    """
    
    ilines_1 = hedge1.ilines()
    ilines_2 = hedge2.ilines()
    
    for start_point, end_point in ilines_1:
        x_max = max( start_point[0], end_point[0] )
        x_min = min( start_point[0], end_point[0] )
        for start_point2, end_point2 in ilines_2:
            print "A:", start_point, end_point, " B:", start_point2, end_point2
    
    return 2
    
          
       
