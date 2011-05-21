#!/usr/bin/env python
import sys
import unittest

sys.path.append('./')
sys.path.append('../')
import matrix
import helpers

class MatrixReversion( unittest.TestCase ):
    "Connectivity Matrix Row Reversion Tests."


    def test_row_reversion_1(self):
        edges = [
            'A.1:Z.2', 'A.2:Z.3',
            'B.1:X.2', 'B.2:X.3', 'B.3:X.4',
            'C.1:X.1', 
            'D.1:Y.1', 'D.2:Y.2', 'D.3:Z.1'
            ]
        V_top, V_bot, E = helpers.parse_shorthand(';'.join(edges))
        M = matrix.Matrix( V_top, V_bot, E )
        print "BEFORE:", M.pretty()
        
        # Check setup
        expected_block_order = [ 'A', 'C', 'B', 'D' ]
        for expected, actual in zip( expected_block_order, M.row_blocks ):
            self.assertEquals( expected, actual.name )
         
        # Reverse and check   
        M.row_reversion()
        print "AFTER:", M.pretty()
        expected_block_order = [ 'A', 'C', 'D', 'B' ]
        for expected, actual in zip( expected_block_order, M.row_blocks ):
            self.assertEquals( expected, actual.name )        


        
    def test_col_reversion_1(self):
        M = matrix.Matrix( self.vertices_top, self.vertices_bot, self.edges )
        print M
        
        M.col_reversion()
        self.assertEquals( M.col_vertices, list('efgih') )
        print M

        

               


        
        
        
        
        
        
        
        
