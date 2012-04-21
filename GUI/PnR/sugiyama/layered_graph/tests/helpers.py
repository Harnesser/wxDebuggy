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


def paper_cct():
	""" Circuit from the Extended Sugiyama Presentation. """

	modules_top = (
		('U1', [], ['y','z'] ),
		('U2', [], ['z'] ),
		('U3', [], ['x','y','z'] ),
		('U4', [], ['x','y','z'] ),
		('U5', [], ['y','z'] ),
		)
	
	modules_bot = (
		('U6', ['a'], []),
		('U7', ['a','b','c'], []),
		('U8', ['a'], []),
		('U9', ['a','b'], []),
		('U10', ['a'], []),
		)

	g = graph.Graph('extended_sugiyama_paper_cct')
	for name, ins, outs in modules_top:
		m = build_module(name, ins, outs)
		g.add_vertex(0, m)
	for name, ins, outs in modules_bot:
		m = build_module(name, ins, outs)
		g.add_vertex(1, m)

	nets = (
		('n1',  ('U1','y'), ('U7','a') ),
		('n2',  ('U1','z'), ('U9','a') ),
		('n3',  ('U2','z'), ('U8','a') ),
		('n4',  ('U3','x'), ('U6','a') ),
		('n5',  ('U3','y'), ('U7','c') ),
		('n6',  ('U3','y'), ('U9','b') ),
		('n7',  ('U3','z'), ('U10','a') ),
		('n8',  ('U4','x'), ('U10','a') ),
		('n9',  ('U4','y'), ('U8','a') ),
		('n10', ('U4','z'), ('U7','b') ),
		('n11', ('U5','y'), ('U7','b') ),
		('n12', ('U5','z'), ('U8','a') ),
		)

	for name, source, target in nets:
		e = edge.Edge(name, source, target)
		g.add_edge(e)

	return g


def orig_sugiyama_cct():
	""" Reimagined circuit from Sugiyama's original paper. """

	g = graph.Graph('orig_sugiyama')

	# Vertices|Modules
	modules = [ [
			('U0', [], ['w','x','y','z']),
			('U1', [], ['y','z']),
		], [
			('U2', ['a','b'], ['z']),
			('U3', ['a'], ['x','y','z']),
			('U4', ['a'], ['y','z']),
			('U5', ['a','b'], []),
		], [
			('U6', ['a','b'], ['z']),
			('U7', ['a'], []),
			('U8', ['a'], ['y','z']),
			('U9', ['a','b'], ['y','z']),
		], [
			('U10', ['a','b','c'], []),
			('U11', ['a'], []),
			('U12', ['a'], []),
		], 
		]
	
	for layer in range(len(modules)):
		for name, ins, outs in modules[layer]:
			m = build_module(name, ins, outs)
			g.add_vertex(layer, m)

	# Connections
	nets = (
		('n1', ('U0','w'), ('U2','a')),
		('n2', ('U0','x'), ('U3','a')),
		('n3', ('U0','y'), ('U4','a')),
		('n4', ('U0','z'), ('U5','a')),
		('n5', ('U1','y'), ('U2','b')),
		('n6', ('U1','z'), ('U5','b')),

		('n7',  ('U2','z'), ('U6','a')),
		('n8',  ('U3','x'), ('U7','a')),
		('n9',  ('U3','y'), ('U8','a')),
		('n10', ('U3','z'), ('U9','a')),
		('n11', ('U4','y'), ('U6','b')),
		('n12', ('U4','z'), ('U9','b')),
		
		('n13', ('U6','z'), ('U10','a')),
		('n14', ('U8','y'), ('U10','b')),
		('n15', ('U8','z'), ('U12','a')),
		('n16', ('U9','y'), ('U10','c')),
		('n17', ('U9','z'), ('U11','a')),
		)

	for name, source, target in nets:
		e = edge.Edge(name, source, target)
		g.add_edge(e)

	return g

				
