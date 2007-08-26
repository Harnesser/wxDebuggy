# $Id: Module.py,v 1.3 2007-08-25 03:09:03 marty Exp $
from Object import Object

class Module( Object ):
    """
    A class to hold the information for a verilog module.
    me?
    
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


    def GetPinDirection( self, pin_name ):
        port_direction = None
        port = self.port_dict[ pin_name ]
        return port.direction


    def GetInputPinNames( self ):
        input_pin_names = []
        for pin in self.port_dict.values():
            if pin.direction == 'input':
                input_pin_names.append( pin.name )

        return input_pin_names

    def GetOutputPinNames( self ):
        output_pin_names = []
        for pin in self.port_dict.values():
            if pin.direction == 'output':
                output_pin_names.append( pin.name )

        return output_pin_names
    

    def add_port( self, vv_port_object ):
        self.port_name_list.append( vv_port_object.name )
        self.port_dict[ vv_port_object.name ] = vv_port_object  

     
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


        return "Don't print me, just call me"


if __name__ == '__main__' :
    print "Module...."
