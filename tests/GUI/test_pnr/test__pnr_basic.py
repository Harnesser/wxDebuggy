#!/usr/bin/env python

import pnr_test_base
pnr_test_base.set_paths()

from PnR.pnr import PnR

class PnR_Basic_Operations( pnr_test_base.PnR_Test_Base ):

    def load_spider(self):
        module = self.load_rtl_module_pickle('spider')
        pnr = PnR()
        pnr.module = module
        pnr._build_graph()
        return pnr        
    
    def test__pickle_loader(self):
        module = self.load_rtl_module_pickle('spider')
        self.assertEquals(module.name, 'spider')
        
    def test__pnr_graph_builder_1(self):
        pnr = self.load_spider()
        
        # spot checks
        self.assertEquals( pnr.layer_dict['U9'], 5 )
        
    def test__pnr_graph_builder_sugiyama_vertices(self):
        pnr = self.load_spider()

        names_5 = [ block.name for block in pnr.sugiyama_vertices[5] ]
        self.assertEquals( names_5, ['U11', 'U10', 'U13', 'U12'])
        
    def test__pnr_graph_builder_sugiyama_edges(self):
        pnr = self.load_spider()
        
        self.assertEquals( pnr.sugiyama_edges[4], [(('U8', 'out2'), ('U11', 'in')),
            (('U8', 'out1'), ('U10', 'in')),
            (('U9', 'out1'), ('U12', 'in')),
            (('U9', 'out2'), ('U13', 'in'))] )

