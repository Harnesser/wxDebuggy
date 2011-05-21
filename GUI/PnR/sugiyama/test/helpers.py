import pprint
from collections import namedtuple

Block = namedtuple('Block', 'name inputs outputs')
   
def parse_shorthand( graph_string, set_order=None, debug=True ):
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
        
        
    if set_order:
        top_order, bot_order = set_order
        V_top = reorder_vertices( V_top, top_order )
        V_bot = reorder_vertices( V_bot, bot_order )
        
    return V_top, V_bot, E

def reorder_vertices( vertex_list, vertex_order ):
    vertex_dict = make_dict( vertex_list )
    new_vertex_list = []
    for vertex_name in vertex_order:
        new_vertex_list.append( vertex_dict[vertex_name] )
    return new_vertex_list
    
def make_dict( vertex_list ):
    vertex_dict = {}
    for vertex in vertex_list:
        vertex_dict[vertex.name] = vertex
    return vertex_dict
        
