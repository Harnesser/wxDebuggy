#! /usr/bin/env python

import os
import sys
import unittest

def find_base():
    path = os.getcwd()
    while path != '/':
        basename = os.path.basename(path)
        if basename == 'wxDebuggy' or basename == 'workspace':
            return path
        else:
            path = os.path.dirname(path)
    return None
    
def set_paths():
    # Set path to module under test
    proj_dir = find_base()
    sys.path.append(proj_dir) # for vv.
    sys.path.append( os.path.join( proj_dir, 'GUI/PnR/sugiyama') )

set_paths()

import graph
import vertex
import port
import edge

class Graph_Test_Base(unittest.TestCase):
    """ Base class for Graph Unittests. """
    
    
    def build_graph_from_shorthand( graph_string, set_order=None, debug=True ):
        """ Return a Graph() instance of the parsed shorthand string. """
        
        V_top, V_bot, E = self._parse_shorthand( graph_string, set_order, debug )
           
        G = graph.Graph( [ V_top, V_bot ], E )
        return G
        
        
        
    def _parse_shorthand( graph_string, set_order=None, debug=True ):
        """Take a string representing a graph and build a suitable datastructure
        2-layer graphs only.
        
        String is in the form:
            <source>.<port>:<sink>.<port>;
        
        Data Structures look like:
            source vertex list :  [ Vertex, ... ]
            target vertex list :  [ Vertex, ... ]
            edge list          :  [ Edge, ... ]
            
        """
        
        E = []
        V_top = []
        V_bot = []
        
        V_top_dict = {}
        V_bot_dict = {}
        
        source_outputs = {}
        sink_inputs = {}
        
        # Split into edges
        edge_strs = graph_string.split(';')
        for edge_str in edge_strs:
            source, target = edge_str.split(':')
            
            # Build source Vertex and Port objects if required
            v_source, p_source = source.split('.')
            if v_source not in V_top_dict:
                V = vertex.Vertex(v_source)
                P = port.Port(p_source, 'right')
                V.add_port(P)
            else:
                V = V_top_dict[v_source]
                if p_source not in V.port_dict:
                    P = port.Port(p_source, 'right')
                    V.add_port(P)
            
            # Build target Vertex and Port objects if required                       
            v_target, p_target = target.split('.')
            
            #v_target, p_target = 
            block, port = source.split('.')
            if block not in source_outputs:
                source_outputs.setdefault(block, []).append(port)
            elif port not in source_outputs[block]:
                source_outputs[block].append(port)
            
            edge = [ (block, port) ]
                        
            block, port = sink.split('.')
            if block not in sink_inputs:
                sink_inputs.setdefault(block, []).append(port)
            elif port not in sink_inputs[block]:
                sink_inputs[block].append(port)
            
            edge.append( (block, port) )
        
            # Add edges
            edge = tuple(edge)
            E.append(edge)
            
            
        # Build vertice lists
        for block in source_outputs:
            vertex = Block(name=block, inputs=tuple(), outputs=tuple(source_outputs[block]) )
            V_top.append(vertex)
            
        for block in sink_inputs:
            vertex = Block(name=block, inputs=tuple(sink_inputs[block]), outputs=tuple() )
            V_bot.append(vertex)
                       
        if debug:
            pprint.pprint(V_top)
            pprint.pprint(V_bot)
            pprint.pprint(E)
            
            
        if set_order:
            top_order, bot_order = set_order
            V_top = reorder_vertices( V_top, top_order )
            V_bot = reorder_vertices( V_bot, bot_order )
            
        return V_top, V_bot, E

