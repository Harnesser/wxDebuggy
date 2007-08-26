# Declaration Data Types
#
# $Id: declaration_data_types.py,v 1.1 2007-08-15 23:52:41 marty Exp $
#

import pyparsing as pyp

__full_implementation__ = False

# A.2.2 Declaration data types
__enbf__ = '''

//A.2.2.1 Net and variable types
net_type ::=
supply0 | supply1
| tri | triand | trior | tri0 | tri1
| wire | wand | wor
output_variable_type ::= integer | time
real_type ::=
real_identifier [ = constant_expression ]
| real_identifier dimension { dimension }
variable_type ::=
variable_identifier [ = constant_expression ]
| variable_identifier dimension { dimension }


//A.2.2.2 Strengths
drive_strength ::=
( strength0 , strength1 )
| ( strength1 , strength0 )
| ( strength0 , highz1 )
| ( strength1 , highz0 )
| ( highz0 , strength1 )
| ( highz1 , strength0 )
strength0 ::= supply0 | strong0 | pull0 | weak0
strength1 ::= supply1 | strong1 | pull1 | weak1
charge_strength ::= ( small ) | ( medium ) | ( large )


//A.2.2.3 Delays
delay3 ::= # delay_value | # ( delay_value [ , delay_value [ , delay_value ] ] )
delay2 ::= # delay_value | # ( delay_value [ , delay_value ] )
delay_value ::=
unsigned_number
| parameter_identifier
| specparam_identifier
| mintypmax_expression
'''

net_type = ( pyp.Literal('supply0') | pyp.Literal('supply1') |
             pyp.Literal('tri') | pyp.Literal('triand') |
             pyp.Literal('trior') | pyp.Literal('tri0') | 
             pyp.Literal('tri1') | pyp.Literal('wire') | 
             pyp.Literal('wand') | pyp.Literal('wor')
            ).setName('NetType')

output_variable_type = ( pyp.Literal('integer') | pyp.Literal('time') ).setName('output_variable_type')
