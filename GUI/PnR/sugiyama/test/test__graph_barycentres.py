#! /usr/bin/env python
""" Graph Upper and Lower Barycentre calculation tests. """

import sys
sys.path.append('../')

import graph
import unittest

class GraphBarycentreOperations( unittest.TestCase ):

    def setUp(self):
        self.V = [ list('ab') , list('cdef'), list('ghij'), list('klm') ]
        self.E = [  [('a','c'), ('a','d'), ('a','e'), ('a','f'), ('b','c'), ('b','f') ],
                    [('c','g'), ('d','h'), ('d','i'), ('d','j'), ('e','g'), ('e','j') ],
                    [('g','k'), ('i','k'), ('i','m'), ('j','k'), ('j','l') ]
                 ]
        self.G = graph.Graph( self.V, self.E )
        self.G.build_connection_matrices()
        self.G.calc_upper_connectivities()
        self.G.calc_lower_connectivities()            
                 
    def test_upper_barycentre_calcs(self):
        
        layer = 2
        x = [4, 6, 7, 10 ]
        bc = self.G.calc_upper_barycentres( layer, x )
        
        expected = [ int( ( x[0] + x[2]) / 2 ),
                     int( ( x[1] ) / 1 ),
                     int( ( x[1] ) / 1 ),
                     int( ( x[1] + x[2]) / 2 )
                   ]
        
        self.assertEquals(bc, expected)
               
        
    def test_lower_barycentre_calcs(self):
            
        layer = 2
        x = [1,4,7,10]
        bc = self.G.calc_lower_barycentres( layer, x )
        
        expected = [ int( ( x[0] ) / 1 ),
                     int( ( 0 ) ),  # woot - accidental edge case found!
                     int( ( x[0] + x[2] ) / 2 ),
                     int( ( x[0] + x[1] ) / 2 ),
                   ]
        
        self.assertEquals(bc, expected)
    
