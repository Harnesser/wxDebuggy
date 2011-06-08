import os
import sys
import unittest
import pickle
import pprint

def find_base():
    path = os.getcwd()
    while path != '/':
        basename = os.path.basename(path)
        if basename == 'wxDebuggy' or basename == 'workspace':
            return path
        else:
            path = os.path.dirname(path)
    return None
    
def set_paths():
    # Set path to module under test
    proj_dir = find_base()
    sys.path.append(proj_dir) # for vv.
    sys.path.append( os.path.join( proj_dir, 'GUI') )

        
class PnR_Test_Base( unittest.TestCase ):
    
    def load_rtl_module_pickle( self, module_name ):
        """ Load pickled RTL module datastructure. """
        pickle_dir = os.path.join( find_base(), 'tests', 'module_pickles' )
        pickle_name = os.path.join( pickle_dir, module_name +'.dat' )
        hPICKLE = open( pickle_name,'rb')
        module = pickle.load(hPICKLE)
        pprint.pprint(module)
        
        hPICKLE.close()
        return module

    def get_block_names(self, G):
        """ Return the Block.names in every sub-list. """
        names = []
        for layer in G.vertices:
            _names = [ block.name for block in layer ]
            names.append( _names)
        return names
        
