#!/usr/bin/env python
"""
Class: hdl_parser.py


$Id: hdl_parser.py,v 1.5 2007-08-25 04:15:17 marty Exp $
"""
import sys

# Import wxVV stuff
rootdir = '../../'
sys.path.append( rootdir )
import Verilog2001.BNF as bnf
import vv


class hdl_parser( object ):
    """
    """

    def __init__(self):
        self.cds = {} # Circuit Data Structure - a dictionary of vv.Module objects
        self.current_module = None

        self.set_parse_actions()

    def build_cds_from_file(self, filename ):
        return bnf.module_declaration.parseFile( filename )

    def set_parse_actions(self):

        # Modules
        bnf.module_keyword.setParseAction( self.new_module )
        bnf.module_identifier.setParseAction( self.name_module )
        bnf.endmodule.setParseAction( self.add_module )

        # Ports
        bnf.port_declaration.setParseAction( self.add_port )

        # Instanciations
        bnf.module_instanciation.setParseAction( self.add_instanciation )



    #
    # Parse Actions
    #

    # Modules
    def new_module( self, parse_str, loc, toks ):
        print "New Module:"
        self.current_module = vv.Module()    

    def name_module( self, parse_str, loc, toks ):
        if not self.current_module.name:    # Is this hackky? 
            print "  Naming module: ", toks[0]
            self.current_module.name = toks[0]

    def add_module( self, parse_str, loc, toks ):
        print "  Adding module..."
        self.cds[self.current_module.name] = self.current_module
        print "  CDS:", self.cds

    # Ports
    def add_port( self, parse_str, loc, toks ):
        print "    Found Port named:", toks['Port_Identifier'] 
        port =  vv.Port( toks['Port_Identifier'], toks['Direction'] )
        self.current_module.add_port( port )


    # Instanciations
    def add_instanciation( self, parse_str, loc, toks ):
        print "   Found module instanciation:"
        for key in toks.keys():
            print "     ", key, toks[key]
        inst = vv.Instance( toks['name_of_instance'], toks['Module_Identifier'] )

        for connection in toks['Named_Port_Connection']:
            port,net = connection
            inst.port_dict[port] = net          
            self.current_module.add_implicit_net( net )
            
        self.current_module.add_instanciation( inst )



if __name__ == '__main__':
    my_parse = hdl_parser()

    my_parse.build_cds_from_file('../../tests/rtl/trivial/top.v')
    my_parse.build_cds_from_file('../../tests/rtl/trivial/a.v')

    for mod in my_parse.cds.values():
        print mod
        mod.Display()





    
