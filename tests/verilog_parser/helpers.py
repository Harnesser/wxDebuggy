
import sys
import os

def find_base():
    
    path = os.getcwd()
    while path != '/':
        basename = os.path.basename(path)
        if basename == 'wxDebuggy' or basename == 'workspace':
            return path
        else:
            path = os.path.dirname(path)
    return None
    
def set_path():
    rootdir = find_base()
    sys.path.append( rootdir + '/Verilog2001/BNF' )
    
def rtl_dir():
    rootdir = find_base()
    return rootdir + '/tests/rtl'
    
if __name__ == '__main__':
    print find_base()
    print rtl_dir()
