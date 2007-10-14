import wx
from Hier_Ctrl import *
from Schem_View import *
from Drawing_Object import *
import PnR.placement_mfl as placement

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
# Splitter_Window
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
class Splitter_Window( wx.SplitterWindow ):
    """ a splitter window"""


    def __init__(self, parent) :
        wx.SplitterWindow.__init__( self, parent )

        self.driver_dict = {}
        self.connection_list = []
        self.module_drive_dict = {} # for column placement

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
        """ Build the list of objects to display on the screen.

        Add the instance modules and ports."""


        # Get vv.Module object 
        module = self.p1.module_dict[ self.p1.cur_module_ref ]
        
        # Determine connectivity
        self.driver_dict = self.build_driver_dict(module)
        self.connection_list, self.module_drive_dict = self.get_block_connections(module)


        if True:
            self.show_connection_lists_and_dictionaries()

        #self.write_graphviz( module )

        # Place the blocks in columns
        inst_col_dict = {}
        for inst in module.inst_dict.values():
            inst_col_dict[ inst.name ] = 0
        inst_col_dict['_oport'] = 0
        inst_col_dict['_iport'] = 0
        
        print r"////oOOo\\\\" * 20
        inst_col_dict = placement.columnize( self.module_drive_dict, '_iport', inst_col_dict )


        prev_y_pos = [0] * ( max( inst_col_dict.values() ) + 1 )

        self.p2.drawobj_list = []  # Initialise the list

        # Add module instanciations to the list
        # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        if module.inst_dict.values() :
            for iii,inst in enumerate(module.inst_dict.values()):

                x_pos = ( 150 * inst_col_dict[inst.name] )
                y_pos = prev_y_pos[ inst_col_dict[inst.name] ] + 10         

                drawobj = Drawing_Object( name=inst.module_ref.name,
                                           parent=self.p2, #hmmm
                                           label=inst.name,
                                           obj_type='module',
                                           position=wx.Point(x_pos, y_pos)
                                        )

                submod = inst.module_ref
                for port_name in submod.port_name_list:
                    port = submod.port_dict[ port_name ] # This preserves port ordering
                    if port.direction == 'input':
                        drawobj.lhs_ports.append( port.GetLabelStr() )
                    else:
                        drawobj.rhs_ports.append( port.GetLabelStr() )

                drawobj._update_sizes()
                
                # Add to drawing object list
                self.p2.drawobj_list.append( drawobj )

                # Next y_position
                prev_y_pos[ inst_col_dict[inst.name] ] = y_pos + drawobj.getSize().y
                
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
                
                if port.direction == 'input':
                    key = '_iport'
                else:
                    key = '_oport'

                x_pos = 50 + ( 150 * inst_col_dict[key] )
                y_pos = prev_y_pos[ inst_col_dict[key] ] + 10   
                drawobj = Drawing_Object( name='port',
                                           parent=self.p2, #hmmm
                                           label=port.GetLabelStr(),
                                           obj_type='port' )

                #print port.direction
                drawobj.position = wx.Point( x_pos, y_pos )
                if port.direction == 'output':
                    drawobj.mirror = True

                drawobj._update_sizes()

                self.p2.drawobj_list.append( drawobj )

                # Next y_position
                prev_y_pos[ inst_col_dict[key] ] = y_pos + drawobj.getSize().y

        else:
            print "Woops, modules should have ports, " + \
                  module.name + " doesn't seem to have ones!"

        # Now generate the ratsnest connections.
        self.BuildRatsnest(module)

        # Make a call to redraw the schematic
        self.p2.Refresh()


    def BuildRatsnest( self, module ):
        """Draw the ratsnest connections
        """

        for connection in self.connection_list:

            conn1,conn2 = connection
            #conn1 = conn1.replace('_iport.','')
            #conn1 = conn1.replace('_oport.','')                                             
            #conn2 = conn2.replace('_iport.','')
            #conn2 = conn2.replace('_oport.','')   

            # Create the flightline
            drawobj = Drawing_Object( name='conn',
                                        parent=self,
                                        label=conn1,
                                        obj_type='conn' )
            
            drawobj.startpt  = conn1
            drawobj.endpt    = conn2
            self.p2.drawobj_list.append( drawobj )
            


    def build_driver_dict(self, module, debug = False ):
        """ Build a dictionary of what each net and input port drives.

        Loops thru the instanciations in the current module and adds each
        bit of the .pin(net) list to the drivers dict depending on the 
        direction of the pin.  For example, if pin is an output it drives
        the net, and it's name is the key to the dict.  Otherwise the net 
        drives the pin, so the net name is the key to the dict.        
        """

        driver_dict = {}

        # Loop thru instanciations in this module
        for inst in module.inst_dict.values():

            # Get the module definition of the instanciated module
            inst_module = inst.module_ref

            # Get the pin:net connections.    
            for pin,net in inst.port_dict.iteritems():
            
                # is 'net' actually a schematic port? if so, rename it
                if net in module.port_dict:

                    if module.port_dict[net].direction == 'input':
                        net = ('_iport', net)
                    else:
                        net = ('_oport', net) 

                # if it's a net, give it an instance name of '_net' so everything
                # is a tuple now...
                elif type(net) is not tuple:
                    net = ('_net', net)
    

                # Add to driver_dict if inst.pin is an output...
                if inst_module.GetPinDirection( pin ) == 'output':
                    driver_name = (inst.name, pin) #'.'.join( [inst.name, pin] )
                    driver_dict.setdefault(driver_name, []).append(net)

                # ...
                else:
                    sink_name = (inst.name, pin) #'.'.join( [inst.name, pin] )
                    driver_dict.setdefault(net, []).append(sink_name)


        if debug:
            print "\nDriver Dictionary"
            for key in driver_dict:
                print "  ",key, "::::", driver_dict[key]

        return driver_dict



    def get_block_connections( self, module, debug=False):
        """Determine the connections in the current module

        This uses the driver_dict to build a connections list.  The driver_dict will
        contain ((inst,pin),('_net',net)) or (('_net',net),(inst,pin)) and this module 
        builds a connection list in the form ((inst,pin),(inst,pin))
        (where inst can also be input or output ports ('_iport' or '_oport') ).

        """
 
        module_drive_dict = {} # for column placement
        point_to_point_connection_list = []

        for driver in self.driver_dict.keys():
            driver_inst, driver_name = driver # untuple

            driven_things = self.driver_dict[ driver ]
            for net in driven_things:
                net_inst, net_name = net # untuple

                if  net_inst is '_oport': # Add output port connections
                    point_to_point_connection_list.append( (driver,net) )

                    # This section builds the module-module driver list    
                    module_drive_dict.setdefault(driver_inst, []).append('_oport')           

                if driver_inst is ('_iport'): # Add input port connections 
                    point_to_point_connection_list.append( (driver, net) )

                    # This section builds the module-module driver list        
                    instantiated_module = module.inst_dict[net_inst]
                    sink_port = instantiated_module.module_ref.port_dict[net_name]
                    print "()()() sink_port:", sink_port
                    if sink_port.sigtype == 'normal':
                        module_drive_dict.setdefault('_iport',[]).append(net_inst)      
                    else:   
                        print "%s looks like a reset/clock" % ( net_inst )

    
                if net in self.driver_dict:

                    sink_list = self.driver_dict[net]
                    for sink in sink_list:
                        sink_inst, sink_name = sink # untuple

                        point_to_point_connection_list.append( (driver, sink) )

                        # This section builds the module-module driver list 
                        instantiated_module = module.inst_dict[sink_inst]
                        sink_port = instantiated_module.module_ref.port_dict[sink_name]
                        print "()()() sink_port:", sink_port
                        if sink_port.sigtype == 'normal':
                            module_drive_dict.setdefault(driver_inst,[]).append(sink_inst)      
                        else:   
                            print "%s looks like a reset/clock" % ( sink_port )
                     

        module_drive_dict['_oport'] = [ ] 

        if debug:
            #print "\nPoint-to-Point"
            #for connection in point_to_point_connection_list:
            #    print "   ",connection 
            print "\nModule Driver Dict"
            for key in module_drive_dict:
                print "   ", key, " drives: ", module_drive_dict[key]

        return point_to_point_connection_list, module_drive_dict  


    def show_connection_lists_and_dictionaries(self):
        """ A debug thing """

        print "\n\n### Driver Dictionary"
        for key in self.driver_dict.keys():
            print "  [%s]: %s" % ( key, self.driver_dict[key] )
        
        print "\n\n### Connection Tuple List"
        for conn in self.connection_list:
            print "  ", conn

        print "\n\n### Module Drive Dictionary"
        for key in self.module_drive_dict.keys():
            print "  [%s]: %s" % ( key, self.module_drive_dict[key] )



    def write_graphviz( self, module ):
        """ Write out a graphviz file for the connection list """

        hDOT = open(module.name + ".dot" , 'w' )
        hDOT.write('digraph ' + module.name + ' {')
        hDOT.write('  rankdir = LR;')
        for connection in self.connection_list:
            source,sink = connection.split('=')
            write_str = '  %s -> %s;' % ( source, sink )  
            hDOT.write(write_str.replace('.',':'))
        hDOT.write('}')



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
            module_ref = inst.module_ref
            output_port_names = module_ref.GetOutputPinNames()

            #  Now check the port/net name dictionary of the instn
            # to see if we can match the net name
            for pin_name in output_port_names :
                if inst.port_dict[pin_name] == net_name :
                    driver = inst.name + "." + pin_name

        return driver
        
