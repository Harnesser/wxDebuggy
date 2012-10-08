
class Edge():
    """ Edge Class """
    
    def __init__(self, net, source, target ):
        self.name = net
        self.net = net
        self.source, self.source_port = source
        self.target, self.target_port = target
        
        
    def __str__(self):
        return '"%s" (%s) %s.%s -> %s.%s' % ( self.name, self.net,
            self.source, self.source_port,
            self.target, self.target_port )

    def __repr__(self):
        return self.__str__()
