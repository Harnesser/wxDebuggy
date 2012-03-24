#!/usr/bin/env python

import helpers
from .. import graph

class Test_GraphConnectivityOperations():

	def test_upper_connectivity(self):
		G = helpers.orig_sugiyama_cct()
 
		G.build_connection_matrices()
		G.calc_upper_connectivities()
 
		expected = [ [],            # this is to keep indexing sweet
			[2, 1, 1, 2],
			[2, 1, 1, 2],
			[3, 1, 1] ]
 	
		assert G.upper_connectivities == expected 
 
 
	def test_lower_connectivity(self):
		G = helpers.orig_sugiyama_cct()
 	
		G.build_connection_matrices()
		G.calc_lower_connectivities()
 
		expected = [ [4,2], [1,3,2,0], [1,0,2,2] ]
 
		assert G.lower_connectivities == expected
 
 
