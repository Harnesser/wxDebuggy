# Declaration Types
#
#
# $Id: declaration_types.py,v 1.1 2007-08-15 23:52:41 marty Exp $
#

import pyparsing as pyp
import declaration_data_types as vddt
import declaration_lists as vdl

__full_implementation__ = False

#A.2.1 Declaration types
__ebnf__ = '''
//A.2.1.1 Module parameter declarations
local_parameter_declaration ::=
localparam [ signed ] [ range ] list_of_param_assignments ;
| localparam integer list_of_param_assignments ;
| localparam real list_of_param_assignments ;
| localparam realtime list_of_param_assignments ;
| localparam time list_of_param_assignments ;
parameter_declaration ::=
parameter [ signed ] [ range ] list_of_param_assignments ;
| parameter integer list_of_param_assignments ;
| parameter real list_of_param_assignments ;
| parameter realtime list_of_param_assignments ;
| parameter time list_of_param_assignments ;
specparam_declaration ::= specparam [ range ] list_of_specparam_assignments ;

//A.2.1.2 Port declarations
inout_declaration ::= inout [ net_type ] [ signed ] [ range ]
list_of_port_identifiers
input_declaration ::= input [ net_type ] [ signed ] [ range ]
list_of_port_identifiers
output_declaration ::=
output [ net_type ] [ signed ] [ range ]
list_of_port_identifiers
| output [ reg ] [ signed ] [ range ]
list_of_port_identifiers
| output reg [ signed ] [ range ]
list_of_variable_port_identifiers
| output [ output_variable_type ]
list_of_port_identifiers
| output output_variable_type
list_of_variable_port_identifiers
//A.2.1.3 Type declarations
event_declaration ::= event list_of_event_identifiers ;
genvar_declaration ::= genvar list_of_genvar_identifiers ;
integer_declaration ::= integer list_of_variable_identifiers ;
net_declaration ::=
net_type [ signed ]
[ delay3 ] list_of_net_identifiers ;
| net_type [ drive_strength ] [ signed ]
[ delay3 ] list_of_net_decl_assignments ;
| net_type [ vectored | scalared ] [ signed ]
range [ delay3 ] list_of_net_identifiers ;
| net_type [ drive_strength ] [ vectored | scalared ] [ signed ]
range [ delay3 ] list_of_net_decl_assignments ;
| trireg [ charge_strength ] [ signed ]
[ delay3 ] list_of_net_identifiers ;
| trireg [ drive_strength ] [ signed ]
[ delay3 ] list_of_net_decl_assignments ;
| trireg [ charge_strength ] [ vectored | scalared ] [ signed ]
range [ delay3 ] list_of_net_identifiers ;
| trireg [ drive_strength ] [ vectored | scalared ] [ signed ]
range [ delay3 ] list_of_net_decl_assignments ;
real_declaration ::= real list_of_real_identifiers ;
realtime_declaration ::= realtime list_of_real_identifiers ;
reg_declaration ::= reg [ signed ] [ range ]
list_of_variable_identifiers ;
time_declaration ::= time list_of_variable_identifiers ;
'''

SIGNED = pyp.Literal('signed')
OUTPUT = pyp.Literal('output').setResultsName('Direction')
REG = pyp.Literal('reg')

input_declaration = ( pyp.Literal('input').setResultsName('Direction') + pyp.Optional(vddt.net_type) + 
                      pyp.Optional( SIGNED ) + vdl.list_of_port_identifiers 
                    ).setName('Input_Declaration')  # [range] Incomplete 

inout_declaration = ( pyp.Literal('inout').setResultsName('Direction') + pyp.Optional(vddt.net_type) + 
                      pyp.Optional( SIGNED ) + vdl.list_of_port_identifiers 
                    ).setName('Inout_Declaration')  # [range] Incomplete 
                    
output_declaration =( 
                      ( OUTPUT + pyp.Optional(vddt.net_type) + pyp.Optional( SIGNED ) + vdl.list_of_port_identifiers ) ^
                      ( OUTPUT + pyp.Optional(REG) + pyp.Optional( SIGNED ) + vdl.list_of_port_identifiers ) ^
                      ( OUTPUT + REG + pyp.Optional( SIGNED ) + vdl.list_of_variable_port_identifiers ) ^
                      ( OUTPUT + pyp.Optional( vddt.output_variable_type ) + vdl.list_of_port_identifiers ) ^
                      ( OUTPUT + vddt.output_variable_type + vdl.list_of_variable_port_identifiers ) 
                    ).setName('Output_Declaration')
                    

                    
if __name__ == '__main__':
    verilog_snippets_list = (
    '''
    output reg marty
    ''',
    
    '''
    input marty
    ''',
    
    '''
    output signed wire marty
    ''',    
    
    '''
    what the fecking feck?
    ''',
    
    '''
    marty
    ''',
    
    '''
    marty, is, a, legend
    ''',
    
    '''
    output signed wire marty
    ''',    
    
    '''
    what the fecking feck?
    ''',
    
    '''
    input clk,
    input reset,
    output reg data_out,
    output signed wire data_out2
    '''
    )
    
    decl = ( input_declaration ^ output_declaration ^ inout_declaration )
    
    decl.setDebug()
    
    for verilog in verilog_snippets_list:
        print ('* ')* 30
        print verilog
        
        try:
            print  decl.parseString( verilog )
        except: 
            print "Can't match"
        
        
    

                    
