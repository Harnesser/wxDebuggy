#!/usr/bin/env python

import pprint

import pnr_test_base
pnr_test_base.set_paths()

from PnR.graph_builder import Graph_Builder

class Graph_Builder_Dummy_Vertices( pnr_test_base.PnR_Test_Base ):

    def test__dummy_vertices_1(self):
        module = self.load_rtl_module_pickle('long_1')
       
        builder = Graph_Builder()
        builder.set_module(module)
        V, E = builder.get_graph_for_sugiyama()
        pprint.pprint(V)
        pprint.pprint(E)
        
        # There should be 1 dummmy vertices in this cct
        self.assertEquals( len(self.get_dummy_names(V) ), 1 )
        
                
    def test__dummy_vertices_2(self):
        module = self.load_rtl_module_pickle('long_2')
       
        builder = Graph_Builder()
        builder.set_module(module)
        V, E = builder.get_graph_for_sugiyama()
        pprint.pprint(V)
        pprint.pprint(E)
                
        # There should be 3 dummmy vertices in this cct
        self.assertEquals( len(self.get_dummy_names(V) ), 3 )
        
        
    def test__dummy_vertices_feedback_1(self):
        module = self.load_rtl_module_pickle('feedback_1')
        
        builder = Graph_Builder()
        builder.set_module(module)
        V, E = builder.get_graph_for_sugiyama()
        pprint.pprint(V)
        pprint.pprint(E)       
        
        #  There should be 1 feedback dummy vertex in this cct
        self.assertEquals( len(self.get_dummy_names(V) ), 1)        


    def test__dummy_vertices_feedback_2(self):
        module = self.load_rtl_module_pickle('feedback_2')
        
        builder = Graph_Builder()
        builder.set_module(module)
        V, E = builder.get_graph_for_sugiyama()
        pprint.pprint(V)
        pprint.pprint(E)       
        
        #  There should be 2 feedback dummy vertices in this cct
        self.assertEquals( len(self.get_dummy_names(V) ), 2)        
        
        
    def test__dummy_vertices_feedback_3(self):
        module = self.load_rtl_module_pickle('feedback_3')
        
        builder = Graph_Builder()
        builder.set_module(module)
        V, E = builder.get_graph_for_sugiyama()
        pprint.pprint(V)
        pprint.pprint(E)       
        
        #  There should be 4 feedback dummy vertices in this cct
        self.assertEquals( len(self.get_dummy_names(V) ), 4)        
                        
                        
    def get_dummy_names(self, layers):
        names = []
        for layer in layers:
            names_ = [ block.name for block in layer ]
            names.extend(names_)
        dummies = [ name for name in names if name.startswith('_') ]
        print "DUMMIES", dummies
        return dummies
