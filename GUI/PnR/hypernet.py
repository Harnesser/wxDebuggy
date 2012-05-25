""" Hypernets

We'll be using hypernets for drawing the connections in the circuit. For the
moment, I'm only going deal with 1:n connections.

I'll want to do a few things with a hypernet:
* traverse it and return line segments
* tweak the co-ordinate of the vertical segment
* build a hypernet, given some normal graph edges, or maybe target
  co-ordinates.

"""

SEPARATION = 5

        
class Hypernet(object):
    """ Hypernet Class.
    
    Also includes one or two methods to traverse the hypernet tree:
    * returns line segments for drawing and crossover counting
    """ 
    
    def __init__(self, name=''):
        self.netname = name
        self.track = 1
        
        self.start_point = None
        self.end_points = []
        self.vertical = self.track * SEPARATION
       
    def add_connection(self, start_point, end_point ):
        """ Add hypernet to connect start_point to end_point.
        All edges for this hypernet must have the same start point. """
        
        if self.start_point == None:
            self.start_point = start_point
        elif start_point != self.start_point:
            print "Warning: Hypernet connection start co-ordinate doesn't match."""
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
        """ Return an iterator to return the lines in the hypernet"""
        x_vertical = self.track * SEPARATION + self.start_point[0]
        
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
        """ Return a string representation of the hypernet. """
        gen = self.ilines()
        _str = []
        for line in gen:
            _str.append(str(line))
            
        return '\n'.join(_str)
        
    def __repr__(self):
        return self.__str__()
  
  
def count_crossovers( hedge1, hedge2 ):
    """ Count the crossovers between two Hypernet. 
    
    What's the brute-force algorithm? Go through each line segment of
    hypernet 1 and check if it overlaps with each line segment of
    hypernet 2.
    
    The lines are guaranteed to be orthogonal, are there any optimisations
    I can use, so?
    
    For the lines to cross, there has to be an overlap in the x dimensions
    and in the y dimensions, right? And the points are going to be non-negative
    integers.
    """
    
    crossings = 0
    ilines_1 = hedge1.ilines()

    for line1 in ilines_1:
        for line2 in hedge2.ilines() :
            if _check_for_crossing(line1, line2):
                crossings += 1
    
    return crossings
    
    
def _check_for_crossing( flightline1, flightline2):
    """ Check if two line segments cross.
    
    Adapted from here:
    * http://stackoverflow.com/a/1968345
    
    !!!FIXME!!! Crashes on two vertical lines:
    Crossover counting
    Lines: ((10, 3), (5, 3)) ((10, 5), (5, 5))
    """
    (p0_x, p0_y), (p1_x, p1_y) = flightline1
    (p2_x, p2_y), (p3_x, p3_y) = flightline2

    # rule out parallel lines
    # http://en.wikipedia.org/wiki/Line-line_intersection#n-line_intersection
    a = (p0_x - p1_x) * (p2_y - p3_y) - (p0_y - p1_y) * (p2_x - p3_x ) 
    if a == 0:
        return False
        
    s1_x = 1.0 * p1_x - p0_x
    s1_y = 1.0 * p1_y - p0_y
    s2_x = 1.0 * p3_x - p2_x
    s2_y = 1.0 * p3_y - p2_y
    
    s = (-s1_y * (p0_x - p2_x) + s1_x * (p0_y - p2_y)) / (-s2_x * s1_y + s1_x * s2_y)
    t = ( s2_x * (p0_y - p2_y) - s2_y * (p0_x - p2_x)) / (-s2_x * s1_y + s1_x * s2_y )

    if s >= 0 and s <= 1 and t >= 0 and t <= 1:
        return True

    return False    
