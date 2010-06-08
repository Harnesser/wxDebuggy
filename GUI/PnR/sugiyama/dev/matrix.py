
class Matrix(object):
    """ A Class to model a matrix for Sugiyama Layouts.
    A collection of these matrices will form the Martix Realisation
    of a graph. """

    
    def __init__(self, row_vertices, col_vertices, edges):
        
        self.row_vertices = row_vertices
        self.col_vertices = col_vertices
        self.edges = edges
        
        self.update()
        
        
    def get_size(self):
        """ Return the size of the connectivity matrix."""
        return (self.c_rows, self.c_cols)
        
        
    def update(self):
        """ Recalculate the recalculable."""
        self.c_rows = len(self.row_vertices)
        self.c_cols = len(self.col_vertices)

        self.M = self._build_connection_matrix()
        
        self.row_barycentres = self._calc_row_barycentres()
        self.col_barycentres = self._calc_col_barycentres()
        
        
    def get_crossover_count(self):
        """ Return the crossover count of the connectivity matrix. """
        return self._calc_crossover_count()
        
        
    def copy(self):
        """ Return a deepish copy of the instance."""
        
        M_copy = Matrix( list(self.row_vertices),
            list(self.col_vertices), list(self.edges) )

        return M_copy   
            
        
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
        
        
    def _new_row_order(self, new_vertice_order):
        """ Reorder the connection matrix based on a new ordering. """

        # Rejigg the connection matrix for the new order
        row_dict = {}
        for key,value in zip( self.row_vertices, self.M ):
            row_dict[key] = value
    
        new_M = []
        for vertice in new_vertice_order:
            new_M.append( row_dict[vertice] )
        self.M = new_M
        
        # Rejigg the row barycentre numbers and vertices
        bc_dict = {}
        for key,value in zip( self.row_vertices, self.row_barycentres ):
            bc_dict[key] = value
            
        new_bc = []
        for vertice in new_vertice_order:
            new_bc.append( bc_dict[vertice] )
        self.row_barycentres = new_bc
                
        self.row_vertices = new_vertice_order
        
        # Recalculate the column barycentre numbers
        self.col_barycentres = self._calc_col_barycentres()         
        
        
    def barycentre_row_reorder(self):
        """ Reorder the rows based on their barycentres. """
        
        # Find the new vertice order
        dec = [ ( bc, v ) for (v, bc)  in zip( self.row_vertices, self.row_barycentres ) ]
        dec.sort()
        new_vertice_order = [ v for (bc, v) in dec ]
         
        self._new_row_order( new_vertice_order )

        
    def _get_column(self, i):
        """ Return the specified column as a list. """
        column = []
        for row in self.M:
            column.append( row[i] )
        return column


    def _new_col_order(self, new_vertice_order):
        """ Reorder the connection matrix based on a new ordering. """
        
        # Rejigg the connection matrix for the new order
        col_dict = {}
        for i in xrange( len(self.col_vertices) ):
           col_dict[self.col_vertices[i]] = self._get_column(i)

        new_M = []
        for j in xrange( len(self.row_vertices) ):
            new_row = []
            for new_vertice in new_vertice_order:
                new_row.append( col_dict[new_vertice][j] )
            new_M.append( new_row )
        self.M = new_M
        
        # Rejigg the row barycentre numbers and vertices
        bc_dict = {}
        for key,value in zip( self.col_vertices, self.col_barycentres ):
            bc_dict[key] = value
            
        new_bc = []
        for vertice in new_vertice_order:
            new_bc.append( bc_dict[vertice] )
        self.col_barycentres = new_bc
       
        self.col_vertices = new_vertice_order
        
        # Recalculate the row barycentre numbers
        self.row_barycentres = self._calc_row_barycentres()
        
                
    def barycentre_col_reorder(self):
        """ Reorder the columns based on their barycentres. """
        
        # Find the new vertice order
        dec = [ ( bc, v ) for (v, bc)  in zip( self.col_vertices, self.col_barycentres ) ]
        dec.sort()
        new_vertice_order = [ v for (bc, v) in dec ]
        
        self._new_col_order(new_vertice_order)
        
        
    def _reversion(self, vertices, barycentres ):
        """ Vertice Reversion"""
        
        new_vertice_order = []
        vertice_group = [ vertices[0] ]
       
        for i in xrange(1, len(barycentres) ):
            if barycentres[i] == barycentres[i-1]:
                vertice_group.append( vertices[i] )
            else:
                vertice_group.reverse()
                new_vertice_order.extend(vertice_group)
                vertice_group = [ vertices[i] ]

        vertice_group.reverse()
        new_vertice_order.extend(vertice_group)
        
        return new_vertice_order
          
          
    def row_reversion(self):
        """ Reverse rows sequences that have equal barycentres."""
        new_order = self._reversion( self.row_vertices, self.row_barycentres )
        self._new_row_order( new_order )

     
    def col_reversion(self):
        """ Reverse columns with equal barycentre numbers."""
        new_order = self._reversion( self.col_vertices, self.col_barycentres )
        self._new_col_order( new_order )
                     
    
    def _barycentres_are_monotonic(self, barycentres):
        """ Barycentre list is always on the increase?"""
        
        if len(barycentres) == 1:
            return True
            
        for i in xrange(1, len(barycentres) ):
            if barycentres[i] < barycentres[i-1]:
                return False
                
        return True
        
        
    def row_barycenters_are_monotonic(self):
        return self._barycentres_are_monotonic(self.row_barycentres)
        
        
    def col_barycenters_are_monotonic(self):
        return self._barycentres_are_monotonic(self.col_barycentres)
                      
                      
    def __str__(self):
        """ Printout
        Print the connection matrix with row and col headers, and with
        row and column barycentre numbers just like in Sugiyama's paper.
        """
  
        repr_str_list = ['\nConnection Matrix:']
        
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
           
        # Add crossover count:
        repr_str_list[3] += "    K = %d" % ( self.get_crossover_count() )
        return '\n'.join(repr_str_list)
        
        
        
              
        
        
        
     
    
    
