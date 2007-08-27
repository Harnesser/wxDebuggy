import wx
from Hier_Ctrl import *
from Schem_View import *
from Drawing_Object import *

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
# Splitter_Window
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
class Splitter_Window( wx.SplitterWindow ):
    """ a splitter window"""


    def __init__(self, parent) :
        wx.SplitterWindow.__init__( self, parent )

        self.driver_net_dict = {}
        self.connection_list = []
        
        self.filename = None
        self.p1 = Hier_Ctrl( self )
        self.p2 = Schem_View( self )

        self.SplitVertically( self.p1, self.p2, sashPosition = 200 )

        self.Bind(wx.EVT_TREE_SEL_CHANGED, self.onTreeSelChanged )

        self.BuildDrawObjList()
        




    def onTreeSelChanged( self, event ):

        self.BuildDrawObjList( )
        event.Skip()

        
    def BuildDrawObjList( self ):
        """ Biuld the list of objects to display on the screen.

        Add the instance modules and ports."""


        # Get vv..Module object from dictionary
        module = self.p1.module_dict[ self.p1.cur_module_ref ]

        self.p2.drawobj_list = []  # Initialise the list



        # Add module instanciations to the list
        # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        if module.inst_dict.values() :
            for iii,inst in enumerate(module.inst_dict.values()):
                drawobj = Drawing_Object( name=inst.module_ref,
                                           parent=self.p2, #hmmm
                                           label=inst.name,
                                           obj_type='module',
                                           position=wx.Point(200, iii*100 + 10))

                submod = self.p1.module_dict[ inst.module_ref ]
                for port in submod.port_dict.values():
                    if port.direction == 'input':
                        drawobj.lhs_ports.append( port.GetLabelStr() )
                    else:
                        drawobj.rhs_ports.append( port.GetLabelStr() )

                # Add to drawing object list
                self.p2.drawobj_list.append( drawobj )
                
        else:
            # a wee fake thingy for modules with no sub modules
            drawobj = Drawing_Object( name='_Nothing',
                                       parent=self.p2, #hmmm
                                       label='_here',
                                       obj_type='module')
            self.p2.drawobj_list.append( drawobj )


        # Add the port instances
        # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        in_y, out_y = 10, 10
        if module.port_name_list:
            for port in module.port_dict.values():
                drawobj = Drawing_Object( name='port',
                                           parent=self.p2, #hmmm
                                           label=port.GetLabelStr(),
                                           obj_type='port' )

                #print port.direction
                if port.direction == 'input':
                    drawobj.position = wx.Point( 100, 10 + in_y )
                    in_y = in_y + 25
                else:
                    drawobj.position = wx.Point( 500, 10 + out_y )
                    out_y = out_y + 25
                    drawobj.mirror = True

                self.p2.drawobj_list.append( drawobj )

        else:
            print "Woops, modules should have ports, " + \
                  module.name + " doesn't seem to have ones!"

        # My checks
        self.build_connection_dicts( module )
        self.connection_list = self.get_block_connections()

        # Now generate the ratsnest connections.
        self.BuildRatsnest(module)

        # Make a call to redraw the schematic
        self.p2.Refresh()


    def BuildRatsnest( self, module ):
        """Draw the ratsnest connections
        """

        for connection in self.connection_list:

            conn1,conn2 = connection.split('=')
            conn1 = conn1.replace('_iport.','')
            conn1 = conn1.replace('_oport.','')                                             
            conn2 = conn2.replace('_iport.','')
            conn2 = conn2.replace('_oport.','')   

            # Create the flightline
            drawobj = Drawing_Object( name='conn',
                                        parent=self,
                                        label=conn1,
                                        obj_type='conn' )
            
            drawobj.startpt  = conn1
            drawobj.endpt    = conn2
            self.p2.drawobj_list.append( drawobj )
            


    def build_connection_dicts(self, module ):
        """ Create schematic view Connection lists
        """

        self.driver_net_dict = {}
        self.net_sink_dict = {}
       
        # Loop thru instanciations in this module
        for inst in module.inst_dict.values():

            # Get the module definition of the instanciated module
            inst_module = self.p1.module_dict[ inst.module_ref ]
            
            # Get the pin:net connections.    
            for pin,net in inst.port_dict.iteritems():
                conn_str = net + '=' + inst.name + '.' + pin

                # is 'net' actually a schematic port? if so, rename it
                if net in module.port_dict:

                    if module.port_dict[net].direction == 'input':
                        net = '_iport.' + net
                    else:
                        net = '_oport.' + net

                # Add to driver_net_dict if inst.pin is an output...
                if inst_module.GetPinDirection( pin ) == 'output':
                    driver_name = '.'.join( [inst.name, pin] )
                    if driver_name in self.driver_net_dict:
                        self.driver_net_dict[driver_name].append(net)
                    else:
                        self.driver_net_dict[driver_name] = [ net ]

                # ...else add to the net_sink_dict
                else:
                    sink_name = '.'.join( [inst.name, pin] )
                    if net in self.driver_net_dict:
                        self.driver_net_dict[net].append(sink_name)
                    else:
                        self.driver_net_dict[net] = [ sink_name]    
                 

    def get_block_connections( self ):
        """
        """
        block_to_block_connection_list = []
        for driver in self.driver_net_dict.keys():


            nets = self.driver_net_dict[ driver ]
            for net in nets:

                
                if driver.startswith('_iport.'): # Add input port connections 
                    block_to_block_connection_list.append( driver + '=' + net )

                elif net.startswith('_oport.'): # Add output port connections
                    block_to_block_connection_list.append( driver + '=' + net )

                elif net in self.driver_net_dict:
                    sink_list = self.driver_net_dict[net]

                    for sink in sink_list:
                        block_to_block_connection_list.append( driver + '=' + sink )

         
        return block_to_block_connection_list   
            

    def Columnize( self, inst, col_dict, load = []):
        """ Find the drivers of the current inst, and set their
        column numbers to one less than the current.

        Look out for loops by doing something magical..."""

        col_num = col_dict[inst] - 1

        #print "Inst", inst, "col", col_dict[inst]
        load.append(inst)

        #  Go through the drivers of this sink and update their
        # column numbers if necessary
        for ii,driver in enumerate(inst_driver_dict[inst]):

            # Loop dectection...
            if driver in load :
                print "Loop!!: ", driver, ":", load
                continue

            # Only update the column count if needed.  If the driver
            # is already to the left of this inst, then leave its
            # col number alone.
            if col_num < col_dict[driver]:
                col_dict[driver] = col_num
                col_dict = Columnize( driver, col_dict, load )

        load.pop()
        return col_dict


    def FindDriver( self, module, pin_or_net, instanciation = '' ):
        """ Find the driver of the given net or instanciation port name.

        A driver for the given net/inst.port is given in the form "aaa.bbb".
        A driver is defined as an output pin of an instanciation or an
        input port of the current schematic.

        If the input is of the form "xxx", then "xxx" is taken as a net
        name, and a driver found for this net.
        
        If the input is of the form "xxx.yyy" then xxx is taken as an
        instance name, and yyy as the port name.  A driver is found for
        this port.
        """

        driver = None

        # First, find the name of the net connected to inst.pin_or_net
        if instanciation != '' :
            if instanciation not in module.inst_dict.keys():
                print "Cannot find instance ", instanciation, \
                      " in module ", module.name
            else:
                if pin_or_net not in module.inst_dict[ instanciation ].port_dict.keys():
                    print "Cannot find the pin", pin_or_net, \
                          "on the instance", instanciation
                else:
                    net_name = module.inst_dict[ instanciation ].port_dict[pin_or_net]

        else:
            net_name = pin_or_net
            
        # Now find a driver...

        # Check input ports.
        module_input_pins = module.GetInputPinNames()
        if net_name in module_input_pins:
            driver = "_iPort." + net_name
            

        # Now check each of the instanciations
        for inst in module.inst_dict.values():

            # Find the output pins of the instance's reference module
            module_ref = self.p1.module_dict[inst.module_ref]
            output_port_names = module_ref.GetOutputPinNames()

            #  Now check the port/net name dictionary of the instn
            # to see if we can match the net name
            for pin_name in output_port_names :
                if inst.port_dict[pin_name] == net_name :
                    driver = inst.name + "." + pin_name

        return driver
        
