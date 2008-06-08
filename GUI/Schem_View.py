import wx

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
    
    def __init__(self, parent ):

        self.parent = parent
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
        
        # Drawing object list
        self.drawobj_list = []
        self.glue_points = {}

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
        self.parent.p1.SelectChildModule( self.dclick_module )
        self.parent.BuildDrawObjList()
        

    def onRightDoubleClickEvent( self, event ):
        self.parent.p1.SelectParentModule()
        self.parent.BuildDrawObjList()
        #self.parent.parent.IndicateCurrentDesign()
        
    def onPaint( self, event ):
        self.DrawSchematic()

        
    def DrawSchematic( self ):
        """ Draw the schematic
        """

        # First, get the device context of the window
        dc = wx.PaintDC(self)
        self.PrepareDC(dc)
        self._set_scale(dc)

        # Draw Stuff
        dc.BeginDrawing()
        
        for part in self.drawobj_list:
            part.Draw(dc,True)
            # build gluepoints list -
            # NOTE! Connections must be drawn last or we'll have no
            # gluepoint list!
            for pin,position in part.glue_points.iteritems():
                self.glue_points[pin] = position
                
        hypernet_list = self.parent.get_hypernet_list()
        for hypernet in hypernet_list:
            hypernet.Draw(dc,True)
            
        dc.EndDrawing()


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
        
        for part in self.drawobj_list:
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
        


