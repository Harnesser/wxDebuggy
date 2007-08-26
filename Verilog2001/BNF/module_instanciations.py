# Parse a bunch of verilog module instanciations
#
# Started 26-JUL-07 by Marty
# $Id: module_instanciations.py,v 1.2 2007-08-25 04:16:46 marty Exp $
#

import pyparsing as pyp
import expressions as ve
import identifiers as vi
import literals as vl


#A.4.1 Module instantiation
__enbf__ = """
module_instantiation ::=
module_identifier [ parameter_value_assignment ]
module_instance { , module_instance } ;
parameter_value_assignment ::= # ( list_of_parameter_assignments )
list_of_parameter_assignments ::=
ordered_parameter_assignment { , ordered_parameter_assignment } |
named_parameter_assignment { , named_parameter_assignment }
ordered_parameter_assignment ::= expression
named_parameter_assignment ::= . parameter_identifier ( [ expression ] )
module_instance ::= name_of_instance ( [ list_of_port_connections ] )
name_of_instance ::= module_instance_identifier [ range ]
list_of_port_connections ::=
ordered_port_connection { , ordered_port_connection }
| named_port_connection { , named_port_connection }
ordered_port_connection ::= { attribute_instance } [ expression ]
named_port_connection ::= { attribute_instance } .port_identifier ( [ expression ] )

"""



named_port_connection = ( vl.DOT + vi.port_identifier + 
                          vl.OPENBRA + pyp.ZeroOrMore( ve.expression ) + 
                          vl.CLOSEBRA ).setResultsName('Named_Port_Connection', True)
                          
ordered_port_connection = pyp.ZeroOrMore( ve.expression ).setResultsName('Ordered_Port_Connection')
list_of_port_connections = (
                             (ordered_port_connection + pyp.ZeroOrMore( vl.COMMA + ordered_port_connection ) )
                             ^
                             (named_port_connection + pyp.ZeroOrMore( vl.COMMA + named_port_connection ) )
                           ).setResultsName('List_of_Port_Connections')
                           

name_of_instance = vi.module_instance_identifier.setResultsName('name_of_instance') # [ range ] incomplete

module_instance = name_of_instance + vl.OPENBRA + pyp.Optional(list_of_port_connections)  + vl.CLOSEBRA 
module_instanciation = vi.module_identifier + module_instance + vl.SEMICOLON # Incomplete


#
# Test this bad boy...
#

if __name__ == '__main__':
    
    module_instanciation_list = (
    '''
    emptyness empty ();
    ''',
    
    '''
    jesus christman ( apostles, mary, john, mark, steven );
    ''',
    
    '''
    marty is_great( .r(), .e() );
    ''',
    
    '''
    marty is_great( .r(fre34), .e(jkkljlkj) );
    ''',
 
    )
    module_instanciation.setDebug()
    
    for verilog in module_instanciation_list:
        print ('* ')* 30
        print verilog
        print  module_instanciation.parseString( verilog )
        
        
    
