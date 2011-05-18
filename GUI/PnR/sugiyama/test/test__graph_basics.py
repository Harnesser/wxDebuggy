#!/usr/bin/env python
import sys
import unittest
from collections import namedtuple

sys.path.append('../')
import graph

class GraphBasicOperations( unittest.TestCase ):


    def get_circuit(self):
        Block = namedtuple('Block', 'name inputs outputs')
        
        V = [[Block(name='in4', inputs=('in4',), outputs=('in4',)),
              Block(name='in1', inputs=('in1',), outputs=('in1',)),
              Block(name='in2', inputs=('in2',), outputs=('in2',)),
              Block(name='in3', inputs=('in3',), outputs=('in3',))],
             [Block(name='U1', inputs=('A', 'B'), outputs=('Y',)),
              Block(name='U2', inputs=('A', 'B'), outputs=('Y',))],
             [Block(name='U3', inputs=('A', 'B'), outputs=('Y',))],
             [Block(name='out1', inputs=('out1',), outputs=('out1',))],
             ]
        E = [[(('_iport', 'in4'), ('U2', 'B')),
              (('_iport', 'in2'), ('U1', 'B')),
              (('_iport', 'in3'), ('U2', 'A')),
              (('_iport', 'in1'), ('U1', 'A'))],
             [(('U2', 'Y'), ('U3', 'B')), (('U1', 'Y'), ('U3', 'A'))],
             [(('U3', 'Y'), ('_oport', 'out1'))]]


        G = graph.Graph(V, E)
        return G


    def test_initialiser(self):
        G = self.get_circuit()
        # Check size of connection matrix
        self.assertEquals(G.c_levels, 4)

        
    def test_matrices_ckt_M0(self):
        G = self.get_circuit()
        G.build_connection_matrices()
        self.assertEquals( G.matrices[0].M, 
            [[0,0,0,1],
             [1,0,0,0],
             [0,1,0,0],
             [0,0,1,0]] )
        
        
    def test_matrices_ckt_M1(self):
        G = self.get_circuit()
        G.build_connection_matrices()
        print G.matrices[1]
        self.assertEquals( G.matrices[1].M, 
            [[1,0],
             [0,1]] )


    def test_matrices_ckt_M2(self):
        G = self.get_circuit()
        G.build_connection_matrices()
        print G.matrices[2]
        self.assertEquals( G.matrices[2].M, 
            [[1]] )

        
    def test_crossovers_1(self):
        G = self.get_circuit()
        G.build_connection_matrices()
        self.assertEquals( G.get_crossover_count(), 3)
        
