import hyperedge

class Test_Hyperedges(object):

    def test__build_1to1_hyperedge(self):
        start_point = (2,3)
        end_point = (19,6)
        
        hedge = hyperedge.Hyperedge()
        hedge.add_connection(start_point, end_point)
        lines = [line for line in hedge.ilines()]
        
        assert lines == [ (start_point, (7,3)),
                           ((7,3), (7,6)),
                           ((7,6), end_point) ]

    def test_build_1to1_hyperedge_2(self):
        start_point = (2,3)
        end_point = (13,5)
        
        hedge = hyperedge.Hyperedge()
        hedge.add_connection(start_point, end_point)
        lines = [line for line in hedge.ilines()]
        
        assert lines == [ (start_point, (7,3)),
                           ((7,3), (7,5)),
                           ((7,5), end_point) ]
        
    def test__build_1to2_hyperedge(self):
        start_point = (2,3)
        end_point1 = (14,6)
        end_point2 = (15,4)
        
        hedge = hyperedge.Hyperedge()
        hedge.add_connection(start_point, end_point1)
        hedge.add_connection(start_point, end_point2)
        lines = [line for line in hedge.ilines()]

        assert lines == [ (start_point, (7,3)),
                           ((7,3), (7,6)),
                           ((7,6), end_point1),
                           ((7,4), end_point2) ]

    def test__build_bad_hyperedge(self):
        start_point1 = (2,3)
        start_point2 = (3,3)
        end_point1 = (13,5)
        end_point2 = (14,6)
        
        # what happens if i try to add a connection with a different
        # starting point? Ignore?
        hedge = hyperedge.Hyperedge()
        hedge.add_connection(start_point1, end_point1)
        hedge.add_connection(start_point2, end_point2)
        
        # it should be ignored... (raise an exception?)
        lines = [line for line in hedge.ilines()]
        assert lines == [ (start_point1, (7,3)),
                           ((7,3), (7,5)),
                           ((7,5), end_point1) ]
    
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
        assert lines == [ (start_point, (30,6)),
                           ((30,1), (30,8)),
                           ((30,8), end_point1),
                           ((30,1), end_point2)]

class Test_Hyperedge_Xover_Counting(object):
    """ Crossover Counting Function Tests.
               +--------*
        *------+  +=====*
               +--------*
                  |
        *=========+=====*
    """
    
    # line crossing algorithm checks
    def test__line_crossing_parallel(self):
        line1, line2 = ((10,3), (5,3)), ((10, 5), (5, 5))
        assert hyperedge._check_for_crossing(line1, line2) == False
    
    def test__lines_overlap(self): # !!!FIXME!!!
        line1, line2 = ((10,3), (10,7)), ((10,5), (10, 20))
        assert hyperedge._check_for_crossing(line1, line2) == True
        
    def test__lines_dont_overlap(self):
        line1, line2 = ((10,3), (10,7)), ((10,10), (10, 20))
        assert hyperedge._check_for_crossing(line1, line2) == False
        
    def test__lines_cross(self):
        line1, line2 = ((0,0), (3,4)), ((2,2), (0,5))
        assert hyperedge._check_for_crossing(line1, line2) == True
        
    def test__lines_do_not_cross(self):
        line1, line2 = ((2,2), (2,6)), ((3,3), (3,6))
        assert hyperedge._check_for_crossing(line1, line2) == False

        
    # hyperedge crossover counting checks
    def test__single_crossover(self): #
        hedge1 = hyperedge.Hyperedge()
        hedge1.add_connection((10,3), (60,6))
        hedge1.add_connection((10,3), (60,4))
        hedge1.set_track(2)

        hedge2 = hyperedge.Hyperedge()
        hedge2.add_connection((14,7), (50,5))
        hedge2.add_connection((14,7), (50,8))
        hedge2.set_track(3)

        xovers = hyperedge.count_crossovers(hedge1, hedge2)
        assert xovers == 1
        
    def test__double_crossover(self): #
        hedge1 = hyperedge.Hyperedge()
        hedge1.add_connection((10,3), (60,6))
        hedge1.add_connection((10,3), (60,4))
        hedge1.set_track(2)

        hedge2 = hyperedge.Hyperedge()
        hedge2.add_connection((5,7), (50,5))
        hedge2.add_connection((5,7), (50,8))
        hedge2.set_track(3)

        xovers = hyperedge.count_crossovers(hedge1, hedge2)
        assert xovers == 2   
        
