#! /usr/bin/env python

import graph_test_base
import port
import vertex

class VertexBasicOperations(graph_test_base.Graph_Test_Base):

    def add_some_ports(self, _vertex, port_shorthand):
        """ Add some ports to the vertex. """

        port_names = []

        for name, direction in port_shorthand:
            _port = port.Port(name, direction)
            _vertex.add_port(_port)
            port_names.append(name)
        
        return port_names
        
        
    def test_initialiser(self):
        V = vertex.Vertex('U0')
        self.assertEquals( V.get_name(), 'U0')
    
        
    def test_port_additions(self):
        """ Check that the order ports are added are remembered. """
        V = vertex.Vertex('A Thing')
        port_shorthand = [ ('in1','left'), ('in2','left'), 
            ('out1','right'), ('out2','right') ]
            
        port_names = self.add_some_ports(V, port_shorthand)
        self.assertEquals(port_names, V.get_port_names() )
        self.assertEquals(len(V.get_port_names()) , 4 )
        
        
    def test_vertex_rank(self):
        extended_rank = 23
        V = vertex.Vertex('another')
        V.set_rank(extended_rank)
        
        self.assertEquals(extended_rank, V.get_rank() )
        
        
    def test_vertex_rank_width_1(self):
        V = vertex.Vertex('a vertex')
        port_shorthand =  [ ('in1','left'), ('in2','left'), 
            ('out1','right'), ('out2','right') ]
        port_names = self.add_some_ports(V, port_shorthand)     
        
        self.assertEquals( V.get_rank_width(), 4 )  
        
                
    def test_vertex_rank_width_2(self):
        V = vertex.Vertex('a vertex')
        port_shorthand =  [ ('in1','left'), ('in2','left'), 
            ('in3','left'), ('in4','left'),
            ('out3','right'), ('out4','right'),
            ('out1','right'), ('out2','right') ]
        port_names = self.add_some_ports(V, port_shorthand)     
 
        self.assertEquals( V.get_rank_width(), 8 )
        
        
    def test_input_port_list(self):
        V = vertex.Vertex('something')
        port_shorthand = [ ('in1','left'), ('in2','left'), 
            ('in3','left'), ('in4','left'),
            ('out3','right'), ('out4','right'), ]
        port_names = self.add_some_ports(V, port_shorthand)
        
        ports = V.get_input_ports()
        port_names = V._extract_port_names(ports)
        
        self.assertEquals( port_names,  ['in1', 'in2', 'in3', 'in4'] )
        
            
    def test_output_port_list(self):
        V = vertex.Vertex('something')
        port_shorthand =  [ ('in1','left'), ('in2','left'), 
            ('in3','left'), ('in4','left'),
            ('out3','right'), ('out4','right'),
            ('out1','right'), ('out2','right') ]
        port_names = self.add_some_ports(V, port_shorthand)
        
        ports = V.get_output_ports()
        port_names = V._extract_port_names(ports)
        
        self.assertEquals( port_names,  ['out3','out4','out1','out2'] )
