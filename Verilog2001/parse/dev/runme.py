print "<>" * 40
import sys
import os.path

# Import wxVV stuff
rootdir = '../../../'
sys.path.append( rootdir )
import Verilog2001.BNF as bnf
import vv

port_list = []

def new_port( parse_str, loc, toks ):
    print ('- - ')*10
    print "Found Port named:", toks['Port_Identifier']
    print "       Direction:", toks['Direction']
    print toks
    print ('----')*10
    
    port =  vv.Port( toks['Port_Identifier'], toks['Direction'] )
    port_list.append(port)    
    

def new_named_port_connection( parse_str, loc, toks ):
    print ('- - ')*10
    print "Found Port Connection:"
    print toks
    for key in toks.keys():
        print " ", key, toks[key]
    print ('----')*10

if __name__ == '__main__':
    # Attach parse actions
    bnf.port_declaration.setParseAction( new_port )
    bnf.named_port_connection.setParseAction( new_named_port_connection )

    # Parse an RTL file using my new parser
    res = bnf.module_declaration.parseFile( os.path.join( rootdir, 'tests/rtl/trivial/top.v') )

    print res
    print res.keys()
    print res.Port_v01
    
    for port in port_list:
        print port

