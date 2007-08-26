# Parse a bunch of verilog declaration lists
# Started 26-JUL-07 by Marty
# $Id: declaration_lists.py,v 1.1 2007-08-15 23:52:41 marty Exp $
#

import pyparsing as pyp
import identifiers as vi
import literals as vl

#A.2.3 Declaration lists

__full_implementation__ = False

__enbf__ = '''
list_of_event_identifiers ::= event_identifier [ dimension { dimension }]
{ , event_identifier [ dimension { dimension }] }
list_of_genvar_identifiers ::= genvar_identifier { , genvar_identifier }
list_of_net_decl_assignments ::= net_decl_assignment { , net_decl_assignment }
list_of_net_identifiers ::= net_identifier [ dimension { dimension }]
{ , net_identifier [ dimension { dimension }] }
list_of_param_assignments ::= param_assignment { , param_assignment }
list_of_port_identifiers ::= port_identifier { , port_identifier }
list_of_real_identifiers ::= real_type { , real_type }
list_of_specparam_assignments ::= specparam_assignment { , specparam_assignment }
list_of_variable_identifiers ::= variable_type { , variable_type }
list_of_variable_port_identifiers ::= port_identifier [ = constant_expression ]
{ , port_identifier [ = constant_expression ] }
'''

list_of_port_identifiers = vi.port_identifier + pyp.ZeroOrMore( vl.COMMA + vi.port_identifier )
list_of_variable_port_identifiers = ( vi.port_identifier + 
                                      pyp.ZeroOrMore( vl.COMMA + vi.port_identifier ) ) # incomplete
                                      

if __name__ == '__main__':
    verilog_snippets_list = (
    '''
    marty
    ''',
    
    '''
    marty, is, a, legend
    '''
    )
        
    list_of_port_identifiers.setDebug()
    
    for verilog in verilog_snippets_list:
        print ('* ')* 30
        print verilog
        print  list_of_port_identifiers.parseString( verilog )
        
        
    
