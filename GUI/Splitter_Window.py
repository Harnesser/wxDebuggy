import wx
from Hier_Ctrl import *
from Schem_View import *

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
# Splitter_Window
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
class Splitter_Window( wx.SplitterWindow ):
    """ a splitter window"""

    def __init__(self, parent) :
        wx.SplitterWindow.__init__( self, parent )
        
        #  Bring hier_ctrl up first so that the schematic view should have
        # something to draw
        self.p1 = Hier_Ctrl( self )
        self.p2 = Schem_View( self, self.p1 )

        # give the schematic a pointer to the hierachy 
        self.p2.set_treeview = self.p1
        self.SplitVertically( self.p1, self.p2, sashPosition = 200 )
        self.Bind(wx.EVT_TREE_SEL_CHANGED, self.onTreeSelChanged )
        
    def onTreeSelChanged( self, event ):
        self.p2.draw_new_schematic()
        event.Skip()

        

        
