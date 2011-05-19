
class Engine(object):
    """ Sugiyama Graph Layout Engine.
    Modified to work with graphs suitable for circuit drawing.
    
    This expects a layered graph with dummy vertices inserted in long edges.
    OR maybe this should be able to insert long dummy edges? Are the dummy edges
    specific to Sugiyama, or is that something that could be used for a lot of
    layout engine experiments? YAGNI?
    
    The graph will be ordered in-place.
    
    Algorithms are implemented as generators so that they can be stepped through
    easily (for debug and coolness).
    
    """
    
    def __init__(self):
        self.G = None
        self.x_positions = None
        self.animate = False
        
    def set_graph(self, G):
        self.G = G
        
    def run(self):
        self.animate = animate
        self.untangle()
        self.position()
        
    def get_results(self):
        return self.G, self.x_positions
        
    def untangle(self):
        reorder_eng = Layer_Reorder_Engine()
        reorder_eng.set_graph(self.G)
        reorder_eng.run_iter()
        
    def position(self):
        place_eng = Placement_Engine()
        place_eng.set_graph(self.G)
        place_eng.run()
        
    # What about string representation of a graph? All the connectivity matrices?
    # should the algs be generators so I can easily step through each of the stages?
    # probably.
    
    # I've a bit more thinking to do. If I want to animate so I can debug, the at each
    # stage I need to return a layered graph and some x-positions for each object.
    # While I'm reordering, these x-positions need to be the default, so I need to
    # compute the default x-positions up-front. As long as this doesn't make things
    # difficult to test.
        
        
    
    
