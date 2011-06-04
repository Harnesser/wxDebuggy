#!/usr/bin/env python

import pnr_test_base
pnr_test_base.set_paths()

from PnR.pnr import PnR

from PnR.Drawing_Object import Drawing_Object

class PnR_Drawing_Object_Checks( pnr_test_base.PnR_Test_Base ):

    def test__pnr_drawing_objects_easy(self):
        module = self.load_rtl_module_pickle('gates1')
        pnr = PnR()
        _dict = pnr.place_and_route(module, animate=False)
        
        expected = ['U1', 'U2', 'in1', 'in2', 'in3', 'in4', 'out1', 'out2']
        objects = _dict.keys()
        objects.sort()
        self.assertEquals( objects, expected )
        
        
    def test__pnr_drawing_objects_type_check(self):
        module = self.load_rtl_module_pickle('gates1')
        pnr = PnR()
        _dict = pnr.place_and_route(module, animate=False)
        
        mod = _dict.keys()[0]
        self.assertTrue( isinstance( _dict[mod] , Drawing_Object ) )
