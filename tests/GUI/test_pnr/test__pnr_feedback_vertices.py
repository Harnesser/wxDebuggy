#!/usr/bin/env python

import pnr_test_base
pnr_test_base.set_paths()

from PnR.pnr import PnR

class PnR_Feedback_Vertices( pnr_test_base.PnR_Test_Base ):

    def test__pnr_drawing_objects_feedback_vertices_1(self):
        module = self.load_rtl_module_pickle('feedback_1') 
        pnr = PnR()
        pnr.place_and_route(module, animate=False)
        names = self.get_block_names(pnr.G)
        
        # main check
        self.assertEquals( len(names), 3 )
        self.assertEquals( names[0], ['in1'] )
        self.assertEquals( names[1], ['_B_U1_out2_U1_in2_2', 'U1'] )
        self.assertEquals( names[2], ['out1'] )
        
    def test__pnr_drawing_objects_feedback_vertices_2(self):
        module = self.load_rtl_module_pickle('feedback_2') 
        pnr = PnR()
        pnr.place_and_route(module, animate=False)
        names = self.get_block_names(pnr.G)
        
        # main check
        self.assertEquals( len(names), 4 )
        self.assertEquals( names[0], ['in1'] )
        self.assertEquals( names[1], ['_B_U2_out2_U1_in2_2', 'U1'] )
        self.assertEquals( names[2], ['_B_U2_out2_U1_in2_3', 'U2'] )
        self.assertEquals( names[3], ['out1'] )
