import pickle
import wx
import wx.gizmos as gizmos
from Verilog2001.parse.hdl_parser import hdl_parser
import GUI.artwork.hier_tree_icons as hier_tree_icons

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
# Hier_Ctrl
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -    
class Hier_Ctrl(wx.gizmos.TreeListCtrl):
    """
    Another test comment
    """
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
        self.cur_module_ref = None
        
        #
        # Read in a few verilog models that are hierarchical
        #
        if True:
            rtl_files = [
                         'tests/rtl/trivial/top.v',
                         'tests/rtl/trivial/a.v',
                         'tests/rtl/trivial/b.v',
                         'tests/rtl/trivial_clk_rstb/top_clk_rstb.v',
                         'tests/rtl/trivial_clk_rstb/a_clk_rstb.v',
                         'tests/rtl/trivial_clk_rstb/b_clk_rstb.v',
                         'tests/rtl/spider/four_in_four_out.v',
                         'tests/rtl/spider/one_in_one_out.v',
                         'tests/rtl/spider/spider.v',
                         'tests/rtl/spider/two_in_two_out.v',  
                         'tests/rtl/spider/one_in_two_out.v',
                         'tests/rtl/spider/two_in_one_out.v',
                         'tests/rtl/spider/spider_2.v',
                         'tests/rtl/gates/and2.v',
                         'tests/rtl/gates/inv.v',
                         'tests/rtl/gates/gates1.v',
                         'tests/rtl/gates/gates2.v',
                         'tests/rtl/gates/gates3.v',
                         "tests/rtl/snake/one_in_four_out.v",
                         "tests/rtl/snake/snake_1.v",
                         "tests/rtl/snake/three_in_one_out.v",
                         "tests/rtl/snake/two_in_three_out.v",
                         "tests/rtl/snake/two_in_two_out.v",
                         "tests/rtl/snake/two_in_one_out.v",
                         "tests/rtl/long_traces/long_1.v",
                         "tests/rtl/long_traces/long_2.v",
                         "tests/rtl/long_traces/one_in_three_out.v",
                         "tests/rtl/feedback/feedback_1.v",
                         "tests/rtl/feedback/feedback_2.v",
                         "tests/rtl/feedback/feedback_3.v",
                         "tests/rtl/feedback/three_in_three_out.v",
                         ]
        else:               
            rtl_files = [
                         'tests/rtl/trivial/top.v',
                         'tests/rtl/trivial/a.v',
                         'tests/rtl/trivial/b.v',
                         'tests/rtl/gates/and2.v',
                         'tests/rtl/gates/inv.v',
                         'tests/rtl/gates/gates1.v',
                         'tests/rtl/gates/gates2.v',
                         'tests/rtl/gates/gates3.v',
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
        self.green_id  = image_list.Add( hier_tree_icons.getGreenBitmap() )
        self.red_id    = image_list.Add( hier_tree_icons.getRedBitmap()   )
        self.black_id  = image_list.Add( hier_tree_icons.getBlackBitmap() )
        self.blue_id   = image_list.Add( hier_tree_icons.getBlueBitmap()  )

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
                
                # See if inst.module_ref_name string corresponds to an actual vv.Module
                if inst.module_ref_name in self.module_dict:
                    inst.module_ref = self.module_dict[inst.module_ref_name]
                    # Build the module list ref
                    module_ref_list.append( inst.module_ref )
                else:
                    print "Warning: Undefined Module: %s" % (inst.module_ref_name)


        for module in self.module_dict.values() :
            if module in module_ref_list :
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
        
        print "Initialised Hier_Ctrl"
        
    def get_current_module_ref(self):
        return self.module_dict[self.cur_module_ref]
        

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

        if True:
            print "Current Hierarchy Path:", self.cur_hier_path
            print "Current Module Reference", self.cur_module_ref 
            self._pickle_module_for_tests(self.module_dict[self.cur_module_ref])
            
        
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
            #print self.module_dict.keys()
            #print inst.module_ref.name, inst.name
            self.AddModule( child, inst.module_ref, inst.name )
           

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

        
    def _pickle_module_for_tests(self, module):
        """ Pickle an RTL module data structure for unittesting this module. 
        
        Only executed in full GUI mode.
        """       
        
        filename = module.name + '.dat'
        hPICKLE = open('./tests/module_pickles/' + filename,'wb')
        pickle.dump( module, hPICKLE )
        hPICKLE.close()
        print 'Pickling: "%s"' % filename

