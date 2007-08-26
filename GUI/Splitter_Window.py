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
                    

        # Now generate the ratsnest connections.
        self.BuildRatsnest(module)

        # Make a call to redraw the schematic
        self.p2.Refresh()


        # Check the 'FindDriver' Method
        output_ports = module.GetOutputPinNames()
        for port_name in output_ports:
            driver = self.FindDriver( module, port_name )
            print "***Port:", port_name, "; Driver:", driver

    def BuildRatsnest( self, module ):
        """Build the list of connections.

        Connection list is constructed by first listing the net names
        and instance_name.pin name pairs followed by the port and netname
        pairs. These are kept in strings so that the first list may be
        sorted.

        For example double-ff schematic, see notebook 13-NOV-06.
        eg [ 'A=U1.D', 'CLK=U1.CK', 'n1=U1.Q', 'n1=U2.D',
          'CLK=U2.CK', 'B=U2.Q',
          'A=A', 'B=B', 'CLK=CLK' ] # ports

        This list is then sorted so I can tell which pin is connected
        to what.  Again, see notebook for more details.
        """

        # Build list of pin/net connections
        raw_conn_list = []
        for inst in module.inst_dict.values():
            for pin,net in inst.port_dict.iteritems():
                conn_str = net + '=' + inst.name + '.' + pin
                raw_conn_list.append( conn_str )
                #print conn_str


        # Now add the port names
        for port in module.port_dict.values():
            conn_str = port.name + '=' + port.name
            raw_conn_list.append( conn_str )
            #print conn_str

        #  Now we build the pin/pin connection list.  Do this
        # by sorting the raw list, and taking list item off in pairs
        # of matching netnames.
        raw_conn_list.sort()    # an in-place sort, whatever that means...
        #print "Sorted Connection List", raw_conn_list
        
        max_index = len( raw_conn_list )
        iii = 0
        last_net = ''
        
        while iii < max_index - 1:

            # Split string into net/inst_name.pin pairs
            net1,conn1 = raw_conn_list[iii].split('=')
            net2,conn2 = raw_conn_list[iii+1].split('=')
            #print 'Bits: "' + net1 + '", "'+ conn1 + \
            #      '", "' + net2 + '", "' + conn2 +'"'
            # Check that we've a pairing
            if net1 != net2 :
                #print "Warning - unconnected net.." #not correct...
                #print "  NetName:", net1
                #print "         :", raw_conn_list[iii]
                #print "         :", raw_conn_list[iii+1]
                pass
            else:
                # Create the flightline
                #print net1 + '=' + conn1 + ';' + conn2
                drawobj = Drawing_Object( name='conn',
                                           parent=self,
                                           label=net1,
                                           obj_type='conn' )
                
                drawobj.startpt  = conn1
                drawobj.endpt    = conn2
                self.p2.drawobj_list.append( drawobj )

            last_net = net1
            iii = iii + 1


            
    def PlaceAndRoute(self, module):
        """ Schematic Place and Route.

        The instances are to be placed in virtual columns depending
        on the drivers of each instance.  The output port column is 0
        with the column to the left, -1 etc.

        The column number for each instance is calculated by first
        determining the drivers of each of the instances.  Starting
        from the output ports, this instaciation/driver dictionary
        is traversed, updating the driver instanciation's column number
        at each stage.

        Then each column is given a width dependant on its fattest member.
        """

        # First, find the drivers of each instanciation in the schematic
        for inst in module.inst_dict.values():

            input_port_list = []
            
            inst_module = self.p1.module_dict[ inst.module_ref ]
            for port in inst_module.port_dict.values():
                if port.direction == 'input':
                    input_port_list




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
        
