#! /usr/bin/env python
import graph_builder

class PnR:
    """ Schematic Layout Engine.
    
    This class co-ordinates the generation of a schematic of an RTL module. The
    steps involved in producing a schematic from a Verilog description of a
    module are:
    
     1:  Create a layered graph of the Verilog module. Instantiations are nodes,
        and nets are edges. 
        self.grapher takes care of this.
        
     2:  Reorder the layers of this graph in an effort to reduce the number of
        edge crossovers, which makes for a nicer and easier-to-follow schematic.
        self.reorderer will do this.
        
     3:  Decide on the drawing co-ordinates for the Verilog module instantiations, 
        ports, etc in the schamtic drawing.
        self.placer decide on the co-ords.
     
     4:  Figure out graphics co-ords for the net traces in the drawing.
        self.router will decide the traces are for each net.
        
     5:  Return a list of drawing objects with their positions filled in to the
       Schem_View class.
    """
    
    def __init__(self, use_pickled_module=False):
        self.module = None    # The Module to draw
        
        # Worker classes
        self.grapher = None

        # Graph Info
        self.graph_edges = []          #
        self.layer_dict = {}           # look up which layer an object is in
        self.connection_list = []

        self.sugiyama_edges = []
        self.sugiyama_vertices = []
                
    def place_and_route(self, module, animate=False, debug=False ):
        """ Place and Route a Module.
        
        This will return a Python Generator and if set to animate, will
        pause at intermediate steps in the graph layout process so the GUI
        above can draw them.
        """
        
        self.module = module # should I type-check?
        self._build_graph()
        
        # Reorder layers to reduce xovers
        
        # Decide on block co-ords
        
        # Route nets
        
        # Return drawing objects
        
        
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
    # Private Methods
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    def _build_graph(self):
        """ Call Graph_Builder on the specified module. """
        self.grapher = graph_builder.Graph_Builder()
        
        self.graph_edges     = self.grapher.extract_graph( self.module )
        self.layer_dict      = self.grapher.get_layer_dict()
        self.connection_list = self.grapher.get_conn_list()
        
        self.sugiyama_vertices, self.sugiyama_edges = self.grapher.get_graph_for_sugiyama()
        
        
