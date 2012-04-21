#! /usr/bin/env python
""" Graph Upper and Lower Barycentre calculation tests. """

import pprint
from .. import graph
import helpers

class Test_GraphBarycentreOperations():

	#
	# Barycentre Calculations
	#
	def test_calc_barycentres_lower(self):
		G = helpers.paper_cct()
		G.update()
 	
		pprint.pprint(G.vertices)
		expected_bcs = [ 3.0, 4.0, 4.0, 13.0/3, 3.0 ]
		bcs = G.calc_barycentres(0,'lower')
		assert bcs == expected_bcs 
 
 
	def test_calc_barycentres_upper(self):
		G = helpers.paper_cct()
		G.update()
 
		expected_bcs = [ 3.0, 21.0/4, 19.0/3, 2.5, 11.0/2]
		bcs = G.calc_barycentres(1, 'upper')
		assert bcs == expected_bcs 
        
	#
	# Layer Reordering
	#
	def test_layer_reorder_upper(self):
		G = helpers.paper_cct()
		G.update()
        
		pprint.pprint(G.vertices)
		expected_vertex_order = 'U9:U6:U7:U10:U8'.split(':')

		i_layer = 1
		G.reorder_layer(i_layer, 'upper')
		assert G.get_vertex_labels(i_layer) == expected_vertex_order
 
 
	def test_layer_reorder_lower(self):
		G = helpers.paper_cct()
		G.update()
 
		pprint.pprint(G.vertices)
		expected_vertex_order = 'U1:U5:U2:U3:U4'.split(':')
		i_layer = 0
 
		G.reorder_layer(i_layer, 'lower')
		assert G.get_vertex_labels(i_layer) == expected_vertex_order
		
		
	#
	# Layer Reversion
	#
	def test_layer_reversion_1(self):
	    G = helpers.paper_cct()
	    G.update()
	    G.layer_reversion(0, 'lower')
	    
	    expected_vertex_order = 'U1:U3:U2:U4:U5'.split(':') 
	    new_vertex_order = G.get_vertex_labels(0)
	    assert new_vertex_order == expected_vertex_order
	    
	    
