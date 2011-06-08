# Parse a bunch of verilog style numbers
#
# Started 10-JUL-07 by Marty
# $Id: numbers.py,v 1.1 2007-08-15 23:52:41 marty Exp $
#

import pyparsing as pyp

# Section A.8.7
__ebnf__ = '''
number = decimal_number
	| octal_number
	| binary_number
	| hex_number
	| real_number ;

real_number = unsigned_number,  '.',  unsigned_number
	| unsigned_number, [ '.', unsigned_number ],  exp,  [ sign ],  unsigned_number ;
	
exp = 'e' | 'E' ;

decimal_number = unsigned_number  
	| [ size ],  decimal_base,  unsigned_number
	| [ size ],  decimal_base,  x_digit,  { '_' }
	| [ size ],  decimal_base,  z_digit,  { '_' } ;
	
binary_number = [ size ], binary_base, binary_value ;

octal_number = [ size ], octal_base, octal_value ;

hex_number = [ size ], hex_base, hex_value ;

sign = '+' | '-' ;

size = non_zero_unsigned_number;

non_zero_unsigned_number = non_zero_decimal_digit, { '_' | decimal_digit };

unsigned_number = decimal_digit, { '_' | decimal_digit };

binary_value = binary_digit, { '_' | binary_digit };

octal_value = octal_digit,  { '_' | octal_digit };

hex_value = hex_digit, { '_' | hex_digit };

decimal_base = "'", ['s'|'S'], 'd' | "'", ['s'|'S'], 'D';


binary_base = "'", ['s'|'S'], 'b' | "'", ['s'|'S'], 'B';

octal_base = "'", ['s'|'S'], 'o' | "'", ['s'|'S'], 'O';

hex_base = "'", ['s'|'S'], 'h' | "'", ['s'|'S'], 'H';

non_zero_decimal_digit = '1' | '2' | '3' | '4' | '5' | '6' | '7' | '8' | '9';

decimal_digit = '0' | '1' | '2' | '3' | '4' | '5' | '6' | '7' | '8' | '9';

binary_digit = x_digit | z_digit | '0' | '1';

octal_digit = x_digit | z_digit | '0' | '1' | '2' | '3' | '4' | '5' | '6' | '7';

hex_digit = x_digit | z_digit
	| '0' | '1' | '2' | '3' | '4' | '5' | '6' | '7' | '8' | '9'
	| 'a' | 'b' | 'c' | 'd' | 'e' | 'f' | 'A' | 'B' | 'C' | 'D' | 'E' | 'F';
	
x_digit = 'x' | 'X' ;

z_digit = 'z' | 'Z' | '?';

'''


# Literals
EXP = pyp.CaselessLiteral('E')
POINT = pyp.Literal('.')

# Digits
x_digit = pyp.oneOf('x X')
z_digit = pyp.oneOf('z Z ?')

hex_digit =  ( x_digit | z_digit | pyp.oneOf('0 1 2 3 4 5 6 7 8 9 A B C D E F a b c d e f') )
	
octal_digit = ( x_digit | z_digit | pyp.oneOf('0 1 2 3 4 5 6 7') )
binary_digit = ( x_digit | z_digit | pyp.oneOf('0 1') )
decimal_digit = pyp.oneOf('0 1 2 3 4 5 6 7 8 9')
non_zero_decimal_digit = pyp.oneOf('1 2 3 4 5 6 7 8 9')

# Base Identifiers
hex_base = pyp.Combine(pyp.Literal("'") + pyp.Optional(pyp.oneOf('s S')) + pyp.oneOf('h H') )
octal_base = pyp.Combine(pyp.Literal("'") + pyp.Optional(pyp.oneOf('s S')) + pyp.oneOf('o O') )
binary_base = pyp.Combine(pyp.Literal("'") + pyp.Optional(pyp.oneOf('s S')) + pyp.oneOf('b B') )
decimal_base = pyp.Combine(pyp.Literal("'") + pyp.Optional(pyp.oneOf('s S')) + pyp.oneOf('d D') )

# Values
hex_value = pyp.Combine( hex_digit + pyp.ZeroOrMore(hex_digit | pyp.Literal('_') ) )
octal_value = pyp.Combine( octal_digit + pyp.ZeroOrMore(octal_digit | pyp.Literal('_') ) )
binary_value = pyp.Combine( binary_digit + pyp.ZeroOrMore(binary_digit | pyp.Literal('_') ) )
unsigned_number = pyp.Combine( decimal_digit + pyp.ZeroOrMore(decimal_digit | pyp.Literal('_') ) )
non_zero_unsigned_number = pyp.Combine(non_zero_decimal_digit + pyp.ZeroOrMore(decimal_digit | pyp.Literal('_') ) )

size = non_zero_unsigned_number;

#
sign = pyp.oneOf('+ -')

# Numbers
hex_number = pyp.Combine(pyp.Optional(size) + hex_base + hex_value )
octal_number = pyp.Combine( pyp.Optional(size) + octal_base + octal_value )
binary_number = pyp.Combine( pyp.Optional(size) + binary_base + binary_value )
decimal_number = ( unsigned_number | 
                 pyp.Combine( pyp.Optional(size) + decimal_base + unsigned_number ) | 
	             pyp.Combine( pyp.Optional(size) + decimal_base + x_digit ) |#  { '_' }
	             pyp.Combine( pyp.Optional(size) + decimal_base + z_digit)  # { '_' } ;
				 )

# Real Numbers
real_number = ( pyp.Combine(unsigned_number + POINT + unsigned_number ) |
                pyp.Combine(unsigned_number + 
                  pyp.Optional( POINT + unsigned_number ) +
                  EXP + pyp.Optional(sign) +  unsigned_number
                 )
			  )

# Number
number = decimal_number ^ octal_number ^ binary_number ^ hex_number ^ real_number


# I promise to unittest eventually
if __name__ == '__main__':
    number_strings = ( '34', '34.4545454', 
                       "'d34", "'h343ea_a7",
                       "34e-9", "34675",
                       "6'b00_x010?", "34'SH44AA"
                       )
    
    for numstr in number_strings:
        print numstr + ":", number.parseString( numstr )
        
    print "SuperString theory"
    ebnf = pyp.OneOrMore( number )
    superstring = ' '.join( number_strings )
    
    print ebnf.parseString( superstring )
    