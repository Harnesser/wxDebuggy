#! /usr/bin/env python
""" Sugiyama Stuff """

import sys
sys.path.append('../../')

import dev.sugiyama as sugiyama
import unittest

class SugiyamaOperations( unittest.TestCase ):

    ##
    ## Left Shifts
    ##
    def test__shift_left_to_ideal_all(self):
        x_pos    = [ 1, 2, 3, 4, 5, 6 ]
        expected = [ -4, -3, -2, -1, 0, 1 ]
        shifted = sugiyama.shift_left_to_ideal(j=5, x_ideal=1, x_pos=x_pos)
        self.assertEquals( shifted, expected )
        
    def test__shift_left_to_ideal(self):
        x_pos    = [ -7, -6,  5,  6,  7, 8 ]
        expected = [ -7, -6, -2, -1, 0, 1]
        shifted = sugiyama.shift_left_to_ideal(j=5, x_ideal=1, x_pos=x_pos)
        self.assertEquals( shifted, expected )
        
#    def test__shift_left_to_ideal_leftmost(self):
#        x_pos    = [ 2, 3, 4, 5, 6, 7 ]
#        expected = [ 1, 3, 4, 5, 6, 7 ]
#        shifted = sugiyama.shift_left_to_ideal(j=0, x_ideal=1, x_pos=x_pos)
#        self.assertEquals( shifted, expected )    
    
    def test__shift_left_near_all(self):
        x_pos    = [ 3, 4, 5, 10, 11, 12, 13]
        expected = [ 3, 4, 5, 6,  7,  8,  9]
        shifted = sugiyama.shift_left_to_near_ideal(j=6, k=2, x_ideal=1, x_pos=x_pos)
        self.assertEquals( shifted, expected )
        
    ##
    ## Right Shifts
    ##
    def test__shift_right_to_ideal_all(self):
        x_pos    = [ 1, 2, 3, 4, 5, 6, 7]
        expected = [ 4, 5, 6, 7, 8, 9, 10]
        shifted = sugiyama.shift_right_to_ideal(j=0, x_ideal=4, x_pos=x_pos )
        self.assertEquals( shifted, expected )
        
    def test__shift_right_to_ideal(self):
        x_pos    = [ 1, 2, 3, 4,  5,  6,  7,  8]
        expected = [ 1, 2, 3, 9, 10, 11, 12, 13]
        shifted = sugiyama.shift_right_to_ideal(j=3, x_ideal=9, x_pos=x_pos)
        self.assertEquals( shifted, expected )
        
    def test__shift_right_near_ideal(self):
        x_pos    = [ 1,  2,  3, 12, 13, 14, 15, 16 ]
        expected = [ 1, 10, 11, 12, 13 ,14 ,15 ,16 ]
        shifted = sugiyama.shift_right_to_near_ideal(j=1, k=3, x_ideal=14, x_pos=x_pos)
        self.assertEquals( shifted, expected )
    
