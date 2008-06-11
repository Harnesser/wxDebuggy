# placement_sugiyama.py 
""" Sugiyama Layout

Place the instanciations of the current module using a scheme based on 
Sugiyama's approach. This algorithm has a few stages:

 1: Remove cycles from graph
 2: Determine the layering of the graph
 3: Replace any edges which cross more than one layer with dummy nodes
 4: Sort the nodes on each layer in a manner to reduce the crossover count
 
"""


def build_graph(module):
    """ Build a graph for the current module to be displayed.
    """
    
    graph = extract_graph(module)
    graph = remove_cycles(graph)
    graph = determine_layering(graph)
    graph = insert_dummy_nodes(graph)
    graph = reduce_crossings(graph)
    
    return graph
    
    
def extract_graph(module):
    """ Get a graph of the circuit to display.
    
    Returns the graph in the form ( [List of Vertices], [List of Edges] ).
    """
    
    driver_dictionary = build_driver_dictionary(module)
    connection_list = get_connection_list(driver_dictionary)
    graph = get_graph_dictionary(connection_list)
    
    
    return graph
    
    
def remove_cycles(graph):
    """ Remove cycles from graph.
    Reverse certain edges to ensure the graph is acyclic.
    """
    
    return acyclic_graph
    
    
def determine_layering(graph):
    """ Layer the graph.
    """
    
    return layered_graph
    
    
def insert_dummy_nodes(graph):
    """ Insert dummy nodes for long edges.
    Produces a 'proper graph'.    
    """
    
    return proper_graph
    
    
def reduce_crossings(graph):
    """ Reduce edge crossings.
    By reordering the nodes in each layer, the number of edge crossings is
    reduced.
    """

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

    Pins on each instantiation are ignored.
    
    See: http://www.python.org/doc/essays/graphs.html 
    """
    
    graph_dictionary = {}
    for source,sink in connection_list:
        
        # Determine names for vertices
        source_name = source[0]
        if source_name.startswith('_'): # deal with ports
            source_name = source[1] 
    
        sink_name = sink[0]
        if sink_name.startswith('_'): # again, deal with ports
            sink_name = sink[1] 
    
        # Now fill in the dictionary
        graph_dictionary.setdefault(source_name, []).append(sink_name)
        
    
    if debug:
        print "\n\n### Graph Dictionary"
        for key in graph_dictionary.keys():
            print "  [%s]: %s" % ( key, graph_dictionary[key] )
            
    return graph_dictionary
    
    
## ================================================================================
##
##
## ================================================================================
    
    
def columnize( driver_dict, inst, col_dict, load = [], debug = True ):
    """ Find the drivers of the current inst, and set their
    column numbers to one less than the current.

    col_dict[<instn_name>] = <column_number>

    Column[0] = Input ports
    Column[-1] = Output ports

    Look out for loops by doing something magical..."""

    col_num = col_dict[inst] + 1
    load.append(inst)

    print "::", inst, driver_dict.keys()

    #  Go through the drivers of this sink and update their
    # column numbers if necessary
    for driver in driver_dict[inst]:

        # Loop dectection...
        if driver in load :
            print "Loop!!: ", driver, ":", load
            continue

        # Only update the column count if needed.  If the load
        # is already to the right of this inst, then leave its
        # col number alone. 
        if col_num > col_dict[driver]:
            col_dict[driver] = col_num
            col_dict = columnize( driver_dict, driver, col_dict, load )

    load.pop()
    
    if debug:
        for key in col_dict.keys():
            print ("        " * ( col_dict[key] )) + key.center(8) 
        print "-" * 80
        print col_dict

    return col_dict



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


    
