
class Edge():
    """ Edge Class """
    
    def __init__(self, net, source, target ):
        self.net = net
        self.source, self.source_port = source
        self.target, self.target_port = target
        
        
    def __str__(self):
        print '"%s" %s.%s -> %s.%s' % ( self.net,
            self.source, self.source_port,
            self.target, self.target_port )
