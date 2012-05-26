import GUI.PnR.sifting_router as sifting_router
import GUI.PnR.hypernet as hypernet

class Test__Crossing_Matrix(object):

    def _build_hypernet(self, name, start, ends):
        hnet = hypernet.Hypernet(name)
        for end in ends:
            hnet.add_connection(start, end)
        return hnet
        
    def _build_two_hypernets(self):
        """ Build two hypernets. 
        Expected crossings matrix 
        
                 spud     potato  < below
        spud       0        3 
        potato     1        0         'Above' == track number is lower.
          ^
        Above
        """
        hnets = []
        hnets.append( self._build_hypernet('spud', (10,10), [(80,23), (80, 50)] ))
        hnets.append( self._build_hypernet('potato', (10, 20), [(70, 30), (70, 60)] ))
        return hnets

    def test__simple(self):
        hnets = self._build_two_hypernets()
        crossing_matrix = sifting_router._build_crossing_matrix(hnets)
        
        expected = { 'spud' :
                        { 'spud' : 0, 'potato' : 3 },
                     'potato':
                        { 'spud' : 1, 'potato' : 0 },
                    }
                        
        assert crossing_matrix == expected



