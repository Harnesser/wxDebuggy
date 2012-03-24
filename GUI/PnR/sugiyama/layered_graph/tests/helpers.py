""" Helper functions to build graphs. """

from .. import port
from .. import vertex
from .. import graph
from .. import edge

def build_module(name, in_ports = [], out_ports = []):
	""" Build a vertex representation of a verilog module. """
	
	_vertex = vertex.Vertex(name)
	for p in in_ports:
		_port = port.Port(p, 'left')
		_vertex.add_port(_port)
	for p in out_ports:
		_port = port.Port(p, 'right')
		_vertex.add_port(_port)
	return _vertex


def very_simple_cct():
	""" Build a very simple graph of a very simple cct.

                  +-------+       +-------+
                  |       |       |       |
                  |    o1 +-------> i1    |
                  |       |       |       |
                  +-------+       +-------+
                      A               B
	"""	

	m_a = build_module('A', [], ['o1'])
	m_b = build_module('B', ['i1'], [])

	g = graph.Graph('very_simple_cct')
        g.add_vertex(0, m_a)
	g.add_vertex(1, m_b)

        e = edge.Edge('n1', ('A', 'o1'), ('B','i1') )
        g.add_edge(e)

	return g


def simple_cct():
	""" Build a simple cct.

                 +-----+ 
       in1  +----> a   |
                 |   y +---+
       in2  +----> b   |   |
                 +-----+   |   +-----+
                   U0      +---> a   |
                               |   y +---> out1
                 +-----+   +---> b   |
       in3  +----> a   |   |   +-----+
                 |   y +---+a    U2
       in4  +----> b   |
                 +-----+       
                   U1
	"""

	g = graph.Graph('simple_cct')

	# input ports
        input_ports = ( 'in1', 'in2', 'in3', 'in4' )
	for port in input_ports:
		p = build_module(port, [], [port])
		g.add_vertex(0, p)
	
        # layer 1
       	modules =  ( ( 'U0', ['a','b'], ['y'] ),
	             ( 'U1', ['a','b'], ['y'] ),
		   )
        for name, ins, outs in modules:
		m = build_module( name, ins, outs)
		g.add_vertex(1, m)

	# layer 2 
	modules = ( ( 'U2', ['a','b'], ['y'] ),
	          )
	for name, ins, outs in modules:
		m = build_module(name, ins, outs)
		g.add_vertex(2, m)

	# output ports
	p = build_module('out1', ['out1'], [])
	g.add_vertex(3, p)

        
        ## Connections
	connections = ( ('in1', ('in1', 'in1'), ('U0', 'a') ),
	                ('in2', ('in2', 'in2'), ('U0', 'b') ),
	                ('in3', ('in3', 'in3'), ('U1', 'a') ),
	                ('in4', ('in4', 'in4'), ('U1', 'b') ),
	                ('n1',  ('U0', 'y'),    ('U2', 'a') ),
	                ('n2',  ('U1', 'y'),    ('U2', 'b') ),
	                ('out1', ('U2', 'y'),   ('out1', 'out1') ),
	              )
	for name, source, target in connections:
		e = edge.Edge(name, source, target)
		g.add_edge(e)

	return g
