import wx
import PnR
import time
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
        self.current_module = None
        
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

        # Layout Engine
        self.layout_engine = PnR.Layout_Engine()
                
        # Drawing objects
        self.drawing_object_dict = {}

        # Timer for algorithm visualisation
        self.gen = None
        self.animate = True
        self.timer = wx.Timer(self)
        self.timer.Start(2000) # 1000 milliseconds = 1 second
        self.Bind(wx.EVT_TIMER, self.OnTimer)

    def set_treeview( self, treeview ):
        """ A pointer to the treeview hierarchy object.
        
        So we can talk to it, and tell it that we've changed hierarchy.
        """
        self.treeview = treeview
               

    def onDoubleClickEvent( self, event ):
        """ See if we've hit a module.  Step into it if we can"""

        # Check for a module doubleclick by checking the bounding boxes
        mousepoint = self._getEventCoordinates( event )
        for obj in self.drawing_object_dict.values():
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
        self.Refresh()
        #self.parent.parent.IndicateCurrentDesign()
        
        
    def onPaint( self, event ):
        self.draw_schematic()


    def draw_new_schematic(self):
        """ """
        self._get_current_module()
        self.gen = self.layout_engine.place_and_route(self.current_module,
                                                      animate = self.animate)
        self.drawing_object_dict = self.gen.next()
        self.draw_schematic()

    def OnTimer(self,event):
        """ """
        if self.animate:
            try:  
                self.drawing_object_dict = self.gen.next()
            except StopIteration:
                pass
                
            self.Refresh()
        
    def draw_schematic( self ):
        """ Draw the schematic
        """

        # First, get the device context of the window
        dc = wx.PaintDC(self)
        self.PrepareDC(dc)
        self._set_scale(dc)

        # Draw Stuff
        dc.BeginDrawing()
        dc.Clear()
                
        for part in self.drawing_object_dict.values():
            part.Draw(dc,True)
            
        dc.EndDrawing()


    def _get_current_module(self, debug=True):
        """ Find out which module we should be drawing."""
        
        self.current_module = self.treeview.get_current_module_ref()  
        
        if debug:
            print "Changed module to ", self.current_module.name


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


