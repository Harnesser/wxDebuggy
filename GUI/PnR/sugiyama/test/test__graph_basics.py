#!/usr/bin/env python
import sys

sys.path.append('../')

import graph
import unittest

class GraphBasicOperations( unittest.TestCase ):

    def get_graph_1(self):
        V = [ list('abc'), list('defg') ]
        E = [ [('a','g'), ('b','f'), ('b','e'), ('c','d')] ]
        G = graph.Graph( V, E )    
        return G
        

    def get_graph_2(self):
        V = [ list('ab') , list('cdef'), list('ghij'), list('klm') ]
        E = [  [('a','c'), ('a','d'), ('a','e'), ('a','f'), ('b','c'), ('b','f') ],
               [('c','g'), ('d','h'), ('d','i'), ('d','j'), ('e','g'), ('e','j') ],
               [('g','k'), ('i','k'), ('i','m'), ('j','k'), ('j','l') ]
            ]
        G = graph.Graph( V, E )      
        return G
            
        
    def test_initialiser(self):
        G = self.get_graph_1()
        # Check size of connection matrix
        self.assertEquals( G.c_levels, 2 )

        
    def test_matrices_1(self):
        G = self.get_graph_1()
        G.build_connection_matrices()
        self.assertEquals( G.matrices[0].M, [ [0,0,0,1], [0,1,1,0], [1,0,0,0] ] )
        
        
    def test_matrices_2(self):
        G = self.get_graph_2()
        G.build_connection_matrices()
        
        self.assertEquals( G.matrices[0].M, [ [1,1,1,1], [1,0,0,1]] )
        self.assertEquals( G.matrices[1].M, [ [1,0,0,0], [0,1,1,1], [1,0,0,1], [0,0,0,0] ] )
        self.assertEquals( G.matrices[2].M, [ [1,0,0], [0,0,0], [1,0,1], [1,1,0] ] )
        
        
    def test_crossovers_1(self):
        G = self.get_graph_1()
        G.build_connection_matrices()
        self.assertEquals( G.get_crossover_count(), 5)
        
        
    def test_crossovers_2(self):
        G = self.get_graph_2()
        G.build_connection_matrices()
        self.assertEquals( G.get_crossover_count(), 8 )
