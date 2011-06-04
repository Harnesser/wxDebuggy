import os
import sys
import unittest
import pickle
import pprint

PICKLE_DIR = '../../module_pickles/'

def set_paths():
    # Set path to module under test
    if os.path.exists('../../../GUI/'): # run from this dir
        sys.path.append('../../../GUI/')
        sys.path.append('../../../') # for vv.
    else:
        print "Can't set the correct path"
        
        
class PnR_Test_Base( unittest.TestCase ):
    
    def load_rtl_module_pickle( self, module_name ):
        """ Load pickled RTL module datastructure. """
        hPICKLE = open(PICKLE_DIR + module_name +'.dat','rb')
        module = pickle.load(hPICKLE)
        pprint.pprint(module)
        
        hPICKLE.close()
        return module


