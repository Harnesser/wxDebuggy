#! /usr/bin/env python
""" Graph Upper and Lower Barycentre calculation tests. """

import pprint
import graph_test_base
import graph

class GraphBarycentreOperations( graph_test_base.Graph_Test_Base ):

    graph_str = ';'.join(['1.a:7.a;1.b:90.a',
                          '2.a:8.a',
                          '3.a:6.a;3.b:7.c;3.b:90.b;3.c:91.a',
                          '4.a:91.a;4.b:8.a;4.c:7.b',
                          '5.a:7.b;5.b:8.a'
                          ])
                          
        
    #
    # Barycentre Calculations
    #
    def test_calc_barycentres_up(self):
        G = self.build_graph_from_shorthand(self.graph_str)
        G.update()
        
        pprint.pprint(G.vertices)
        expected_bcs = [ 3.0, 4.0, 4.0, 13.0/3, 3.0 ]
        bcs = G.calc_barycentres(0,'down')
        self.assertEqual( bcs, expected_bcs )
        
        
    def test_calc_barycentres_down(self):
        G = self.build_graph_from_shorthand(self.graph_str)
        G.update()
        
        expected_bcs = [ 3.0, 21.0/4, 19.0/3, 2.5, 11.0/2]
        bcs = G.calc_barycentres(1, 'up')
        self.assertEqual( bcs, expected_bcs )
        
        
    #
    # Layer Reordering
    #
    def test_layer_reorder_down(self):
        G = self.build_graph_from_shorthand(self.graph_str)
        G.update()
        
        pprint.pprint(G.vertices)
        expected_vertex_order = '90:6:7:91:8'.split(':')

        i_layer = 1
        G.reorder_layer(i_layer, 'down')
        self.assertEquals( G.get_vertex_labels(i_layer), expected_vertex_order)
    
    
    def test_layer_reorder_up(self):
        G = self.build_graph_from_shorthand(self.graph_str)
        G.update()
        
        pprint.pprint(G.vertices)
        expected_vertex_order = '1:5:2:3:4'.split(':')
        i_layer = 0
        
        G.reorder_layer(i_layer, 'up')
        self.assertEquals( G.get_vertex_labels(i_layer), expected_vertex_order)
    
