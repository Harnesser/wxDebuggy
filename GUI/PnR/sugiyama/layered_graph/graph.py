import pprint

class Graph():
    """ A Graph Class.
    For Layered, directed, acyclic graphs.
    Add vertices, then the edges.
    """
    
    def __init__(self, name):
        self.vertices = {} # keyed by layer
        self.edges = {}    # keyed by layer

        self.vertex_dict = {}
        self.down_conn_dicts = []
        self.up_conn_dicts = []    

    def add_vertex(self, i_layer, vertex):
	""" Should this be add_module? """
        self.vertices.setdefault(i_layer, []).append(vertex)
        self.vertex_dict[vertex.name] = vertex

    def add_edge(self, edge):
        """ Should this be add_connection?
        Should I figure out which layers this is between?
        """
        i_layer = 0
        self.edges.setdefault(i_layer, []).append(edge)

    def update(self):
        """ Build a few connection dictionaries.
        You should probably call this task after you've built the graph of
        your circuit.
        """
        
        assert len(self.vertices) - 1 == len(self.edges)
        
        # Downward connectivity dictionaries
        self.down_conn_dicts = []
        print self.edges
        for i_layer in self.edges:
            print self.edges[i_layer]
            conn_dict = {}
            for edge in self.edges[i_layer]:
                conn = (edge.target, edge.target_port)
                conn_dict.setdefault(edge.source, []).append(conn)
            self.down_conn_dicts.append(conn_dict)
            
        # Upward connectivity dictionaries
        self.up_conn_dicts = [ [] ]
        for i_layer in self.edges:
            conn_dict = {}
            for edge in self.edges[i_layer]:
                conn = (edge.source, edge.source_port)
                conn_dict.setdefault(edge.target, []).append(conn)
            self.up_conn_dicts.append(conn_dict)
            
        # Set port ranks for each vertex
        for i_layer in self.vertices:
            for vertex in self.vertices[i_layer]:
                #print vertex
                vertex.rank_ports(debug=False)
                
        # Set extended vertex ranks
        for i in range(len(self.vertices)):
            self.rank_vertices(i)
    
        
    def rank_vertices(self, i):
        """ Update the ranks of each vertex in layer i. """
        rank = 0
        for vertex in self.vertices[i]:
            vertex.set_rank(rank)
            rank += vertex.get_rank_width()
            
            
    def calc_barycentres(self, i, direction):
        """ Calculate the extended barycentres of layer i. """
        
        pprint.pprint(self.down_conn_dicts)
        barycentres = []
        
        if direction == 'up':
            edge_dict = self.up_conn_dicts[i]
        elif direction == 'down':
            edge_dict = self.down_conn_dicts[i]
            
        print "Barycentre Calc:", i, direction
        for vertex in self.vertices[i]:
            adjacent_conns = edge_dict[vertex.name]
            extended_ranks = []
            for vertex_name, port_name in adjacent_conns:
                vertex = self.vertex_dict[vertex_name]
                extended_ranks.append( vertex.get_port_extended_rank(port_name) )
            barycentres.append( 1.0 * sum(extended_ranks) /  len(adjacent_conns) )
            print " ", extended_ranks, " ", barycentres[-1]

        print " ", barycentres
        return barycentres
        
        
    def reorder_layer(self, i, direction):
        """ Barycentre Reordering of Layer i.
        If direction is:
        * 'down' - reorder layer i using upper barycentres.
        * 'up'   - reorder layer i using lower barycentres. 
        
        To preserve original ordering of vertices which share a barycentre
        measure, we'll do a DSU.
        """
        
        i_orig = range( len( self.vertices[i]) )
        bc_dir = 'down'
        if direction.lower() == 'down':
            bc_dir = 'up'
        barycentres = self.calc_barycentres(i, bc_dir )
        
        tmp = zip( barycentres, i_orig, self.vertices[i] )
        tmp.sort()
        self.vertices[i] = [ vertex for (bc,j,vertex) in tmp ]
        
        
    def get_vertex_labels(self, i):
        """ Return a list of the labels of each vertex in layer i. """
        return [ vertex.name for vertex in self.vertices[i] ]

        
        
    def display(self):
        str_ = ['Graph:']
        for layer in self.vertices:
            for vertex in layer:
                str_.append( vertex.display() )
                
        return '\n'.join(str_)
                
        
            
