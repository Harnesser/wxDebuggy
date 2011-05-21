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
        
    def get_graph_snake1(self):

        V = [[Block(name='in1', inputs=('in1',), outputs=('in1',))],
             [Block(name='U1', inputs=('in1',), outputs=('out1', 'out2', 'out3', 'out4'))],
             [Block(name='U3', inputs=('in1', 'in2'), outputs=('out1', 'out2')),
              Block(name='U2', inputs=('in1', 'in2'), outputs=('out1', 'out2', 'out3'))],
             [Block(name='U5', inputs=('in1', 'in2'), outputs=('out1', 'out2')),
              Block(name='U4', inputs=('in1', 'in2'), outputs=('out1', 'out2', 'out3')),
              Block(name='_dummy_U2__to__U7_4', inputs=('_in',), outputs=('_out',))],
             [Block(name='U7', inputs=('in1', 'in2', 'in3'), outputs=('out1',)),
              Block(name='U6', inputs=('in1', 'in2', 'in3'), outputs=('out1',))],
             [Block(name='U8', inputs=('in1', 'in2'), outputs=('out',))],
             [Block(name='out1', inputs=('out1',), outputs=('out1',))],
             ]
        E = [[(('_iport', 'in1'), ('U1', 'in1'))],
             [(('U1', 'out2'), ('U2', 'in2')),
              (('U1', 'out3'), ('U3', 'in1')),
              (('U1', 'out4'), ('U3', 'in2')),
              (('U1', 'out1'), ('U2', 'in1'))],
             [(('U2', 'out2'), ('U4', 'in1')),
              (('U3', 'out1'), ('U5', 'in1')),
              (('U2', 'out3'), ('U4', 'in2')),
              (('U3', 'out2'), ('U5', 'in2')),
              (('U2', 'out1'), ('_dummy_U2__to__U7_4', '_in'))],
             [(('U5', 'out1'), ('U7', 'in1')),
              (('U5', 'out2'), ('U7', 'in3')),
              (('U4', 'out3'), ('U6', 'in3')),
              (('U4', 'out2'), ('U6', 'in2')),
              (('U4', 'out1'), ('U6', 'in1')),
              (('_dummy_U2__to__U7_4', '_out'), ('U7', 'in2'))],
             [(('U6', 'out1'), ('U8', 'in1')), (('U7', 'out1'), ('U8', 'in2'))],
             [(('U8', 'out'), ('_oport', 'out1'))]]

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
        
        
    def test__reorder_snake1(self):
        V, E = self.get_graph_snake1()
        G = self.setup_graph(V, E)
        eng = reordering.Reordering_Engine()
        eng.set_graph(G)
        self.show_conn_matrices(eng.G)
        
        self.assertEquals( eng.G.get_crossover_count(), 11) 
        eng.run()
        self.assertEquals( eng.G.get_crossover_count(), 2)

        self.show_conn_matrices(eng.G)
        
               
        
