#!/usr/bin/env python
import sys

sys.path.append('../../')

import dev as sugiyama
import unittest

class GraphBasicOperations( unittest.TestCase ):

    def test_initialiser(self):
        V = [ list('abc'), list('defg') ]
        E = [ [('a','g'), ('b','f'), ('b','e'), ('c','d')] ]
        G = sugiyama.Graph( V, E )
        
        # Check size of connection matrix
        self.assertEquals( G.c_levels, 2 )
        
        # Check the connection matrix entries       
        print G

        
    def test_matrices_1(self):
        V = [ list('abc'), list('defg') ]
        E = [ [('a','g'), ('b','f'), ('b','e'), ('c','d')] ]
        G = sugiyama.Graph( V, E )  
        G.build_connection_matrices()
        
        self.assertEquals( G.matrices[0].M, [ [0,0,0,1], [0,1,1,0], [1,0,0,0] ] )
        
        
    def test_matrices_2(self):
    
        V = [ list('ab') , list('cdef'), list('ghij'), list('klm') ]
        E = [  [('a','c'), ('a','d'), ('a','e'), ('a','f'), ('b','c'), ('b','f') ],
               [('c','g'), ('d','h'), ('d','i'), ('d','j'), ('e','g'), ('e','j') ],
               [('g','k'), ('i','k'), ('i','m'), ('j','k'), ('j','l') ]
            ]
            
        G = sugiyama.Graph( V, E )  
        G.build_connection_matrices()
        
        self.assertEquals( G.matrices[0].M, [ [1,1,1,1], [1,0,0,1]] )
        self.assertEquals( G.matrices[1].M, [ [1,0,0,0], [0,1,1,1], [1,0,0,1], [0,0,0,0] ] )
        self.assertEquals( G.matrices[2].M, [ [1,0,0], [0,0,0], [1,0,1], [1,1,0] ] )
