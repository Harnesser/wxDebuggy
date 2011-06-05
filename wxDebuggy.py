#!/usr/bin/env python
"""
  wxDebuggy - An RTL Visualiser.
  
 * Reads in verilog files and displays schematics and hierarchy -DONE
 * A splitter window, left = hier tree, right = autogen schematics -DONE
 * Status bar shows current hierarchy path -DONE
 * Window title shows name of module on view -DONE
 * Schematic to be displayed is determined by tree selection. -DONE
     Alternatively, double-clicking on the bounding box of a schematic's
     child module will bring up the schematics of that module, and
     update the hier tree selection accordingly. -DONE
 * Doubleclicking the Right mouse button will move up the hierarchy -DONE
 * Scrolling the mousewheel will zoom in on the cursor.
"""

import wx
import sys
import GUI

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
# myApp
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
class myApp( wx.App ):
    """Application class."""
    
    def OnInit(self):
        self.frame = GUI.Top_Frame("wxDebuggy 'Rainwater'")
        self.frame.Show()
        self.SetTopWindow(self.frame)
        return True


def main():
    app = myApp()
    #app = myApp(True, "drawing_mockup.log")
    app.MainLoop()

if __name__ == '__main__':
    main()
