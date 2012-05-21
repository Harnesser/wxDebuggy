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
    
    def test__adjust_track_number(self):
        start_point = (10,6)
        end_point1 = (50,8)
        end_point2 = (50,1)
        
        hedge = hyperedge.Hyperedge()
        hedge.add_connection(start_point, end_point1)
        hedge.add_connection(start_point, end_point2)        
        hedge.set_track(4)
        lines = [line for line in hedge.ilines()]        
        
        print lines
        assert lines == [ (start_point, (20,6)),
                           ((20,1), (20,8)),
                           ((20,8), end_point1),
                           ((20,1), end_point2)]

class Test_Hyperedge_Xover_Counting(object):
    """ Crossover Counting Function Tests.
               +--------*
        *------+  +=====*
               +--------*
                  |
        *=========+=====*
    """
    
    def test__single_crossover(self):
        hedge1 = hyperedge.Hyperedge()
        hedge1.add_connection((10,3), (60,6))
        hedge1.add_connection((10,3), (60,4))
        
        hedge2 = hyperedge.Hyperedge()
        hedge2.add_connection((10,5), (60,5))
        hedge2.add_connection((10,5), (60,8))
        
        xovers = hyperedge.count_crossovers(hedge1, hedge2)
        assert xovers == 1
