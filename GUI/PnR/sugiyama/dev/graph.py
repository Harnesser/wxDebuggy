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
        return 'V:%s\nE:%s' % ( self.vertices, self.edges )
