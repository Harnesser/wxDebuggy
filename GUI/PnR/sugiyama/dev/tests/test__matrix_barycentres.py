#!/usr/bin/env python

import sys

sys.path.append('../../')

import dev as sugiyama
import unittest

class MatrixBarycentreOperations( unittest.TestCase ):

    def setUp(self):
        
        edges = 'ae:af:be:bh:bi:cf:ch:ci:de:dg:di'
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
        
        
    def test_row_barycentre_calcs(self):

        M = sugiyama.Matrix( self.vertices_top, self.vertices_bot, self.edges )
        print M
        
        self.assertAlmostEqual( M.row_barycentres[0], 0.5 )
        self.assertAlmostEqual( M.row_barycentres[1], 2.3333333 )
        self.assertAlmostEqual( M.row_barycentres[2], 2.66666666 )        
        self.assertAlmostEqual( M.row_barycentres[3], 2.0 )        
        

    def test_row_barycentre_calcs(self):
        
        M = sugiyama.Matrix( self.vertices_top, self.vertices_bot, self.edges )
        print M
        
        self.assertAlmostEqual( M.col_barycentres[0], 1.3333333 )
        self.assertAlmostEqual( M.col_barycentres[1], 1.0 )
        self.assertAlmostEqual( M.col_barycentres[2], 3.0 )        
        self.assertAlmostEqual( M.col_barycentres[3], 1.5 )        
        self.assertAlmostEqual( M.col_barycentres[4], 2.0 )  
        
        
    def test_row_barycentre_calcs_2(self):

        self.vertices_top = list('adbc')
        M = sugiyama.Matrix( self.vertices_top, self.vertices_bot, self.edges )
        print M
        
        self.assertAlmostEqual( M.row_barycentres[0], 0.5 )
        self.assertAlmostEqual( M.row_barycentres[1], 2.0 )
        self.assertAlmostEqual( M.row_barycentres[2], 2.3333333 )        
        self.assertAlmostEqual( M.row_barycentres[3], 2.7777777 )        
        

    def test_row_barycentre_calcs_2(self):
        
        self.vertices_top = list('adbc')
        M = sugiyama.Matrix( self.vertices_top, self.vertices_bot, self.edges )
        print M
        
        self.assertAlmostEqual( M.col_barycentres[0], 1.0 )
        self.assertAlmostEqual( M.col_barycentres[1], 1.5 )
        self.assertAlmostEqual( M.col_barycentres[2], 1.0 )        
        self.assertAlmostEqual( M.col_barycentres[3], 2.5 )        
        self.assertAlmostEqual( M.col_barycentres[4], 2.0 )  
                    

        
        
        
        
        
        
        
        
