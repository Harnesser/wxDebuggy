#
#
#
# $Id: Net.py,v 1.1 2007-08-15 23:53:10 marty Exp $
from Object import Object

class Net( Object ):

    def __init__(self,
                 name ='',
                 nettype = 'wire',
                 msb = 0,
                 lsb = 0
                 ):
        
        Object.__init__( self, name )
        
        self.nettype = nettype
        self.msb = msb
        self.lsb = lsb
        self.size = 0
        self.sigtype = 'normal' # or 'clock' or 'reset' - should be an enumneration
        self.module_ref  = None

        self.Calc_Size()

    def Calc_Size(self):
        self.size = self.msb - self.lsb + 1
      
        
    def Display(self):
        self.Calc_Size()
        print "Net        : ", self.name
        print " MSB       : ", self.msb
        print " LSB       : ", self.lsb
        print " Type      : ", self.nettype
        print " (Size)    : ", self.size
        print ""

    def GetLabelStr(self):
        """ Return the label for the net.  If its a bus,
        include the range."""
        if self.msb :
            return self.name + '[' + str(self.msb) + \
                   ':' + str(self.lsb) + ']'
        else :
            return self.name
        
        
if __name__ == '__main__':

    net = Net('marty','reg', 4)
    net.Display()

    net.name      = 'marty2'
    net.msb       = 8
    net.lsb       = 3
    net.nettype   = 'wire'
    net.Display()

