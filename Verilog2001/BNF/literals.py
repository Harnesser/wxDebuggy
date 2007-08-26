#
# Literals
#
# $Id: literals.py,v 1.1 2007-08-15 23:52:41 marty Exp $

import pyparsing as pyp

DOT = pyp.Literal('.').suppress()
OPENBRA = pyp.Literal('(').suppress()
CLOSEBRA = pyp.Literal(')').suppress()
COMMA = pyp.Literal(',').suppress()
SEMICOLON = pyp.Literal(';').suppress()

# Verilog Keywords
keyword = pyp.oneOf('''
module endmodule 
input output inout
parameter localparam
always fork join begin end
reg wire 
''').setName('Keyword')

    