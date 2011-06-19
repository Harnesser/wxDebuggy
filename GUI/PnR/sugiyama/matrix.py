
class Matrix(object):
    """ A Class to model a matrix for Sugiyama Layouts.
    A collection of these matrices will form the Martix Realisation
    of a graph. 
    
    Some modifications are made to handle circuits, namely:
     * Edges are grouped if they belong to the same block
     * Each block has input and output vertices
     
    """
    
    def __init__(self, row_blocks, col_blocks, edges):
        self.row_blocks = row_blocks
        self.col_blocks = col_blocks
        self.row_vertices = []  # flattened 
        self.col_vertices = []
        self.edges = edges
        self.update()
        
        self.N = 10
                
    def get_size(self):
        """ Return the size of the connectivity matrix."""
        return (self.c_rows, self.c_cols)
        
        
    def update(self):
        """ Recalculate the recalculable."""

        self.row_vertices = []
        self.col_vertices = []
        
        # Flatten the connections        
        for block in self.row_blocks:
            for out_pin in block.outputs:
                self.row_vertices.append( '.'.join([block.name, out_pin]) )
        for block in self.col_blocks:
            for in_pin in block.inputs:
                self.col_vertices.append( '.'.join([block.name, in_pin]) )
            
        self.c_rows = len(self.row_vertices)
        self.c_cols = len(self.col_vertices)

        self.M = self._build_connection_matrix()
        
        self.row_barycentres = self._calc_row_barycentres()
        self.col_barycentres = self._calc_col_barycentres()
        
        self.block_row_barycentres = self._calc_block_row_barycentres()
        self.block_col_barycentres = self._calc_block_col_barycentres()
        
        
    def get_crossover_count(self):
        """ Return the crossover count of the connectivity matrix. """
        return self._calc_crossover_count()
        
        
    def copy(self):
        """ Return a deepish copy of the instance."""
        M_copy = Matrix( list(self.row_blocks),
            list(self.col_blocks), list(self.edges) )

        return M_copy   

        
    def _build_connection_matrix(self):
        """ Initialise the connection matrix for this layer. """
        
        M = []

        # Size matrix and initialise to zero
        for i in xrange( self.c_rows ):
            row = [0] * self.c_cols
            M.append(row)

        # Fill in the connections
        for ( (source, o_pin), (sink, i_pin) ) in self.edges:

            # First, names for port connections
            if source == '_iport':
                source_name = '.'.join([o_pin, o_pin])
            else:
                source_name = '.'.join([source, o_pin])
            if sink == '_oport':
                sink_name = '.'.join([i_pin, i_pin])
            else:
                sink_name = '.'.join([sink, i_pin])


            #  Now look for the index of each end of the edge in the upper and 
            # lower layer. These form the row and col index of the '1' 
            # representing this connection in the matrix.
            #  I've put try/excepts on each as the name lookup won't work if we've
            # got the start/end of a feedback edge. This, is a !!!FIXME!!! ftm.
            feed_forward = True
            try:                
                row_index = self.row_vertices.index( source_name )
            except ValueError:
                feed_forward = False
                
            try:
                col_index = self.col_vertices.index( sink_name )
            except ValueError:
                feed_forward = False
                
            #  Only register the connection if it's not the start/end of a 
            # feedback loop.
            if feed_forward:
                M[row_index][col_index] = 1
            
        return M

        
    def _calc_row_barycentres(self):
        """ Calculate the row barycentres of the matrix. """
 
        barycentres = []
        
        for k in xrange(self.c_rows):
            numer = 0.0
            denom = 0.0
            
            for l in xrange(self.c_cols):
                numer += (l+1) * self.M[k][l]
                denom += self.M[k][l]
                
            if denom:
                barycentre = numer / denom
            else:
                barycentre = 0.0
                
            barycentres.append(barycentre)
        
        return barycentres
                
    
    def _calc_block_row_barycentres(self):
        """ Calculate the block row barycentres of the matrix. 
        
        These are the average of the barycentres of the output ports 
        of each row block.
        """
        i = 0
        barycentres = []
        for block in self.row_blocks:
            bc_tmp = 0
            n_ports = len(block.outputs)
            for j in xrange(n_ports):
                bc_tmp += self.row_barycentres[i]
                i += 1
            bc_tmp /= n_ports
            barycentres.append(bc_tmp)
            
        return barycentres
        
        
    def _calc_block_col_barycentres(self):      
        """ Calculate the block col barycentres of the matrix. 
        
        These are the average of the barycentres of the input ports 
        of each col block.
        """
        i = 0
        barycentres = []
        for block in self.col_blocks:
            bc_tmp = 0
            n_ports = len(block.inputs)
            for j in xrange(n_ports):
                bc_tmp += self.col_barycentres[i]
                i += 1
            bc_tmp /= n_ports
            barycentres.append(bc_tmp)
            
        return barycentres
        
        
    def _calc_col_barycentres(self):
        """ Calculate the column barycentres of the matrix. """
        
        barycentres = []
        
        for l in xrange(self.c_cols):
            numer = 0.0
            denom = 0.0
            
            for k in xrange(self.c_rows):
                numer += (k+1) * self.M[k][l]
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
        
        
    def _new_row_order(self, new_block_order):
        """ Reorder the connection matrix based on a new ordering. 
        There are 4 stages to this:
        #1: reorder the connection matrix rows
        #2: reorder the barycentre numbers to match te new row order
        #3: reorder the block barycentre numbers
        #4: recalculate the flattened column barycentres
        #5: recalculate the block column barycentres
        """

        # Rejigg the connection matrix for the new order. Reorder flattened 
        # vertex names too
        i = 0
        row_data = zip( self.row_vertices, self.M, self.row_barycentres )
        row_dict = {}
        for block in self.row_blocks:
            for port in block.outputs:
                row_dict[(block.name, port)] = row_data[i]
                i += 1
    
        new_M = []
        new_vertices = []
        new_bcs = []
        for block in new_block_order:
            for port in block.outputs:
                vertex, conns, bcs = row_dict[(block.name, port)]            
                new_M.append(conns)
                new_vertices.append(vertex)
                new_bcs.append(bcs)
        self.M = new_M
        self.row_vertices = new_vertices
        self.row_barycentres = new_bcs
                
        # Rejig the block level barycentre numbers
        bc_dict = {}
        for block, bcs in zip( self.row_blocks, self.block_row_barycentres):
            bc_dict[block.name] = bcs
            
        new_bc = []
        for block in new_block_order:
            new_bc.append( bc_dict[block.name] )
        self.block_row_barycentres = new_bc
        
        self.row_blocks = new_block_order
        
        # Recalculate the column barycentre numbers
        self.col_barycentres = self._calc_col_barycentres()
        self.block_col_barycentres = self._calc_block_col_barycentres()        
        
        
    def barycentre_row_reorder(self):
        """ Reorder the rows based on their barycentres. """
        new_vertice_order = self._barycentre_reorder( self.row_blocks,
            self.block_row_barycentres )
        self._new_row_order( new_vertice_order )

        
    def _new_col_order(self, new_block_order):
        """ Reorder the connection matrix based on a new ordering. """
        
        # Flip cols into rows to make them easier to work with
        cols = zip( *self.M )
        
        # Rejigg the connection matrix for the new order. Reorder flattened 
        # vertex names too
        i = 0
        col_data = zip( self.col_vertices, cols, self.col_barycentres )
        col_dict = {}
        for block in self.col_blocks:
            for port in block.inputs:
                col_dict[(block.name, port)] = col_data[i]
                i += 1
                
        new_M = []
        new_vertices = []
        new_bcs = []
        for block in new_block_order:
            for port in block.inputs:
                vertex, conns, bcs = col_dict[(block.name, port)]
                new_M.append(conns)
                new_vertices.append(vertex)
                new_bcs.append(bcs)
        self.col_vertices = new_vertices
        self.col_barycentres = new_bcs
        self.M = [ list(a) for a in zip(*new_M) ] # zip() produces tuples, need lists

        # Rejig the block level barycentre numbers
        bc_dict = {}
        for block, bcs in zip( self.col_blocks, self.block_col_barycentres):
            bc_dict[block.name] = bcs
            
        new_bc = []
        for block in new_block_order:
            new_bc.append( bc_dict[block.name] )
        self.block_col_barycentres = new_bc
        
        self.col_blocks = new_block_order
        
        # Recalculate the column barycentre numbers
        self.row_barycentres = self._calc_row_barycentres()
        self.block_row_barycentres = self._calc_block_row_barycentres() 
        
                
    def barycentre_col_reorder(self):
        """ Reorder the columns based on their barycentres. """
        new_vertice_order = self._barycentre_reorder( self.col_blocks,
            self.block_col_barycentres )
        self._new_col_order( new_vertice_order )
        
        
    def _barycentre_reorder(self, blocks, barycentres):
        """ Reorder blocks based on barycentres.

        We're using Decorate-Sort-Undecerate here, decorating the block
        list with their barycentres, and with their order. This means that
        if we pass over a set of blocks with the same barycentre, the order
        within this small group is kept.
        """
        
        # Find the new vertice order
        orders = range( len( barycentres) )
        dec = [ ( bc, _ord, v ) for (bc, _ord, v)  in zip (
             barycentres, orders, blocks ) ]
        dec.sort()
        new_vertice_order = [ v for (bc, _ord, v) in dec ]
        
        return new_vertice_order
        
        
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
        if self._can_use_reversion(self.block_row_barycentres):
            print "Reversing..."
            print self.pretty()
            new_order = self._reversion( self.row_blocks, self.block_row_barycentres )
            self._new_row_order( new_order )
            print self.pretty()
            return True
        else:
            return False
             
    def col_reversion(self):
        """ Reverse columns with equal barycentre numbers."""
        if self._can_use_reversion(self.block_col_barycentres):
            new_order = self._reversion( self.col_blocks, self.block_col_barycentres )
            self._new_col_order( new_order )
            return True
        else:
            return False
    
    def _can_use_reversion(self, barycentres):
        """ Are there consequitive equal barycenters? 
        eg, [ 1.0, 2.0, 3.4, 3.4, 5.0 ]
        but not: [ 1.0, 2.0, 3.4, 5.0, 3.4 ]
        """
        TOL = 0.00001
        
        if len(barycentres) == 1:
            return False
        for i in xrange(1, len(barycentres) ):
            if barycentres[i-1] + TOL > barycentres[i] > barycentres[i-1] - TOL:
                return True
        return False

        
    def barycentres_are_monotonic(self, barycentres):
        """ Are barycentres monotonic? """
        if len(barycentres) == 1:
            return True
        for i in xrange(1, len(barycentres) ):
            if barycentres[i] <= barycentres[i-1]:
                return False
        return True
                    
    def row_barycenters_are_monotonic(self):
        return self._barycentres_are_monotonic(self.row_barycentres)
        
    def col_barycenters_are_monotonic(self):
        return self._barycentres_are_monotonic(self.col_barycentres)

                  
    def _truncate_name(self, name):
        if len(name) >= self.N-1:
            name = name[0:3] + '~' + name[-(self.N-5):]
        return name

    def __str__(self):
        """ Printout
        Print the connection matrix with row and col headers, and with
        row and column barycentre numbers just like in Sugiyama's paper.
        """
        fmt_str = '%%%ds' % (self.N)
        repr_str_list = ['\nConnection Matrix:']
        
        first_line = fmt_str % (' ')
        for vertice in self.col_vertices:
            first_line += fmt_str % ( self._truncate_name(vertice) )
        repr_str_list.append(first_line)
        repr_str_list.append('  ')
        
        for j in xrange(self.c_rows):
            line = fmt_str %( self._truncate_name(self.row_vertices[j]) )
            for conn in self.M[j]:
                line += fmt_str % (conn)
            line += '    : %.1f' % (self.row_barycentres[j])
            repr_str_list.append(line)
        
        repr_str_list.append('  ')
        last_line = fmt_str %('')
        for bc in self.col_barycentres:
            trunc = '%0.1f' % (bc)
            last_line += fmt_str % (trunc) 
        repr_str_list.append(last_line)
           
        # Add crossover count:
        repr_str_list[3] += "    K = %d" % ( self.get_crossover_count() )
        return '\n'.join(repr_str_list)
        
        
    def pretty(self):
        """ Return a fancy string representation of the matrix 
        __str__() can't use unicode chars, so this...
        """
        
        str_list = self.__str__().split('\n')
        str_list[4] = str_list[4].split('    K =')[0]
        
        # Add block barycentres
        self.__str_add_block_row_barycentres(str_list)
        self.__str_add_block_col_barycentres(str_list)

        # Nicer hit graphic
        new_str_list = []
        for line in str_list:
            line = line.replace('    0 ', '    - ')
            line = line.replace('    1 ', u'    \u2b1b ')
            new_str_list.append(line)
            
        str_list = new_str_list
        
        str_list[1] = str_list[1].replace('Matrix:',
            'Matrix (%0d crossovers)' % self.get_crossover_count() )
        return '\n'.join(str_list)
      
                          
    def __str_add_block_row_barycentres(self, str_list):
        """ Add the block barycenters to the matrix string representation. """
        
        i = 0
        i_str = 4
        for block in self.row_blocks:
            n = len(block.outputs)
            if n == 1:
                str_list[i_str] += u' \u2500\u2500 %.3f' % (self.block_row_barycentres[i])
            else:
                str_list[i_str] += u' \u252c\u2500 %.3f' % (self.block_row_barycentres[i])
                for j in xrange(n-2):
                    i_str += 1
                    str_list[i_str] += u' \u2502'
                i_str += 1
                str_list[i_str] += u' \u2518'
            i += 1
            i_str += 1      
          
          
    def __str_add_block_col_barycentres(self, str_list):
        """ Add col block barycentres to end of the string representation."""
        graphics_line = [ (' ' * self.N) ]
        barycentre_line = [ (' ' * self.N ) ]
        leadin = ' ' * (self.N-2)
        fmt_str = '%%%ds' % (self.N)
        
        i = 0
        i_str = 3
        for block in self.col_blocks:
            n = len(block.inputs)
            trunc = '%0.1f' % (self.block_col_barycentres[i])
            if n == 1:
                graphics_line.append( leadin + u'\u2502 ' )
                barycentre_line.append(fmt_str % (trunc))
            else:
                graphics_line.append( leadin + u'\u251c\u2500' )
                barycentre_line.append(fmt_str % (trunc) )
                for j in xrange(n-2):
                    graphics_line.append( (u'\u2500' * self.N) )
                    barycentre_line.append( (' ' * self.N ) )

                graphics_line.append( ( u'\u2500' * (self.N-2) ) + u'\u2518 ' )
                barycentre_line.append( (' ' * self.N ) )
            i += 1

        str_list.append( ''.join(graphics_line) )
        str_list.append( ''.join(barycentre_line) )
                    
        
