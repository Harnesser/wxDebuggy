#! /usr/bin/env python
""" Sugiyama Layer Reordering Operations"""

import pprint
from ..layered_graph.tests import helpers
from .. import reordering
           
DEBUG = False

class Test_SugiyamaLayerReordering():
       
	def test__reorder_gates1_phase1(self):
		G = helpers.paper_cct()
		G.update()
		print G.display()

		eng = reordering.Reordering_Engine()
		eng.set_graph(G)
		#self.show_conn_matrices(eng.G, 'I N I T I A L')
		#        
		assert eng.G.count_crossovers() == 8
		#for x in eng.gen_phase1():
		#    self.show_conn_matrices(eng.G)
		#        
		assert eng.G.count_crossovers() == 0
		#
		#self.show_conn_matrices(eng.G, 'F I N A L   R E S U L T')

