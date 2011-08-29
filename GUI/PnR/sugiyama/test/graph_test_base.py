#! /usr/bin/env python

import os
import sys
import unittest
import pprint

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

import graph2
from vertex import Vertex
from port import Port
from edge import Edge

class Graph_Test_Base(unittest.TestCase):
    """ Base class for Graph Unittests. """
    
    
    def build_graph_from_shorthand(self, graph_string, debug=False ):
        """ Return a Graph() instance of the parsed shorthand string. """
        
        V_top, V_bot, E = self._parse_shorthand( graph_string, debug )
           
        G = graph2.Graph2( [ V_top, V_bot ], [E] )
        return G
        
        
    def _parse_shorthand( self, graph_string, debug=False ):
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
        target_inputs = {}
        
        # Split into edges
        edge_strs = graph_string.split(';')
        for edge_str in edge_strs:
            source, target = edge_str.split(':')
            
            # Build source Vertex and Port objects if required
            v_source, p_source = source.split('.')
            if v_source not in V_top_dict:
                V = Vertex(v_source)
                P = Port(p_source, 'right')
                V.add_port(P)
                V_top_dict[v_source] = V
            else:
                V = V_top_dict[v_source]
                if p_source not in V.port_dict:
                    P = Port(p_source, 'right')
                    V.add_port(P)
            
            # Build target Vertex and Port objects if required                       
            v_target, p_target = target.split('.')
            if v_target not in V_bot_dict:
                V = Vertex(v_target)
                P = Port(p_target, 'left')
                V.add_port(P)
                V_bot_dict[v_target] = V
            else:
                V = V_bot_dict[v_target]
                if p_target not in V.port_dict:
                    P = Port(p_target, 'left')
                    V.add_port(P)
            
            # Add to edges list
            edge = Edge( 'n_' + edge_str, (v_source, p_source), (v_target, p_target) )
            E.append(edge)
            
            
        # Alphabetically Ordered Vertex list
        blocks = V_top_dict.keys()
        blocks.sort()
        V_top = [ V_top_dict[block] for block in blocks ]

        blocks = V_bot_dict.keys()
        blocks.sort()
        V_bot = [ V_bot_dict[block] for block in blocks ]
        
        # Alphabetically ordered port lists
        for block in V_bot:
            block.port_list.sort()
        for block in V_top:
            block.port_list.sort()
            
        if debug:
            pprint.pprint(V_top)
            pprint.pprint(V_bot)
            pprint.pprint(E)
            
        return V_top, V_bot, E

