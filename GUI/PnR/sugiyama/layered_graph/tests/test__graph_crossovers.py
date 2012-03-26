#! /usr/bin/env python
""" Graph Crossover counting tests. """

import pprint
from .. import graph
import helpers

class Test_Graph_Crossover_Counting():

	def test_calc_crossovers(self):
		G = helpers.orig_sugiyama_cct()
		G.update()
		assert G.count_crossovers() == 8 	
 
