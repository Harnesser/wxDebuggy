#! /usr/bin/env python

import graph_test_base
import vertex

class VertexBasicOperations(graph_test_base.Graph_Test_Base):

    def test_initialiser(self):
        V = vertex.Vertex('U0')
        self.assertEquals( V.get_name(), 'U0')
        
