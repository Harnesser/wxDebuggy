#!/usr/bin/env python

import wx
import sys
sys.path.insert(0, '../../')
import hypernet

class MainWindow(wx.Frame):
    def __init__(self, parent, title, size=wx.DefaultSize):
        wx.Frame.__init__(self, parent, wx.ID_ANY, title, wx.DefaultPosition, size)
        
        
        self.hyperedges = None
        self.read_hyperedge_data()

        self.timer = wx.Timer(self)
        self.timer.Start(1000)
        
        # event bindings
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_TIMER, self.OnTimer)
                   
    def read_hyperedge_data(self):
        d = {}
        execfile('_hyperedge_data.pye', d)
        self.hyperedges = d['hedges']

    def OnTimer(self, e):
        self.read_hyperedge_data()
        self.Refresh()
        
    def OnPaint(self, e):
        dc = wx.PaintDC(self)
        rainbow = [ wx.RED, wx.BLUE, wx.GREEN]
        for hedge in self.hyperedges:
            self.draw_hyperedge(dc, hedge, rainbow[0])
            del rainbow[0]

    def draw_hyperedge(self, dc, hedge, colour):
        """ """
        # module block
        dc.SetPen(wx.Pen(colour))
        iterlines = hedge.ilines()
        sf = 10
        for (x1,y1),(x2,y2) in iterlines:
            dc.DrawLine(x1*sf,y1*sf,x2*sf,y2*sf)
        
       
def main():
    app = wx.App()
    win = MainWindow(None, "Hyperedge Drawings ", size=(820,300))
    win.Show()
    app.MainLoop()
   
if __name__ == "__main__":
    main()
