#!/usr/bin/env python

import sys

sys.path.append('../')

import matrix
import unittest

class MatrixCrossoverCounting( unittest.TestCase ):

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
        
        
    def test_crossover_counts(self):

        M = matrix.Matrix( self.vertices_top, self.vertices_bot, self.edges )
        
        self.assertEqual( M.get_crossover_count(), 14 )
    
        
    def test_crossover_counts_2(self):
        
        self.vertices_top = list('adbc')
        M = matrix.Matrix( self.vertices_top, self.vertices_bot, self.edges )
        
        self.assertEqual( M.get_crossover_count(), 11 )
    
         
    def test_crossover_counts_3(self):
        
        self.vertices_top = list('dabc')
        self.vertices_bot = list('geifh')
        M = matrix.Matrix( self.vertices_top, self.vertices_bot, self.edges )
        
        self.assertEqual( M.get_crossover_count(), 7 )
    
        


               


        
        
        
        
        
        
        
        
