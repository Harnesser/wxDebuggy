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
        
        i = 1
        for place in self.gen_phase1(max_runs):
            if debug: print "<<< Iteration %0d >>>" % (i) + ( '=' * 50 ) 
            if debug: print place
            i += 1

        for place in self.gen_phase2(max_runs):
            if debug: print "<<< Iteration %0d >>>" % (i) + ( '=' * 50 ) 
            i += 1
                        
                    
    def gen_phase1(self, max_runs=3):
        if self.G == None:
            print "Ooops - you might want to set a graph first..."
            
        for i in xrange(0, max_runs):
            self._phase1_down_up()
            yield 'Run %d of %d' % (i+1, max_runs)      


    def gen_phase2(self, max_runs=3):
        for i in xrange(0, max_runs):
            self._phase2_down_up()
            yield 'Run %d of %d' % (i+1, max_runs)      

            
    def get_graph(self):
        """ Return the graph. """
        return self.min_graph
        
    # =================================================================
    #  Phase 1: Barycentre Reordering
    # =================================================================
    def _phase1_down(self):
        for i in xrange(0, self.G.c_levels-1):
            m = Matrix(self.G.vertices[i], self.G.vertices[i+1], self.G.edges[i] )
            m.barycentre_col_reorder()
	    self.G.matrices[i] = m
            self.G.set_layer(i+1, m.col_blocks)
        self._keep_if_best_yet()
        
    def _phase1_up(self):
        for i in xrange(self.G.c_levels-1, 0, -1):
            m = Matrix( self.G.vertices[i-1], self.G.vertices[i], self.G.edges[i-1] )
            m.barycentre_row_reorder()
            self.G.matrices[i-1] = m
            self.G.set_layer(i-1, m.row_blocks)
        self._keep_if_best_yet()
                    
    def _phase1_down_up(self):
        self._phase1_down()
        self._phase1_up()
        
    def _phase1_up_down(self):
        self._phase1_up()
        self._phase1_down()                
        

    # =================================================================
    #  Phase 2: Reversion
    # =================================================================
    def _phase2_down(self):
        for i in xrange(0, self.G.c_levels-1):
            m = self.G.matrices[i]
            if m.col_reversion():
                self.c_reversions += 1
            self.G.matrices[i] = m
            self.G.set_layer(i+1, m.col_blocks)
            self._phase1_down_up()
                        
    def _phase2_up(self):
        for i in xrange(self.G.c_levels-1, 0, -1):
            m = self.G.matrices[i-1]
            if m.row_reversion():
                self.c_reversions += 1
            self.G.matrices[i-1] = m
            self.G.set_layer(i-1, m.row_blocks)
            self._phase1_up_down()

    def _phase2_up_down(self):
        self._phase2_up()
        self._phase2_down()
            
    def _phase2_down_up(self):
        self._phase2_down()
        self._phase2_up()

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
                    

