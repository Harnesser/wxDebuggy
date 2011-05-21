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
        print M.pretty()
        
        M.row_reversion()
        #self.assertEquals( M.row_vertices, list('abdc') )
        print M

        
    def test_col_reversion_1(self):
        M = matrix.Matrix( self.vertices_top, self.vertices_bot, self.edges )
        print M
        
        M.col_reversion()
        self.assertEquals( M.col_vertices, list('efgih') )
        print M

        

               


        
        
        
        
        
        
        
        
