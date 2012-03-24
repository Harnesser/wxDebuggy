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

	_graph = graph.Graph('very_simple_cct')
        _graph.add_vertex(0, m_a)
        _graph.add_vertex(1, m_b)

        _edge = edge.Edge('n1', ('A', 'o1'), ('B','i1') )
        _graph.add_edge(_edge)

	return _graph
