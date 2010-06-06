#!/usr/bin/env python

import sys

sys.path.append('../../')

import dev as sugiyama
import unittest

class MatrixReversion( unittest.TestCase ):

    def setUp(self):
        """"
                     e    f    g    h    i
                a    1    0    0    0    0 : 0.0
                b    1    1    0    0    1 : 1.7
                c    0    1    0    1    0 : 2.0
                d    1    0    1    0    1 : 2.0
                   1.3  1.5  3.0  2.0  2.0
        """
                            
        edges = 'ae:be:bi:bf:cf:ch:de:dg:di'
        E = []
        V_top = set()
        V_bot = set()
        
        for edge in edges.split(':'):
            e = tuple(edge)
            E.append(e)
            V_top.add(e[0])
            V_bot.add(e[1])
            
        self.vertices_top = list(V_top)
        self.vertices_bot = list(V_bot)
        self.edges = E
        
        self.vertices_top.sort()
        self.vertices_bot.sort()
        
        
    def test_row_reversion_1(self):
        M = sugiyama.Matrix( self.vertices_top, self.vertices_bot, self.edges )
        print M
        
        M.row_reversion()
        self.assertEquals( M.row_vertices, list('abdc') )
        print M

        
    def test_col_reversion_1(self):
        M = sugiyama.Matrix( self.vertices_top, self.vertices_bot, self.edges )
        print M
        
        M.col_reversion()
        self.assertEquals( M.col_vertices, list('efgih') )
        print M

        

               


        
        
        
        
        
        
        
        
