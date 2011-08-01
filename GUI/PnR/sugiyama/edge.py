
class Edge():
    """ Edge Class """
    
    def __init__(self, net, source, target ):
        self.net = net
        self.source, self.source_port = source
        self.target, self.target_port = target
