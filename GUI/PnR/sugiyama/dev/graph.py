#! /usr/bin/env python

from matrix import Matrix

class Graph(object):
    """ A class to hold a proper, layered graph.
    Calculates connectivity matrices too, I think...
    """
    
    def __init__(self, vertices, edges):
        self.edges = edges  
        self.vertices = vertices
        self.matrices = []
        
        self.c_levels = 0
        
        self.lower_connectivities = []
        self.upper_connectivities = []
        
        self.update()
        
        
    def update(self):
        self.c_levels = len(self.vertices)
        assert( len(self.vertices) -1 == len(self.edges) )
            
    # ===========================================================
    #  Connectivities
    # ===========================================================       
            
    def build_connection_matrices(self):
        """ Construct connection matrices for the graph. """
        print self.vertices
        for i in xrange(self.c_levels-1):
            M = Matrix( self.vertices[i], self.vertices[i+1], self.edges[i] )
            self.matrices.append(M)
   
            
    def calc_lower_connectivities(self):
        """ Calculate the Upper Connectivites for each layer. 
        Equation (7) in Sugiyama."""

        self.lower_connectivities = []
        for M in self.matrices:
            connectivities = [ sum(x) for x in M.M ]
            self.lower_connectivities.append(connectivities)

                            
    def calc_upper_connectivities(self):    
        """ Calculate the Lower Connectivites for each layer.
        Equation (6) in Sugiyama's Paper.
        See here for adding columns:
        http://stackoverflow.com/questions/3223043
        """

        self.upper_connectivities = [ [] ] # extra level to keep indices consistent
        for M in self.matrices:
            connectivities = [ sum(x) for x in zip(*M.M) ]
            self.upper_connectivities.append(connectivities)
            
            
    # ===========================================================
    #  Barycentres
    # ===========================================================
                  
    def calc_upper_barycenters(self, i, upper_x_positions, debug=True):
        """ Calculate the upper connectivity of layer i.
        Equation (11) in Sugiyama's Paper.
        """
        
        p = len(self.vertices[i-1])
        upper_barycentres = []
        
        for k in xrange(len(self.vertices[i])): # sweep vertices in layer i
        
            barycentre = 0.0
           
            for j in xrange(p): # sweep vertices in layer i-1
                barycentre += self.matrices[i-1][j][k] * upper_x_positions[j]
            
            barycentre /= self.upper_connectivities[i][k]
            upper_barycentres.append(barycentre)    
        
        if debug:
            print "Upper barycenters for layer", i
            print "  ", upper_barycentres
            
        return upper_barycentres
        
        
        
    def __str__(self):
        repr_str_list = ["Graph:\n"]
        
        repr_str_list.append(" Vertices:")
        for i in xrange(self.c_levels):
            repr_str_list.append( "%10d %s" % (i, self.vertices[i] ) )
                    
        repr_str_list.append("\n    Edges:")
        for i in xrange(self.c_levels-1):
            repr_str_list.append( "%10d %s" % (i, self.edges[i] ) )
            
        return '\n'.join(repr_str_list)
