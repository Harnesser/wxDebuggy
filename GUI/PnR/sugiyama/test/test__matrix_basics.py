#!/usr/bin/env python
""" Unittest for verilog numbers """

import unittest
from collections import namedtuple

import helpers
helpers.set_path()
import matrix

Block = namedtuple('Block', 'name inputs outputs')

class MatrixBasicOperations( unittest.TestCase ):

    def setUp(self):
        self.vertices1 = [Block(name='in4', inputs=('in4',), outputs=('in4',)),
                          Block(name='in1', inputs=('in1',), outputs=('in1',)),
                          Block(name='in2', inputs=('in2',), outputs=('in2',)),
                          Block(name='in3', inputs=('in3',), outputs=('in3',))]
        self.vertices2 = [Block(name='U1', inputs=('A', 'B'), outputs=('Y',)),
                          Block(name='U2', inputs=('A', 'B'), outputs=('Y',))]
                     
        self.edges = [(('_iport', 'in4'), ('U2', 'B')),
                      (('_iport', 'in2'), ('U1', 'B')),
                      (('_iport', 'in3'), ('U2', 'A')),
                      (('_iport', 'in1'), ('U1', 'A'))]        
        
        
    def test_initialiser(self):                 
        M = matrix.Matrix( self.vertices1, self.vertices2, self.edges )

        # Check size of connection matrix
        self.assertEquals( M.get_size(), (4,4) )
        
        # Check the connection matrix entries
        self.assertEquals( M.M[0], [ 0, 0, 0, 1] )
        self.assertEquals( M.M[1], [ 1, 0, 0, 0] )
        self.assertEquals( M.M[2], [ 0, 1, 0, 0] )    
        self.assertEquals( M.M[3], [ 0, 0, 1, 0] )    
                
        print M
        print M.pretty()
        
    def test_copy(self):
        M = matrix.Matrix( self.vertices1, self.vertices2, self.edges )
        
        M1 = M.copy()
        M1.col_blocks = [Block(name='U2', inputs=('A', 'B'), outputs=('Y',)),
                         Block(name='U1', inputs=('A', 'B'), outputs=('Y',))]
        M1.update()
        
        self.assertEquals( M.col_vertices, ['U1.A', 'U1.B', 'U2.A', 'U2.B'] )
        self.assertEquals( M1.col_vertices, ['U2.A', 'U2.B', 'U1.A', 'U1.B'] )
         
        self.assertEquals( M.M[0],  [ 0, 0, 0, 1] )
        self.assertEquals( M1.M[0],  [ 0, 1, 0, 0 ] )
        
        
