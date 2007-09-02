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
        """ Biuld the list of objects to display on the screen.

        Add the instance modules and ports."""


        # Get vv.Module object from dictionary
        module = self.p1.module_dict[ self.p1.cur_module_ref ]

        # Determine connectivity
        self.build_connection_dicts( module )
        self.connection_list = self.get_block_connections()
        self.write_graphviz( module )

        # Place the blocks in columns
        inst_col_dict = {}
        for inst in module.inst_dict.values():
            inst_col_dict[ inst.name ] = 0
        inst_col_dict['_oport'] = 0
        inst_col_dict['_iport'] = 0
        
        print r"////oOOo\\\\" * 20
        inst_col_dict = self.columnize( self.module_drive_dict, '_iport', inst_col_dict )


        prev_y_pos = [0] * ( max( inst_col_dict.values() ) + 1 )

        self.p2.drawobj_list = []  # Initialise the list

        # Add module instanciations to the list
        # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        if module.inst_dict.values() :
            for iii,inst in enumerate(module.inst_dict.values()):

                x_pos = ( 150 * inst_col_dict[inst.name] )
                y_pos = prev_y_pos[ inst_col_dict[inst.name] ] + 10         

                drawobj = Drawing_Object( name=inst.module_ref,
                                           parent=self.p2, #hmmm
                                           label=inst.name,
                                           obj_type='module',
                                           position=wx.Point(x_pos, y_pos)
                                        )

                submod = self.p1.module_dict[ inst.module_ref ]
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
                        self.driver_net_dict[net] = [sink_name]    
                 

    def get_block_connections( self ):
        """
        """
 
        self.module_drive_dict = {} # for column placement
        block_to_block_connection_list = []

        for driver in self.driver_net_dict.keys():

            inst_name = driver.split('.')[0]

            nets = self.driver_net_dict[ driver ]
            for net in nets:
                inst_net = net.split('.')[0]

                if  net.startswith('_oport.'): # Add output port connections
                    block_to_block_connection_list.append( driver + '=' + net )

                    # This section builds the module-module driver list                           
                    if inst_name in self.module_drive_dict:
                        self.module_drive_dict[inst_name].append('_oport')
                    else:
                        self.module_drive_dict[inst_name] = ['_oport']                  

                if driver.startswith('_iport.'): # Add input port connections 
                    block_to_block_connection_list.append( driver + '=' + net )

                    # This section builds the module-module driver list                           
                    if '_iport' in self.module_drive_dict:
                        self.module_drive_dict['_iport'].append( inst_net )
                    else:
                        self.module_drive_dict['_iport'] = [ inst_net ]        

                if net in self.driver_net_dict:
                    sink_list = self.driver_net_dict[net]

                    for sink in sink_list:
                        sink_inst_name = sink.split('.')[0]
                        block_to_block_connection_list.append( driver + '=' + sink )

                        # This section builds the module-module driver list                           
                        if inst_name in self.module_drive_dict:
                            self.module_drive_dict[inst_name].append( sink_inst_name)
                        else:
                            self.module_drive_dict[inst_name] = [ sink_inst_name ]        
                
        self.module_drive_dict['_oport'] = [ ] 

        return block_to_block_connection_list   


    def columnize( self, driver_dict, inst, col_dict, load = []):
        """ Find the drivers of the current inst, and set their
        column numbers to one less than the current.

        Look out for loops by doing something magical..."""

        col_num = col_dict[inst] + 1
        load.append(inst)
        

        #  Go through the drivers of this sink and update their
        # column numbers if necessary
        for driver in driver_dict[inst]:

            # Loop dectection...
            if driver in load :
                print "Loop!!: ", driver, ":", load
                continue

            # Only update the column count if needed.  If the load
            # is already to the right of this inst, then leave its
            # col number alone.
            if col_num > col_dict[driver]:
                col_dict[driver] = col_num
                col_dict = self.columnize( driver_dict, driver, col_dict, load )

        load.pop()
        
        for key in col_dict.keys():
            print ("        " * ( col_dict[key] )) + key.center(8) 
        print col_dict
        return col_dict

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
            module_ref = self.p1.module_dict[inst.module_ref]
            output_port_names = module_ref.GetOutputPinNames()

            #  Now check the port/net name dictionary of the instn
            # to see if we can match the net name
            for pin_name in output_port_names :
                if inst.port_dict[pin_name] == net_name :
                    driver = inst.name + "." + pin_name

        return driver
        
