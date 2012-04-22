from layered_graph.graph import Graph

class Reordering_Engine(object):
    """ Graph Layer-Reordering Engine.

    Implementation of Sugiyama's n-Level Barycentre Method. 
        
    Reorder layers of a graph to reduce edge crossover count. Based on the Sugiyama 
    algorithm, but with modifications to be useful when drawing schematic diagrams.
        
    The input to this algorithm is a layered graph, where the vertices in each 
    layer are ordered, but likely not in an order which minimises the edge 
    crossover count of the graph.
        
    The n-Level BC method is a heuristic algorithm that attempts to reorder the
    vertices within each layer to minimise edge crossovers in the graph. It 
    operates by sweeping down and up the graph, reordering one layer at a time
    - fixing the position of one layer and using a heuristic to reorder the other
    layer to minimize crossings.         
        
    Layers 0 -> n-1 
    Layer i=1 is 'top'          (Python array index [0] )
          i='n-1' the bottom    (Python array index [n-2] )
    """
    
    def __init__(self):
        self.G = None
        self.verbose = True
        self.c_reversions = 0
               
        # Keep track of minimal graph
        self.min_xovers = None
        self.min_graph = None
        
        self._reset()

                
    def set_graph(self, G):
        """ Set the graph to reorder """
        self.G = G    

    def run(self, max_runs=2, debug = False):
        """ Run the layer reordering algorithm. """
        self._reset()
       
        print '\n' 
        print '#' * 80
        print '### here we go'
        print '#' * 80
        gen = self.gen_run()
        for place in gen:
            pass

                        
    def gen_run(self, max_runs=2, debug=False):
        """ Generator for the reordering algorithm."""
        i = 1
        gen = self.gen_phase1(max_runs)
        for place in gen:
            yield place
            i += 1
            
        gen = self.gen_phase1(max_runs)
        for place in gen:
            yield place
            i += 1
        
        
    def gen_phase1(self, max_runs=3):
        if self.G == None:
            print "Ooops - you might want to set a graph first..."

        for i in xrange(0, max_runs):
            gen = self._phase1_down_up()
            for (layer, direction) in gen:
                yield (layer, direction)


    def gen_phase2(self, max_runs=3):
    
        for i in xrange(0, max_runs):
            gen = self._phase2_down_up()
            for (layer, direction) in gen:
                yield (layer, direction)

            
    def get_graph(self):
        """ Return the graph. """
        return self.min_graph
        
    # =================================================================
    #  Phase 1: Barycentre Reordering
    # =================================================================
    def _phase1_down_up(self):
        num_layers = self.G.count_layers()
        for i in xrange(1, num_layers):
            self.G.reorder_layer(i, 'upper')
            yield (i, 'Down')
        self.G.count_crossovers()
        for i in xrange(num_layers-2, -1, -1):
            self.G.reorder_layer(i, 'lower')
            yield (i, 'Up')
        self.G.count_crossovers()
        
    def _phase1_up_down(self):
        num_layers = self.G.count_layers()
        for i in xrange(num_layers-2, -1, -1):
            self.G.reorder_layer(i, 'lower')
            yield (i, 'Up')
        self.G.count_crossovers()
        for i in xrange(1, num_layers):
            self.G.reorder_layer(i, 'upper')
            yield (i, 'Down')
        self.G.count_crossovers()
         

    # =================================================================
    #  Phase 2: Reversion
    # =================================================================
    def _phase2_down_up(self):
        num_layers = self.G.count_layers()
        
        for i in xrange(0, num_layers-1):
            self.G.layer_reversion(i, 'lower')
            gen = self._phase1_down_up()
            for (layer, direction) in gen:
                yield (layer, direction)
               
            
        for i in xrange(num_layers-1, -1, -1):
            self.G.layer_reversion(i, 'upper')
            gen = self._phase1_up_down()
            for (layer, direction) in gen:
                yield (layer, direction)           


    # =================================================================
    #  Bookkeeping helper methods
    # =================================================================
    def _reset(self):
        self.min_xovers = 1e12
        self.min_graph = None
        self.c_reversions = 0
                
    def _keep_if_best_yet(self):
        """ Hold onto this graph if it's the best encountered so far. """
        c_xovers = self.G.get_crossover_count()
        if c_xovers < self.min_xovers:
            self.min_xovers = c_xovers
            self.min_graph = self.G.copy()
                    

