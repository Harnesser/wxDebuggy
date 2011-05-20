#!/usr/bin/env python
import sys
import unittest
from collections import namedtuple
import pprint

sys.path.append('../')
import matrix

Block = namedtuple('Block', 'name inputs outputs')

class MatrixReversion( unittest.TestCase ):
    "Connectivity Matrix Row Reversion Tests."
   
   
    def parse_shorthand(self, graph_string, debug=True ):
        """Take a string representing a graph and build a suitable datastructure
        2-layer graphs only.
        
        String is in the form:
            <source>.<port>:<sink>.<port>;
        
        Data Structures look like:
            vertex list :  [ Block(name='U1', inputs=('A', 'B'), outputs=('Y',) , ... ]
            edge list   :  [ (('_iport', 'in3'), ('U2', 'A')), ... ]
            
        """
        
        E = []
        V_top = []
        V_bot = []
        
        source_outputs = {}
        sink_inputs = {}
        
        # Split into edges
        edge_strs = graph_string.split(';')
        for edge_str in edge_strs:
            source, sink = edge_str.split(':')
            
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
            
        return V_top, V_bot, E

        
    def test_row_reversion_1(self):
        edges = [
            'A.1:Z.2', 'A.2:Z.3',
            'B.1:X.2', 'B.2:X.3', 'B.3:X.4',
            'C.1:X.1', 
            'D.1:Y.1', 'D.2:Y.2', 'D.3:Z.1'
            ]
        V_top, V_bot, E = self.parse_shorthand(';'.join(edges))
        M = matrix.Matrix( V_top, V_bot, E )
        print M
        
        M.row_reversion()
        self.assertEquals( M.row_vertices, list('abdc') )
        print M

        
    def test_col_reversion_1(self):
        M = matrix.Matrix( self.vertices_top, self.vertices_bot, self.edges )
        print M
        
        M.col_reversion()
        self.assertEquals( M.col_vertices, list('efgih') )
        print M

        

               


        
        
        
        
        
        
        
        
