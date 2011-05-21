#! /usr/bin/env python
""" Sugiyama Layer Reordering Operations"""

import sys
import unittest
from collections import namedtuple

sys.path.append('../')
import graph
import reordering
            
Block = namedtuple('Block', 'name inputs outputs')

class SugiyamaLayerReordering( unittest.TestCase ):

    def get_graph_gates1(self):
    
        V = [[Block(name='in4', inputs=('in4',), outputs=('in4',)),
              Block(name='in1', inputs=('in1',), outputs=('in1',)),
              Block(name='in2', inputs=('in2',), outputs=('in2',)),
              Block(name='in3', inputs=('in3',), outputs=('in3',))],
             [Block(name='U1', inputs=('A', 'B'), outputs=('Y',)),
              Block(name='U2', inputs=('A', 'B'), outputs=('Y',))],
             [Block(name='out1', inputs=('out1',), outputs=('out1',)),
              Block(name='out2', inputs=('out2',), outputs=('out2',))],
             ]
        E = [[(('_iport', 'in4'), ('U2', 'B')),
              (('_iport', 'in2'), ('U1', 'B')),
              (('_iport', 'in3'), ('U2', 'A')),
              (('_iport', 'in1'), ('U1', 'A'))],
             [(('U2', 'Y'), ('_oport', 'out2')), (('U1', 'Y'), ('_oport', 'out1'))]]
   
        return V, E      
        

    def setup_graph(self, V, E):
        G = graph.Graph( V, E )
        G.build_connection_matrices()
        self.show_conn_matrices(G)
        return G
        

    def show_conn_matrices(self, G):
        print "#" * 80
        for i in xrange(G.c_levels-1):
            print G.matrices[i].pretty()
        print "Crossover Count: ", G.get_crossover_count()
        

    def test__reorder_gates1(self):
        V, E = self.get_graph_gates1()
        G = self.setup_graph(V, E)
        eng = reordering.Reordering_Engine()
        eng.set_graph(G)
        
        self.assertEquals( eng.G.get_crossover_count(), 3) 
        eng.run()
        self.assertEquals( eng.G.get_crossover_count(), 0)

        self.show_conn_matrices(eng.G)
        
        
        
