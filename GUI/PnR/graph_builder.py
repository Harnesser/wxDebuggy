#! /usr/bin/env python
""" Graph Builder.

Take a circuit module and build its Layered Directed Acyclic Graph.
"""
import lib_pnr_debug as libdb # debug prints only...
from collections import namedtuple

class Graph_Builder:
    """ """
    
    def __init__(self):
        self.module = None
        self.connection_list = []
        self.graph_dict = {}
        self.layer_dict = {}

        self.Block = namedtuple('Block', 'name inputs outputs')

    def set_module(self, module):
        self.module = module
    
    
    def get_graph_for_sugiyama(self):
        """ """
        
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
                if thing == '_oport':
                    continue
                tmp.append( block_dict[thing] )
            special_vertices.append(tmp)

        # Now for the edge list. Again, this has to be layered.
        edge_dict = {}
        for conn in self.connection_list:
            ( (source, port1), (sink, port2) ) = conn
            if source == '_iport':
                layer = 1
            else:
                layer = self.layer_dict[source]
            edge_dict.setdefault(layer, []).append(conn)
        
        layers = edge_dict.keys()
        layers.sort()
        edges = []
        for layer in layers:
            edges.append(edge_dict[layer])

        del special_vertices[-1] # empty list to get rid of
        return special_vertices, edges        
        

    def extract_graph(self, debug=False):
        """ Get a graph of the circuit to display.
        """
                
        # Extract edges from circuit
        driver_dictionary = self._build_driver_dictionary()
        self.connection_list = self._get_connection_list(driver_dictionary)
        
        #  Now we can build the graph since we've the vetices(instantiations) and
        # the edges (circuit point-to-point connections).
        self.graph_dict = self._get_graph_dictionary(self.connection_list)
        
        # Determine which layer of the schematic the blocks belong on
        self.layer_dict = {}
        self.layer_dict = self._determine_layering(self.graph_dict,
                                                   col_dict=self.layer_dict)   
    
        #  Insert dummy nodes to break up long edges - make the graph 'proper'
        self._split_long_edges()
        
        # DEBUG
        if debug:
            libdb.show_dictionary("Graph Edges Dictionary", self.graph_dict )
            libdb.show_dictionary("Graph Layer Dictionary", self.layer_dict )
            self.show_connections(debug)
            
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
    
    def _build_driver_dictionary(self, debug=False ):
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


    def _get_connection_list( self, driver_dict, debug=False):
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


    def _get_graph_dictionary(self, connection_list, debug=False):
        """Build a graph from the circuit connection list.
        
        Returns a directed graph of the circuit as a dictionary. Keys are vertices,
        values are lists of vertices that they connect to, eg:

        graph = {'A': ['B', 'C'],
                 'B': ['C', 'D'],
                 'C': ['D'],
                 'D': ['C'],
                 'E': ['F'],
                 'F': ['C']}

        Pins on each instantiation are ignored.  Two additional vertices are added,
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
    
    
    def _determine_layering(self, graph, inst='_iport', 
                            col_dict = {}, path = [], debug = False ):
        """ Layer the graph.
        
        Find the drivers of the current inst, and set their
        column numbers to one less than the current.

        col_dict[<instn_name>] = <column_number>

        Column[0] = Input ports
        Column[-1] = Output ports

        Look out for loops by doing something magical..."""
        
        col_num = col_dict.get(inst, 0) + 1
        path.append(inst)

        if debug:
            print ":: Determine Layering"
            print "  Inst:",inst
            print " Graph keys", graph.keys()

        #  Go through the drivers of this sink and update their
        # column numbers if necessary

        if debug: print "Inst:", inst, "; Sinks:", graph.get(inst,[])        
        for sink in graph.get(inst,[]):

            if debug: print "SINK:" + sink
            # Loop detection...
            if sink in path :
                if debug: print "Loop!!: ", sink, ":", path
                continue

            # Only update the column count if needed.  If the load
            # is already to the right of this inst, then leave its
            # col number alone. 
            if col_num > col_dict.get(sink,0):
                col_dict[sink] = col_num
                col_dict = self._determine_layering( graph, sink, col_dict, path)
                
        path.pop()
        
        if debug:
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

        start_point = source        
        start_layer = self._get_layer(block1) 
        end_layer   = self._get_layer(block2)
        
        # Remove sink from source connection set
        self.graph_dict[block1].discard(block2) 
        
        for i in range( min(start_layer,end_layer) + 1, max(start_layer,end_layer) ):
            new_vertex_name = '_U_%s_%s_%s_%s_%d' % (block1, port1, block2, port2, i)
            new_conn = ( start_point, (new_vertex_name, '_i') )
            (block, port) = start_point     

            new_connections.append(new_conn)
            self.graph_dict.setdefault(block,set()).add(new_vertex_name)
            self.layer_dict[new_vertex_name] = i
            
            start_point = (new_vertex_name, '_o')
            
        new_connections.append( (start_point, sink) )
        self.graph_dict.setdefault(new_vertex_name,set()).add(block2)
        
        return new_connections
        
           
    def _split_long_edges(self):
        """ Return all the edges which span more than one layer. """
        new_connections = []
        for connection in self.connection_list:
            ( (block1, port1), (block2, port2) ) = connection
                
            start_layer = self._get_layer(block1) 
            end_layer   = self._get_layer(block2)
            span = abs( start_layer - end_layer )
            
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
        for inst in module.inst_dict.keys():
            inputs = []
            outputs = []
            submod = module.inst_dict[inst].module_ref
            for port_name in submod.port_name_list:
                port = submod.port_dict[ port_name ]
                if port.direction == 'input':
                    inputs.append(port.name)
                else:
                    outputs.append(port.name)
            block = self.Block(inst, tuple(inputs), tuple(outputs))
            block_dict[inst] = block
            
        # Add the ports
        for port_name in module.port_name_list:
            block = self.Block( port_name, (port_name,), (port_name,) )
            block_dict[port_name] = block
            
        # Add the dummy_edges
        for vertex in self.layer_dict:
            if vertex.startswith('_U_'):
                if vertex not in block_dict:
                    dummy = self.Block(vertex, ('_i',), ('_o',) )
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
    dag.extract_graph(module)
    dag.show_connections(debug=True)
    V,E = dag.get_graph_for_sugiyama(module)
    pprint.pprint(V)
    pprint.pprint(E)
