#! /usr/bin/env python
""" Graph Builder.

Take a circuit module and build its Layered Directed Acyclic Graph.
"""
import lib_pnr_debug as libdb # debug prints only...
import sugiyama.layered_graph as graph

DEBUG = True
DEBUG_LAYERING = False

class Graph_Builder:
    """ Extract the DAG of the circuit. """

    def __init__(self):
        self.module = None
        self.connection_list = []
        self.edge_list = []
        self.graph_dict = {}
        self.layer_dict = {}

    def set_module(self, module):
        self.module = module

    def get_graph_for_sugiyama(self):
        """ Construct the graph of the circuit.
        This uses the data structures in the layered_graph module.
        """

        edges = self.extract_graph()
        block_dict = self._build_special_vertices(self.module)

        # flip layer dict so it's indexed by the layer
        layers = self._invert_dict(self.layer_dict)

        # use this layer dict to make the special vertices list of lists
        l = layers.keys()
        l.sort()
        special_vertices = []
        for i in l:
            tmp = []
            for thing in layers[i]:
                tmp.append( block_dict[thing] )
            special_vertices.append(tmp)

        # Now for the edge list. Again, this has to be layered.
        edge_dict = {}
        for conn in self.connection_list:
            ( (source, port1), (sink, port2) ) = conn
            layer = self.layer_dict[source]
            edge_dict.setdefault(layer, []).append(conn)

        layers = edge_dict.keys()
        layers.sort()
        edges = []
        for layer in layers:
            edges.append(edge_dict[layer])

        # Now for the graph
        g = graph.Graph(self.module.name)
        layer = 0
        for vertices in special_vertices:
            for v in vertices:
                g.add_vertex(layer, v)
            layer += 1

        n = 0 # !!!FIXME!!! have to fix net names...
        print "Something"
        for source,target in self.connection_list:
            e = graph.Edge('n%d' %(n), source, target)
            print e
            g.add_edge(e)
            n += 1
        g.update()
        return g

    def extract_graph(self):
        """ Get a graph of the circuit to display.
        """

        # Extract edges from circuit
        driver_dictionary = self._build_driver_dictionary()
        self.connection_list = self._get_connection_list(driver_dictionary)
        self.edge_list = self._get_edge_list(driver_dictionary)

        #  Now we can build the graph since we've the vetices(instantiations) and
        # the edges (circuit point-to-point connections).
        self.graph_dict = self._get_graph_dictionary(self.edge_list)

        # Determine which layer of the schematic the blocks belong on
        self.layer_dict = {}
        self.layer_dict = self._determine_layering(self.graph_dict,
                                                   col_dict=self.layer_dict)

        #  Insert dummy nodes to break up long edges - make the graph 'proper'
        self._split_long_edges()

        # DEBUG
        if DEBUG:
            libdb.show_dictionary("Graph Edges Dictionary", self.graph_dict )
            libdb.show_dictionary("Graph Layer Dictionary", self.layer_dict )
            self.show_connections()

        return self.graph_dict

    def get_layer_dict(self):
        return self.layer_dict

    def get_conn_list(self):
        return self.connection_list

    def show_connections(self, debug=False ):
        if debug:
            print "\nPoint-to-Point"
            for connection in self.connection_list:
                print "   ", connection

    ##
    ## Private stuff
    ##
    def _build_driver_dictionary(self ):
        """ Build a dictionary of what each net and input port drives.

        Loops thru the instanciations in the current module and adds each
        bit of the .pin(net) list to the drivers dict depending on the
        direction of the pin.  For example, if pin is an output it drives
        the net, and it's name is the key to the dict.  Otherwise the net
        drives the pin, so the net name is the key to the dict.
        """

        driver_dict = {}

        # Loop thru instanciations in this module
        for inst in self.module.inst_dict.values():

            # Get the module definition of the instanciated module
            inst_module = inst.module_ref

            # Get the pin:net connections.
            for pin,net in inst.port_dict.iteritems():

                # is 'net' actually a schematic port? if so, rename it
                if net in self.module.port_dict:

                    if self.module.port_dict[net].direction == 'input':
                        net = (net, net)
                    else:
                        net = (net, net)

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

        if DEBUG:
            print "\nDriver Dictionary"
            for key in driver_dict:
                print "  ",key, "::::", driver_dict[key]

        return driver_dict

    def _get_edge_list( self, driver_dict):
        """Determine the edges (aka connections) in the current module
                port = graph.Port(port_name)
        This uses the driver_dict to build an edge list. The driver_dict will
        contain ((inst,pin),('_net',net)) or (('_net',net),(inst,pin)) and this module
        builds an edge list of Edge objects.
        """
        # !!!FIXME!!! floating nets?
        edge_list = []
        oops_id = 1

        for driver in driver_dict.keys():
            driver_inst, driver_name = driver # untuple
            driven_things = driver_dict[ driver ]
            for driven in driven_things:
                driven_inst, driven_name = driven # untuple

                # port connections don't have an intermediate net
                if driven_inst == driven_name or driver_inst == driver_name:
                    net_name = driven_inst
                    edge = graph.Edge( net_name, driver, driven)
                    edge_list.append(edge)

                # if the driven is in the dict itself, then it's an intermediate
                # net, so find the ultimate target of this connection
                sink_list = driver_dict.get(driven, [])
                for sink in sink_list:
                    sink_inst, sink_name = sink # untuple

                    # figure out net name
                    if driven_inst == '_net':
                        net_name = driven_name
                    else:
                        print "Oops, can't determine net name"
                        net_name = 'Broken%0d' % (oops_id)
                        oops_id += 1

                    edge = graph.Edge( net_name, driver, sink)
                    edge_list.append(edge)

        if DEBUG:
            print "\nPoint-to-Point Edge List"
            for edge in edge_list:
                print "   ", edge

        return edge_list

    def _get_connection_list( self, driver_dict):
        """Determine the connections in the current module
                port = graph.Port(port_name)
        This uses the driver_dict to build a connections list.  The driver_dict will
        contain ((inst,pin),('_net',net)) or (('_net',net),(inst,pin)) and this module
        builds a connection list in the form ((inst,pin),(inst,pin))
        """

        point_to_point_connection_list = []

        for driver in driver_dict.keys():
            driver_inst, driver_name = driver # untuple

            driven_things = driver_dict[ driver ]
            for net in driven_things:
                net_inst, net_name = net # untuple

                if net_inst == net_name: # Add output port connections
                    point_to_point_connection_list.append( (driver,net) )

                if driver_inst == driver_name: # Add input port connections
                    point_to_point_connection_list.append( (driver, net) )

                if net in driver_dict:

                    sink_list = driver_dict[net]
                    for sink in sink_list:
                        sink_inst, sink_name = sink # untuple

                        point_to_point_connection_list.append( (driver, sink) )


        if DEBUG:
            print "\nPoint-to-Point"
            for connection in point_to_point_connection_list:
                print "   ",connection

        return point_to_point_connection_list

    def _get_graph_dictionary(self, edge_list):
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
        for edge in edge_list:
            graph_dictionary.setdefault(edge.source, set()).add(edge.target)

        # add origin so the layering has a single point to start from
        graph_dictionary['_origin'] = self.module.GetInputPinNames()

        if DEBUG:
            print "\n\n### Graph Dictionary"
            for key in graph_dictionary.keys():
                print "  [%s]: %s" % ( key, graph_dictionary[key] )

        return graph_dictionary

    def _determine_layering(self, graph, inst='_origin',
                            col_dict = {}, path = [] ):
        """ Layer the graph.

        Find the drivers of the current inst, and set their
        column numbers to one less than the current.

        col_dict[<instn_name>] = <column_number>

        Column[0] = Input ports
        Column[-1] = Output ports

        Look out for loops by doing something magical..."""

        col_num = col_dict.get(inst, 0) + 1
        path.append(inst)

        if DEBUG_LAYERING :
            print ":: Determine Layering"
            print "  Inst:",inst
            print " Graph keys", graph.keys()

        #  Go through the drivers of this sink and update their
        # column numbers if necessary

        if DEBUG_LAYERING : print "Inst:", inst, "; Sinks:", graph.get(inst,[])
        for sink in graph.get(inst,[]):

            if DEBUG_LAYERING : print "SINK:" + sink
            # Loop detection...
            if sink in path :
                if DEBUG_LAYERING : print "Loop!!: ", sink, ":", path
                continue

            # Only update the column count if needed.  If the load
            # is already to the right of this inst, then leave its
            # col number alone.
            if col_num > col_dict.get(sink,0):
                col_dict[sink] = col_num
                col_dict = self._determine_layering( graph, sink, col_dict, path)

        path.pop()

        if DEBUG_LAYERING :
            print '::::: Layering Dictionary'
            for key in col_dict.keys():
                print ("        " * ( col_dict[key] )) + key.center(8)
            print "-" * 80
            print col_dict

        return col_dict

    def _get_layer(self, block):
        layer = self.layer_dict.get(block,0)
        if block == '_iport':
            layer += 1
        elif block == '_oport':
            layer -= 1
        return layer

    def _get_dummy_connections(self, connection):
        """ Build intermediate dummy connections for this long one.
        This also updates:
         * graph dict
         * layer dict
        """
        new_connections = []

        source, sink = connection
        (block1, port1) = source
        (block2, port2) = sink

        start_layer = self._get_layer(block1)
        end_layer   = self._get_layer(block2)

        # Remove sink from source connection set
        self.graph_dict[block1].discard(block2)

        if ( end_layer - start_layer ) > 0:
            prefix = '_U'
            layers = range( start_layer + 1, end_layer )
            loopback = False
            start_point = source
        else:
            prefix = '_B'
            layers = range( end_layer, start_layer+1 )
            loopback = True
            start_point = sink

        for i in layers:
            new_vertex_name = '_'.join([prefix, block1, port1, block2, port2, str(i)] )
            new_conn = ( start_point, (new_vertex_name, '_i') )
            new_connections.append(new_conn)

            (block, port) = start_point
            self.graph_dict.setdefault(block,set()).add(new_vertex_name)
            self.layer_dict[new_vertex_name] = i

            start_point = (new_vertex_name, '_o')

        if loopback:
            new_connections.append( (start_point, source) )
        else:
            new_connections.append( (start_point, sink) )

        self.graph_dict.setdefault(new_vertex_name,set()).add(block2)

        return new_connections

    def _split_long_edges(self):
        """ Split up all edges which span more than one layer. """
        new_connections = []
        for connection in self.connection_list:
            ( (block1, port1), (block2, port2) ) = connection

            start_layer = self._get_layer(block1)
            end_layer   = self._get_layer(block2)
            span = end_layer - start_layer

            if span == 1:
                new_connections.append( connection )
            else: # we've found a long edge..
                print "!Found a long edge:", connection
                dummy_connections = self._get_dummy_connections(connection)
                new_connections.extend( dummy_connections )

        self.connection_list = new_connections

    def _build_special_vertices(self, module):
        """ Build special vertices for layout alg. """

        block_dict = {}

        # add the instantiations
        for inst in module.inst_dict.keys():
            block = graph.Vertex(inst)
            submod = module.inst_dict[inst].module_ref
            for port_name in submod.GetInputPinNames():
                port = submod.port_dict[ port_name ]
                block.add_port( graph.Port(port_name, 'left') )
            for port_name in submod.GetOutputPinNames():
                port = submod.port_dict[ port_name ]
                block.add_port( graph.Port(port_name, 'right') )
            block_dict[inst] = block

        # Add the ports - these are vertices in their own right
        for port_name in module.GetInputPinNames():
            v_in = graph.Vertex(port_name, 'port')
            v_in.add_port( graph.Port(port_name, 'right') )
            block_dict[port_name] = v_in

        for port_name in module.GetOutputPinNames():
            v_out = graph.Vertex(port_name, 'port')
            v_out.add_port( graph.Port(port_name, 'left') )
            block_dict[port_name] = v_out

        # Add the dummy vertices that split long edges
        for vertex in self.layer_dict:
            if vertex.startswith('_U_') or vertex.startswith('_B_'):
                if vertex not in block_dict:
                    dummy = graph.Vertex(vertex, 'dummy')
                    dummy.add_port( graph.Port('_i', 'left') )
                    dummy.add_port( graph.Port('_o', 'right') )
                    block_dict[vertex] = dummy


        return block_dict

    def _invert_dict(self, _dict):
        new_dict = {}
        for key in _dict:
            new_dict.setdefault(_dict[key], []).append(key)
        return new_dict


if __name__ == '__main__':

    import sys
    sys.path.append('../../')
    import pprint
    import pickle

    def load_rtl_module_pickle(module_name):
        """ Load pickled RTL module datastructure. """

        hPICKLE = open('../../tests/module_pickles/' + module_name + '.dat','rb')
        module = pickle.load(hPICKLE)
        pprint.pprint(module)

        hPICKLE.close()
        return module

    try:
        module_name = sys.argv[1]
    except IndexError:
        module_name = 'top'

    module = load_rtl_module_pickle(module_name)
    dag = Graph_Builder()
    dag.set_module(module)
    dag.extract_graph()
    g = dag.get_graph_for_sugiyama()
    print g.display()
    pprint.pprint(g.edges)
