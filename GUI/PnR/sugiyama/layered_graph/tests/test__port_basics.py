#! /usr/bin/env python
from .. import port 

class Test_PortBasicOperations():

    def setUp(self):
        self.port = port.Port('marty', 'left')
                
    def test_initialiser(self):
        assert self.port.get_name() == 'marty'
        
    def test_direction_check_output(self):
        assert self.port.is_on_right() == False
        
    def test_direction_check_input(self):
        assert self.port.is_on_left() == True
