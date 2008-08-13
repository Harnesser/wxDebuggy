import wx

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
# DrawingObject
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -            
class Drawing_Object:
    
    def __init__(self,
                 parent,
                 name     = 'rrr',
                 label    = 'sss',
                 position = wx.Point(0,0),
                 bbox     = wx.Size(0,0),
                 obj_type = None):

        #
        self.parent    = parent
        self.label     = label
        self.position  = position
        self.bbox      = bbox
        self.mbox      = wx.Size(0,0)
        self.label_pos = wx.Point(0,0)
        self.obj_type  = obj_type
        self.mirror    = False          # If true, flip horizontally
        self.lhs_ports = []
        self.rhs_ports = []
    
        # For nets
        self.startpt = None
        self.endpt   = None

        # For hypernets 
        self.hypernet_tree = []
        
        # Virtual column number
        self.column_number = 0
        
        # Bounding box
        self.pen_colour         = wx.BLACK
        self.fill_colour        = wx.WHITE
        self.line_size          = 1

        # Pin label font
        self.pin_label_size   = 10
        self.pin_label_colour = wx.RED
        self.pin_label_font = wx.SystemSettings_GetFont(wx.SYS_DEFAULT_GUI_FONT).GetFaceName()
        self.pin_separation   = 14
        self.pin_length       = 10

        # Glue Points - this is where the outside world should
        # connect to the drawing object.  It's a dictionary, keys are
        # electrical names, values are a wx.Point of the connection.
        # We probably should have an approach direction too...
        self.glue_points = {}
        
    def Display( self ):
        print "Object:"
        print "  type:", self.type
        print "  name:", self.name
        print " label:", self.label
        print "   pos:", self.position
        print "  bbox:", self.bbox

    def SetPosition( self, position = wx.Point(0,0) ):
        self.position = position

    def SetBoundBox( self, size = wx.Size(0,0) ):
        self.bbox = size

    def objectContainsPoint(self, x, y):
        """ Returns True if this object bounds the given point.

            This is used to determine if the user clicked on the object.
        """
        # Ignore any points outside of the object's bounds.
        if x < self.position.x: return False
        if x > self.position.x + self.bbox.width: return False
        if y < self.position.y: return False
        if y > self.position.y + self.bbox.height: return False
        return True

    def setPosition(self, position = wx.Point(0,0) ):
        """ Set the origin (top-left corner) for this DrawingObject.
        """
        self.position = position

    def getPosition(self):
        """ Return this vv.DrawingObject's position.
        """
        return self.position

    def setSize(self, size):
        """ Set the size for this DrawingObject.
        """
        self.bbox = size
        
    def getSize(self):
        """ Return this vv.DrawingObject's bounding box size.
        """
        self._update_sizes()
        return self.bbox


    def _pointInSelRect(self, x, y, rX, rY):
        """ Return True iff (x, y) is within the selection handle at (rX, ry).
        """
        if   x < rX - 3: return False
        elif x > rX + 3: return False
        elif y < rY - 3: return False
        elif y > rY + 3: return False
        else:            return True

    def objectWithinRect(self, x, y, width, height):
        """ Return True if this object falls completely within the given rect.
        """
        if x          > self.position.x:                    return False
        if x + width  < self.position.x + self.bbox.width:  return False
        if y          > self.position.y:                    return False
        if y + height < self.position.y + self.bbox.height: return False
        return True

    def getBounds(self):
        return ( self.position.x, \
                 self.position.x + self.bbox.width, \
                 self.position.y, \
                 self.position.y + self.bbox.height )


    # PRIVATE METHODS
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    def _calc_instance_height(self):
        """ Calculate the size of the module for drawing.

            Based on the number of pins...
        """
        height = self.pin_separation * ( max( len(self.lhs_ports),
                                              len(self.rhs_ports)) + 1)
        if height < self.pin_separation:
            height = self.pin_separation * 2
        
        return height

    def _calc_instance_width(self):
        """ Calculate the width of the instance box.
        Based on the length of the port names"""
        approx_char_width = 7

        lhs_max = 0
        for port in self.lhs_ports:
            if len(port) > lhs_max :
                lhs_max = len(port)

        rhs_max = 0
        for port in self.rhs_ports:
            if len(port) > rhs_max :
                rhs_max = len(port)

        width = ( lhs_max + rhs_max ) * approx_char_width
        if width < 80:
            width = 80

        return width
    
    def _calc_instance_size( self ):
        return wx.Size( self._calc_instance_width(),
                        self._calc_instance_height() )

    
    def _update_sizes(self):
        self.mbox = self._calc_instance_size()
        self.bbox = self.mbox + wx.Size( (self.pin_length * 2 ), 0 )
        


    # PUBLIC DRAWING METHOD
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 

    def build_glue_points_dict(self):
        """
        """

        self.glue_points = {}
        
        if self.obj_type == 'module':
            for iii, port_name in enumerate(self.lhs_ports):
                ypos_pin = self.position.y + (iii+1)*self.pin_separation

                # Draw the line
                start_point = wx.Point( self.position.x, ypos_pin )

                glue_point_key = (self.label, port_name)
                self.glue_points[glue_point_key] = start_point # - self.position


            xpos_pin = self.position.x + self.bbox.width
            for iii, port_name in enumerate(self.rhs_ports):
                ypos_pin = self.position.y + (iii+1)*self.pin_separation

                # Draw the line
                start_point = wx.Point( xpos_pin, ypos_pin )
           
                glue_point_key = (self.label, port_name)
                self.glue_points[glue_point_key] = start_point #- self.position       


        elif self.obj_type == 'port':

            # Draw the polygon
            port_height = 15
            port_width  = 20
            if self.mirror: # Output Ports
                port_polygon_points = [ wx.Point(port_width/3,0), 
                                        wx.Point(port_width,0),
                                        wx.Point(port_width,port_height),
                                        wx.Point(port_width/3,port_height),
                                        wx.Point(0,port_height/2) ]       # glue point
     
            else: # Input ports
                port_polygon_points = [ wx.Point(0,0), 
                                        wx.Point((2.0/3.0)*port_width,0),
                                        wx.Point(port_width,port_height/2), # glue point
                                        wx.Point((2.0/3.0)*port_width,port_height),
                                        wx.Point(0,port_height) ]
          
                
            # Move the port polygons to the required screen position
            for pin,point in enumerate( port_polygon_points ) :
                port_polygon_points[pin] = point + self.position
            
            
            # See if we need to RJ text, and fill the glue point dictionary
            if self.mirror: # output ports
                glue_point_key = ('_oport', self.label)
                self.glue_points[glue_point_key] =  port_polygon_points[4] #- self.position
            else: # input ports
                glue_point_key = ('_iport', self.label)
                self.glue_points[glue_point_key] =  port_polygon_points[2] #- self.position
      

        elif self.obj_type == 'passthru':

            glue_point_key = ( self.label, '_in' )
            self.glue_points[glue_point_key] =  self.startpt + self.position

            glue_point_key = ( self.label, '_out' )
            self.glue_points[glue_point_key] =  self.endpt + self.position

        



    def Draw(self, dc, selected=False):

        #print "Drawing.. ", self.obj_type
        if self.obj_type == 'module':
            self.Draw_Module( dc, selected)

        elif self.obj_type == 'port':
            self.Draw_Port( dc )

        elif self.obj_type == 'conn':
            #print "Start", self.startpt, " End", self.endpt
            self.Draw_FlightLine( dc )

        elif self.obj_type == 'hypernet':
            start_point = wx.Point( self.hypernet_tree.pop(0), self.hypernet_tree.pop(0) )
            self.draw_hypernet( dc, start_point, self.hypernet_tree, "horizontal" )
            
	        # redo the poping
            self.hypernet_tree.insert(0,start_point.y)
            self.hypernet_tree.insert(0,start_point.x)
        
        elif self.obj_type == 'passthru':
            self._draw_passthru( dc )

        else:
            print "hmmmm...."

        self.MarkGluePoints(dc)

    def Draw_Module( self, dc, selected ):
        """ Draw a module symbol """
        
        # Recalculate, just in case - probaby not necessary
        self._update_sizes()

        scaling,same_scaling = dc.GetUserScale()
        
        # Set the pen
        if self.line_size == 0:
            dc.SetPen(wx.Pen(self.pen_colour, self.line_size, wx.TRANSPARENT))
        else:
            dc.SetPen(wx.Pen(self.pen_colour, \
                             self.line_size / scaling, wx.SOLID))
        dc.SetBrush(wx.Brush(self.fill_colour, wx.SOLID))

        # Draw the module rectangle
        dc.DrawRectanglePointSize( self.position + ( self.pin_length,0) ,
                                   self.mbox )


        # Draw the input pins on the left-hand size of the module box
        for iii, port_name in enumerate(self.lhs_ports):
            ypos_pin = self.position.y + (iii+1)*self.pin_separation

            # Draw the line
            start_point = wx.Point( self.position.x, ypos_pin )
            end_point   = wx.Point( self.position.x + self.pin_length, \
                                    ypos_pin )
            dc.DrawLinePoint( start_point, end_point)
                        
            # Label this pin
            self.drawPinLabel( dc, port_name, end_point )

            # Update the gluepoints dictionary - keep them
            # relatice to the position so we can move the thing around
            # easier
            glue_point_key = (self.label, port_name)
            self.glue_points[glue_point_key] = start_point # - self.position

        # Draw the output lines on the right-hand side of the module box
        xpos_pin = self.position.x + self.bbox.width
        for iii, port_name in enumerate(self.rhs_ports):
            ypos_pin = self.position.y + (iii+1)*self.pin_separation

            # Draw the line
            start_point = wx.Point( xpos_pin, ypos_pin )
            end_point   = wx.Point( xpos_pin - self.pin_length, ypos_pin )
            dc.DrawLinePoint( start_point, end_point )
        
            # Label this output
            self.drawPinLabel( dc, port_name, end_point, True) # RJ

            # Update the gluepoints dictionary - keep them
            # relatice to the position so we can move the thing around
            # easier
            glue_point_key = (self.label, port_name)
            self.glue_points[glue_point_key] = start_point #- self.position

        # draw the instance name of the module
        self.drawInstName( dc, self.label )


    def Draw_Port( self, dc, selected=False ):
        """ Draw a port symbol """

        scaling,same_scaling = dc.GetUserScale()

        # Set the pen
        if self.line_size == 0:
            dc.SetPen(wx.Pen(self.pen_colour, self.line_size, wx.TRANSPARENT))
        else:
            dc.SetPen(wx.Pen(self.pen_colour, \
                             self.line_size / scaling, wx.SOLID))
        dc.SetBrush(wx.Brush(self.fill_colour, wx.SOLID))
        

        # Draw the polygon
        port_height = 15
        port_width  = 20
        if self.mirror: # Output Ports
            port_polygon_points = [ wx.Point(port_width/3,0), 
                                    wx.Point(port_width,0),
                                    wx.Point(port_width,port_height),
                                    wx.Point(port_width/3,port_height),
                                    wx.Point(0,port_height/2) ]       # glue point
 
        else: # Input ports
            port_polygon_points = [ wx.Point(0,0), 
                                    wx.Point((2.0/3.0)*port_width,0),
                                    wx.Point(port_width,port_height/2), # glue point
                                    wx.Point((2.0/3.0)*port_width,port_height),
                                    wx.Point(0,port_height) ]
      
            
        # Move the port polygons to the required screen position
        for pin,point in enumerate( port_polygon_points ) :
            port_polygon_points[pin] = point + self.position

        # See if we need to RJ text, and fill the glue point dictionary
        label_position = self.position + wx.Point( 0, port_height/2)
        if self.mirror: # output ports
            rj = False
            glue_point_key = ('_oport', self.label)
            label_position = label_position + wx.Point( port_width, 0 )
            self.glue_points[glue_point_key] =  port_polygon_points[4] #- self.position
        else: # input ports
            glue_point_key = ('_iport', self.label)
            rj = True
            self.glue_points[glue_point_key] =  port_polygon_points[2] #- self.position

        # Draw and label port
        dc.DrawPolygon( port_polygon_points )
        self.drawPinLabel( dc, self.label, label_position, rj )


    def _draw_passthru( self, dc, selected=False ):
        """ Draw a passthru.
         (a fake module for layering purposes)
        """
        
        # Set the pen - black
        dc.SetPen(wx.Pen('#000000', 1, wx.SOLID))

        dc.DrawLinePoint( self.glue_points[ (self.label, '_in') ] ,
                          self.glue_points[ (self.label, '_out') ] )
        


    def Draw_FlightLine( self, dc, selected=False ):
        """ Draw a connection flightline """

        # Set the pen - green
        dc.SetPen(wx.Pen('#00DD00', 1, wx.SOLID))

        # Decode the start and end points.
        #print self.parent.p2.glue_points.keys()
        if self.startpt in self.parent.p2.glue_points.keys():
            start_point = self.parent.p2.glue_points[self.startpt]
        else:
            print "Warning ", self.startpt, "not a gluepoint"
            start_point = None
            
        if self.endpt in self.parent.p2.glue_points.keys():
            end_point = self.parent.p2.glue_points[self.endpt]
        else:
            print "Warning ", self.endpt, "not a gluepoint"
            end_point   = None

        if start_point and end_point:
            #print "Draw flightline between", start_point, end_point
            dc.DrawLinePoint( start_point, end_point + wx.Point(1,1) )

    
    def draw_hypernet( self, dc, start_point, tree, direction):
        """ Draw orthogonal wires.
        Uses a tree structure as described in [Sander]"""

        # Set the pen - green
        dc.SetPen(wx.Pen('#00DD00', 1, wx.SOLID))
        
        # self.draw_hypernet( dc, start_point, self.hypernet_tree, "vertical" )
        prev_point = start_point
        
        for coord in tree:
            
            if type(coord) is list:
                self.draw_hypernet( dc, prev_point, coord, direction )
            else:
                         
                # determine end point
                if direction == 'vertical':
                    end_point = wx.Point( prev_point.x, coord )
                    direction = 'horizontal'
                else:
                    end_point = wx.Point( coord, prev_point.y )
                    direction = 'vertical'
                    
                # draw line segment
                dc.DrawLinePoint( prev_point, end_point )            
            
                prev_point = end_point
    
    
    
    def drawInstName( self, dc, inst_name ):
        """ Display the instance name """

        font = wx.Font(self.pin_label_size,
                       wx.DEFAULT,     #
                       wx.NORMAL,      # Weight
                       wx.NORMAL,      # Style
                       False,          # Underlined?
                       self.pin_label_font)

        # Set the pin label font specs
        dc.SetTextForeground(wx.BLACK)
        dc.SetTextBackground(wx.WHITE)
        dc.SetFont(font)

        # text extent.
        label_width, label_height = dc.GetTextExtent( inst_name )
    
        # Now centre the instance name within the module's outline block
        xpos = self.position.x + self.bbox.width/2 - label_width/2
        ypos = self.position.y + self.bbox.height/2 - label_height/2

        dc.DrawTextPoint( inst_name, (xpos,ypos) )



    def drawPinLabel( self, dc, pin_label, position, rj = False ):

        font = wx.Font(self.pin_label_size,
                       wx.DEFAULT,     #
                       wx.NORMAL,      # Weight
                       wx.NORMAL,      # Style
                       False,          # Underlined?
                       self.pin_label_font)
        
        # Set the pin label font specs
        dc.SetTextForeground(self.pin_label_colour)
        dc.SetTextBackground(wx.WHITE)
        dc.SetFont(font)

        # text extent.
        label_width, label_height = dc.GetTextExtent( pin_label )
        
        # If we've been instructed to draw the text right-justified,
        # we have to do a little messing.  We'll draw it so that it
        # ends up at 'position', whereas LJ text will begin at
        # 'position'
        if( rj ):
            start_position = wx.Point( position.x - label_width, position.y )
            start_position = start_position + wx.Point( -2, -label_height/2)
        else:
            start_position = position + wx.Point( 2, -label_height/2)

        #print "pos", position
        #print "start", start_position
        
        dc.DrawTextPoint( pin_label, start_position )

            
    def MarkGluePoints( self, dc ):
        """Mark glue points with a tiny blue cross, sort've like in OpenOffice."""

        mark_size = 3
        dc.SetPen(wx.Pen('#0000FF', 1, wx.SOLID))

        for glue_point in self.glue_points.values():
            sp1 = glue_point + wx.Point(  mark_size,  mark_size )
            ep1 = glue_point + wx.Point( -mark_size-1, -mark_size-1 )
            sp2 = glue_point + wx.Point(  mark_size, -mark_size )
            ep2 = glue_point + wx.Point( -mark_size-1,  mark_size+1 )
            
            dc.DrawLinePoint( sp1, ep1 )
            dc.DrawLinePoint( sp2, ep2 )
        

