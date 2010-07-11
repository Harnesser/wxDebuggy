#! /usr/bin/env python
"""
  Python implementation of some Sugiyama graph drawing algorithms.
"""

from matrix import Matrix
from graph import Graph

if True:
    V = [ list('ab') , list('cdef'), list('ghij'), list('klm') ]
    E = [  [('a','c'), ('a','d'), ('a','e'), ('a','f'), ('b','c'), ('b','f') ],
           [('c','g'), ('d','h'), ('d','i'), ('d','j'), ('e','g'), ('e','j') ],
           [('g','k'), ('i','k'), ('i','m'), ('j','k'), ('j','l') ]
        ]
else:
    V = [ list('abc'), list('def'), list('ghi'), list('jkl') ]
    E = [ [ ('a','e'), ('b','d'), ('c','d') ],
          [ ('d','g'), ('e','g'), ('e','h'), ('e','i'), ('f','h') ],
          [ ('g','l'), ('h','j'), ('h','k') ],
        ]
        
def reorder_down(G, i):
    """ """
    print '(Reorder Down)'
    M = Matrix( G.vertices[i], G.vertices[i+1], G.edges[i] )
    print "Before", M
    M.barycentre_col_reorder()
    G.vertices[i+1] = M.col_vertices
    print "After", M
  
def reorder_up(G, i):
    """ """
    print '(Reorder Up)'
    print '  ', G.vertices[i] 
    print '  ', G.vertices[i-1]
    print '  ', G.edges[i-1]
    M = Matrix( G.vertices[i-1], G.vertices[i], G.edges[i-1] )
    print "Before", M
    M.barycentre_row_reorder()
    G.vertices[i-1] = M.row_vertices
    print "After", M
        
def phase_1_down(G):
    """ """
    print '(Phase 1 Down)'
    for i in xrange(0, G.c_levels-1):
        print " Layer", i
        reorder_down(G, i )
        
               
def phase_1_up(G):
    """ """
    print '(Phase 1 Up)'
    for i in xrange(G.c_levels-1, 0, -1):
        print " Layer", i
        reorder_up(G, i)

def phase_1_down_up(G):
    """ """
    print '(Phase 1 Down/Up)'
    K = 10
    for i in xrange(1, K):
        print " Iteration", i
        phase_1_down(G)
        phase_1_up(G)
    
    
def multilayer_bc_method(G):
    """ Implementation of the Multilayer Barycentre Method. """
    
    phase_1_down_up(G)
    

if __name__ == '__main__':
    
    G1 = Graph(V, E)
    print G1
    multilayer_bc_method(G1)
    print G1
    
