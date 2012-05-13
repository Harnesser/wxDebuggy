import hyperedge

class Test_Hyperedges(object):

    def test__3segment_hyperedge(self):
        start_point = (2,3)
        end_point = (7,6)
        
        hype = hyperedge.Hyperedge()
        hype.add_connection(start_point, end_point)
        hype.display()

        lines = [line for line in hype.ilines()]
        print lines
        assert lines == [ ((2,3), (5,3)),
                           ((5,3), (5,6)),
                           ((5,6), (7,6)) ]
       


    
