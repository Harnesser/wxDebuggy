#! /usr/bin/env python
""" Sugiyama Trials with some graphs """

import sys
sys.path.append('../../')

import dev.sugiyama as sugiyama
import unittest

class SugiyamaGraphs( unittest.TestCase ):

    def setup_graph(self, V, E):
        G = sugiyama.Graph( V, E )
        G.build_connection_matrices()
        G.calc_upper_connectivities()
        G.calc_lower_connectivities()
        print "#" * 80
        return G
        
    def test__2_layer_2_vertices(self):
        """ Layout of 2-layer, 2-vertice Graph.
        Should get something like:
           
            A
            |
            B
        """
        V = [ list('a') , 
              list('b') ]
        E = [  [('a','b')],
            ]
            
        G = self.setup_graph(V, E)
        layout = sugiyama.priority_layout(G)
        self.assertEquals(layout, [[1], [1]])
        

    def test__3_layer_3_vertices(self):
        """ Layout of 3-layer, 3-vertice Graph.
        Should get something like:
           
            A
            |
            B
            |
            C
        """
        V = [ list('a') , 
              list('b'),
              list('c') ]
        E = [  [('a','b')],
               [('b','c')],
            ]
            
        G = self.setup_graph(V, E)
        layout = sugiyama.priority_layout(G)
        self.assertEquals(layout, [[1], [1], [1]])    

        
    def test__2_layer_triangle(self):
        """ Layout of 2-layer, 4-vertice Graph.
        Should get something like:
           
            A
           /|\
          B C D
        """
        
        V = [ list('a'), 
              list('bcd')
            ]
        E = [  [('a','b'), ('a','c'), ('a','d')]
            ]
                
        G = self.setup_graph(V, E)
        layout = sugiyama.priority_layout(G)
        self.assertEquals(layout, [[2], [1,2,3]] )    

    
    def test__3_layer_ponzi(self):
        """ Layout of a 3 layer ponzi scheme, two suckers per sucker
        
                    A
                   / \
                  B   C
                 / \ / \
                D  E F  G
        """
                
        V = [ list('a'), 
              list('bc'),
              list('defg')
            ]
        E = [  [('a','b'), ('a','c')],
               [('b','d'), ('b','e'), ('c','f'), ('c','g')]
            ]
                
        G = self.setup_graph(V, E)
        layout = sugiyama.priority_layout(G)
        self.assertEquals(layout, [ [2], [2,3], [1,2,3,4] ] )            
        
    
    def test__3_layer_inverse_ponzi(self):
        """ Layout of a 3 layer inverted ponzi scheme, two suckers per sucker
        
                D  E F  G
                 \ / \ /
                  H   I
                   \ /
                    J                 
        """
                
        V = [ list('defg'),
              list('hi'),
              list('j')
            ]
            
        E = [ [ ('d','h'), ('e','h'), ('f','i'), ('g','i') ],
              [ ('h','j'), ('i','j') ]
            ]
                
        G = self.setup_graph(V, E)
        layout = sugiyama.priority_layout(G)
        self.assertEquals(layout, [ [1,2,3,4], [1,3], [2],] )            
                
                
    def test__5_layer_diamond(self):
        """ 5 layer Diamond
        
                    A
                   / \
                  B   C
                 / \ / \
                D  E F  G
                 \ / \ /
                  H   I
                   \ /
                    J          
        """

        V = [ list('a'), 
              list('bc'),
              list('defg'),
              list('hi'),
              list('j')
            ]
        E = [  [('a','b'), ('a','c')],
               [('b','d'), ('b','e'), ('c','f'), ('c','g')],
               [('d','h'), ('e','h'), ('f','i'), ('g','i')],
               [('h','j'), ('i','j')]
            ]
                
        G = self.setup_graph(V, E)
        layout = sugiyama.priority_layout(G)
        self.assertEquals(layout, [ [2], [2,3], [1,2,3,4], [1,3], [2] ] )            
                
        
        
    
    
