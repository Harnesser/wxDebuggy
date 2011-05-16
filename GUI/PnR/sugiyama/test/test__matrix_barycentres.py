#!/usr/bin/env python

import sys
import unittest
from collections import namedtuple

sys.path.append('../')
import matrix

Block = namedtuple('Block', 'name inputs outputs')

class MatrixBarycentreOperations( unittest.TestCase ):

    def setUp(self):
        self.vertices_top = [Block(name='in4', inputs=('in4',), outputs=('in4',)),
                             Block(name='in1', inputs=('in1',), outputs=('in1',)),
                             Block(name='in2', inputs=('in2',), outputs=('in2',)),
                             Block(name='in3', inputs=('in3',), outputs=('in3',))]
        self.vertices_bot = [Block(name='U1', inputs=('A', 'B', 'C'), outputs=('Y',)),
                             Block(name='U2', inputs=('A', 'B'), outputs=('Y',))]
                     
        self.edges = [(('_iport', 'in4'), ('U2', 'B')),
                      (('_iport', 'in2'), ('U1', 'B')),
                      (('_iport', 'in2'), ('U1', 'C')),
                      (('_iport', 'in3'), ('U2', 'A')),
                      (('_iport', 'in1'), ('U1', 'A'))]    
                      
        self.vertices_top_ordered = [ self.vertices_top[1],
                                      self.vertices_top[2],
                                      self.vertices_top[3],
                                      self.vertices_top[0] ] 
                                      

        self.vertices_top_2 = [Block(name='U1', inputs=('A', 'B', 'C'), outputs=('Y1', 'Y2', 'Y3' )),
                               Block(name='U2', inputs=('A', 'B'), outputs=('Y1', 'Y2'))]
        self.edges_2 = [(('U1', 'Y1'), ('_oport', 'in2' )),
                        (('U1', 'Y2'), ('_oport', 'in4' )),
                        (('U2', 'Y2'), ('_oport', 'in1' )),
                        (('U1', 'Y3'), ('_oport', 'in3' ))]
                        
    #
    # Flattened Barycentre Checks
    #
    def test_row_barycentre_calcs(self):
        M = matrix.Matrix( self.vertices_top, self.vertices_bot, self.edges )
        self.check_M0_row_barycentres(M)
        

    def test_col_barycentre_calcs(self):
        M = matrix.Matrix( self.vertices_top, self.vertices_bot, self.edges )
        self.check_M0_col_barycentres(M)

        
    def test_row_barycentre_calcs_2(self):
        M = matrix.Matrix( self.vertices_top_ordered, self.vertices_bot, self.edges )
        self.check_M1_row_barycentres(M)        


    def test_col_barycentre_calcs_2(self):
        M = matrix.Matrix( self.vertices_top_ordered, self.vertices_bot, self.edges )
        self.check_M1_col_barycentres(M)    
                    
    #
    # Block Barycentre Checks
    #
    def test_block_row_barycentre_calcs_1(self): 
        M = matrix.Matrix( self.vertices_top, self.vertices_bot, self.edges )
        self.assertEquals( len(M.block_row_barycentres), 4 )
        self.assertAlmostEqual( M.block_row_barycentres[0], 5.0 )
        self.assertAlmostEqual( M.block_row_barycentres[1], 1.0 )
        self.assertAlmostEqual( M.block_row_barycentres[2], 2.5 )        
        self.assertAlmostEqual( M.block_row_barycentres[3], 4.0 )   
    
    def test_block_row_barycentre_calcs_2(self):
        M = matrix.Matrix( self.vertices_top_2, self.vertices_top, self.edges_2 )
        print M
        self.assertEquals( len(M.block_row_barycentres), 2 )
        self.assertAlmostEqual( M.block_row_barycentres[0], ( 1.0 + 4.0 + 3.0 ) / 3.0 )
        self.assertAlmostEqual( M.block_row_barycentres[1], ( 2.0 + 0.0 ) / 2.0 )
        
    def test_block_col_barycentre_calcs_1(self):
        M = matrix.Matrix( self.vertices_top, self.vertices_bot, self.edges )
        self.assertEquals( len(M.block_col_barycentres), 2 )
        self.assertAlmostEqual( M.block_col_barycentres[0], ( 2.0 + 3.0 + 3.0 ) / 3.0 )
        self.assertAlmostEqual( M.block_col_barycentres[1], ( 4.0 + 1.0 ) / 2.0 )        
    #
    # Reordering Checks
    #
    def test_row_reorder_1(self):
        M = matrix.Matrix( self.vertices_top, self.vertices_bot, self.edges )
        print M
        M.barycentre_row_reorder()
        print M
        
        self.assertEquals( M.row_vertices, list('adbc') )
        self.check_M1_row_barycentres(M)
        self.check_M1_col_barycentres(M)      
        

    def test_col_reorder_1(self):
        self.vertices_top = list('adbc')
        M = matrix.Matrix( self.vertices_top, self.vertices_bot, self.edges )
        print M
        M.barycentre_col_reorder()
        print M
        
        self.assertEquals( M.col_vertices, list('egfih') )
        self.check_M2_row_barycentres(M)
        self.check_M2_col_barycentres(M)              
        
        
    #  These functions below check the barycentres for both rows and
    # columns based on the first 3 matrices in Sugiyama's worked example
    # of the two-layer crossing barycentre algorithm.
        
    def check_M0_row_barycentres(self, M):
        self.assertAlmostEqual( M.row_barycentres[0], 5.0 )
        self.assertAlmostEqual( M.row_barycentres[1], 1.0 )
        self.assertAlmostEqual( M.row_barycentres[2], 2.5 )        
        self.assertAlmostEqual( M.row_barycentres[3], 4.0 )      
    
    def check_M0_col_barycentres(self, M):
        self.assertAlmostEqual( M.col_barycentres[0], 2.0 )
        self.assertAlmostEqual( M.col_barycentres[1], 3.0 )
        self.assertAlmostEqual( M.col_barycentres[2], 3.0 )        
        self.assertAlmostEqual( M.col_barycentres[3], 4.0 )        
        self.assertAlmostEqual( M.col_barycentres[4], 1.0 ) 

    
    # Row Reordered
    def check_M1_row_barycentres(self, M):
        self.assertAlmostEqual( M.row_barycentres[0], 1.0 )
        self.assertAlmostEqual( M.row_barycentres[1], 2.5 )
        self.assertAlmostEqual( M.row_barycentres[2], 4.0 )        
        self.assertAlmostEqual( M.row_barycentres[3], 5.0)  
                
    def check_M1_col_barycentres(self, M):    
        self.assertAlmostEqual( M.col_barycentres[0], 1.0 )
        self.assertAlmostEqual( M.col_barycentres[1], 2.0 )
        self.assertAlmostEqual( M.col_barycentres[2], 2.0 )        
        self.assertAlmostEqual( M.col_barycentres[3], 3.0 )        
        self.assertAlmostEqual( M.col_barycentres[4], 4.0 )             
        
    # Col Reordered
    def check_M2_row_barycentres(self, M):
        self.assertAlmostEqual( M.row_barycentres[0], 2.0 )
        self.assertAlmostEqual( M.row_barycentres[1], 2.3333333 )
        self.assertAlmostEqual( M.row_barycentres[2], 3.3333333 )        
        self.assertAlmostEqual( M.row_barycentres[3], 4.0 )  
                
    def check_M2_col_barycentres(self, M):    
        self.assertAlmostEqual( M.col_barycentres[0], 2.0 )
        self.assertAlmostEqual( M.col_barycentres[1], 2.0 )        
        self.assertAlmostEqual( M.col_barycentres[2], 2.5 )
        self.assertAlmostEqual( M.col_barycentres[3], 3.0 )             
        self.assertAlmostEqual( M.col_barycentres[4], 3.5 )        

