# Parse a bunch of verilog primaries
#
# Started 26-JUL-07 by Marty
# $Id: primaries.py,v 1.1 2007-08-15 23:52:41 marty Exp $
#

import pyparsing as pyp
import numbers as vn
import identifiers as vi

#A.8.4 Primaries
__enbf__ = '''
'''

primary = vn.number | vi.identifier # Way incomplete
