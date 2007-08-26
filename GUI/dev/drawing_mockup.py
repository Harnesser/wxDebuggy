# A Drawing Mockup for vv.Debuggy.
#
#  * Reads in verilog files and displays schematics and hierarchy -DONE
#  * A splitter window, left = hier tree, right = autogen schematics -DONE
#  * Status bar shows current hierarchy path -DONE
#  * Window title shows name of module on view -DONE
#  * Schematic to be displayed is determined by tree selection. -DONE
#     Alternatively, double-clicking on the bounding box of a schematic's
#     child module will bring up the schematics of that module, and
#     update the hier tree selection accordingly. -DONE
#  * Doubleclicking the Right mouse button will move up the hierarchy -DONE
#  * Scrolling the mousewheel will zoom in on the cursor.
#
#
# $Id: drawing_mockup.py,v 1.2 2007-08-25 03:10:07 marty Exp $
#
# Resizing can act a bit funny...
#

import wx
import sys
import wx.gizmos as gizmos

# Import wxvv. stuff
rootdir = '../../'
sys.path.append( rootdir )
import Verilog2001.BNF as bnf
from Verilog2001.parse.hdl_parser import hdl_parser
import vv


import images_marty


#
# Global Constants
#

# Size of the drawing page, in pixels.
PAGE_WIDTH  = 400
PAGE_HEIGHT = 400

# Global Variables


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
# myApp
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
class myApp( wx.App ):
    """Application class."""
    
    def OnInit(self):
        self.frame = myFrame('A Frame, would you believe')
        self.frame.Show()
        self.SetTopWindow(self.frame)
        return True

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
# myFrame
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
class myFrame( wx.Frame ):
    """ My frame class """
    
    def __init__( self, name ):

        wx.Frame.__init__( self, None, -1,
                                     name,
                                     pos = (50,50), size=(800,500),
                                     style = wx.DEFAULT_FRAME_STYLE)

        self.Bind( wx.EVT_TREE_SEL_CHANGED, self.OnNewInstance )
        
        self.sp = mySplitter( self )
        self.CreateStatusBar( number = 1 )
        self.IndicateCurrentDesign()

    def OnNewInstance( self, event ):
        self.IndicateCurrentDesign()
        event.Skip()


    def IndicateCurrentDesign( self ):
        self.SetStatusText( self.sp.p1.cur_hier_path, 0 )
        self.SetTitle( self.sp.p1.cur_module_ref )     


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
# mySplitter
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
class mySplitter( wx.SplitterWindow ):
    """ a splitter window"""


    def __init__(self, parent) :
        wx.SplitterWindow.__init__( self, parent )
        
        self.filename = None
        self.p1 = HierCtrl( self )
        self.p2 = SchemView( self )

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
                drawobj = vvDrawingObject( name=inst.module_ref,
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
            drawobj = vvDrawingObject( name='_Nothing',
                                       parent=self.p2, #hmmm
                                       label='_here',
                                       obj_type='module')
            self.p2.drawobj_list.append( drawobj )


        # Add the port instances
        # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        in_y, out_y = 10, 10
        if module.port_name_list:
            for port in module.port_dict.values():
                drawobj = vvDrawingObject( name='port',
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
                drawobj = vvDrawingObject( name='conn',
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
        
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
# SchemView
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
class SchemView( wx.ScrolledWindow ):
    
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




# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
# HierCtrl
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -    
class HierCtrl(wx.gizmos.TreeListCtrl):
        
    def __init__(self, parent):
    
        #
        # Build and display the hierarchy treecontrol
        #
        gizmos.TreeListCtrl.__init__(self, parent,
                                     style = wx.TR_DEFAULT_STYLE
                                            | wx.TR_FULL_ROW_HIGHLIGHT
                                            | wx.TR_HIDE_ROOT
                                     )

        self.Bind(wx.EVT_TREE_SEL_CHANGED, self.OnSelectModule)

        self.file_to_load   = None
        self.cur_hier_path  = ''
        self.cur_module_ref = ''
        
        #
        # Read in a few verilog models that are hierarchical
        #
        rtl_files = [
                     '../../tests/rtl/trivial/top.v',
                     '../../tests/rtl/trivial/a.v',
                     '../../tests/rtl/trivial/b.v'
                     ]

        myparser = hdl_parser()
        for rtl_file in rtl_files:
            myparser.build_cds_from_file( rtl_file )

        # Get the module dictionary
        self.module_dict = myparser.cds

            
        
        #
        # Image List stuff
        #
        image_size = (16,16)
        image_list = wx.ImageList(image_size[0], image_size[1])
        self.green_id  = image_list.Add( images_marty.getGreenBitmap() )
        self.red_id    = image_list.Add( images_marty.getRedBitmap()   )
        self.black_id  = image_list.Add( images_marty.getBlackBitmap() )
        self.blue_id   = image_list.Add( images_marty.getBlueBitmap()  )

        self.SetImageList(image_list)
        self.image_list = image_list  # what's this for?

        # create some columns
        self.AddColumn("Hierarchy Tree")
        self.AddColumn("Module Name")
        self.SetMainColumn(0) # the one with the tree in it...
        self.SetColumnWidth(0, 175)


        self.root = self.AddRoot("_top")
        self.SetItemText(self.root, "None", 1)
        self.SetItemImage(self.root, self.green_id, which = wx.TreeItemIcon_Normal)
        self.SetItemImage(self.root, self.blue_id, which = wx.TreeItemIcon_Expanded)


        
        #
        # Now build the hierarchy
        #
        if not self.module_dict.values():
            print 'arrrrrgggghhhhh!!'

        #  Build a list of module names referenced in each of the
        # modules.  Any modules in the module list not in the referenced
        # module list are toplevel modules which need to be traversed
        module_ref_list = []
        for module in self.module_dict.values():
            for inst in module.inst_dict.values():
                module_ref_list.append( inst.module_ref )
        

        # 
        for module in self.module_dict.values() :
            if module.name in module_ref_list :
                #  A referenced (instanciated) module, which are not
                # added to the root of the tree
                continue

            self.AddModule( self.root, module, module.name )
            
        
        # Expand the root?    
        self.Expand( self.root )
        

        # Select the first module and display the code for it
        first_module,cookie = self.GetFirstChild( self.root )
        self.SelectItem( first_module )
        self.UpdateHierInfo()
        
        

    def OnSelectModule( self, event ):
        # Find out if we've clicked on module in the hier list.
        #  If so, set file_to_load...
        module_to_load = self.GetItemPyData( event.GetItem() )
        self.file_to_load = '../rtl/' + module_to_load + '.v'
        self.UpdateHierInfo()
        event.Skip()


    def UpdateHierInfo( self ):
        inst_name   = self.GetItemText( self.GetSelection() )
        module_name = self.GetItemPyData( self.GetSelection() )

        self.cur_hier_path  = self.MakeCurHierStr()
        self.cur_module_ref = module_name


        
    # Danger here! A recursive module!
    def AddModule( self, item, module, inst_name ):
        
        child = self.AppendItem( item, inst_name )
        self.SetItemText( child, module.name, 1)
        self.SetItemPyData( child, module.name )

        if not child.IsOk():
            print "Something fishy..."
        
        if module.inst_dict.values():
            # Hierarchical Cell
            self.SetItemImage( child, self.green_id,
                                    which = wx.TreeItemIcon_Normal)
            self.SetItemImage( child, self.blue_id,
                                    which = wx.TreeItemIcon_Expanded)            
        else:
            # Leaf Cell
            self.SetItemImage( child, self.black_id,
                               which = wx.TreeItemIcon_Normal)
            self.SetItemImage( child, self.red_id,
                               which = wx.TreeItemIcon_Selected)

        # look up the name/module dictionary to get the vv.Module object

        for inst in module.inst_dict.values():
            print self.module_dict.keys()
            print inst.module_ref, inst.name
            self.AddModule( child, self.module_dict[inst.module_ref], inst.name )
           

    def SelectChildModule( self, inst_name ):
        # Find the appropriate child.
        parent = self.GetSelection()
        child,cookie = self.GetFirstChild(parent)
        
        while child.IsOk():
            if self.GetItemText(child) == inst_name :
                break
            else:
                child,cookie = self.GetNextChild(parent, cookie)

        if  child.IsOk():
            self.Expand(parent)
            self.SelectItem(child)
            self.UpdateHierInfo()

    def SelectParentModule(self):
        # There's only one child's parent, only one child's parent,
        #  only one child's paarrrrent, there's only one child's parent!
        parent = self.GetItemParent( self.GetSelection() )
        if parent.IsOk():
            self.Collapse(parent)
            self.SelectItem(parent)
            self.UpdateHierInfo()

        
                
    def MakeCurHierStr(self):
        """ Make the hierarchy path string.

        Build the full hierarhical path string by traversing
        the tree backwards from the current selected tree item."""
        item = self.GetSelection()
        hier_pos = self.GetItemText( item )
        
        while item :
            item = self.GetItemParent( item )
            if item.IsOk() :
                hier_pos = self.GetItemText( item ) + '.' + hier_pos
            else :
                item = None

        #print "Hierarchy Position: ", self.cur_hier_pos
        #if type(self.cur_hier_pos) != str:
        #    print "  Hmmmmm, why's this not a string?"

        return hier_pos



# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
# vv.DrawingObject
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -            
class vvDrawingObject:
    
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
        self.startpt = ''
        self.endpt   = ''

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

    def Draw(self, dc, selected=False):

        print "Drawing.. ", self.obj_type
        if self.obj_type == 'module':
            self.Draw_Module( dc, selected)
        elif self.obj_type == 'port':
            self.Draw_Port( dc )
        elif self.obj_type == 'conn':
            print "Start", self.startpt, " End", self.endpt
            self.Draw_FlightLine( dc )
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
            glue_point_key = self.label + '.' + port_name
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
            glue_point_key = self.label + '.' + port_name
            self.glue_points[glue_point_key] = start_point #- self.position



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
        glue_point_key = self.label
        if self.mirror: # output ports
            rj = False
            label_position = label_position + wx.Point( port_width, 0 )
            self.glue_points[glue_point_key] =  port_polygon_points[4] #- self.position
        else: # input ports
            rj = True
            self.glue_points[glue_point_key] =  port_polygon_points[2] #- self.position

        # Draw and label port
        dc.DrawPolygon( port_polygon_points )
        self.drawPinLabel( dc, self.label, label_position, rj )


    def Draw_FlightLine( self, dc, selected=False ):
        """ Draw a connection flightline """

        scaling,same_scaling = dc.GetUserScale()

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
            print "Draw flightline between", start_point, end_point
            dc.DrawLinePoint( start_point, end_point + wx.Point(1,1) )

    
        




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
        

def main():
    app = myApp()
    #app = myApp(True, "drawing_mockup.log")
    app.MainLoop()

if __name__ == '__main__':
    main()
