
class Matrix(object):
    """ A Class to model a matrix for Sugiyama Layouts.
    A collection of these matrices will form the Martix Realisation
    of a graph. """

    
    def __init__(self, row_vertices, col_vertices, edges):
        
        self.row_vertices = row_vertices
        self.col_vertices = col_vertices
        self.edges = edges
        
        self.c_rows = len(self.row_vertices)
        self.c_cols = len(self.col_vertices)

        self.M = self._build_connection_matrix()
        
        self.row_barycentres = self._calc_row_barycentres()
        self.col_barycentres = self._calc_col_barycentres()
        
        
    def get_size(self):
        """ Return the size of the connectivity matrix."""
        return (self.c_rows, self.c_cols)
        
        
    def _build_connection_matrix(self):
        """ Initialise the connection matrix for this layer. """
        
        M = []

        # Size matrix and initialise to zero
        for i in xrange( self.c_rows ):
            row = [0] * self.c_cols
            M.append(row)

        # Fill in the connections
        for source, sink in self.edges:
            row_index = self.row_vertices.index( source )
            col_index = self.col_vertices.index( sink )
            M[row_index][col_index] = 1
            
        return M

        
    def _calc_row_barycentres(self):
        """ Calculate the row barycentres of the matrix. """
 
        barycentres = []
        
        for k in xrange(self.c_rows):
            numer = 0.0
            denom = 0.0
            
            for l in xrange(self.c_cols):
                numer += l * self.M[k][l]
                denom += self.M[k][l]
                
            if denom:
                barycentre = numer / denom
            else:
                barycentre = 0.0
                
            barycentres.append(barycentre)
        
        return barycentres
                
                
    def _calc_col_barycentres(self):
        """ Calculate the column barycentres of the matrix. """
        
        barycentres = []
        
        for l in xrange(self.c_cols):
            numer = 0.0
            denom = 0.0
            
            for k in xrange(self.c_rows):
                numer += k * self.M[k][l]
                denom += self.M[k][l]
                
            if denom:
                barycentre = numer / denom
            else:
                barycentre = 0.0
                
            barycentres.append(barycentre)
            
        return barycentres
        
                         
    def __str__(self):
        """ Printout
        Print the connection matrix with row and col headers.
        """
  
        repr_str_list = []
        
        first_line = '%5s' % (' ')
        for vertice in self.col_vertices:
            first_line += '%5s' % (vertice )
        repr_str_list.append(first_line)
 
        for j in xrange(self.c_rows):
            line = '%5s' %(self.row_vertices[j])
            for conn in self.M[j]:
                line += '%5s' % (conn)
            line += ' : %.1f' % (self.row_barycentres[j])
            repr_str_list.append(line)
        
        last_line = '%5s' %('')
        for bc in self.col_barycentres:
            trunc = '%0.1f' % (bc)
            last_line += '%5s' % (trunc) 
        repr_str_list.append(last_line)
           
        return '\n'.join(repr_str_list)
        
        
        
              
        
        
        
     
    
    
