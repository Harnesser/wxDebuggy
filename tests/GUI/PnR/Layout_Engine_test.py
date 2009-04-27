#!/usr/bin/env python
""" Unittest for EGB Layout Algorithm """

import sys
import os
import pickle
import pprint
import unittest

# Set path to module under test
if os.path.exists('../../../GUI/PnR'): # run from this dir
    sys.path.append('../../../GUI/PnR')
    sys.path.append('../../../') # for vv.
else:
    print "Can't set the correct path"
    
import vv
import Layout_Engine as mut

class ValidCrossingSegments( unittest.TestCase ):

    #
    # Test Methods
    #
    def testCrossoverCount_Spider(self):
        """ Crossover Check: 'spider' """        
        self._coreCrossoverCount( 'spider', 0 )
        
    def testCrossoverCount_Spider2(self):
        """ Crossover Check: 'spider_2' """        
        self._coreCrossoverCount( 'spider_2', 0 )
        
    def testCrossoverCount_Spider1(self):
        """ Crossover Check: 'snake_1' """        
        self._coreCrossoverCount( 'snake_1', 0 )

    def testCrossoverCount_Gates1(self):
        """ Crossover Check: 'gates1' """        
        self._coreCrossoverCount( 'gates1', 0 )
        
    def testCrossoverCount_Gates2(self):
        """ Crossover Check: 'gates2' """        
        self._coreCrossoverCount( 'gates2', 0 )
        
    def testCrossoverCount_Gates3(self):
        """ Crossover Check: 'gates3' """        
        self._coreCrossoverCount( 'gates3', 0 )
        
    def testCrossoverCount_Top(self):
        """ Crossover Check: 'top' """        
        self._coreCrossoverCount( 'top', 0 )
                      
    #
    # Helper Methods
    #
    def _load_rtl_module_pickle( self, module_name ):
        """ Load pickled RTL module datastructure. """
        
        hPICKLE = open('../../module_pickles/' + module_name +'.dat','rb')
        module = pickle.load(hPICKLE)
        pprint.pprint(module)
        
        hPICKLE.close()
        return module
 

    def _coreCrossoverCount(self, module_name, c_crossovers_expected):
        """ """
        module = self._load_rtl_module_pickle(module_name)
    
        eng = mut.Layout_Engine( use_pickled_module=True )
        eng.place_and_route(module)      
        c_crossovers = eng._count_crossovers()
        print 'Final crossovers for %s:%d' % ( module_name, c_crossovers )
        self.assert_( c_crossovers == c_crossovers_expected )
               

        
def suite():
    suite = unittest.TestSuite()
    return suite
        
if __name__ == '__main__':
    unittest.main()
