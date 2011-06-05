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
        layout = self._get_layout('spider')
        self.assert_( layout._count_crossovers() == 0 )
        
    def testLaterCount_Spider(self):
        """ Layer Count Check: 'spider' """
        layout = self._get_layout('spider')
        self.assert_( layout.get_number_of_layers() == 7 )
        
    def testBlockCounts_Spider(self):
        """ Block Count Check: 'spider' """
        layout = self._get_layout('spider')
        self.assert_( layout.get_blocks_per_layer(1) == 4 )
        self.assert_( layout.get_blocks_per_layer(2) == 4 )
        self.assert_( layout.get_blocks_per_layer(3) == 2 )
        self.assert_( layout.get_blocks_per_layer(4) == 1 )
        self.assert_( layout.get_blocks_per_layer(5) == 2 )
        self.assert_( layout.get_blocks_per_layer(6) == 4 )
        self.assert_( layout.get_blocks_per_layer(7) == 4 )
        
    def testHypernetCounts_Spider(self):
        """ Hypernet Count Check: 'spider' """
        layout = self._get_layout('spider')
        self.assert_( layout.get_hypernets_per_layer(1) == 4 )
        self.assert_( layout.get_hypernets_per_layer(2) == 4 )        
        self.assert_( layout.get_hypernets_per_layer(3) == 2 )        
        self.assert_( layout.get_hypernets_per_layer(4) == 2 )        
        self.assert_( layout.get_hypernets_per_layer(5) == 4 )
        self.assert_( layout.get_hypernets_per_layer(6) == 4 )

                
#    def testCrossoverCount_Spider2(self):
#        """ Crossover Check: 'spider_2' """        
#        self._coreCrossoverCount( 'spider_2', 0 )
        
#    def testCrossoverCount_Spider1(self):
#        """ Crossover Check: 'snake_1' """        
#        self._coreCrossoverCount( 'snake_1', 0 )

#    def testCrossoverCount_Gates1(self):
#        """ Crossover Check: 'gates1' """        
#        self._coreCrossoverCount( 'gates1', 0 )
        
#    def testCrossoverCount_Gates2(self):
#        """ Crossover Check: 'gates2' """        
#        self._coreCrossoverCount( 'gates2', 0 )
        
#    def testCrossoverCount_Gates3(self):
#        """ Crossover Check: 'gates3' """        
#        self._coreCrossoverCount( 'gates3', 0 )
        
#    def testCrossoverCount_Top(self):
#        """ Crossover Check: 'top' """        
#        self._coreCrossoverCount( 'top', 0 )
                      
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

    def _get_layout(self, module_name ):
        """ Load in the module and run the layout. """
        module = self._load_rtl_module_pickle(module_name)
        layout = mut.Layout_Engine( use_pickled_module=True )
        layout.place_and_route(module)        
    
        return layout


        
def suite():
    suite = unittest.TestSuite()
    return suite
        
if __name__ == '__main__':
    unittest.main()
