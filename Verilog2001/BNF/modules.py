# Parse a bunch of verilog modules
#
# Started 25-JUL-07 by Marty
# $Id: modules.py,v 1.1 2007-08-15 23:52:41 marty Exp $
#

import pyparsing as pyp

import identifiers as vi
import literals as vl
import declaration_data_types as vddt
import declaration_types as vdt
import declaration_lists as vdl
import module_items as vmitems

__enbf__ = """

// A.1.3 Module and Primitive Source Text
source_text = { description };

description = module_declaration
	| udp_declaration ;
	
module_declaration =
	{ attribute_instance }, module_keyword, module_identifier,
	[ module_parameter_port_list ],
	[ list_of_ports ], ';',
	{ module_item },
	'endmodule' 
	| { attribute_instance }, module_keyword ,module_identifier,
	[ module_parameter_port_list ],
	[ list_of_port_declarations ], ';', 
	{ non_port_module_item },
	'endmodule' ;
	
module_keyword = 'module' | 'macromodule';


//  A.1.4 Module Parameters and Ports
module_parameter_port_list = '#', '(', parameter_declaration, { parameter_declaration }, ')';

list_of_ports = '(' port, { ',', port } ')';

list_of_port_declarations = '(' port_declaration, { ',',port_declaration } ')'
  | '(', ')';
  
port = [ port_expression ]
	| '.', port_identifier, '(', [ port_expression ], ')';
	
port_expression = port_reference
	| { port_reference, { ',', port_reference } };
	
port_reference = port_identifier
	| port_identifier [ constant_expression ]
	| port_identifier [ range_expression ];
	
port_declaration = {attribute_instance} inout_declaration
	| {attribute_instance} input_declaration
	| {attribute_instance} output_declaration ;


// A.1.5 - Incomplete
module_item = module_or_generate_item;
non_port_module_item = non_port_module_item;

"""

# A.1.4 - Incomplete

#port_declaration = ( vdt.inout_declaration ^
#                     vdt.input_declaration ^ 
#                     vdt.output_declaration ).setName('Port_Declaration') # Incomplete

port_declaration = ( vdt.input_declaration ^ vdt.output_declaration ^ vdt.inout_declaration )

                     
list_of_port_declarations = ( ( vl.OPENBRA + port_declaration + 
                                pyp.ZeroOrMore( vl.COMMA + port_declaration ) +
                                vl.CLOSEBRA ).setResultsName('Port_v01')
                            )
                            
       
port_reference = vi.port_identifier.setResultsName('reference')

port_expression = port_reference # Incomplete

port = ( pyp.Optional( port_expression ) 
        | 
         ( vl.DOT + vi.port_identifier + vl.OPENBRA + pyp.Optional( port_expression )  + vl.CLOSEBRA )
       ).setResultsName('Port')


list_of_ports = ( vl.OPENBRA + port + pyp.ZeroOrMore( vl.COMMA + port ) + vl.CLOSEBRA ).setResultsName('Port_List')


# A.1.3 - Incomplete

module_keyword = ( pyp.Literal('module') | pyp.Literal('macromodule') ).suppress()
endmodule = pyp.Literal('endmodule').suppress()

#verilog95_port_list = ( list_of_ports + pyp.Literal(';') + module_item )
#verilog01_port_list = ( list_of_port_declarations + pyp.Literal(';') + non_port_module_item ) 

module_declaration = ( 
                       ( module_keyword + vi.module_identifier + 
                         pyp.Optional( list_of_ports ) +
                         vl.SEMICOLON + 
                         pyp.ZeroOrMore( vmitems.module_item ) +
                         endmodule
                        ).setResultsName('Meeodule')
                      ^
                       ( module_keyword + vi.module_identifier + 
                         pyp.Optional( list_of_port_declarations ) +
                         vl.SEMICOLON + 
                         pyp.ZeroOrMore( vmitems.non_port_module_item ) +
                         endmodule
                       ).setResultsName('Modttule')
                     ).setResultsName('Module')
                     
                       
                     
                      
                      

#
# 
#


if __name__ == '__main__':
    print '\n' * 10
    verilog_snippets_list = (
    
    '''
    module fantastic ( input marty ); endmodule
    ''',
    
    '''module evanescence ( input marty, output jesus ); endmodule''',
    
    '''
    module moddy
    (
      input wire ttt,
      input marty, 
      input seven );
      
    endmodule
    ''',    
    
    '''
    what the fecking feck?
    endmodule
    '''
    )
        
    module_declaration.setDebug()
    
    for verilog in verilog_snippets_list:
        print ('* ')* 30
        print verilog
        print 
        try:
            print  module_declaration.parseString( verilog )
            print "\n * MATCHED * \n"
        except:
            print "\n ** CAN'T MATCH ** \n"
        
 
if __name__ == '__main_old__':
 
    verilog_snippets_list = (
    
    '''
    ( input marty )
    ''',
    
    '''( input marty, output jesus ) ''',
    
    '''
    ( input reg ttt, input marty
    , 
    input seven )
    ''',    
    
   '''
   what the fecking feck?
   '''
    )
        
    list_of_port_declarations.setDebug()
    
    for verilog in verilog_snippets_list:
        print ('* ')* 30
        print verilog
        print 
        try:
            print  list_of_port_declarations.parseString( verilog )
            print "\n * MATCHED * \n"
        except:
            print "\n ** CAN'T MATCH ** \n"
        
    
