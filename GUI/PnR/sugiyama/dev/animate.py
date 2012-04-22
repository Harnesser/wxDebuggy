#!/usr/bin/env python

import wx
import random
import sys

sys.path.append('../')
import reordering
import layered_graph 
import layered_graph.tests.helpers as ccts
    
MODULE_WIDTH  = 100
MODULE_HEIGHT = 60
PORT_WIDTH    = 5
PORT_HEIGHT   = 5            
                
class MainWindow(wx.Frame):
    def __init__(self, parent, title, size=wx.DefaultSize):
        wx.Frame.__init__(self, parent, wx.ID_ANY, title, wx.DefaultPosition, size)
        
        self.circles = list()
        self.displaceX = 30
        self.displaceY = 30

        self.vertices = []
        self.edges = []
        
        self.Bind(wx.EVT_LEFT_UP, self.OnClick)
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        
        self.layout_iter = None
        self.G1 = None
        self.layer = 10909090909090
        self.direction = ''
        self.eng = reordering.Reordering_Engine()
        self.port_positions = {}
        self.init_graph()
        
        
    def init_graph(self):
        self.G1 = ccts.orig_sugiyama_single_port_cct()
        self.G1.update()
        self.eng.set_graph(self.G1)
        self.layout_iter = self.eng.gen_run()  # plug in a generator here
        self.update_positions()

        
    def OnPaint(self, e):
        #print "OnPaint called"
        self.port_positions = {}        
        dc = wx.PaintDC(self)

        # Go through the list of vertices to draw all of them
        for vertex in self.vertices:
            x,y,v,c = vertex
            self.draw_vertex(dc, v, x, y, c)

        # draw the connetions
        if not self.port_positions:
            return
            
        for layer in range(self.G1.count_layers()-1):
            for edge in self.G1.edges[layer]:
                x1,y1 = self.port_positions[ (edge.source, edge.source_port) ]
                x2,y2 = self.port_positions[ (edge.target, edge.target_port) ]
                dc.DrawLine(x1,y1,x2,y2)

        self.display_crossovers(dc)
        

    def draw_vertex(self, dc, vertex, x, y, colour):
        """ """
        # module block
        dc.SetBrush(wx.Brush(colour))
        dc.DrawRectangle( x, y, MODULE_WIDTH, MODULE_HEIGHT)
        
        # instance name
        dc.SetTextForeground(wx.WHITE)
        font = wx.Font( pointSize=20, family=wx.MODERN,
            style=wx.NORMAL, weight=wx.BOLD )
        dc.SetFont(font)
        dc.DrawText( vertex.get_name(), x+30, y+10 )
        
        # extended rank
        dc.SetTextForeground(wx.WHITE)
        font = wx.Font( pointSize=10, family=wx.MODERN,
            style=wx.ITALIC, weight=wx.NORMAL )
        dc.SetFont(font)
        dc.DrawText( str(vertex.get_rank()), x+MODULE_WIDTH-20, y+MODULE_HEIGHT-20 )
        
        # ports
        dc.SetBrush(wx.Brush(wx.BLACK))
        dc.SetTextForeground(wx.RED)
        font = wx.Font( pointSize=8, family=wx.MODERN,
            style=wx.NORMAL, weight=wx.NORMAL)
        dc.SetFont(font)
        
        xp, yp = x + 5, y - PORT_HEIGHT
        for port in vertex.get_input_ports():
            dc.DrawRectangle(xp, yp, PORT_WIDTH, PORT_HEIGHT) 
            dc.DrawText( str(port.get_rank()), xp, yp-12 )
            # register port position so we can find it for net drawing
            self.port_positions[ (vertex.get_name(), port.get_name()) ] = (xp+2, yp+2)
            xp += PORT_WIDTH + 5
            
        xp, yp = x + 5, y + MODULE_HEIGHT
        for port in vertex.get_output_ports():
            dc.DrawRectangle(xp, yp, PORT_WIDTH, PORT_HEIGHT) 
            dc.DrawText( str(port.get_rank()), xp, yp+5)
            # register port position so we can find it for net drawing
            self.port_positions[ (vertex.get_name(), port.get_name()) ] = (xp+2, yp+2)
            xp += PORT_WIDTH + 5                                   
        
    def display_crossovers(self,dc):
        dc.SetTextForeground(wx.BLACK)
        font = wx.Font( pointSize=20, family=wx.MODERN,
            style=wx.NORMAL, weight=wx.BOLD )
        dc.SetFont(font)
        dc.DrawText( 'Crossovers: %d' % (self.G1.count_crossovers()) , 50, 600 )
    
        
    def next(self):
        """ Take the next step in the layout algorithm. """
        try:
            (self.layer, self.direction) = self.layout_iter.next()
            print "Animate: layer %d, %s" % (self.layer, self.direction)
        except StopIteration:
            print "Out of stuff..."
            pass
        
            
    def update_positions(self):
        self.vertices = []
        for i in range( self.G1.count_layers() ):
            if i == self.layer:
                colour = wx.RED
            else:
                colour = wx.BLUE
            y_pos = 40 + ( i * (MODULE_HEIGHT * 2.0) )
            for j in range( len(self.G1.vertices[i]) ):
                vertex = self.G1.vertices[i][j]
                x_pos = 75 + ( j * (MODULE_WIDTH * 1.5) )
                self.vertices.append( [x_pos, y_pos, vertex, colour])


    def OnClick(self, e):
        """ Advance the layout alg?. """
        self.next()
        self.update_positions()
        self.Refresh()
        
def main():
    app = wx.App()
    win = MainWindow(None, "Animate Layout Algorithm ", size=(820,660))
    win.Show()
    app.MainLoop()
   
if __name__ == "__main__":
    random.seed()
    main()
