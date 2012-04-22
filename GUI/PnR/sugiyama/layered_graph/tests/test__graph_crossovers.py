#! /usr/bin/env python
""" Graph Crossover counting tests. """

import pprint
from .. import graph
import helpers

class Test_Graph_Crossover_Counting():

    def test_calc_crossovers(self):
        G = helpers.orig_sugiyama_cct()
        G.update()
        assert G.count_crossovers() == 8     
 
    def test_calc_crossovers_1(self):
        G = helpers.orig_sugiyama_single_port_cct()
        G.update()
        assert G.count_crossovers() == 8
        
    def test_calc_crossovers_2(self):
        G = helpers.orig_sugiyama_single_port_cct()
        G.update()
        
        vdict = G.vertex_dict
        new_order = [ [ 'A', 'B' ],
                      [ 'D', 'E', 'C', 'F' ],
                      [ 'H', 'I', 'J', 'G' ],
                      [ 'M', 'K', 'L' ] ]
              
        i_layer = 0        
        for layer in new_order:
            vertices = []
            for name in layer:
                vertices.append(vdict[name])
                
            G.vertices[i_layer] = vertices
            i_layer += 1
            
        G.update
        print G.display()
        assert G.count_crossovers() == 2
