# Parse a bunch of verilog style identifiers
#
# Started 13-JUL-07 by Marty
# $Id: identifiers.py,v 1.1 2007-08-15 23:52:41 marty Exp $
#

import pyparsing as pyp
import literals as vl

# A.9.3 Identifiers - Incomplete
__enbf__ = """
arrayed_identifier =
	simple_arrayed_identifier
	| escaped_arrayed_identifier ;
	
block_identifier = identifier ;
cell_identifier = identifier ;
config_identifier = identifier ;

escaped_arrayed_identifier = escaped_identifier, '[',  range,  ']';

escaped_hierarchical_identifier =
	escaped_hierarchical_branch
	{ '.', simple_hierarchical_branch | '.', escaped_hierarchical_branch };
	
escaped_identifier = identifier; (* fix me *)

event_identifier = identifier ;
function_identifier = identifier ;
gate_instance_identifier = arrayed_identifier ;
generate_block_identifier = identifier ;
genvar_function_identifier = identifier ;(* Hierarchy disallowed *)
genvar_identifier = identifier;

hierarchical_block_identifier = hierarchical_identifier ;
hierarchical_event_identifier = hierarchical_identifier ;
hierarchical_function_identifier = hierarchical_identifier ;

hierarchical_identifier =
	simple_hierarchical_identifier
	| escaped_hierarchical_identifier ;
hierarchical_net_identifier = hierarchical_identifier ;
hierarchical_variable_identifier = hierarchical_identifier ;
hierarchical_task_identifier = hierarchical_identifier ;
identifier = simple_identifier | escaped_identifier;

inout_port_identifier = identifier;
input_port_identifier = identifier;
instance_identifier = identifier;
library_identifier = identifier;
memory_identifier = identifier;
module_identifier = identifier;
module_instance_identifier = arrayed_identifier;
net_identifier = identifier;
output_port_identifier = identifier;
parameter_identifier = identifier;
port_identifier = identifier;
real_identifier = identifier;

simple_arrayed_identifier = simple_identifier, '[', range, ']';

simple_hierarchical_identifier = simple_hierarchical_branch, [ '.', escaped_identifier ];

(*
simple_identifier = [ a-zA-Z_ ] { [ a-zA-Z0-9_$ ] }
*)
specparam_identifier = identifier ;

(*
system_function_identifier = $[ a-zA-Z0-9_$ ]{ [ a-zA-Z0-9_$ ] }
system_task_identifier5 = $[ a-zA-Z0-9_$ ]{ [ a-zA-Z0-9_$ ] }
*)

task_identifier = identifier;
terminal_identifier = identifier;
text_macro_identifier = simple_identifier;
topmodule_identifier = identifier;
udp_identifier = identifier;
udp_instance_identifier = arrayed_identifier;
variable_identifier = identifier;

"""

#  pyp.NotAny('reg wire input output inout signed module endmodule')

# Basic Identifiers
simple_identifier =  ( pyp.NotAny( vl.keyword ) +
                       pyp.Word( pyp.alphas, pyp.alphanums +'_' + '$' ).setName('simple_identifier')
                     )

#simple_identifier = pyp.Word( pyp.alphas, pyp.alphanums +'_' + '$' ).setName('simple_identifier')
                        
escaped_identifier = (pyp.Literal('\\') + pyp.OneOrMore( simple_identifier )).setName('escaped_identifier') # whitespace?
identifier = ( simple_identifier ^ escaped_identifier )

#
module_identifier = identifier.setResultsName('Module_Identifier')
port_identifier = identifier.setResultsName('Port_Identifier')

simple_arrayed_identifier = simple_identifier.setName('simple_array_identifier') # Incomplete
escaped_array_identifier = escaped_identifier.setName('escaped_array_identifier') # Incomplete
arrayed_identifier = ( simple_arrayed_identifier | escaped_array_identifier ).setName('arrayed_identifier')

module_instance_identifier = arrayed_identifier


#
# I promise to unittest eventually
#
if __name__ == '__main__':
    id_strings = ( 'marty xcxcxcxc',
                   'Hendrix67 xcxcxcxc',
                   'steven_oneill_03 cxcxcx',
                   '\cdcdcd xcxcxc',
                   'reg'
                 )
    
    for id_str in id_strings:
        print
        print '-*' * 10
        print id_str + ":", identifier.parseString( id_str )
        
    print "SuperString theory"
    ebnf = pyp.OneOrMore( identifier )
    superstring = ' '.join( id_strings )
    
    print ebnf.parseString( superstring )
    
    
