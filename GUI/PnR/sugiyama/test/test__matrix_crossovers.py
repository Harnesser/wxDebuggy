#!/usr/bin/env python

from collections import namedtuple
import unittest
import sys
sys.path.append('../')

import matrix
Block = namedtuple('Block', 'name inputs outputs')

class MatrixCrossoverCounting( unittest.TestCase ):

    def setUp(self):
        self.vertices_top = [Block(name='in4', inputs=('in4',), outputs=('in4',)),
                             Block(name='in1', inputs=('in1',), outputs=('in1',)),
                             Block(name='in2', inputs=('in2',), outputs=('in2',)),
                             Block(name='in3', inputs=('in3',), outputs=('in3',))]
        self.vertices_bot = [Block(name='U1', inputs=('A', 'B'), outputs=('Y',)),
                             Block(name='U2', inputs=('A', 'B'), outputs=('Y',))]
                     
        self.edges = [(('_iport', 'in4'), ('U2', 'B')),
                      (('_iport', 'in2'), ('U1', 'B')),
                      (('_iport', 'in3'), ('U2', 'A')),
                      (('_iport', 'in1'), ('U1', 'A'))] 
        
        
    def test_crossover_counts(self):

        M = matrix.Matrix( self.vertices_top, self.vertices_bot, self.edges )
        
        self.assertEqual( M.get_crossover_count(), 3 )
    
        
    def test_crossover_counts_2(self):
        
        self.vertices_top = [Block(name='in1', inputs=('in1',), outputs=('in1',)),
                             Block(name='in2', inputs=('in2',), outputs=('in2',)),
                             Block(name='in3', inputs=('in3',), outputs=('in3',)),
                             Block(name='in4', inputs=('in4',), outputs=('in4',))]
                             
        M = matrix.Matrix( self.vertices_top, self.vertices_bot, self.edges )
        
        self.assertEqual( M.get_crossover_count(), 0 )
    
         
    def test_crossover_counts_3(self):
        
        self.vertices_top = [Block(name='in1', inputs=('in1',), outputs=('in1',)),
                             Block(name='in2', inputs=('in2',), outputs=('in2',)),
                             Block(name='in3', inputs=('in3',), outputs=('in3',)),
                             Block(name='in4', inputs=('in4',), outputs=('in4',))]
        self.vertices_top.reverse()
        M = matrix.Matrix( self.vertices_top, self.vertices_bot, self.edges )
        
        self.assertEqual( M.get_crossover_count(), 6 )
    
        


               


        
        
        
        
        
        
        
        
