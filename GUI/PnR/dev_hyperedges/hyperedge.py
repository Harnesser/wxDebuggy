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
        
       
