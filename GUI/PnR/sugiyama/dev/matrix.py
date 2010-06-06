
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
        
        
    def get_crossover_count(self):
        """ Return the crossover count of the connectivity matrix. """
        return self._calc_crossover_count()
        
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
        
        
    def _calc_k(self, j, k):
        """ Calculate the crossings between an ordered pair of vertex rows.
        Calculates k( r(u,v), r(v,u) ) """
        q = self.c_cols
        k_jk = 0
        
        for a in xrange(0, self.c_cols-1 ):  # 0 ... q-2
            for b in xrange(a+1, self.c_cols ): # a+1 ... q-1
                k_jk += self.M[j][b] * self.M[k][a]
        
        return k_jk


    def _calc_crossover_count(self):
        """ Find out how many crossovers this connectivity matrix has."""
        K_M = 0
        
        for j in xrange(0, self.c_rows-1):
            for k in xrange(j+1, self.c_rows):
                K_M += self._calc_k( j, k )
        
        return K_M
        
        
    def _barycentre_row_reorder(self):
        """ Reorder the rows based on their barycentres. """
        
        # Find the new vertice order
        dec = [ ( bc, v ) for (v, bc)  in zip( self.row_vertices, self.row_barycentres ) ]
        dec.sort()
        new_vertice_order = [ v for (bc, v) in dec ]
        new_row_barycentres = [ bc for (bc, v) in dec ]
        
        print self.row_barycentres
        print new_row_barycentres
        
        # Rejigg the connection matrix for the new order
        row_dict = {}
        for key,value in zip( self.row_vertices, self.M ):
            row_dict[key] = value
  
        new_M = []
        for vertice in new_vertice_order:
            new_M.append( row_dict[vertice] )
        self.M = new_M
        
        # Rejigg the row barycentre numbers
        self.row_barycentres = new_row_barycentres
        
        # Recalculate the column barycentre numbers
        self.col_barycentres = self._calc_col_barycentres()
        
                                 
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
        
        
        
              
        
        
        
     
    
    
