#!/usr/bin/env python

import sys
import os
import pickle
import pprint
import unittest

# Set path to module under test
if os.path.exists('../../../GUI/'): # run from this dir
    sys.path.append('../../../GUI/')
    sys.path.append('../../../') # for vv.
else:
    print "Can't set the correct path"
    
import PnR


class PnR_Basic_Operations( unittest.TestCase ):
    def test_initi(self):
        self.assertTrue(True)
