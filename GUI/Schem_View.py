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
        dc.SetUserScale(self.scaling, self.scaling)


        # Draw Stuff
        dc.BeginDrawing()
        
        for part in self.drawobj_list:
            part.Draw(dc,True)
            # build gluepoints list -
            # NOTE! Connections must be drawn last or we'll have no
            # gluepoint list!
            for pin,position in part.glue_points.iteritems():
                self.glue_points[pin] = position
                

        dc.EndDrawing()



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



