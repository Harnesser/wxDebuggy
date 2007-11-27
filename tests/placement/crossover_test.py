#!/usr/bin/env python
""" Unittest for verilog numbers """

import sys
import os

# Set path to module under test
if os.path.exists('../../GUI/PnR'): # run from this dir
    sys.path.append('../../GUI/PnR')
else:
    print "Can't set the correct path"

import placement_ga as mut
import unittest

class ValidCrossingSegments( unittest.TestCase ):

    def testGradients(self):
        """ Gradient checks """
        
        segments_and_gradients = [ [(0,2),(2,0),     -1.0] ,
                                   [(0,6),(4,2),     -1.0],
                                   [(2,2),(7,4),     (2.0/5.0)],
                                 ]

        for p1,p2,grad in segments_and_gradients:
            self.assert_( mut.gradient( (p1,p2) ) == grad )
            self.assert_( mut.gradient( (p2,p1) ) == grad )


    def testValidCrossovers( self ):
        """ All these line segments should cross """

        segments = [ ( ( (2,0), (0,2) ), ( (0,0), (2,2) ) ),
                     ( ( (0,5), (7,2) ), ( (5,2), (2,5) ) ),
                     ( ( (2,0), (0,2) ), ( (0,0), (2,1) ) ),
                    ]

        for seg1, seg2 in segments:
            self.assert_( mut.is_crossover( seg1, seg2 ) )


#    def testParallelLines( self ):


#    def testDoNotCross( self ):

 
                       
        
def suite():
    suite = unittest.TestSuite()
    #suite.addTest(unittest.makeSuite(ValidNumberStrings))
    return suite
        
if __name__ == '__main__':
    unittest.main()
