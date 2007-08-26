"""
    An Instance class...

A vvInstance is the building block of a design.  Designs are stored within
the program as a list of instances,


"""

# $Id: Instance.py,v 1.2 2007-08-25 03:09:32 marty Exp $

from Object import Object

class Instance( Object ):
    
    def __init__(self, name = '', module_ref = '' ):

        Object.__init__( self, name ) 

        # Electrical Stuff
        self.module_ref = module_ref
        self.port_dict  = {}
        self.param_dict = {}

        # Derived Electrical Stuff
        self.num_inputs  = 0
        self.num_outputs = 0


    def Display( self ):
        print '\nInstance "%s" of module "%s" ' % (self.name , self.module_ref)
        for port, net in self.port_dict.iteritems():
            print "  ", port.ljust(20), " - ", net
    
         
      
