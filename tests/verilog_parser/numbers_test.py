#!/usr/bin/env python
""" Unittest for verilog numbers """

import sys
sys.path.append('../../Verilog2001/BNF')

import pyparsing
import numbers as mut
import unittest

class ValidNumberStrings( unittest.TestCase ):
    valid_number_strings = ( '34',
                             '34.4545454', 
                             "'d34",
                             "'h343ea_a7",
                             "34e-9",
                             "34675",
                             "6'b00_x010?",
                             "34'SH44AA",
                        )
                        
    def testAcceptValidNumberStrings(self):
        """ Make sure known valid number strings are parsed """
        for verilog in self.valid_number_strings:
            result = mut.number.parseString( verilog )
            
            is_ok = ( result[0].lower() == verilog.lower() )
            self.assert_( is_ok )
        
    invalid_number_strings = (
                              '3l',
                              "'n343434",
                              "7'b01_01_1110_2",
                              "7'h34_3g",
                              "7'd0134787667d78668",
                              "34.e34343",
                              )
                              
    def testRejectInvalidNumberStrings(self):
        """ Make sure known invalid number strings are not parsed """
        for verilog in self.invalid_number_strings:
            #fails if doesn't match the whole thing or raises an exception
            try:
                result = mut.number.parseString( verilog )
            except pyparsing.ParseException:
                self.assert_(True)
            else:
                is_ok = not ( result[0].lower() == verilog.lower() )
                self.assert_( is_ok )
                
            # 
            #self.assertRaises( pyparsing.ParseException,
            #                   mut.number.parseString, verilog  )
        
    def suite(self):
        return unittest.makeSuite( ValidNumberStrings )
        
if __name__ == '__main__':
    unittest.main()
