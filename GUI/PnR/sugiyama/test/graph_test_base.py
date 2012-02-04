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

import graph
from vertex import Vertex
from port import Port
from edge import Edge

class Graph_Test_Base(unittest.TestCase):
    """ Base class for Graph Unittests. """
    
    
    def build_multilayer_graph_from_shorthand(self, edges_string, vertices=None ):
        """ Return a multilayer Graph() instance by parsing shorthand.
        Vertices are ordered alphabetically by default. """
        
        layer_strs = graph_string.split('\n')
        
        # Have I specified the order I want to see the vertices in each layer?
        if vertices:
            for layer in vertices:
                for vertex in vertices:
                    V = Vertex(vertex)
                    
        
        v_bot_prev = set()
        V = []
        E = []
        for layer_str in layer_strs:
            V_top, V_bot, E_layer = self._parse_shorthand( layer_str )
            
            names = [ vertex.name for vertex in V_top ]
            print "Before:", v_bot_prev
            v_bot_prev.update( set(names) )
            print "After:", v_bot_prev
            
            V.append( list(v_bot_prev) )
            V[-1].sort()
            v_bot_prev = set(V_bot)
            
            E.append(E_layer)
                
        V.append(v_bot_prev)
        
        G = graph.Graph( V, E )
        return G
        
        
    def build_graph_from_shorthand(self, graph_string, debug=False ):
        """ Return a Graph() instance of the parsed shorthand string. """
        
        V_top, V_bot, E = self._parse_shorthand( graph_string, debug )
           
        G = graph.Graph( [ V_top, V_bot ], [E] )
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
                if p_source.startswith('o_'):
                    P = Port(p_source, 'right')
                else:   
                    P = Port(p_source, 'left')
                V.add_port(P)
                V_top_dict[v_source] = V
            else:
                V = V_top_dict[v_source]
                if p_source not in V.port_dict:
                    if p_source.startswith('o_'):
                        P = Port(p_source, 'right')
                    else:
                        P = Port(p_source, 'left')
                    V.add_port(P)
            
            # Build target Vertex and Port objects if required                       
            v_target, p_target = target.split('.')
            if v_target not in V_bot_dict:
                V = Vertex(v_target)
                if p_target.startswith('i_'):
                    P = Port(p_target, 'left')
                else:
                    P = Port(p_target, 'right')
                V.add_port(P)
                V_bot_dict[v_target] = V
            else:
                V = V_bot_dict[v_target]
                if p_target not in V.port_dict:
                    if p_target.startswith('i_'):
                        P = Port(p_target, 'left')
                    else:
                        P = Port(p_target, 'right')
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

