#!/usr/bin/env python

import pnr_test_base
pnr_test_base.set_paths()

import PnR

class PnR_Basic_Operations( pnr_test_base.PnR_Test_Base ):

    def test__pickle_loader(self):
        module = self.load_rtl_module_pickle('spider')
        self.assertEquals(module.name, 'spider')
        
    
