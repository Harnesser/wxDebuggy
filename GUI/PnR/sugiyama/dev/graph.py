#! /usr/bin/env python

from matrix import Matrix

class Graph(object):
    """ A class to hold a proper, layered graph.
    Calculates connectivity matrices too, I think...
    """
    
    def __init__(self, vertices, edges):
        self.edges = edges  
        self.vertices = vertices
        self.matrices = []
        
        self.c_levels = 0
        
        self.update()
        
        
    def update(self):
        self.c_levels = len(self.vertices)
        assert( len(self.vertices) -1 == len(self.edges) )
            
            
    def __str__(self):
        repr_str_list = ["Graph:\n"]
        
        repr_str_list.append(" Vertices:")
        for i in xrange(self.c_levels):
            repr_str_list.append( "%10d %s" % (i, self.vertices[i] ) )
                    
        repr_str_list.append("\n    Edges:")
        for i in xrange(self.c_levels-1):
            repr_str_list.append( "%10d %s" % (i, self.edges[i] ) )
            
        return '\n'.join(repr_str_list)
