#!/usr/bin/env python

import wx
import hyperedge

class MainWindow(wx.Frame):
    def __init__(self, parent, title, size=wx.DefaultSize):
        wx.Frame.__init__(self, parent, wx.ID_ANY, title, wx.DefaultPosition, size)
        
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.hyperedges = self.init_hyperedges()
                
    def init_hyperedges(self):
        hedge1 = hyperedge.Hyperedge()
        hedge1.add_connection((10,3), (60,6))
        hedge1.add_connection((10,3), (60,4))
        hedge1.set_track(2)
        
        hedge2 = hyperedge.Hyperedge()
        hedge2.add_connection((10,5), (60,5))
        hedge2.add_connection((10,5), (60,8))
        hedge2.set_track(3)
        
        return [hedge1, hedge2]

        
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
        for (x1,y1),(x2,y2) in hedge.ilines():
            dc.DrawLine(x1*10,y1*10,x2*10,y2*10)
        
       
def main():
    app = wx.App()
    win = MainWindow(None, "Hyperedge Drawings ", size=(820,300))
    win.Show()
    app.MainLoop()
   
if __name__ == "__main__":
    main()
