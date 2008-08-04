# placement_sugiyama.py 
""" Sugiyama Layout

Place the instanciations of the current module using a scheme based on 
Sugiyama's approach. This algorithm has a few stages:

 1: Remove cycles from graph
 2: Determine the layering of the graph
 3: Replace any edges which cross more than one layer with dummy nodes
 4: Sort the nodes on each layer in a manner to reduce the crossover count
 
This module swaps stages 1 & 2 - a recursive algorithm to produce the layering,
then any arcs which are pointing backwards are reversed.

"""


def build_graph(module):
    """ Build a graph for the current module to be displayed.
    """
    #
    # 1: Exract the graph from the circuit description    
    graph_edges = extract_graph(module)
    
    #
    # 2: Remove cycles
    #graph = remove_cycles(graph)

    #
    # 3: Layer the graph
    layer_dictionary = determine_layering(graph_edges)
    
    print "\nGraph Edges Dictionary"
    for key in graph_edges.keys():
        print key," :", graph_edges[key]
        

    #
    # 4: Insert dummy nodes - this makes the graph 'proper'
    graph = break_up_long_edges(layer_dictionary, graph_edges)
    # graph returns (layer_dictionary, graph_edges)
    
    #
    # 5: Reduce crossovers by reordering the layers
    #graph = reduce_crossings(graph)
    
    
    return graph
    
    
def extract_graph(module):
    """ Get a graph of the circuit to display.
    
    Returns the graph in the form ( [List of Vertices], [List of Edges] ).
    """
    
    driver_dictionary = build_driver_dictionary(module)
    connection_list = get_connection_list(driver_dictionary)
    graph_edges = get_graph_dictionary(connection_list)
    
    return graph_edges
    
    
def remove_cycles(graph, debug=True):
    """ Remove cycles from graph.
    Reverse certain edges to ensure the graph is acyclic.
    """
        
    
    return graph
    
    
def determine_layering(graph, inst='_iport', col_dict = {}, path = [], debug = False ):
    """ Layer the graph.
    
    Find the drivers of the current inst, and set their
    column numbers to one less than the current.

    col_dict[<instn_name>] = <column_number>

    Column[0] = Input ports
    Column[-1] = Output ports

    Look out for loops by doing something magical..."""

    col_num = col_dict.get(inst, 0) + 1
    path.append(inst)

    print "::", inst, graph.keys()

    #  Go through the drivers of this sink and update their
    # column numbers if necessary
    
    for sink in graph.get(inst,[]):

        print "SINK:" + sink
        # Loop detection...
        if sink in path :
            print "Loop!!: ", sink, ":", path
            continue

        # Only update the column count if needed.  If the load
        # is already to the right of this inst, then leave its
        # col number alone. 
        if col_num > col_dict.get(sink,0):
            col_dict[sink] = col_num
            col_dict = determine_layering( graph, sink, col_dict, path )
            
    path.pop()
    
    if debug:
        for key in col_dict.keys():
            print ("        " * ( col_dict[key] )) + key.center(8) 
        print "-" * 80
        print col_dict

    return col_dict
    
    
    
def break_up_long_edges(layer_dictionary, graph_edges, debug=True):
    """ Insert dummy nodes for long edges.
    Produces a 'proper graph'.    
    """
    
    # turn the layer graph inside out so that layer numbers are the keys.
    graph_layers = {}
    for key in layer_dictionary.keys():
        graph_layers.setdefault( layer_dictionary[key], []).append(key)     

    
    # Dummy nodes are placed in long edges (span >1)
    edges_for_removal = []
    for u in graph_edges.keys():
        for v in graph_edges[u]:
            start_layer = layer_dictionary.get(v,0) 
            end_layer   = layer_dictionary.get(u,0) 
            span = abs( start_layer - end_layer )
            
            if span > 1: # we've found a long edge..
                print "!Found a long edge: (%s,%s)" % (u,v)   
                edges_for_removal.append( (u,v) )
            
    # Delete edges - can't delete items from lists when iterating over them
    for u,v in edges_for_removal:
        start_layer = layer_dictionary.get(v,0) 
        end_layer   = layer_dictionary.get(u,0)        

        start_vertice = u
        for i in range( min(start_layer,end_layer) + 1, max(start_layer,end_layer) ):
            new_vertice_name = '_' + u + '__to__' + v + '_' + str(i)
            graph_layers[i].append(new_vertice_name)
            graph_edges.setdefault(start_vertice,set()).add(new_vertice_name)
                
        graph_edges.setdefault(new_vertice_name,set()).add(v)
                
    #                
    if debug:
    
        print "\nGraph Edges Dictionary"
        for key in graph_edges.keys():
            print key," :", graph_edges[key]        
                    
    
        print "\nGraph Layers Dictionary"
        for key in graph_layers.keys():
            print key," :", graph_layers[key]  
                    
    return True
    
    
    
def reduce_crossings(graph, debug=True):
    """ Reduce edge crossings.
    By reordering the nodes in each layer, the number of edge crossings is
    reduced.
    """

    layer_dictionary, graph_edges = graph
    
    
    
    

    return graph
    
    
## ================================================================================
""" Building a graph from a circuit description.

Edges on a graph are specified as (u,v) where u and v are vertices in the graph.
In an electrical circuit, instantiations are the vertices and the wires are the
edges.  Edges in a graph for an electrical circuit are directed, as there is a 
flow from output to input ports.  A 'netlist' lists the connections of ports to
nets.

To build edges from a netlist, the source and sink for each net must be determined. 
First, a driver dictionary is built.  From this, a point-to-point connection list
is constructed.  Finally, a list of edges (or properly, arcs) is built from this
list.

"""

## ================================================================================

def build_driver_dictionary(module, debug=True ):
    """ Build a dictionary of what each net and input port drives.

    Loops thru the instanciations in the current module and adds each
    bit of the .pin(net) list to the drivers dict depending on the 
    direction of the pin.  For example, if pin is an output it drives
    the net, and it's name is the key to the dict.  Otherwise the net 
    drives the pin, so the net name is the key to the dict.        
    """

    driver_dict = {}

    # Loop thru instanciations in this module
    for inst in module.inst_dict.values():

        # Get the module definition of the instanciated module
        inst_module = inst.module_ref

        # Get the pin:net connections.    
        for pin,net in inst.port_dict.iteritems():
        
            # is 'net' actually a schematic port? if so, rename it
            if net in module.port_dict:

                if module.port_dict[net].direction == 'input':
                    net = ('_iport', net)
                else:
                    net = ('_oport', net) 

            # if it's a net, give it an instance name of '_net' so everything
            # is a tuple now...
            elif type(net) is not tuple:
                net = ('_net', net)


            # Add to driver_dict if inst.pin is an output...
            if inst_module.GetPinDirection( pin ) == 'output':
                driver_name = (inst.name, pin) #'.'.join( [inst.name, pin] )
                driver_dict.setdefault(driver_name, []).append(net)

            # ...
            else:
                sink_name = (inst.name, pin) #'.'.join( [inst.name, pin] )
                driver_dict.setdefault(net, []).append(sink_name)


    if debug:
        print "\nDriver Dictionary"
        for key in driver_dict:
            print "  ",key, "::::", driver_dict[key]

    return driver_dict



def get_connection_list( driver_dict, debug=True):
    """Determine the connections in the current module

    This uses the driver_dict to build a connections list.  The driver_dict will
    contain ((inst,pin),('_net',net)) or (('_net',net),(inst,pin)) and this module 
    builds a connection list in the form ((inst,pin),(inst,pin))
    (where inst can also be input or output ports ('_iport' or '_oport') ).

    """

    point_to_point_connection_list = []

    for driver in driver_dict.keys():
        driver_inst, driver_name = driver # untuple

        driven_things = driver_dict[ driver ]
        for net in driven_things:
            net_inst, net_name = net # untuple

            if  net_inst is '_oport': # Add output port connections
                point_to_point_connection_list.append( (driver,net) )           

            if driver_inst is ('_iport'): # Add input port connections 
                point_to_point_connection_list.append( (driver, net) )

            if net in driver_dict:

                sink_list = driver_dict[net]
                for sink in sink_list:
                    sink_inst, sink_name = sink # untuple

                    point_to_point_connection_list.append( (driver, sink) )


    if debug:
        print "\nPoint-to-Point"
        for connection in point_to_point_connection_list:
            print "   ",connection 

    return point_to_point_connection_list
        
        

def get_graph_dictionary(connection_list, debug=True):
    """Build a graph from the circuit connection list.
    
    Returns a directed graph of the circuit as a dictionary. Keys are vertices,
    values are lists of vertices that they connect to, eg:

    graph = {'A': ['B', 'C'],
             'B': ['C', 'D'],
             'C': ['D'],
             'D': ['C'],
             'E': ['F'],
             'F': ['C']}

    Pins on each instantiation are ignored.  Two additional vesrtices are added,
    '_iport' which connects to input ports, and '_oport' which links output ports.
    
    See: http://www.python.org/doc/essays/graphs.html 
    """
    
    graph_dictionary = {}
    for source,sink in connection_list:
        
        
        # Determine names for vertices
        source_name = source[0]
        if source_name.startswith('_'): # deal with ports
            if source_name is '_iport': # '_iport' drives inputs
                graph_dictionary.setdefault(source[0], []).append(source[1])
            source_name = source[1] 
    
        sink_name = sink[0]
        if sink_name.startswith('_'): # again, deal with ports
            if sink_name is '_oport': # outputs drive '_oport'
                graph_dictionary.setdefault(sink[1], []).append(sink[0]) 
            sink_name = sink[1] 
            
        # Now fill in the dictionary
        graph_dictionary.setdefault(source_name, []).append(sink_name)
        
        
    # remove duplicates
    for key in graph_dictionary.keys():
        graph_dictionary[key] = set( graph_dictionary[key] )
    
    if debug:
        print "\n\n### Graph Dictionary"
        for key in graph_dictionary.keys():
            print "  [%s]: %s" % ( key, graph_dictionary[key] )
            
    return graph_dictionary
    
    
## ================================================================================
##
##
## ================================================================================
    


def yplacement( inst_col_dict, drawing_object_dict, driver_dict ):
    """ Place the instanciations of the current module in the y-axis.

    At the minute, this is pure combinatorial.  Will take ages for big ccts. 
    """

    # Find the number of columns in this design
    num_cols = max( inst_col_dict.values() ) + 1

    # Loop thru the columns, sorting the instantiations in the y-axis as we proceed.
    # Begin at column[2], sort column[1].  Group
    # move to column[3] and sort column[2]
    # Remember, in col_dict, [0] = input ports, and [-1] are output ports
    # when placing the modules I'm only worrying about columns with actual modules
    # in them.
    for i in range(2,len(inst_col_dict)): # jump straight to the 2nd col of instns    

        prev_col_drivers = {}
        # Determine which connections go between col[i] and col[i-1]
        for inst in inst_col_dict[i-1]: # driving modules
                        
            for driver_inst,driver_port in driver_dict.keys():
                if driver_inst == inst:
                     pass
                        

        for col in inst_col_dict.values():

           for other_col in inst_col_dict.values():
                pass


    
