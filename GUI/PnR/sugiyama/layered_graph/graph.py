import pprint

DEBUG = False

class Graph():
    """ A Graph Class.
    For Layered, directed, acyclic graphs.
    Add vertices, then the edges.
    """
    
    def __init__(self, name):
        self.name = name
        self.vertices = {}          # keyed by layer
        self.edges = {}             # keyed by layer

        self.vertex_dict = {}       # keyed by vertex|module name
        self.down_conn_dicts = []
        self.up_conn_dicts = []    


    def add_vertex(self, i_layer, vertex):
        """ Should this be add_module? """
        self.vertices.setdefault(i_layer, []).append(vertex)
        self.vertex_dict[vertex.name] = vertex


    def add_edge(self, edge):
        """ Should this be add_connection?
        Should I figure out which layers this is between?
        Just put on the same layer as its source vertex ftm
        """
        # do it the long way ftm
        for i_layer, vertices in self.vertices.iteritems():
            for v in vertices:
                if edge.source == v.name:
                    self.edges.setdefault(i_layer, []).append(edge)
                    break


    def update(self):
        """ Build a few connection dictionaries.
        You should probably call this task after you've built the graph of
        your circuit.
        """
        assert len(self.vertices) - 1 == len(self.edges)
        
        # Downward connectivity dictionaries
        self.down_conn_dicts = []
        for i_layer in self.edges:
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
      
        barycentres = []
        
        if direction == 'upper':
            edge_dict = self.up_conn_dicts[i]
        else:
            edge_dict = self.down_conn_dicts[i]
            
        if DEBUG:
            print "Barycentre Calc:", i, direction
            print "  edge_dict:"
            pprint.pprint(edge_dict)
        
        for vertex in self.vertices[i]:
            adjacent_conns = edge_dict.get(vertex.name, [])
            if adjacent_conns:
                extended_ranks = []
                for vertex_name, port_name in adjacent_conns:
                    vertex = self.vertex_dict[vertex_name]
                    extended_ranks.append( vertex.get_port_extended_rank(port_name) )
                barycentres.append( 1.0 * sum(extended_ranks) /  len(adjacent_conns) )
            else:
                barycentres.append(-1.0)
                
        # now sweep up the -1s as in section 4.2 in [SFHM09]
        barycentres = self.fix_barycentres(barycentres)
        if DEBUG:
            print "Barycentres of layer %0d %0s: " % ( i, direction), barycentres
        return barycentres

        
    def fix_barycentres(self, barycentres):
        """ Replace the -1s 4.2 """
        
        fixed_barycentres = [0.0] * len(barycentres)
        
        for i in range ( len(barycentres) -1 ):
            if barycentres[i] != -1.0:
                fixed_barycentres[i] = barycentres[i]
            elif i == 0:
                fixed_barycentres[i] = 0.0
            elif barycentres[i+1] == -1:
                fixed_barycentres[i] = barycentres[i-1]
            elif barycentres[i-1] == -1:
                fixed_barycentres[i] = fixed_barycentres[i-1]
            else:
                fixed_barycentres[i] = ( barycentres[i-1] + barycentres[i+1] ) / 2.0
                
        if barycentres[-1] == -1.0:
            fixed_barycentres[-1] = fixed_barycentres[-2]
        else:
            fixed_barycentres[-1] = barycentres[-1]
        return fixed_barycentres
            
        
    def reorder_layer(self, i, direction):
        """ Barycentre Reordering of Layer i.
        If direction is:
        * 'upper' - reorder layer i using upper barycentres.
        * 'lower' - reorder layer i using lower barycentres. 
        
        where layer 0 is the top-most layer.
        
        To preserve original ordering of vertices which share a barycentre
        measure, we'll do a DSU.
        """
        
        i_orig = range( len( self.vertices[i]) )
        bc_dir = 'lower'
        if direction.lower() != 'lower':
            bc_dir = 'upper'
        barycentres = self.calc_barycentres(i, bc_dir )
        
        tmp = zip( barycentres, i_orig, self.vertices[i] )
        tmp.sort()
        self.vertices[i] = [ vertex for (bc,j,vertex) in tmp ]
        
        if DEBUG:
            print "Vertices: ", self.vertices[i]
            print "-" * 70
        self.rank_vertices(i)
        
        
    def layer_reversion(self, i, direction):
        """ Reverse any vertices with equal barycentres."""
     
        bc_dir = 'lower'
        if direction.lower() != 'lower':
            bc_dir = 'upper'
        
        barycentres = self.calc_barycentres(i, bc_dir)
        vertices = self.vertices[i]
               
        new_vertice_order = []
        vertice_group = [ vertices[0] ]
       
        for j in xrange(1, len(barycentres) ):
            if barycentres[j] == barycentres[j-1]:
                vertice_group.append( vertices[j] )
            else:
                vertice_group.reverse()
                new_vertice_order.extend(vertice_group)
                vertice_group = [ vertices[j] ]

        vertice_group.reverse()
        new_vertice_order.extend(vertice_group)
        if DEBUG:
            print "Reversion of layer %0d (%0s)" % (i, bc_dir)
            pprint.pprint( self.get_vertex_labels(i) )
        self.vertices[i] = new_vertice_order
        if DEBUG : pprint.pprint( self.get_vertex_labels(i) )
        self.rank_vertices(i)
        
        
    def get_vertex_labels(self, i):
        """ Return a list of the labels of each vertex in layer i. """
        return [ vertex.name for vertex in self.vertices[i] ]


    def count_crossovers(self):
        """ Count the crossovers in the Graph.
        !!!FIXME!!! This turns out to be a bit tricky to do with the data
        structures available by default...
        !!!TODO!!! "Simple and Efficient Bilayer Cross Counting"
        """
        layers = self.vertices.keys()
        layers.sort()
        x_overs = 0
  
        for layer in layers[:-1]:
            source_extended_ranks = []     
            # connection dict to this layer
            conn_dict = {}
            for edge in self.edges[layer]:
                target = (edge.target, edge.target_port)
                source = (edge.source, edge.source_port)
                conn_dict.setdefault(target, []).append(source)
            
            # get all sinks in the next layer
            targets = []
            for vertex in self.vertices[layer+1]:
                for port in vertex.get_input_ports():
                    targets.append((vertex.name, port.name))
                        
            # build source enumeration
            # can't use the extended rank because this will take the
            # input ports into account too...
            source_ranks = {}
            _i = 1
            for vertex in self.vertices[layer]:
                for oport in vertex.get_output_ports():
                    source_ranks[(vertex.name, oport.name)] = _i
                    _i += 1
                                
            # now we can calculate the crossovers
            lhs_ranks = []
            for target in targets:
                ranks = [ source_ranks[source] for source in conn_dict[target] ]
                ranks.sort()
                for source_rank in ranks:
                    for lhs_rank in lhs_ranks:
                        if lhs_rank > source_rank:
                            x_overs += 1
                    lhs_ranks.append(source_rank)
                                            
        # jeez, I hope we're done now after all that...
        if DEBUG : print 'OK, I see %d crossovers' % (x_overs)
        return x_overs        
        
        
    def count_layers(self):
        """ Return the number of layers. """
        return len(self.vertices)
        
        
    def copy(self):
        g = Graph(self.name)
        for (layer, vertices) in self.vertices.iteritems():
            for v in vertices:
                g.add_vertex(layer, v)
        
        for (layer, edges) in self.edges.iteritems():
            for e in edges:
                g.add_edge(e)
                
        g.update()
        return g
        
        
    def display(self):
        str_ = ['Graph:']
        for layer in self.vertices:
            str_.append('\n## Layer %0d' % (layer))
            for vertex in self.vertices[layer]:
                str_.append( vertex.display() )
                
        return '\n'.join(str_)
        
            
