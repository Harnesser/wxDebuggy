import wx

import PnR.placement_sugiyama as placement
from Drawing_Object import *

#
# Global Constants
#

# Size of the drawing page, in pixels.
PAGE_WIDTH  = 400
PAGE_HEIGHT = 400

# Global Variables

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
# Schem_View
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
class Schem_View( wx.ScrolledWindow ):
    
    def __init__(self, parent, treeview ):

        self.treeview = treeview # pointer to the treeview
        self.cur_module_ref = None
        
        # Set up the window        
        wx.ScrolledWindow.__init__( self, parent, style=wx.SUNKEN_BORDER )       
        self.SetBackgroundColour(wx.WHITE)
        self.EnableScrolling(True, True)
        self.SetScrollbars(20, 20, PAGE_WIDTH / 20, PAGE_HEIGHT / 20)

        # Event bindings
        self.Bind(wx.EVT_LEFT_DCLICK, self.onDoubleClickEvent)
        self.Bind(wx.EVT_RIGHT_DCLICK, self.onRightDoubleClickEvent)
        self.Bind(wx.EVT_PAINT, self.onPaint)

        # Variables
        self.scaling = 1.0
        self.dclick_module = None
        
        # Drawing objects
        self.drawing_object_dict = {}
        self.glue_points = {}


    def set_treeview( self, treeview ):
        """ A pointer to the treeview hierarchy object.
        
        So we can talk to it, and tell it that we've changed hierarchy.
        """
        self.treeview = treeview
        
        

    def onDoubleClickEvent( self, event ):
        """ See if we've hit a module.  Step into it if we can"""

        # Check for a module doubleclick by checking the bounding boxes
        mousepoint = self._getEventCoordinates( event )
        for obj in self.drawobj_list:
            if obj.objectContainsPoint( mousepoint.x, mousepoint.y ):
                self.dclick_module = obj.label
                
        # Now let the object above deal with changing the tree
        #event.Skip() # This doesn't work as mouse events are not
                      # command events.

        # Try a messy parent method call - works though...
        self.treeview.SelectChildModule( self.dclick_module )
        self.draw_new_schematic()
               

    def onRightDoubleClickEvent( self, event ):
        self.treeview.SelectParentModule()
        #self.Refresh()
        #self.parent.parent.IndicateCurrentDesign()
        
        
    def onPaint( self, event ):
        self.draw_new_schematic()


    def draw_new_schematic(self):
        """ """
        self.build_drawing_object_dict()
        self.place_and_route()
        self.draw_schematic()

        
    def draw_schematic( self ):
        """ Draw the schematic
        """

        # First, get the device context of the window
        dc = wx.PaintDC(self)
        self.PrepareDC(dc)
        self._set_scale(dc)

        # Draw Stuff
        dc.BeginDrawing()
        
        for part in self.drawing_object_dict.values():
            part.Draw(dc,True)
            # build gluepoints list -
            # NOTE! Connections must be drawn last or we'll have no
            # gluepoint list!
            for pin,position in part.glue_points.iteritems():
                self.glue_points[pin] = position
                
        #hypernet_list = self.get_hypernet_list()
        #for hypernet in hypernet_list:
        #    hypernet.Draw(dc,True)
            
        dc.EndDrawing()


    def build_drawing_object_dict( self ):
        """ Build the list of objects to display on the screen.

        Add the instance modules and ports."""


        
        # Get vv.Module object 
        print self.treeview
        module = self.treeview.get_current_module_ref()       
        graph = placement.build_graph( module )          
#        prev_y_pos = [0] * ( max( inst_col_dict.values() ) + 1 )
        
        self.drawing_object_dict = {} 
   
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
                                           parent=self, #hmmm
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
                self.drawing_object_dict[inst.name] = drawobj

                # Next y_position
                #max_y_size = max( len(drawobj.lhs_ports), len(drawobj.rhs_ports) )
                #prev_y_pos[ inst_col_dict[inst.name] ] = y_pos + max_y_size
                
        else:
            # a wee fake thingy for modules with no sub modules
            drawobj = Drawing_Object( name='_Nothing_',
                                       parent=self, #hmmm, for flightlines only! FIXME
                                       label='_here',
                                       obj_type='module')

            self.drawing_object_dict['_Nothing'] = drawobj


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
                                           parent=self, #hmmm
                                           label=port.GetLabelStr(),
                                           obj_type='port' )

                #print port.direction
                drawobj.position = wx.Point( x_pos, y_pos )
                if port.direction == 'output':
                    drawobj.mirror = True

                drawobj._update_sizes()

                # Add to drawing object dict
                self.drawing_object_dict[port.GetLabelStr()] = drawobj

                # Next y_position
                #prev_y_pos[ inst_col_dict[key] ] = y_pos + 1

        else:
            print "Woops, modules should have ports, " + \
                  module.name + " doesn't seem to have ones!"



    def place_and_route(self):
        """A simple (useless) place and route."""
        
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
        for draw_obj in self.drawing_object_dict.values():

            if draw_obj.obj_type is 'module':
                x_pos = ( 150 * draw_obj.position.x )
                y_pos = ( draw_obj.position.y ) * 50
            elif  draw_obj.obj_type is 'port':
                x_pos = 50 + ( 150 * draw_obj.position.x )
                y_pos = ( draw_obj.position.y ) * 50       

            draw_obj.setPosition( wx.Point( x_pos, y_pos ) )
            draw_obj._update_sizes()


        # Wiring
        # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        #self.BuildRatsnest(module)
        #self.add_hypernets()

        # Make a call to redraw the schematic
        #self.p2.Refresh()


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
            #self.drawing_object_dict.append( drawobj )
            
            
    def get_hypernet_list(self):
        """ Add a list of nets to draw...
        Each net has at most one vertical segment to simplify the generation
        of the coords, but the drawing task will handle any number
        """
           
        hypernet_list = []
        
        for start_net,end_net in self.connection_list:
        
            # Get start point
            start_point = self.glue_points[start_net]
            end_point   = self.glue_points[end_net]
            
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
        
        #self.p2.drawobj_list.append( drawobj )
        
        drawobj2 = Drawing_Object( name='hypernet', parent=self, label="n1", obj_type='hypernet')
        drawobj2.hypernet_tree = [ 200, 200, 250, [ 175, 310 ], [250, 310, 220, 350] ]
        #self.p2.drawobj_list.append( drawobj2 )
        
        



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
        

    def _set_scale(self, dc):
        """ Determine what scaling factor of the schematic.
        
        Make sure that the whole schematic fits in the client area.
        """
        
        # First, find the size of the client area
        x_dc, y_dc = dc.GetSize()
        
        # Next, find the extent of the schematic. Go through the
        # list of drawing objects to see what the maximum x and y
        # values are.
        x_min, x_max = 0, 0
        y_min, y_max = 0, 0
        
        for part in self.drawing_object_dict.values():
            x1,x2,y1,y2 = part.getBounds()
            
            if x1 < x_min:
                x_min = x1
            elif x2 > x_max:
                x_max = x2
                
            if y1 < y_min:
                y_min = y1
            elif y2 > y_max:
                y_max = y2
        
        # Determine and set the scaling factor.
        self.scaling = min( (1.0 * y_dc ) / y_max,
                            (1.0 * x_dc ) / x_max )
                            
        #  Keep the schematic x:y scaling ratio constant so we don't get
        # stretched schematics
        dc.SetUserScale(self.scaling, self.scaling)
        
        return
        
          

    def _getEventCoordinates(self, event):
        """ Return the coordinates associated with the given mouse event.

            The coordinates have to be adjusted to allow for the current scroll
            position.
        """
        originX, originY = self.GetViewStart()
        unitX, unitY = self.GetScrollPixelsPerUnit()
        #print self.scaling, (event.GetX() + (originX * unitX )) / self.scaling
        return wx.Point(( event.GetX() + (originX * unitX) ) / self.scaling,
                        ( event.GetY() + (originY * unitY) ) / self.scaling )


    def show_glue_point_dict(self):
        """ A debug thing """

        print "\n\n### Glue Point Dictionary"
        for key in self.glue_points.keys():
            print "  [%s]: %s" % ( key, self.glue_points[key] )
        


