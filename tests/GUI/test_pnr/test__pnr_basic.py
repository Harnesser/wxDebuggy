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
        
        names = self.get_block_names(pnr.G)

        self.assertEquals( len(names), 3 )
        self.assertEquals( names[0], 'in4:in1:in2:in3'.split(':') )
        self.assertEquals( names[1], ['U1', 'U2'] )
        self.assertEquals( names[2], ['out1', 'out2'] )


    def test__pnr_reorderer_easy(self):
        module = self.load_rtl_module_pickle('gates1')
        pnr = PnR()
        pnr.place_and_route(module, animate=False)
        names = self.get_block_names(pnr.G)
        
        # main check
        self.assertEquals( pnr.G.get_crossover_count(), 0 )
        self.assertEquals( len(names), 3 )
        self.assertEquals( names[0], 'in1:in2:in3:in4'.split(':') )
        self.assertEquals( names[1], ['U1', 'U2'] )
        self.assertEquals( names[2], ['out1', 'out2'] )
                
        
    def test__pnr_reorderer_snake(self):
        module = self.load_rtl_module_pickle('snake_1')
        pnr = PnR()
        pnr.place_and_route(module, animate=False)
        names = self.get_block_names(pnr.G)
        
        # main check
        self.assertEquals( len(names), 7 )
        self.assertEquals( pnr.G.get_crossover_count(), 3 )
        self.assertEquals( names[0], 'in1'.split(':') )
        self.assertEquals( names[1], ['U1'])        
        self.assertEquals( names[2], ['U2', 'U3'] )
        self.assertEquals( names[3], ['U4', '_U_U2_out1_U7_in2_4', 'U5'] )
        self.assertEquals( names[4], ['U6', 'U7'] )
        self.assertEquals( names[5], ['U8'] )
        self.assertEquals( names[6], ['out1'] )
                
                
