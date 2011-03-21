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
        
# Down
def reorder_down(G, i):
    """ Reorder a Graph Layer. """
    M_star = Matrix(G.vertices[i], G.vertices[i+1], G.edges[i] )
    M1 = M_star.copy()
    M1.barycentre_col_reorder()
    if M1.get_crossover_count() < M_star.get_crossover_count():
        G.matrices[i] = M1    
        G.vertices[i+1] = M1.col_vertices
    else:
        G.matrices[i] = M_star
        G.vertices[i+1] = M_star.col_vertices
  

def phase_1_down(G):
    """ Phase 1 Down Procedure"""
    for i in xrange(0, G.c_levels-1):
        if dbg_reorder: print " Layer", i
        reorder_down(G, i )
        
        
# Up     
def reorder_up(G, i):
    """ """
    M_star = Matrix( G.vertices[i-1], G.vertices[i], G.edges[i-1] )
    M_star = G.matrices[i-1]
    M1 = M_star.copy()
    M1.barycentre_row_reorder()
    if M1.get_crossover_count() < M_star.get_crossover_count():
        G.matrices[i-1] = M1
        G.vertices[i-1] = M1.row_vertices
    else:
        G.matrices[i-1] = M_star
        G.vertices[i-1] = M_star.row_vertices        
        

               
def phase_1_up(G):
    """ """
    if dbg_reorder: print '(Phase 1 Up)'
    for i in xrange(G.c_levels-1, 0, -1):
        if dbg_reorder: print " Layer", i
        reorder_up(G, i)


        
def multilayer_bc_method(G, K=10):
    """ Implementation of Sugiyama's n-Level Barycentre Method. 
    
    The input to this algorithm is a layered graph, where the vertices in each 
    layer are ordered, but likely not in an order which minimises the edge 
    crossover count of the graph.
    
    The n-Level BC method is a heuristic algorithm that attempts to reorder the
    vertices within each layer to minimise edge crossovers in the graph. It 
    operates by sweeping down and up the graph, reordering one layer at a time
    - fixing the position of one layer and using a heuristic to reorder the other
    layer to minimize crossings.
    """

    for i in xrange(1, K):
        if dbg_reorder: print " Iteration", i
        phase_1_down(G)
        phase_1_up(G)

    
# =================================================================
#  Horizontal Placement
# =================================================================

def initial_layout(G, debug=True):
    k0 = 0
    layout = []
    for layer in G.vertices:
         i = 1
         layer_positions = []
         for vertex in layer:
            layer_positions.append(k0+i)
            i += 1
         layout.append(layer_positions)
         
    if debug:
        print G.vertices
        print layout
    return layout
    
def order_by_priority( priorities_by_position ):
    """ Return the indices ordered by their priority."""
    
    # Decorate 
    l = []
    for i in xrange( len(priorities_by_position) ): 
        l.append( [priorities_by_position[i], i ] )
    l.sort(reverse=True)
    ordered = [ p_i[1] for p_i in l ] 

    return ordered


def get_indices_with_higher_priorities( j, priorities, direction ):
    """"""    
    c_vertices = len(priorities)
    
    if direction == 'left':
        s_to_check = range(0, j )
    elif direction == 'right':
        s_to_check = range(j+1, c_vertices)
    else:
        s_to_check = []
        
    S = [ s for s in s_to_check if priorities[s] >= priorities[j] ]
    
    return S
    
    
def shift_left_to_ideal(j, x_ideal, x_pos ):
    """ """
    x_pos[j] = x_ideal
    l = 1
    while x_pos[j-l] > x_ideal-l:
        print "Shifting ideal"
        x_pos[j-l] = x_ideal-l
        if l <= j-1:
            l += 1
        else:
            break
    
    return x_pos


def shift_left_to_near_ideal(j, k, x_ideal, x_pos ):
    """ """
    l = 1
    while l <= j-k:
        print "Shifting close"
        x_pos[k+l] = x_pos[k] + l
        l += 1
    return x_pos
    
    
def shift_right_to_ideal(j, x_ideal, x_pos ):
    """ """
    x_pos[j] = x_ideal
    l = 1
    while x_pos[j+l] < x_ideal+l:
        print "Shifting right ideal"
        x_pos[j+l] = x_ideal+l
        if l < len(x_pos)-j-1:
            l += 1
        else:
            break
    
    return x_pos


def shift_right_to_near_ideal(j, k, x_ideal, x_pos ):
    """ """
    l = 1
    while l <= k-j:
        print "Shifting right close"
        x_pos[k-l] = x_pos[k] - l
        l += 1
    return x_pos
    
    
def _priority_layout(G, debug=True):
    """ Horizontal Coordinate Assignment using Priorty Layout Method. 
    Section IV:B of Sugiyama's paper.
    """
    
    # Initial placement
    layout = initial_layout(G)
    c_layers = G.c_levels
    t = 1
    
    # Gather the connectivity measures
    # Dummy nodes aren't taken into account yet
    G.calc_lower_connectivities()
    G.calc_upper_connectivities() 
    
    # List layers we're going to cycle thru
    L = range(1, c_layers ) + range(c_layers-2,-1,-1) + range(t, c_layers)
    if debug:
        print "Layers:", c_layers
        print "L:", L
    
    for a in range( len(L) ):
        i = L[a]    
        x_pos = layout[i]
        c_nodes = len(x_pos)
        
        up = ( c_layers-1 <= a <= (2*(c_layers-1) - 1) )
        priorities = G.lower_connectivities[i] if up else G.upper_connectivities[i]

        if up:
            x_ideal = G.calc_lower_barycentres(i, layout[i+1])
        else:
            x_ideal = G.calc_upper_barycentres(i, layout[i-1])

        j_by_priority = order_by_priority( priorities )                    
    
        if debug:        
            print "a = %d, i = %d, UP? = %s" % (a, i, up)
            print "  X Positions:", x_pos
            print "  Priorities :", priorities 
            print "  Ideal Pos  :", x_ideal
        #  Go thru the vertices in this layer in order and if they can be
        # moved to their ideal position, move them.
        for j in j_by_priority:

            print "Moving j=%d (%s)" % (j, G.vertices[i][j] )
            x_offset = x_ideal[j] - x_pos[j]
            
            if x_offset < 0:
                # Vertex is right of where we want it
                print "-Trying to move left (ideal = %d, actual=%d)" % (x_ideal[j], x_pos[j])
                # If the vertex is the leftmost, we're free to move it to wherever
                if j == 0:
                    print " - Moving to ideal"
                    x_pos[j] = x_ideal[j]
                    
                else:    
                    # Figure out how far left we can shift the vertex
                    S = get_indices_with_higher_priorities(j, priorities, 'left')

                    if S :
                        print " - Higher priorities to left", S
                        #  There are higher priority vertices to the left, find 
                        # the rightmost - this one can't be moved.
                        k = max(S)
                        
                        # Is this higher priority vertex in the way?
                        can_move_to_ideal = ( x_pos[k] <= x_ideal[j] + k - j )
                        if can_move_to_ideal:
                            layout[i] = shift_left_to_ideal(j, x_ideal[j], x_pos[:])
                        else:
                            layout[i] = shift_left_to_near_ideal(j, k, x_ideal[j], x_pos[:])
                    else:
                        print " - Nothing blocking..."
                        #  No higher priority vertices to the left - we're free 
                        # to shift things
                        layout[i] = shift_left_to_ideal(j, x_ideal[j], x_pos[:])


            elif x_offset > 0:
                # Vertex is to left of where we want it
                print "-Trying to move right (ideal = %d, actual=%d)" % (x_ideal[j], x_pos[j])
                
                # If the vertex is the rightmost, we're free to move it to wherever
                if j == c_nodes-1:
                    print " - Moving to ideal"
                    x_pos[j] = x_ideal[j]
                    
                else:    
                    # Figure out how far right we can shift the vertex
                    S = get_indices_with_higher_priorities(j, priorities, 'right')
                    
                    if S :
                        print " - Higher priorities to left", S
                        #  There are higher priority vertices to the right, find 
                        # the leftmost - this one can't be moved.
                        k = min(S)
                        
                        # Is this higher priority vertex in the way?
                        can_move_to_ideal = ( x_pos[k] >= x_ideal[j] + k - j )
                        if can_move_to_ideal:
                            layout[i] = shift_right_to_ideal(j, x_ideal[j], x_pos[:])
                        else:
                            layout[i] = shift_right_to_near_ideal(j, k, x_ideal[j], x_pos[:])
                    else:
                        print " - Nothing blocking..."
                        #  No higher priority vertices to the left - we're free 
                        # to shift things
                        layout[i] = shift_right_to_ideal(j, x_ideal[j], x_pos[:])
                
            else:
                # It's exactly where we want it          
                print " - is grand where it is."  
                pass

        yield layout


def priority_layout(G):
    x = _priority_layout(G)
    for layout in x:
        print "__---____---___---__----______---_--_"
        for layer in layout:
            print "  ", layer
            
            for i in range(1, len(layer) ):
                if layer[i] - layer[i-1] <= 0:
                    print "ERROR: not monotonic"       
    return layout     
            
                
if __name__ == '__main__':
    
    G1 = Graph(V, E)
    print G1
    G1.build_connection_matrices()
    horz_pos = priority_layout(G1)
    
    
    
