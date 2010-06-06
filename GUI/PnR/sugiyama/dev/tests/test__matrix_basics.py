#!/usr/bin/env python
""" Unittest for verilog numbers """

import sys

sys.path.append('../../')

import dev as sugiyama
import unittest

class MatrixBasicOperations( unittest.TestCase ):

    def test_initialiser(self):
        """ Gradient checks """
        M = sugiyama.Matrix( list('abc'), list('defg'), 
            [('a','g'), ('b','f'), ('b','e'), ('c','d')] )
        

        # Check size of connection matrix
        self.assertEquals( M.get_size(), (3,4) )
        
        # Check the connection matrix entries
        self.assertEquals( M.M[0], [ 0, 0, 0, 1] )
        self.assertEquals( M.M[1], [ 0, 1, 1, 0] )
        self.assertEquals( M.M[2], [ 1, 0, 0, 0] )    
        
        print M
