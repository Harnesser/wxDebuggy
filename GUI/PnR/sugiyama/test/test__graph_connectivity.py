#!/usr/bin/env python
import helpers
helpers.set_path()

import graph
import unittest

class GraphConnectivityOperations( unittest.TestCase ):

    def setUp(self):
    
        self.V = [ list('ab') , list('cdef'), list('ghij'), list('klm') ]
        self.E = [  [('a','c'), ('a','d'), ('a','e'), ('a','f'), ('b','c'), ('b','f') ],
                    [('c','g'), ('d','h'), ('d','i'), ('d','j'), ('e','g'), ('e','j') ],
                    [('g','k'), ('i','k'), ('i','m'), ('j','k'), ('j','l') ]
                 ]

        #
        # Convert into new vertice/edge style. Input port is called 'i', and output 'o'
        #
        

        self.new_V, self.new_E = helpers.new_style_conversion(self.V, self.E)
        print self.new_V                
        print self.new_E
                
                
    def test_upper_connectivity(self):
        G = graph.Graph( self.new_V, self.new_E )
        
        G.build_connection_matrices()
        G.calc_upper_connectivities()
        
        expected = [ [],            # this is to keep indexing sweet
                     [2, 1, 1, 2],
                     [2, 1, 1, 2],
                     [3, 1, 1] ]
                     
        self.assertEquals( G.upper_connectivities, expected )
    
    
    def test_lower_connectivity(self):
        G = graph.Graph( self.new_V, self.new_E )
        
        G.build_connection_matrices()
        G.calc_lower_connectivities()
        
        expected = [ [4,2], [1,3,2,0], [1,0,2,2] ]
                     
        self.assertEquals( G.lower_connectivities, expected )
    
       
