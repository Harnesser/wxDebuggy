#!/usr/bin/env python
import sys
import unittest

import helpers
helpers.set_path()
import matrix

class MatrixReversion( unittest.TestCase ):
    "Connectivity Matrix Row Reversion Tests."


    def test_row_reversion_1(self):
        edges = [
            'A.1:Z.2', 'A.2:Z.3',
            'B.1:X.2', 'B.2:X.3', 'B.3:X.4',
            'C.1:X.1', 
            'D.1:Y.1', 'D.2:Y.2', 'D.3:Z.1'
            ]
        V_top, V_bot, E = helpers.parse_shorthand(';'.join(edges),
            [ list('ACBD'), list('YXZ') ] )
        M = matrix.Matrix( V_top, V_bot, E)
        print "BEFORE:", M.pretty()
        
        # Reverse and check   
        M.row_reversion()
        print "AFTER:", M.pretty()
        expected_block_order = [ 'A', 'C', 'D', 'B' ]
        for expected, actual in zip( expected_block_order, M.row_blocks ):
            self.assertEquals( expected, actual.name )        


        
    def test_col_reversion_1(self):
        edges = [
            'A.1:V.1', 'A.2:W.1', 'A.3:W.2', 'A.4:V.2'
            ]
        V_top, V_bot, E = helpers.parse_shorthand(';'.join(edges),
             [ list('A'), list('VW') ] )
        M = matrix.Matrix( V_top, V_bot, E )
        print "BEFORE:", M.pretty()
        
        M.col_reversion()
        print "AFTER:", M.pretty()
        expected_block_order = [ 'W', 'V' ]
        for expected, actual in zip( expected_block_order, M.col_blocks ):
            self.assertEquals( expected, actual.name )        
        
        
    def test_row_reversion_snake_1(self):
        """ Snake_1 Sub-matrix test.
        This didn't seem to work properly. 
        """
        edges = ['U5.out1:U7.in1',
                 'U5.out2:U7.in3',
                 'U4.out3:U6.in3',
                 'U4.out2:U6.in2',
                 'U4.out1:U6.in1',
                 '_dummy_U2__to__U7_4._out:U7.in2']       
        
        V_top, V_bot, E = helpers.parse_shorthand(';'.join(edges),
             [ ['_dummy_U2__to__U7_4', 'U4', 'U5' ],
               ['U6', 'U7' ] ] )       
               
        M = matrix.Matrix( V_top, V_bot, E )
        print "BEFORE:", M.pretty()
        
