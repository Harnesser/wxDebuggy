import hyperedge

class Test_Hyperedges(object):

    def test__build_1to1_hyperedge(self):
        start_point = (2,3)
        end_point = (7,6)
        
        hedge = hyperedge.Hyperedge()
        hedge.add_connection(start_point, end_point)
        lines = [line for line in hedge.ilines()]
        
        assert lines == [ (start_point, (5,3)),
                           ((5,3), (5,6)),
                           ((5,6), end_point) ]

    def test_build_1to1_hyperedge_2(self):
        start_point = (2,3)
        end_point = (3,5)
        
        hedge = hyperedge.Hyperedge()
        hedge.add_connection(start_point, end_point)
        lines = [line for line in hedge.ilines()]
        
        assert lines == [ (start_point, (5,3)),
                           ((5,3), (5,5)),
                           ((5,5), end_point) ]
        
    def test__build_1to2_hyperedge(self):
        start_point = (2,3)
        end_point1 = (7,6)
        end_point2 = (8,4)
        
        hedge = hyperedge.Hyperedge()
        hedge.add_connection(start_point, end_point1)
        hedge.add_connection(start_point, end_point2)
        lines = [line for line in hedge.ilines()]

        assert lines == [ (start_point, (5,3)),
                           ((5,3), (5,6)),
                           ((5,6), end_point1),
                           ((5,4), end_point2) ]

    def test__build_bad_hyperedge(self):
        start_point1 = (2,3)
        start_point2 = (3,3)
        end_point1 = (3,5)
        end_point2 = (4,6)
        
        # what happens if i try to add a connection with a different
        # starting point? Ignore?
        hedge = hyperedge.Hyperedge()
        hedge.add_connection(start_point1, end_point1)
        hedge.add_connection(start_point2, end_point2)
        
        # it should be ignored... (raise an exception?)
        lines = [line for line in hedge.ilines()]
        assert lines == [ (start_point1, (5,3)),
                           ((5,3), (5,5)),
                           ((5,5), end_point1) ]
    
