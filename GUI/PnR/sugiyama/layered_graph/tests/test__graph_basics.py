#! /usr/bin/env python
import pprint

from .. import graph
from .. import vertex
from .. import edge
from .. import port

import helpers

class Test_GraphBasicOperations():

    def test_graph_init_simples(self):
        G = helpers.very_simple_cct()
        G.update()
        
        vertex_names = G.vertex_dict.keys()
        vertex_names.sort()
        assert vertex_names == ['A', 'B']

"""
    
    def test_graph_init(self):
        G = self.build_graph_from_shorthand(self.graph_str)
        G.update()
       
        vertex_names = G.vertex_dict.keys()
        vertex_names.sort()
        expected_vertex_names = list('12345678')
        expected_vertex_names.extend( [ '90','91'] )
        self.assertEquals(vertex_names, expected_vertex_names )
        
        
    def test_graph_init_names(self):
        G = self.build_graph_from_shorthand(self.graph_str)
        G.update()
        
        names_in_layer_0 = [ vertex.name for vertex in G.vertices[0] ]
        self.assertEquals( list('12345'), names_in_layer_0 )
        
        names_in_layer_1 = [ vertex.name for vertex in G.vertices[1] ]
        self.assertEquals( ['6','7','8','90','91'], names_in_layer_1 )
        
        
    #
    # Vertex Ranking
    #
    def test_graph_init_ranking_top(self):
        G = self.build_graph_from_shorthand(self.graph_str)
        G.update()
        
        expected_ranking = [0, 2, 3, 6, 9]
        ranking = [ vertex.get_rank() for vertex in G.vertices[0] ]
        self.assertEquals( ranking, expected_ranking)
        
         
    def test_graph_init_ranking_bot(self):
        G = self.build_graph_from_shorthand(self.graph_str)
        G.update()
        
        expected_ranking = [0, 1, 4, 5, 7]
        i = 1
        ranking = [ vertex.get_rank() for vertex in G.vertices[i] ]
        self.assertEquals( ranking, expected_ranking)
       
        
"""  
