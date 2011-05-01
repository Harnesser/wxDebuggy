#! /usr/bin/env python
""" Sugiyama Layer Reordering Operations"""

import sys
sys.path.append('../../')

import dev.sugiyama as sugiyama
import unittest

            
class SugiyamaLayerReordering( unittest.TestCase ):

    def setUp(self):
        self.V = [ list('ab') , list('cdef'), list('ghij'), list('klm') ]
        self.E = [  [('a','c'), ('a','d'), ('a','e'), ('a','f'), ('b','c'), ('b','f') ],
                    [('c','g'), ('d','h'), ('d','i'), ('d','j'), ('e','g'), ('e','j') ],
                    [('g','k'), ('i','k'), ('i','m'), ('j','k'), ('j','l') ]
                 ]
     
    def setup_graph(self, V, E):
        G = sugiyama.Graph( V, E )
        G.build_connection_matrices()
        self.show_conn_matrices(G)
        return G
        

    def show_conn_matrices(self, G):
        print "#" * 80
        for i in xrange(G.c_levels-1):
            print G.matrices[i]
        print "Crossover Count: ", G.get_crossover_count()
        

    def test__down_phase1_easy(self):
        """ Reorder downwards one layer of a graph. """
        
        print "=== Reorder Down ==="
        G = self.setup_graph(self.V, self.E)
        i_layer = 0
        
        print "Before", G.matrices[i_layer]
        print "Layer[i+1]:", G.vertices[i_layer+1]
        sugiyama.down_phase1(G, i_layer)
        print "After", G.matrices[i_layer]
        print "Layer[i+1]:", G.vertices[i_layer+1]
        
        # Check crossover count between layer 0 and 1
        self.assertEquals( G.matrices[i_layer].get_crossover_count(), 1)
        self.assertEquals( G.vertices[i_layer+1], list('decf') )
        
        
    def test__up_phase1_easy(self):
        """ Reorder upwards one layer of a graph. """
        
        print "=== Reorder Up ==="
        G = self.setup_graph(self.V, self.E)
        i_layer = 2
        
        print "Before", G.matrices[i_layer-1]
        print "Layer[i-1]:", G.vertices[i_layer-1]
        sugiyama.up_phase1(G, i_layer)
        print "After", G.matrices[i_layer-1]
        print "Layer[i-1]:", G.vertices[i_layer-1]
        
        # Check crossover count between layer 1 and 2
        self.assertEquals( G.matrices[i_layer].get_crossover_count(), 2)
        self.assertEquals( G.vertices[i_layer-1], list('fced') )
        
                
    def test__down_procedure_xover_count(self):
        """ Check out a full down procedure. """
        
        print "=== Phase 1 DOWN Procedure ==="
        G = self.setup_graph(self.V, self.E)
        self.assertEquals( G.get_crossover_count(), 8 )
        
        sugiyama.down_procedure(G)
        self.show_conn_matrices(G)
        
        self.assertEquals( G.get_crossover_count(), 2)
        
        
    def test__down_procedure_conn_matrix_consistency(self):
        """ Check out a full down procedure - Matrix consistency. """
        
        print "=== Phase 1 DOWN Procedure  (Consistency) ==="
        G = self.setup_graph(self.V, self.E)
        self.assertEquals( G.get_crossover_count(), 8 )
        
        sugiyama.down_procedure(G)
        self.assertTrue( G.check_consistency() )



    def test__up_procedure_xover_count(self):
        """ Check out a full up procedure. """
        
        print "=== Phase 1 UP Procedure ==="
        G = self.setup_graph(self.V, self.E)
        self.assertEquals( G.get_crossover_count(), 8 )
        
        sugiyama.up_procedure(G)
        self.show_conn_matrices(G)
        
        self.assertEquals( G.get_crossover_count(), 5)
        
        
    def test__up_procedure_conn_matrix_consistency(self):
        """ Check out a full up procedure - Matrix consistency. """
        
        print "=== Phase 1 UP Procedure (Consistency)==="
        G = self.setup_graph(self.V, self.E)
        self.assertEquals( G.get_crossover_count(), 8 )
        
        sugiyama.up_procedure(G)
        self.assertTrue( G.check_consistency() )
        
                   
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
        self.assertEquals(G.get_crossover_count(), 0) 
        
        
    def test__2_layer_2(self):
        """ Untangle a simple graph #2:
        Example on page 117
        """
        E = "ae:af:be:bh:bi:cf:ch:ci:de:dg:di"
        E = [ tuple(a) for a in E.split(':') ]
        E = [E]
        G = self.setup_graph( V = [ list('abcd'), list('efghi') ], E=E )
        
        # Pre-checks
        self.assertEquals(G.get_crossover_count(), 14 )
        
        # Run and check
        sugiyama.multilayer_bc_method(G)
        
        self.assertEquals(G.get_crossover_count(), 7 )
        
           
                
    
