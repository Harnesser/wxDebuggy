#! /usr/bin/env python

from graph_builder import Graph_Builder
from sugiyama.graph import Graph
from sugiyama.reordering import Reordering_Engine
from object_factory import Object_Factory
from basic_placer import Placer
from basic_router import Trace_Router

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
        self.reorderer = None
        
        # Graph Info
        self.G = Graph()               # Special graph for sugiyama impl
        self.graph_edges = []          #
        self.layer_dict = {}           # look up which layer an object is in
        self.connection_list = []

        self.sugiyama_edges = []
        self.sugiyama_vertices = []

        # Drawing info
        self.drawing_object_dict = {}
        
        
    def place_and_route(self, module, animate=False ):
        """ Place and Route a Module.
        
        This will return a Python Generator and if set to animate, will
        pause at intermediate steps in the graph layout process so the GUI
        above can draw them.
        """
        
        self.module = module # should I type-check?
        self._build_graph()
        
        # Reorder layers to reduce xovers
        self._build_reorderer()
        self._run_reorderer()

        # Decide on block co-ords
        self.drawing_object_dict = self._build_drawing_object_dict()
        self._place_objects()
                
        # Route nets
        self._route_nets()
        
        # Return drawing objects
        return self.drawing_object_dict
        
        
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
    # Private Methods
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    def _build_graph(self):
        """ Call Graph_Builder on the specified module. """
        self.grapher = Graph_Builder()
        self.grapher.set_module(self.module)
        self.graph_edges     = self.grapher.extract_graph()
        self.layer_dict      = self.grapher.get_layer_dict()
        self.connection_list = self.grapher.get_conn_list()
        
        (V, E) = self.grapher.get_graph_for_sugiyama()
        self.sugiyama_vertices, self.sugiyama_edges = V, E
        self.G = Graph( self.sugiyama_vertices, self.sugiyama_edges )
        self.G.update()
        self.G.build_connection_matrices()
        
    def _build_reorderer(self):
        """ Instantiate a reorderer class if not already done so."""
        if not self.reorderer:
            self.reorderer = Reordering_Engine()
        
    def _run_reorderer(self):
        """ Run the reorderer.
        Take special care to get the correct graph from it at the end."""
        self.reorderer.set_graph(self.G)
        self.reorderer.run()
        self.G = self.reorderer.get_graph()
               
    def _build_drawing_object_dict(self):
        """ Build the dict of objects to draw for the schematic. """
        factory = Object_Factory()
        return factory.build_object_dict(self.module, self.graph_edges)
        
    def _place_objects(self):
        """ Use the Graph() to figure out where to place Drawing_Objects(). 
        This will edit the attributes of the Drawing_Objects in the dict."""
        placer = Placer()
        placer.set_graph(self.G)
        placer.set_object_dict(self.drawing_object_dict)
        placer.run()
        
    def _route_nets(self):
        router = Trace_Router()
        router.set_object_dict(self.drawing_object_dict)
        router.set_connections(self.connection_list)
        router.run()
        
        
