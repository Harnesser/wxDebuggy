#! /usr/bin/env python
"""
  Python implementation of some Sugiyama graph drawing algorithms.
"""

from matrix import Matrix
from graph import Graph

dbg_reorder = True
dbg_coords = True

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
    
    
# =================================================================
#  Layer Ordering
# =================================================================
        
def reorder_down(G, i):
    """ """
    if dbg_reorder: print '(Reorder Down)'
    M = Matrix( G.vertices[i], G.vertices[i+1], G.edges[i] )
    if dbg_reorder: print "Before", M
    M.barycentre_col_reorder()
    G.vertices[i+1] = M.col_vertices
    if dbg_reorder: print "After", M
  
def reorder_up(G, i):
    """ """
    if dbg_reorder: 
        print '(Reorder Up)'
        print '  ', G.vertices[i] 
        print '  ', G.vertices[i-1]
        print '  ', G.edges[i-1]
    M = Matrix( G.vertices[i-1], G.vertices[i], G.edges[i-1] )
    if dbg_reorder: print "Before", M
    M.barycentre_row_reorder()
    G.vertices[i-1] = M.row_vertices
    if dbg_reorder: print "After", M
        
def phase_1_down(G):
    """ """
    if dbg_reorder: print '(Phase 1 Down)'
    for i in xrange(0, G.c_levels-1):
        if dbg_reorder: print " Layer", i
        reorder_down(G, i )
        
               
def phase_1_up(G):
    """ """
    if dbg_reorder: print '(Phase 1 Up)'
    for i in xrange(G.c_levels-1, 0, -1):
        if dbg_reorder: print " Layer", i
        reorder_up(G, i)

def phase_1_down_up(G):
    """ """
    if dbg_reorder: print '(Phase 1 Down/Up)'
    K = 10
    for i in xrange(1, K):
        if dbg_reorder: print " Iteration", i
        phase_1_down(G)
        phase_1_up(G)
    
    
def multilayer_bc_method(G):
    """ Implementation of the Multilayer Barycentre Method. """
    
    phase_1_down_up(G)
    
    
# =================================================================
#  Horizontal Placement
# =================================================================

def initial_layout(G):
    k0 = 0
    layout = []
    for layer in G.vertices:
         i = 1
         layer_positions = []
         for vertex in layer:
            layer_positions.append(k0+i)
            i += 1
         layout.append(layer_positions)
         
    print G.vertices
    print layout
    return layout
    
def priority_layout(G):
    """ Horizontal Coordinate Assignment using Priorty Layout Method. 
    Section IV:B of Sugiyama's paper.
    """
    
    # Initial placement
    layout = initial_layout(G)
    
    # Gather the connectivity measures
    # Dummy nodes aren't taken into account yet
    G.calc_lower_connectivities()
    G.calc_upper_connectivities()
    
    print "number of layers:", G.c_levels

    print "DOWN"
    for i in xrange(1, G.c_levels):
        print i, G.vertices[i]

        priorities = G.upper_priorites[i-1]
        barycentres =         
        
    print "UP"
    for i in xrange(G.c_levels-2,-1,-1 ):
        print i, G.vertices[i]
        

    print "DOWN"
    for i in xrange(1, G.c_levels ):
        print i, G.vertices[i]
        
    
    
    
if __name__ == '__main__':
    
    G1 = Graph(V, E)
    print G1
    multilayer_bc_method(G1)
    print G1
    
    horz_pos = priority_layout(G1)
    
    
    
