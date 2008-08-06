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

# Love is all you need! #

# ... and these modules...
#import Routing_Engine
#import Ordering_Engine
import wx
from Drawing_Object import *

class Layout_Engine:
    """ Schematic Layout Engine.
    
    This module extracts the graph information from the module to draw
    then delegates to other classes to do the layout."""
    
    def __init__(self):
        self.module = None    # The Module to draw
        
        self.driver_dictionary = None   #keys = drivers, values = nets/ports driven
        self.connection_list = None
        self.layer_dict = None       
        
        self.glue_points = {}
        self.drawing_object_dict = {}
        #self.routing_engine = PnR.Routing_Engine()
        #self.ordering_engine = PnR.Ordering_Engine()

        
    def place_and_route(self, module ):
        """ Place and Route a Module."""
        
        self.module = module # should I type-check?
        self.graph_edges = self._extract_graph()
        
        #  Build a list of the module and port blocks that we have to place
        # Connections will be added later  
        self.drawing_object_dict = self._build_drawing_object_dict()
        
        # Determine which layer of the schematic the blocks belong on
        self.layer_dict = self._determine_layering(self.graph_edges)       
        
        # Update the x-position of the blocks depending on what layer they've
        # been placed on.
        self._update_block_x_positions()
        
        # Route
        self._route_connections()
        
        return self.drawing_object_dict
        
    ## =============================================================================
    ##
    ## PRIVATE METHODS
    ##
    ## =============================================================================
    
    def _extract_graph(self, debug=True):
        """ Get a graph of the circuit to display.
        
        Returns the graph in the form ( [List of Vertices], [List of Edges] ).
        """
        
        driver_dictionary = self._build_driver_dictionary(self.module)
        self.connection_list = self._get_connection_list(driver_dictionary)
        graph_edges = self._get_graph_dictionary(self.connection_list)
        
        if debug:
            print ":::: Graph Edges"
            print graph_edges
            
        return graph_edges
    
    
    def _build_driver_dictionary(self, debug=True ):
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



    def _get_connection_list( self, driver_dict, debug=True):
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
            
            

    def _get_graph_dictionary(self, connection_list, debug=True):
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
    
    
    def _determine_layering(self, graph, inst='_iport', col_dict = {}, path = [], debug = False ):
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
        
        
        
    def _update_block_x_positions(self, debug=True):
        """ Update the blocks' x positions dependant on their layering."""
        
        y_pos = 10
        if debug:
            print ":::: Update Block Positions"
            
            print 'Drawing Object_Dict Keys\n', self.drawing_object_dict.keys()
            print '\nLayer Dictionary Keys\n', self.layer_dict.keys()
            print
            
        for name in self.drawing_object_dict.keys():
            drawing_obj = self.drawing_object_dict[name]
            position = wx.Point( self.layer_dict[name] * 200, y_pos )
            
            drawing_obj.setPosition( position ) 
            y_pos += 50
        
       
    def _old_place_and_route(self):
        """A simple (useless) place and route."""
        
        # Sort out the y-positions of the modules in each column
        # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        #placement.find_pin_coords( self.connection_list, drawing_object_dict, inst_col_dict, True )
 #       placement.yplacement(
 #           drawing_object_dict,
 #           self.connection_list,
 #           inst_col_dict
 #           )

        # Re-Scale the drawing positions of the objects to draw
        # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        for draw_obj in self.drawing_object_dict.values():

            if draw_obj.obj_type is 'module':
                x_pos = ( 150 * draw_obj.position.x )
                y_pos = ( draw_obj.position.y ) * 50
            elif  draw_obj.obj_type is 'port':
                x_pos = 50 + ( 150 * draw_obj.position.x )
                y_pos = ( draw_obj.position.y ) * 50       

            draw_obj.setPosition( wx.Point( x_pos, y_pos ) )
            draw_obj._update_sizes()


        
    def _build_drawing_object_dict( self ):
        """ Build the list of objects to display on the screen.

        Add the instance modules and ports."""
        
        
        drawing_object_dict = {} 
   
        # Add module instanciations to the list
        # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        if self.module.inst_dict.values() :
            for iii,inst in enumerate(self.module.inst_dict.values()):

                drawobj = Drawing_Object( name=inst.module_ref.name,
                                           parent=self,  #hmmm, for flightlines only! FIXME
                                           label=inst.name,
                                           obj_type='module',
                                        )

                submod = inst.module_ref
                for port_name in submod.port_name_list:
                    port = submod.port_dict[ port_name ] # This preserves port ordering
                    if port.direction == 'input':
                        drawobj.lhs_ports.append( port.GetLabelStr() )
                    else:
                        drawobj.rhs_ports.append( port.GetLabelStr() )

                
                # Add to drawing object dict
                drawing_object_dict[inst.name] = drawobj
                
        else:
            # a wee fake thingy for modules with no sub modules
            drawobj = Drawing_Object( name='_Nothing_',
                                       parent=self, #hmmm, for flightlines only! FIXME
                                       label='_here',
                                       obj_type='moddule')

            drawing_object_dict['_Nothing'] = drawobj


        # Add the port instances
        # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        if self.module.port_name_list:
            for port in self.module.port_dict.values():
                
                if port.direction == 'input':
                    key = '_iport'
                else:
                    key = '_oport'

                # Unitless positions for the meantime
                #x_pos += 2 # inst_col_dict[key]
                drawobj = Drawing_Object( name='port',
                                           parent=self, #hmmm
                                           label=port.GetLabelStr(),
                                           obj_type='port' )

                #print port.direction
                if port.direction == 'output':
                    drawobj.mirror = True

                drawobj._update_sizes()

                # Add to drawing object dict
                drawing_object_dict[port.GetLabelStr()] = drawobj

        else:
            print "Woops, modules should have ports, " + \
                  self.module.name + " doesn't seem to have ones!"

        return drawing_object_dict



    def _determine_glue_points(self):
        """ Find glue Points for pins on instantiations."""
        
        for part in self.drawing_object_dict.values():
            part.build_glue_points_dict()
            
            if part.obj_type == 'hypernet':
                print "Woops - shouldn't have hypernets at this stage..."
             
            for pin,position in part.glue_points.iteritems():
                self.glue_points[pin] = position
                
        self._show_glue_point_dict()
        

    def _show_glue_point_dict(self):
        """ A debug thing """

        print "\n\n### Glue Point Dictionary"
        for key in self.glue_points.keys():
            print "  [%s]: %s" % ( key, self.glue_points[key] )


    def _route_connections( self ):
        """ First cut routing of the nets.
        
        This works layer by layer.  The space between the layers is
        divided into tracks and only one net section may be on a track.
        """
        
        self._determine_glue_points()
        
        #hypernet_list = []
        net_id = 0
        
        for start_net,end_net in self.connection_list:
        
            netname = 'hypernet_'+str(net_id)
            # Get start point
            start_point = self.glue_points[start_net]
            end_point   = self.glue_points[end_net]
            
            # Prepare drawing object
            drawobj = Drawing_Object(name=netname,
                                     parent=self,
                                     label=netname,
                                     obj_type='hypernet')            
                
            drawobj.hypernet_tree = [ start_point.x, start_point.y ]            
            mid_x = ( ( ( end_point.x - start_point.x ) / 2 ) + start_point.x )
            drawobj.hypernet_tree.extend( [ mid_x, end_point.y, end_point.x ] )
        
            #hypernet_list.append( drawobj )    
            
            self.drawing_object_dict[netname] = drawobj  
            net_id += 1
            
        #return hypernet_list
        
        
        
        
    
