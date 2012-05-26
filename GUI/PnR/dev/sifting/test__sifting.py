import GUI.PnR.sifting_router as sifting_router
import GUI.PnR.hypernet as hypernet

class Test__Sifting(object):

    def _build_hypernet(self, name, start, ends):
        hnet = hypernet.Hypernet(name)
        for end in ends:
            hnet.add_connection(start, end)
        return hnet
        
    def _build_two_hypernets(self):
        """ Build two hypernets. 
        Expected crossings matrix 
        
                 spud     potato
        spud       0        3
        potato     1        0
        """
        hnets = []
        hnets.append( self._build_hypernet('spud', (10,40), [(99,30), (99,80)] ))
        hnets.append( self._build_hypernet('potato', (10,60), [(99,20), (99,90)] ))
        return hnets
        
    def _build_three_hypernets(self):
        hnets = self._build_two_hypernets()
        hnets.append( self._build_hypernet('mash', (10,80), [(99,10), (99,99)]))
        return hnets
        
    def test__small_crossing_matrix(self):
        hnets = self._build_two_hypernets()
        crossing_matrix = sifting_router._build_crossing_matrix(hnets)
        
        expected = { 'spud' :
                        { 'spud' : 0, 'potato' : 3 },
                     'potato':
                        { 'spud' : 1, 'potato' : 0 },
                    }
                        
        assert crossing_matrix == expected

    def test__sifting_three_hypernets(self):
        hnets = self._build_three_hypernets()
        sifting_router.assign_tracks(hnets)
        
        expected = { 'spud' : 3, 'potato' : 2, 'mash': 1 }
        
        tracks = {}
        for hn in hnets:
            tracks[hn.netname] = hn.track
        assert tracks == expected
