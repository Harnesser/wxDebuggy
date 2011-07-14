#! /usr/bin/env python

import graph_test_base
import port

class PortBasicOperations(graph_test_base.Graph_Test_Base):

    def setUp(self):
        self.port = port.Port('marty', 'left')
                
    def test_initialiser(self):
        self.assertEquals( self.port.get_name(), 'marty')
        
    def test_direction_check_output(self):
        self.assertFalse( self.port.is_on_right() )
        
    def test_direction_check_input(self):
        self.assertTrue( self.port.is_on_left() )
