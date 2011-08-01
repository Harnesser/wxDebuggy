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
            pprint.pprint(vertices)
            for vertex in vertices:
                self.vertex_dict[vertex.name] = vertex
        
        pprint.pprint(self.vertex_dict)
     
        # Downward connectivity dictionaries
        self.down_conn_dicts = []
        for edges in self.edges:
            conn_dict = {}
            for edge in edges:
                conn = (edge.target, edge.target_port)
                conn_dict.setdefault(edge.source, []).append(conn)
            self.down_conn_dicts.append(conn_dict)
            
        # Upward connectivity dictionaries
        self.up_conn_dicts = []
        for edges in self.edges:
            conn_dict = {}
            for edge in edges:
                conn = (edge.source, edge.source_port)
                conn_dict.setdefault(edge.target, []).append(conn)
            self.up_conn_dicts.append(conn_dict)
            
        
    def set_vertex_ranks(self, i):
        """ Update the ranks of each vertex in layer i. """
        rank = 0
        for vertex in self.vertices[i]:
            vertex.set_rank(rank)
            rank += vertex.get_rank_width()
            
    
                
            
