# $Id: Module.py,v 1.3 2007-08-25 03:09:03 marty Exp $
from Object import Object
from Net import Net

class Module( Object ):
    """
    A class to hold the information for a verilog module.
    me? erere sdfgsfdgsdg
    
    """

    def __init__(self, name = '' ):
        Object.__init__( self, name )
        
        # Electrical Stuff
        self.port_dict   = {}
        self.net_dict    = {}
        self.inst_dict   = {}
        self.param_dict  = {}

        self.port_name_list = []

    def getType(self):
        """ Return this DrawingObject's type.
        """
        #return obj_MODULE
        return 6


    def GetPinDirection( self, pin_name, debug=False ):
        port_direction = None
        
        if debug:
            print self.name
            print self.port_dict
            
        port = self.port_dict[ pin_name ]
        return port.direction


    def GetInputPinNames( self ):
        input_pin_names = []
        for pin_name in self.port_name_list:
            pin = self.port_dict[pin_name]
            if pin.direction == 'input':
                input_pin_names.append( pin.name )

        return input_pin_names


    def GetOutputPinNames( self ):
        output_pin_names = []
        for pin_name in self.port_name_list:
            pin = self.port_dict[pin_name]
            if pin.direction == 'output':
                output_pin_names.append( pin.name )

        return output_pin_names
    

    def add_port( self, vv_port_object ):
        """ Add a port to the module 

        Adds the port name to the port name list, and adds the port object to the
        port object dictionary.  Also determines if the type of signal on the port 
        and tags it accordingly.
        """
        
        # Determine signal type on port
        if vv_port_object.name.startswith('clk') :
            vv_port_object.sigtype = 'clock'
        elif vv_port_object.name.startswith('rst') :
            vv_port_object.sigtype = 'reset'
        
        # Make link to this module
        vv_port_object.module_ref = self

        # Add port
        self.port_name_list.append( vv_port_object.name )
        self.port_dict[ vv_port_object.name ] = vv_port_object  

        
    def add_net( self, vv_net_object ):
        """ Add a net to the module

        """

        #

        # Make a link to this module
        vv_net_object.module_ref = self
    
        # Add Net
        self.net_dict[ vv_net_object.name ] = vv_net_object


    def add_implicit_net( self, net_name_str ):
        """ Add an implicit net

        Usually from an instanciation, where the net in question has
        not previously been declared. It will default to a 1-bit net
        """

        if net_name_str not in self.port_name_list:
            net = Net( net_name_str )        
            self.add_net( net )
        

    def add_instanciation( self, vv_instance_object ):
        self.inst_dict[ vv_instance_object.name ] = vv_instance_object

    def count_ins_and_outs( self ):
        num_inputs, num_outputs = 0, 0
        for port in port_dict.values():
            if port.direction == 'input':
                num_inputs = num_inputs + 1
            elif port.direction == 'output':
                num_outputs = num_outputs + 1
                
        return (num_inputs, num_outputs)


    def Display( self ):
        print ''
        print ('Module: ' + self.name ).center(60)
        print '-'*60

        # Inputs
        directions = ['input','output']
        print 'name'.ljust(25), 'direction', 'msb', 'lsb '
        print '-'*60

        for direction in directions:
            for port_name in self.port_name_list:
                port = self.port_dict[port_name]
                if port.direction == direction:
                    print port.name.ljust(25), port.direction.ljust(9), \
                          str(port.msb).ljust(4), str(port.lsb).ljust(4)

        

        # Instances
        for inst in self.inst_dict.values():
            inst.Display()

        # Nets
        for net in self.net_dict.values():
            net.Display()

        return "Don't print me, just call me"


if __name__ == '__main__' :
    print "Module...."
