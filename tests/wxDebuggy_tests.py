#!/usr/bin/env python

import unittest

import verilog_parser

suite1 = verilog_parser.modules_test.suite()
suite2 = verilog_parser.numbers_test.suite()


suite = unittest.TestSuite()
suite.addTest(suite1)
suite.addTest(suite2)

unittest.TextTestRunner(verbosity=2).run(suite)

