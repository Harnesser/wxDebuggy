#!/usr/bin/env python
""" Unittest for verilog numbers """

import sys

sys.path.append('../../')

import dev as sugiyama
import unittest

class MatrixBasicOperations( unittest.TestCase ):

    def test_initialiser(self):
        """ Gradient checks """
        M = sugiyama.Matrix( list('abc'), list('defg'), [])
        print M

