import pprint

class Graph2():
    """ A Graph Class """
    
    def __init__(self, vertices = [[],[]], edges = []):
        self.vertices = vertices
        self.edges = edges

        self.vertex_dict = {}
        self.down_conn_dicts = []
        self.up_conn_dicts = []    


    def update(self):
        """ Build a few connection dictionaries. """
        
        assert len(self.vertices) - 1 == len(self.edges)
        
        # dict of vertices indexed by their names
        self.vertex_dict = {}
        for vertices in self.vertices:
            for vertex in vertices:
                self.vertex_dict[vertex.name] = vertex
     
        # Downward connectivity dictionaries
        self.down_conn_dicts = []
        for edges in self.edges:
            conn_dict = {}
            for edge in edges:
                conn = (edge.target, edge.target_port)
                conn_dict.setdefault(edge.source, []).append(conn)
            self.down_conn_dicts.append(conn_dict)
            
        # Upward connectivity dictionaries
        self.up_conn_dicts = [ [] ]
        for edges in self.edges:
            conn_dict = {}
            for edge in edges:
                conn = (edge.source, edge.source_port)
                conn_dict.setdefault(edge.target, []).append(conn)
            self.up_conn_dicts.append(conn_dict)
            
        # Set port ranks for each vertex
        for layer in self.vertices:
            for vertex in layer:
                print vertex
                vertex.rank_ports(True)
                
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
        """
        pass
        
        
    def get_vertex_labels(self, i):
        """ Return a list of the labels of each vertex in layer i. """
        return [ vertex.name for vertex in self.vertices[i] ]

        
        
            
