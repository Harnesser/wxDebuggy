#!/usr/bin/env python
# $Id: modules_test.py,v 1.1 2007-08-15 23:47:58 marty Exp $
""" Unittest for verilog modules """


import os
import sys

import pyparsing
import unittest

import helpers
print helpers.set_path()
import modules as mut

class ValidModules( unittest.TestCase ):

    trivial_modules = ( 'a.v',
                        'b.v',
                        'top.v',
                      )
                        
    def testTrivialModules(self):
        """ Check a few simple modules.
            These have no comments, ranges, expressions, concatentations.
        """

        if os.path.exists( '../rtl/trivial' ) :
            rtl_basedir = '../rtl/trivial'
        elif os.path.exists( './rtl/trivial' ) :
            rtl_basedir = './rtl/trivial'
        else:
            print "Can't find RTL directory"


        for rtlfile in self.trivial_modules:
            filename = os.path.join( rtl_basedir, rtlfile )
            result = mut.module_declaration.parseFile( filename )            
            self.assert_( result)
    
    def testTrivialClockedModules(self):
        """ Check a few clocked/reset simple modules.
            These have no comments, ranges, expressions, concatentations.
        """

        if os.path.exists( '../rtl/trivial_clk_rstb' ) :
            rtl_basedir = '../rtl/trivial_clk_rstb'
        elif os.path.exists( './rtl/trivial_clk_rstb' ) :
            rtl_basedir = './rtl/trivial_clk_rstb'
        else:
            print "Can't find RTL directory"


        for rtlfile in self.trivial_modules:
            rtlfile = rtlfile.split('.')[0] + '_clk_rstb.v'
            filename = os.path.join( rtl_basedir, rtlfile )
            result = mut.module_declaration.parseFile( filename )            
            self.assert_( result)   

        
def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(ValidModules))
    return suite

if __name__ == '__main__':
    unittest.main()
