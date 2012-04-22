#!/usr/bin/env python

import wx
import random
import sys

sys.path.append('../')
import reordering
import layered_graph 
import layered_graph.tests.helpers as ccts
                
                
class MainWindow(wx.Frame):
    def __init__(self, parent, title, size=wx.DefaultSize):
        wx.Frame.__init__(self, parent, wx.ID_ANY, title, wx.DefaultPosition, size)

        self.circles = list()
        self.displaceX = 30
        self.displaceY = 30

        self.vertices = []
        self.edges = []
        
        self.timer = wx.Timer(self)
        self.timer.Start(1000) # 1000 milliseconds = 1 second

        self.Bind(wx.EVT_TIMER, self.OnTimer)
        self.Bind(wx.EVT_LEFT_UP, self.OnClick)
        self.Bind(wx.EVT_PAINT, self.OnPaint)

        self.layout_iter = None
        self.G1 = None
        self.init_graph()
        
        
    def init_graph(self):
        self.G1 = ccts.orig_sugiyama_cct()
        self.G1.update()
        
        
    def OnPaint(self, e):
        #print "OnPaint called"
        dc = wx.PaintDC(self)
        dc.SetTextForeground(wx.WHITE)
        dc.SetBrush(wx.Brush(wx.BLUE))
        font = wx.Font( pointSize=20, family=wx.MODERN,
            style=wx.NORMAL, weight=wx.BOLD )
        dc.SetFont(font)
        
        # Go through the list of vertices to draw all of them
        for vertex in self.vertices:
            dc.DrawRectangle( vertex[0], vertex[1], 100, 60)
            dc.DrawText( vertex[2], vertex[0]+30, vertex[1]+10 )
            
            
    def OnTimer(self, e):
        #print "OnTimer called"
        self.vertices = []
        
        # Get next graph layout
#        try:
#            layout = self.layout_iter.next()
#        except StopIteration:
#            self.timer.Stop()
#            print "Done"
#            return
            
        for i in range( self.G1.count_layers() ):
            y_pos = 20 + ( i * 100 )
            for j in range( len(self.G1.vertices[i]) ):
                name = self.G1.vertices[i][j].get_name()
                x_pos = 75 + ( j * 150 )
                self.vertices.append( [x_pos, y_pos, name])
                
        self.Refresh()

    def OnClick(self, e):
        """ Advance the layout alg?. """
        self.Refresh()
        
def main():
    app = wx.App()
    win = MainWindow(None, "Animate Sugiyama et al Algorithm ", size=(820,660))
    win.Show()
    app.MainLoop()
   
if __name__ == "__main__":
    random.seed()
    main()
