#!/usr/bin/env python

import wx
import random

class MainWindow(wx.Frame):
    def __init__(self, parent, title, size=wx.DefaultSize):
        wx.Frame.__init__(self, parent, wx.ID_ANY, title, wx.DefaultPosition, size)

        self.circles = list()
        self.displaceX = 30
        self.displaceY = 30

        self.timer = wx.Timer(self)
        self.timer.Start(1000) # 1000 milliseconds = 1 second

        self.Bind(wx.EVT_TIMER, self.OnTimer)
        self.Bind(wx.EVT_LEFT_UP, self.OnClick)
        self.Bind(wx.EVT_PAINT, self.OnPaint)

    def OnPaint(self, e):
        print "OnPaint called"
        dc = wx.PaintDC(self)
        dc.SetPen(wx.Pen(wx.BLUE))
        dc.SetBrush(wx.Brush(wx.BLUE))

        # Go through the list of circles to draw all of them
        for circle in self.circles:
            dc.DrawCircle(circle[0], circle[1], 10)

    def OnTimer(self, e):
        print "OnTimer called"
        circlePos = (self.displaceX, self.displaceY)
        self.circles.append(circlePos)

        # Change position of the next circle that
        # we want to append to the list next time
        windowSize = self.GetClientSizeTuple()
        maxX = windowSize[0] - 30
        maxY = windowSize[1] - 30
        self.displaceX += 40
        if self.displaceX > maxX:
            self.displaceX = 30
            self.displaceY += 40
            if self.displaceY > maxY:
                self.timer.Stop()        
                print "Timer Stopped"
        self.Refresh()

    def OnClick(self, e):
        print "Window clicked"
        # Do something here to show the click was received.
        # Here we remove a random circle.
        n = len(self.circles)
        if n <= 1: # then dont do it
            return
        i = random.randrange(n)
        del self.circles[i]
        print "Removed %dth circle" % (i,)
        self.Refresh()
        
def main():
    app = wx.App()
    win = MainWindow(None, "Draw delayed circles", size=(620,460))
    win.Show()
    app.MainLoop()
   
if __name__ == "__main__":
    random.seed()
    main()
