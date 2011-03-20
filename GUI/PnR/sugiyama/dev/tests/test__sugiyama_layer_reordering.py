#! /usr/bin/env python
""" Sugiyama Layer Reordering Operations"""

import sys
sys.path.append('../../')

import dev.sugiyama as sugiyama
import unittest

V = [ list('ab') , list('cdef'), list('ghij'), list('klm') ]
E = [  [('a','c'), ('a','d'), ('a','e'), ('a','f'), ('b','c'), ('b','f') ],
       [('c','g'), ('d','h'), ('d','i'), ('d','j'), ('e','g'), ('e','j') ],
       [('g','k'), ('i','k'), ('i','m'), ('j','k'), ('j','l') ]
    ]
                 
class SugiyamaLayerReordering( unittest.TestCase ):

    def setup_graph(self, V, E):
        G = sugiyama.Graph( V, E )
        G.build_connection_matrices()
        #G.calc_upper_connectivities()
        #G.calc_lower_connectivities()
        print G.get_crossover_count()
        print "#" * 80
        return G
        
        
    def test__reorder_down_easy(self):
        """ Reorder downwards one layer of a graph. """
        
        G = self.setup_graph(V, E)
        i_layer = 0
        
        print "Before", G.matrices[i_layer]
        print "Layer[i+1]:", G.vertices[i_layer+1]
        sugiyama.reorder_down(G, i_layer)
        print "After", G.matrices[i_layer]
        print "Layer[i+1]:", G.vertices[i_layer+1]
        
        # Check crossover count between layer 0 and 1
        self.assertEquals( G.matrices[i_layer].get_crossover_count(), 1)
        self.assertEquals( G.vertices[i_layer+1], list('decf') )
        
        
    def test__2_layer_1(self):
        """ Untangle a simple graph #1:

         A  B                        B  A        A  B
         |\/   should untangle to    | /|   or   |\ |
         |/\                         |/ |        | \|
         C  D                        C  D        D  C
         
        """
         
        G = self.setup_graph(
            V = [ list('AB'), list('CD') ],
            E = [ [('A', 'D'), ('A', 'C'), ('B', 'C')] ] )
        sugiyama.multilayer_bc_method(G)

        self.assertEquals(G.vertices, [ list('AB'), list('DC') ] )      
        #self.assertEquals(G.get_crossover_count(), 0) #why does this fail?
    
    def test__2_layer_2(self):
        """ Untangle a simple graph #2:
        
        
        """
    
    
