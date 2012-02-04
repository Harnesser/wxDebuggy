class Port():
    """ Port Class. 
    References to Port() classes are listed in the Vertex() class.
    """
    
    def __init__(self, name, side):
        self.name = name
        self.side = side  # 'left', 'right', 'top' or 'bottom'
        
        self.rank = None
        
    def __str__(self):
        return '"%s" (dir=%s, rank=%d)' % (self.name, self.side, self.rank)
        
    def __repr__(self):
        return self.__str__()
        
        
    def set_rank(self, rank):
        """ Set the rank of the port."""
        self.rank = rank
        
    def get_rank(self):
        """ Return the rank of the port."""
        return self.rank
        
        
    def is_on_left(self):
        """ Is this port a vertex input? """
        return self.side == 'left'
        
    def is_on_right(self):
        """ Is this port a vertex output? """
        return self.side == 'right'
        
    def get_name(self):
        return self.name
        
