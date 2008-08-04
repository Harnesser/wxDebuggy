import wx
from Hier_Ctrl import *
from Schem_View import *
from Drawing_Object import *
import PnR.placement_sugiyama as placement

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

        self.BuildDrawObjDict()
        

    def onTreeSelChanged( self, event ):

        self.BuildDrawObjDict()
        event.Skip()

        
    def BuildDrawObjDict( self ):
        """ Build the list of objects to display on the screen.

        Add the instance modules and ports."""


        # Get vv.Module object 
        module = self.p1.module_dict[ self.p1.cur_module_ref ]       
        graph = placement.build_graph( module )

   
#        prev_y_pos = [0] * ( max( inst_col_dict.values() ) + 1 )
        
        drawing_object_dict = {} 
   
        # Add module instanciations to the list
        # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        x_pos = 3
        y_pos = 0
        
        if module.inst_dict.values() :
            for iii,inst in enumerate(module.inst_dict.values()):

                # Unitless positions for the meantime
                #x_pos += 1 #inst_col_dict[inst.name]
                y_pos += 1 #prev_y_pos[ inst_col_dict[inst.name] ] + 1         

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

                
                # Add to drawing object dict
                drawing_object_dict[inst.name] = drawobj

                # Next y_position
                #max_y_size = max( len(drawobj.lhs_ports), len(drawobj.rhs_ports) )
                #prev_y_pos[ inst_col_dict[inst.name] ] = y_pos + max_y_size
                
        else:
            # a wee fake thingy for modules with no sub modules
            drawobj = Drawing_Object( name='_Nothing_',
                                       parent=self.p2, #hmmm
                                       label='_here',
                                       obj_type='module')

            drawing_object_dict['_Nothing'] = drawobj


        # Add the port instances
        # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        x_pos = 1
        y_pos = 0
        
        if module.port_name_list:
            for port in module.port_dict.values():
                
                if port.direction == 'input':
                    key = '_iport'
                else:
                    key = '_oport'

                # Unitless positions for the meantime
                #x_pos += 2 # inst_col_dict[key]
                y_pos += 2 # prev_y_pos[ inst_col_dict[key] ] + 1  
                drawobj = Drawing_Object( name='port',
                                           parent=self.p2, #hmmm
                                           label=port.GetLabelStr(),
                                           obj_type='port' )

                #print port.direction
                drawobj.position = wx.Point( x_pos, y_pos )
                if port.direction == 'output':
                    drawobj.mirror = True

                drawobj._update_sizes()

                # Add to drawing object dict
                drawing_object_dict[port.GetLabelStr()] = drawobj

                # Next y_position
                #prev_y_pos[ inst_col_dict[key] ] = y_pos + 1

        else:
            print "Woops, modules should have ports, " + \
                  module.name + " doesn't seem to have ones!"


        # Sort out the y-positions of the modules in each column
        # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        #placement.find_pin_coords( self.connection_list, drawing_object_dict, inst_col_dict, True )
 #       placement.yplacement(
 #           drawing_object_dict,
 #           self.connection_list,
 #           inst_col_dict
 #           )

        # Re-Scale the drawing positions of the objects to draw
        # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        for draw_obj in drawing_object_dict.values():

            if draw_obj.obj_type is 'module':
                x_pos = ( 150 * draw_obj.position.x )
                y_pos = ( draw_obj.position.y ) * 50
            elif  draw_obj.obj_type is 'port':
                x_pos = 50 + ( 150 * draw_obj.position.x )
                y_pos = ( draw_obj.position.y ) * 50       

            draw_obj.setPosition( wx.Point( x_pos, y_pos ) )
            draw_obj._update_sizes()

        # don't need a dictionary any more...
        self.p2.drawobj_list = drawing_object_dict.values()


        # Wiring
        # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        #self.BuildRatsnest(module)
        #self.add_hypernets()

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
            
            
    def get_hypernet_list(self):
        """ Add a list of nets to draw...
        Each net has at most one vertical segment to simplify the generation
        of the coords, but the drawing task will handle any number
        """
           
        hypernet_list = []
        
        for start_net,end_net in self.connection_list:
        
            # Get start point
            start_point = self.p2.glue_points[start_net]
            end_point   = self.p2.glue_points[end_net]
            
            # Prepare drawing object
            drawobj = Drawing_Object(name='hypernet',
                                     parent=self,
                                     label='hypernet',
                                     obj_type='hypernet')            
                
            drawobj.hypernet_tree = [ start_point.x, start_point.y ]            
            mid_x = ( ( ( end_point.x - start_point.x ) / 2 ) + start_point.x )
            drawobj.hypernet_tree.extend( [ mid_x, end_point.y, end_point.x ] )
        
            hypernet_list.append( drawobj )    
        
        return hypernet_list
        
            
    def add_fake_hypernets(self):
        """ to test the drawing algorithm """
        
        drawobj = Drawing_Object( name='hypernet', parent=self, label="n1", obj_type='hypernet')
        drawobj.hypernet_tree = [ 50,51, 100, 100, 300 ]
        
        self.p2.drawobj_list.append( drawobj )
        
        drawobj2 = Drawing_Object( name='hypernet', parent=self, label="n1", obj_type='hypernet')
        drawobj2.hypernet_tree = [ 200, 200, 250, [ 175, 310 ], [250, 310, 220, 350] ]
        self.p2.drawobj_list.append( drawobj2 )
        
        



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
            source,sink = connection
            write_str = '  %s -> %s;' % ( '.'.join(source), '.'.join(sink) )  
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
        
