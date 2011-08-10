class Vertex():
    """ Vertex Class for Port Constrained Layouts.
    
    For the algorithm described in:
    'Port Constraints in Hierarchical Layout of Data Flow Diagrams'
    [SFHM09]
    """
    
    def __init__(self, name):
        self.name = name
        self.port_dict = {}
        self.port_list = []
 
        self.rank_width = None
        self.extended_rank = None
        self.type = 'module' # or 'dummy'
        

    def __str__(self):
        return '"%s" (%s)' % ( self.name, self.type)

    def __repr__(self):
        return self.__str__()
        
    def get_name(self):
        """ Return instance name of this vertex."""
        return self.name
        
        
    def add_port(self, port):
        """ Add the Port() to the port list. 
        port should be an instance of port.Port()
        
        Port order is important.
        """
        port_name = port.get_name()
        self.port_list.append(port_name)
        self.port_dict[port_name] = port
        
                 
    def get_port_names(self):
        """ Return the ordered port list. """
        return self.port_list
        
        
    def set_rank(self, extended_rank):
        """ Set the extended rank of this vertex.
        This has to be calculted at a higher level cos it depends on
        the position of this vertex in the graph layer, and on the extended rank
        of vertices to its left.
        """
        self.extended_rank = extended_rank
        
        
    def get_rank(self):
        """ Return the extended rank of this vertex."""
        return self.extended_rank
   
    def get_port_extended_rank(self, port_name):
        """ Return the extended rank of the named port. """
        port = self.port_dict[port_name]
        return self.get_rank() + port.get_rank()
   
    def get_rank_width(self):
        """ Return the rank width of the vertex.
        The 'rank width' is simply the total number of ports.
        """
        if self.rank_width is None:
            self.rank_width = len(self.port_dict)
            assert( self.rank_width >= 1 )
        return self.rank_width
        
        
    def get_input_ports(self):
        """ Return the sublist of input ports. """
        ports = []
        for port_name in self.port_list:
            _port = self.port_dict[port_name]
            if _port.is_on_left():
                ports.append(_port)
                
        return ports
        

    def get_output_ports(self):
        """ Return the sublist of output ports. """
        ports = []
        for port_name in self.port_list:
            _port = self.port_dict[port_name]
            if _port.is_on_right():
                ports.append(_port)
                
        return ports
        
        
    def get_port(self, port_name):
        """ Return the Port() instantiation for the given port name. """
        return self.port_dict[port_name]
        
        
    def _extract_port_names(self, port_list):
        """ Take the list of Port() objects, and return a list of instn names."""
        return [ _port.get_name() for _port in port_list ]


    def rank_ports(self, debug=True):
        """ Determine the rank of each port in this vertex.
        As the ports are fixed, the port ranking need only happen once.
        """
        rank = 0
        inputs = []
        outputs = []
        
        for port_name in self.port_list:
            port = self.port_dict[port_name]
            if port.is_on_left():
                inputs.append(port)
            else:
                outputs.append(port)

        for port in outputs:
            port.set_rank(rank)
            rank += 1
        for port in inputs:
            port.set_rank(rank)
            rank += 1
        
        if debug:
            for port_name in self.port_list:
                print self.port_dict[port_name]
                
        assert( rank == self.get_rank_width() )

        
