#! /usr/bin/env python
""" Sugiyama Layer Reordering Operations"""

import sys
sys.path.append('../../')

import dev.sugiyama as sugiyama
import unittest

class SugiyamaLayerReordering( unittest.TestCase ):

    def setup_graph(self, V, E):
        G = sugiyama.Graph( V, E )
        G.build_connection_matrices()
        #G.calc_upper_connectivities()
        #G.calc_lower_connectivities()
        print "#" * 80
        return G
        
    
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
    
    
    def test__2_layer_2(self):
        """ Untangle a simple graph #2:
        
        
        """
    
    
