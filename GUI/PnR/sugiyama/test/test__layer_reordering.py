#! /usr/bin/env python
""" Sugiyama Layer Reordering Operations"""

import pprint
from ..layered_graph.tests import helpers
from .. import reordering
           
DEBUG = False

class Test_SugiyamaLayerReordering():
 
    """      
    def test__reorder_gd09(self):
        G = helpers.paper_cct()
        G.update()
        print G.display()

        eng = reordering.Reordering_Engine()
        eng.set_graph(G)
        assert eng.G.count_crossovers() == 28

        eng.run(debug=True)    
        assert eng.G.count_crossovers() == 0
"""     

    def test__reorder_sugiyama_cct(self):
        G = helpers.orig_sugiyama_cct()
        G.update()
        print G.display()
        
        eng = reordering.Reordering_Engine()
        eng.set_graph(G)
        assert eng.G.count_crossovers() == 8
        
        eng.run(debug=True)
        print G.display()
        assert eng.G.count_crossovers() == 1
        
        
