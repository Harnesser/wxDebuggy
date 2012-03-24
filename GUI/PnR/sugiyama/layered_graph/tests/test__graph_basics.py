#! /usr/bin/env python
import pprint

from .. import graph
from .. import vertex
from .. import edge
from .. import port

import helpers

class Test_GraphBasicOperations():

	def test_graph_init_simples(self):
		G = helpers.very_simple_cct()
		G.update()
 
		vertex_names = G.vertex_dict.keys()
		vertex_names.sort()
		assert vertex_names == ['A', 'B']


	def test_graph_init_names(self):
		G = helpers.simple_cct()
		G.update()
        	
		expected_names = (
			['in1', 'in2', 'in3', 'in4'],
			['U0', 'U1'],
			['U2'],
			['out1'],
			)

		for i in range(0, len(expected_names)):
			names_in_layer = [ vertex.name for vertex in G.vertices[i] ]
			assert names_in_layer == expected_names[i]

		# make sure the layer count matches
		assert len(expected_names) == len(G.vertices)
       
 
	def test_graph_init_net_names(self):
		G = helpers.simple_cct()
		G.update()

		expected_names = (
			['in1', 'in2', 'in3', 'in4'],
			['n1','n2'],
			['out1'],
			)

		for i in range(0, len(expected_names)):
			nets_in_layer = [ edge.net for edge in G.edges[i] ]
			assert nets_in_layer == expected_names[i]

		# make sure the layer counts match
		assert len(expected_names) == len(G.edges)


	#
	# Vertex Ranking
	#
	def test_graph_init_ranking_top(self):
		G = helpers.simple_cct()
		G.update()
 
		expected_ranking = [0, 1, 2, 3]
		ranking = [ vertex.get_rank() for vertex in G.vertices[0] ]
		assert ranking ==  expected_ranking
 
 
	def test_graph_init_ranking_bot(self):
		G = helpers.simple_cct()
		G.update()
		print "Here, right?"
		expected_ranking = [0, 3]
		i = 1
		ranking = [ vertex.get_rank() for vertex in G.vertices[i] ]
		print "Ranking:", ranking
		assert ranking == expected_ranking
 
