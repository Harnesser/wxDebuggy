#!/usr/bin/env python
# $Id: modules_test.py,v 1.1 2007-08-15 23:47:58 marty Exp $
""" Unittest for verilog modules """


import os
import sys

import pyparsing
import unittest

import helpers
helpers.set_path()
import modules as mut

RTL_DIR = helpers.rtl_dir()

class ValidModules( unittest.TestCase ):

    trivial_modules = ( 'a.v',
                        'b.v',
                        'top.v',
                      )
                        
    def testTrivialModules(self):
        """ Check a few simple modules.
            These have no comments, ranges, expressions, concatentations.
        """
        for rtlfile in self.trivial_modules:
            filename = os.path.join( RTL_DIR, 'trivial', rtlfile )
            result = mut.module_declaration.parseFile( filename )            
            self.assert_( result)
    
    
    def testTrivialClockedModules(self):
        """ Check a few clocked/reset simple modules.
            These have no comments, ranges, expressions, concatentations.
        """

        for rtlfile in self.trivial_modules:
            rtlfile = rtlfile.split('.')[0] + '_clk_rstb.v'
            filename = os.path.join( RTL_DIR, 'trivial_clk_rstb', rtlfile )
            result = mut.module_declaration.parseFile( filename )            
            self.assert_( result)   

        
def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(ValidModules))
    return suite

if __name__ == '__main__':
    unittest.main()
