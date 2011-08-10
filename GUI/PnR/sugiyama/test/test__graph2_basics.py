#! /usr/bin/env python
import pprint
import graph_test_base
import graph2

class Graph2BasicOperations(graph_test_base.Graph_Test_Base):

    graph_str = ';'.join(['1.a:7.a;1.b:90.a',
                          '2.a:8.a',
                          '3.a:6.a;3.b:7.c;3.b:90.b;3.c:91.a',
                          '4.a:91.a;4.b:8.a;4.c:7.b',
                          '5.a:7.b;5.b:8.a'
                          ])
                              
    def test_graph2_init_simples(self):
        G = self.build_graph_from_shorthand( "A.p1:B.p2" )
        G.update()
        
        vertex_names = G.vertex_dict.keys()
        vertex_names.sort()
        self.assertEquals(vertex_names, ['A','B'])
        
        
    def test_graph2_init(self):
        G = self.build_graph_from_shorthand(self.graph_str)
        G.update()
       
        vertex_names = G.vertex_dict.keys()
        vertex_names.sort()
        expected_vertex_names = list('12345678')
        expected_vertex_names.extend( [ '90','91'] )
        self.assertEquals(vertex_names, expected_vertex_names )
        
        
    def test_graph2_init_names(self):
        G = self.build_graph_from_shorthand(self.graph_str)
        G.update()
        
        names_in_layer_0 = [ vertex.name for vertex in G.vertices[0] ]
        self.assertEquals( list('12345'), names_in_layer_0 )
        
        names_in_layer_1 = [ vertex.name for vertex in G.vertices[1] ]
        self.assertEquals( ['6','7','8','90','91'], names_in_layer_1 )
        
        
    def test_graph2_init_ranking_top(self):
        G = self.build_graph_from_shorthand(self.graph_str)
        G.update()
        
        expected_ranking = [0, 2, 3, 6, 9]
        ranking = [ vertex.get_rank() for vertex in G.vertices[0] ]
        self.assertEquals( ranking, expected_ranking)
        
         
    def test_graph2_init_ranking_bot(self):
        G = self.build_graph_from_shorthand(self.graph_str)
        G.update()
        
        expected_ranking = [0, 1, 4, 5, 7]
        i = 1
        ranking = [ vertex.get_rank() for vertex in G.vertices[i] ]
        self.assertEquals( ranking, expected_ranking)
        
        
    def test_calc_barycentres_up(self):
        G = self.build_graph_from_shorthand(self.graph_str)
        G.update()
        
        pprint.pprint(G.vertices)
        expected_bcs = [ 3.0, 4.0, 4.0, 13.0/3, 3.0 ]
        bcs = G.calc_barycentres(0,'down')
        self.assertEqual( bcs, expected_bcs )
        
        
