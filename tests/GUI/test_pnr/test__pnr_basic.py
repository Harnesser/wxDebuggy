#!/usr/bin/env python

import pnr_test_base
pnr_test_base.set_paths()

from PnR.pnr import PnR

class PnR_Basic_Operations( pnr_test_base.PnR_Test_Base ):

    def load_module(self, module_name):
        module = self.load_rtl_module_pickle(module_name)
        pnr = PnR()
        pnr.module = module
        pnr._build_graph()
        return pnr        
    
    def test__pickle_loader(self):
        module = self.load_rtl_module_pickle('spider')
        self.assertEquals(module.name, 'spider')
        
    def test__pnr_graph_builder_1(self):
        pnr = self.load_module('spider')
        
        # spot checks
        self.assertEquals( pnr.layer_dict['U9'], 5 )
        
    def test__pnr_graph_builder_sugiyama_vertices(self):
        pnr = self.load_module('spider')

        names_5 = [ block.name for block in pnr.sugiyama_vertices[5] ]
        self.assertEquals( names_5, ['U11', 'U10', 'U13', 'U12'])
        
    def test__pnr_graph_builder_sugiyama_edges(self):
        pnr = self.load_module('spider')
                
        self.assertEquals( pnr.sugiyama_edges[4], [(('U8', 'out2'), ('U11', 'in')),
            (('U8', 'out1'), ('U10', 'in')),
            (('U9', 'out1'), ('U12', 'in')),
            (('U9', 'out2'), ('U13', 'in'))] )
            
            
    def test__pnr_graph_builder_sugiyama_graph(self):
        pnr = self.load_module('gates1')
        
        names = []
        for layer in pnr.G.vertices:
            _names = [ block.name for block in layer ]
            names.append( _names)
            
        self.assertEquals( len(names), 3 )
        self.assertEquals( names[0], 'in4:in1:in2:in3'.split(':') )
        self.assertEquals( names[1], ['U1', 'U2'] )
        self.assertEquals( names[2], ['out1', 'out2'] )

