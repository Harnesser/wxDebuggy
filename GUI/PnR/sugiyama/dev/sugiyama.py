#! /usr/bin/env python
"""
  Python implementation of some Sugiyama graph drawing algorithms.
"""

from matrix import Matrix
from graph import Graph

V = [ list('ab') , list('cdef'), list('ghij'), list('klm') ]
E = [  [('a','c'), ('a','d'), ('a','e'), ('a','f'), ('b','c'), ('b','f') ],
       [('c','g'), ('d','h'), ('d','i'), ('d','j'), ('e','g'), ('e','j') ],
       [('g','k'), ('i','k'), ('i','m'), ('j','k'), ('j','l') ]
    ]

    
def reorder_down(G, i):
    """ """
    M = Matrix( G.vertices[i], G.vertices[i+1], G.edges[i] )
    print G
    print M
    M.barycentre_col_reorder()
    G.vertices[i+1] = M.col_vertices
    print M
    print G
        
def phase_1_down(G):
    """ """
    for i in xrange(1, G.c_levels-1):
        print " ", i
        reorder_down(G, i )
        
        
def phase_1_up(G):
    """ """
    for i in xrange(G.c_levels, 0, -1):
        print "  ", i

def phase_1_down_up(G):
    """ """
    K = 10
    for i in xrange(1, K):
        print i
        phase_1_down(G)
        phase_1_up(G)
    print G
    
def multilayer_bc_method(G):
    """ Implementation of the Multilayer Barycentre Method. """
    
    phase_1_down_up(G)
    

if __name__ == '__main__':
    
    G1 = Graph(V, E)
    multilayer_bc_method(G1)
    
