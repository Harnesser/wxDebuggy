#!/usr/bin/env python

import pnr_test_base
pnr_test_base.set_paths()

from PnR.pnr import PnR

class PnR_Basic_Operations( pnr_test_base.PnR_Test_Base ):

    def test__pickle_loader(self):
        module = self.load_rtl_module_pickle('spider')
        self.assertEquals(module.name, 'spider')
        
    def test__pnr_graph_builder_1(self):
        module = self.load_rtl_module_pickle('spider')
        pnr = PnR()
        pnr.module = module
        pnr._build_graph()
        
        # spot checks
        self.assertEquals( pnr.layer_dict['U9'], 5 )
        
        
