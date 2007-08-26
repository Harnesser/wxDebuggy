""" Unittest for verilog modules """
# $Id: modules_test.py,v 1.1 2007-08-15 23:47:58 marty Exp $

import sys
sys.path.append('../../Verilog2001/BNF')

import os.path
import pyparsing
import modules as mut
import unittest

class ValidModules( unittest.TestCase ):

    rtl_basedir = '../rtl/trivial'
    trivial_modules = ( 'a.v',
                        'b.v',
                        'top.v',
                        
                      )
                        
    def testTrivialModules(self):
        """ Check a few simple modules.  These have no comments, ranges,
            expressions, concatentations.
        """
        for rtlfile in self.trivial_modules:
            filename = os.path.join( self.rtl_basedir, rtlfile )
            result = mut.module_declaration.parseFile( filename )            
            self.assert_( result)
    
    def suite(self):
        return unittest.makeSuite( ValidModules )
        
if __name__ == '__main__':
    unittest.main()
