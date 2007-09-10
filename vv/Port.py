#
#
#
# $Id: Port.py,v 1.1 2007-08-15 23:53:10 marty Exp $
from Net import Net

class Port( Net ):

    def __init__(self,
                 name ='',
                 direction = 'input',
                 nettype = 'wire',
                 msb = 0,
                 lsb = 0):
        
        Net.__init__(self, name, nettype, msb, lsb )
        self.direction = direction
       
    def __repr__(self):
        module_ref_name = "_undefined_"
        if self.module_ref: 
            module_ref_name = module_ref.name

        return "Port '%s' of module %s (%s, %s, %d bits)" % \
          ( self.name,module_ref_name, self.direction, self.nettype, self.size )

    def Display(self):
        self.Calc_Size()
        print "Port       : ", self.name
        print " MSB       : ", self.msb
        print " LSB       : ", self.lsb
        print " Direction : ", self.direction
        print " Type      : ", self.nettype
        print " (Size)    : ", self.size
        
        
if __name__ == '__main__':

    port = Port()
    port.name      = 'marty'
    port.msb       = 14
    port.lsb       = 5
    port.direction = 'input'
    port.nettype   = 'wire'
    port.Display()

    port = Port( 'Hendrix', 'output', 'reg', 4)
    port.Display()

