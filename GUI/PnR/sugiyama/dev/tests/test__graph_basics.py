#!/usr/bin/env python
import sys

sys.path.append('../../')

import dev as sugiyama
import unittest

class MatrixBasicOperations( unittest.TestCase ):

    def test_initialiser(self):
        V = [ list('abc'), list('defg') ]
        E = [ [('a','g'), ('b','f'), ('b','e'), ('c','d')] ]
        G = sugiyama.Graph( V, E )
        
        # Check size of connection matrix
        self.assertEquals( G.c_levels, 2 )
        
        # Check the connection matrix entries       
        print G

        
