import hyperedge

class Test_Hyperedges(object):

    def test__build_hyperedge(self):
        start_point = (2,3)
        end_point = (7,6)
        
        hedge = hyperedge.Hyperedge()
        hedge.add_connection(start_point, end_point)
        
        lines = [line for line in hedge.ilines()]
        assert lines == [ (start_point, (5,3)),
                           ((5,6), (5,6)),
                           ((5,6), end_point) ]


    def test__build_1to2_hyperedge(self):
        start_point = (2,3)
        end_point1 = (7,6)
        end_point2 = (8,4)
        
        hedge = hyperedge.Hyperedge()
        hedge.add_connection(start_point, end_point1)
        hedge.add_connection(start_point, end_point2)
        
        lines = [line for line in hedge.ilines()]
        assert lines == [ (start_point, (5,3)),
                           ((5,4), (5,6)),
                           ((5,6), end_point1),
                           ((5,4), end_point2) ]

        
    
