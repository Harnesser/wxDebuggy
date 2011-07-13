class Vertex():
    """ Vertex Class for Port Constrained Layouts.
    
    For the algorithm described in:
    'Port Constraints in Hierarchical Layout of Data Flow Diagrams'
    [SFHM09]
    """
    
    def __init__(self, name, ports=None):
        self.name = name
        if ports is None:
            self.ports = ports
        else:
            self.ports = []
            
        self.rank_width = None
        self.extended_rank
        self.port_ranks
        self.type = 'module' # or 'dummy'
        
                
    def set_rank(extended_rank):
        """ Set the extended rank of this vertex.
        This has to be calculted at a higher level cos it depends on
        the position of this vertex in the graph layer, and on the extended rank
        of vertices to its left.
        """
        self.extended_rank = extended_rank
        
        
    def get_rank():
        """ Return the extended rank of this vertex."""
        return self.extended_rank
   
   
    def get_rank_width():
        """ Return the rank width of the vertex.
        The 'rank width' is simply the total number of ports.
        """
        if self.rank_width is None:
            self.rank_width = len(self.ports)
            assert( self.rank_width >= 1 )
        return self.rank_width
        
        
    def rank_ports():
        """ Determine the rank of each port in this vertex.
        As the ports are fixed, the port ranking need only happen once.
        """
        rank = 0
        inputs  = [ port for port in self.ports if self.port.is_on_left()  ]
        outputs = [ port for port in self.ports if self.port.is_on_right() ]
        
        for port in outputs:
            port.set_rank(rank)
            rank += 1
        for port in inputs:
            port.set_rank(rank)
            rank += 1
        
        assert( rank == (self.rank_width-1) )
        
        
