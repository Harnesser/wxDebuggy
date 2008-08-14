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
        self.graph_edges = None

        self.glue_points = {}
        self.drawing_object_dict = {}
        #self.routing_engine = PnR.Routing_Engine()
        #self.ordering_engine = PnR.Ordering_Engine()

        self.layered_connection_dict = {}
        self.layered_drawing_object_dict = {} # key = layer, value = list of objects
	    # Hypernet track dictionary
        self.track_dict = {} # key = layer, values = tracks used. 	

        
    def place_and_route(self, module ):
        """ Place and Route a Module."""
        
        self.module = module # should I type-check?
        self.graph_edges = self._extract_graph()
                
        # Determine which layer of the schematic the blocks belong on
        self.layer_dict = {}
        self.layer_dict = self._determine_layering(self.graph_edges,
                                                   col_dict=self.layer_dict)   
    
        #  Insert dummy nodes to break up long edges -
        # this makes the graph 'proper'
        self._break_up_long_edges()

        #  Build a list of the module and port blocks that we have to place
        # Connections will be added later  
        self._build_drawing_object_dict()


        # Update the x-position of the blocks depending on what layer they've
        # been placed on.
        self._update_block_x_positions()
        
        # Route
        self._route_connections()

        # Layered ditionaries
        self._build_layered_connection_dict()
        self._build_layered_drawing_object_dict()
        
        # Crossover count...
        self._count_crossovers()

        return self.drawing_object_dict
        
    ## =============================================================================
    ##
    ## PRIVATE METHODS
    ##
    ## =============================================================================
    
    def _extract_graph(self, debug=False):
        """ Get a graph of the circuit to display.
        """
        
        driver_dictionary = self._build_driver_dictionary(self.module)
        self.connection_list = self._get_connection_list(driver_dictionary)
        graph_edges = self._get_graph_dictionary(self.connection_list)
        
        if debug:
            print ":::: Graph Edges"
            print graph_edges
            
        return graph_edges
    
    
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


    def _show_connections(self, debug=True ):

        if debug:
            print "\nPoint-to-Point"
            for connection in self.connection_list:
                print "   ",connection 


            
            

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
        
        
        
    def _update_block_x_positions(self, debug=False):
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


        
    def _build_drawing_object_dict( self, debug=False):
        """ Build the list of objects to display on the screen.

        Add the instance modules and ports."""
        
        
        self.drawing_object_dict = {} 
   
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
                self.drawing_object_dict[inst.name] = drawobj
                
        else:
            # a wee fake thingy for modules with no sub modules
            drawobj = Drawing_Object( name='_Nothing_',
                                       parent=self, #hmmm, for flightlines only! FIXME
                                       label='_here',
                                       obj_type='moddule')

            self.drawing_object_dict['_Nothing'] = drawobj


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
                self.drawing_object_dict[port.GetLabelStr()] = drawobj

        else:
            print "Woops, modules should have ports, " + \
                  self.module.name + " doesn't seem to have ones!"


        #  Add any passthrus as they are needed.  These are vertice
        # names in the graph dictionary which are not covered by
        # inst or port names.
        for node in self.graph_edges.keys():
            if not self.drawing_object_dict.get( node, None ):
                if node == '_iport':
                    continue

                if debug: print "Found a new thang..", node
                
                drawobj = Drawing_Object( name=node,
                                          parent=self,  #hmmm, for flightlines only! FIXME
                                          label=node,
                                          obj_type='passthru',
                                        )                

                drawobj.lhs_ports.append( '_in' )
                drawobj.rhs_ports.append( '_out' )
                drawobj.startpt = wx.Point(0,0)
                drawobj.endpt   = wx.Point(20,0)

                self.drawing_object_dict[node] = drawobj


        self._show_dictionary( "Drawing Object Dictionary",
                               self.drawing_object_dict,
                               debug)



    def _determine_glue_points(self, debug=True):
        """ Find glue Points for pins on instantiations."""
        
        self.glue_points = {}

        for part in self.drawing_object_dict.values():
            part.build_glue_points_dict()
            
            if part.obj_type == 'hypernet':
                print "Woops - shouldn't have hypernets at this stage..."
             
            for pin,position in part.glue_points.iteritems():
                self.glue_points[pin] = position
                
        self._show_dictionary( "Glue Point Dictionary",
                               self.glue_points,
                               debug)
        


    def _break_up_long_edges(self, debug=False):
        """ Insert dummy nodes for long edges.
        Produces a 'proper graph'.    
        """
        
        # turn the layer graph inside out so that layer numbers are the keys.
        graph_layers = {}
        for key in self.layer_dict.keys():
            graph_layers.setdefault( self.layer_dict[key], []).append(key)     

        
        # Dummy nodes are placed in long edges (span >1)
        edges_for_removal = []
        for u in self.graph_edges.keys():
            for v in self.graph_edges[u]:
                start_layer = self.layer_dict.get(v,0) 
                end_layer   = self.layer_dict.get(u,0) 
                span = abs( start_layer - end_layer )
                
                if span > 1: # we've found a long edge..
                    print "!Found a long edge: (%s,%s)" % (u,v)   
                    edges_for_removal.append( (u,v) )
                
        # Delete edges - can't delete items from lists when iterating over them
        for u,v in edges_for_removal:
            start_layer = self.layer_dict.get(v,0) 
            end_layer   = self.layer_dict.get(u,0)        

            start_vertice = u
            for i in range( min(start_layer,end_layer) + 1, max(start_layer,end_layer) ):
                new_vertice_name = '_' + u + '__to__' + v + '_' + str(i)
                graph_layers[i].append(new_vertice_name)
                self.graph_edges.setdefault(start_vertice,set()).add(new_vertice_name)
                self.layer_dict[new_vertice_name] = i

            self.graph_edges.setdefault(new_vertice_name,set()).add(v)
                    


        ## Now fix the connection list
        connections_for_removal = []
        new_connection_list = []
        for connection  in self.connection_list:
            (start_inst,start_port),(end_inst,end_port) = connection

            if start_inst.startswith('_'):
                start_layer = self.layer_dict[start_port]
                start_place = start_port
            else:
                start_layer = self.layer_dict[start_inst] 
                start_place = start_inst


            if end_inst.startswith('_'):
                end_layer   = self.layer_dict[end_port]        
                end_place   = end_port
            else:
                end_layer   = self.layer_dict[end_inst] 
                end_place   = end_inst

            span = abs( start_layer - end_layer )
            
            if span > 1: # we've found a long edge..
                print "!Found a long edge connection: ", connection
                connections_for_removal.append( connection )
            else: 
                new_connection_list.append( connection )
        

        for connection in connections_for_removal:
            (start_inst,start_port),(end_inst,end_port) = connection
           
            if start_inst.startswith('_'):
                start_layer = self.layer_dict[start_port]
                start_place = start_port
            else:
                start_layer = self.layer_dict[start_inst] 
                start_place = start_inst


            if end_inst.startswith('_'):
                end_layer   = self.layer_dict[end_port]        
                end_place   = end_port
            else:
                end_layer   = self.layer_dict[end_inst] 
                end_place   = end_inst

            start_vertice = start_inst
            start_edge = start_port

            print "Start place:", start_place
            print "End place:", end_place

            for i in range( min(start_layer,end_layer) + 1, max(start_layer,end_layer) ):
                new_vertice_name = '_' + start_place + '__to__' + end_place + '_' + str(i)
                new_connection = ( ( start_vertice, start_edge ), 
                                   ( new_vertice_name, '_in' ) )

                new_connection_list.append( new_connection )

                # update for the next go...
                start_vertice = new_vertice_name
                start_edge    = '_out'
                

            new_connection = ( ( start_vertice, start_edge ), 
                               ( end_inst, end_port) )
            new_connection_list.append( new_connection )

        self.connection_list = new_connection_list
        self._show_connections()
         
                      
        # DEBUG
        self._show_dictionary( "Graph Edges Dictionary",
                               self.graph_edges,
                               debug )

        self._show_dictionary( "Graph Layers Dictionary",
                               graph_layers,
                               debug )


        return True
        


    def _route_connections( self, debug=False ):
        """ First cut routing of the nets.
        
        This works layer by layer.  The space between the layers is
        divided into tracks and only one net section may be on a track.
        """
        
        self._determine_glue_points()
        
        #  Keep track on which tracks we're routing the horizontal
        # sections of the nets on.  Forcing each horizontal section
        # to be on a unique track will prevent them from running on 
        # top of each other.  Consult this dictionary before assigning
        # horizontal tracks.
        #  Keys are horizontal routing channel ids, '0' is the channel 
        # between the inputs and the first layer of modules.  The 
        # value is the next available track.
        track_dictionary = {}

        # hypernet_list = []
        net_id = 0
        
        for start_conn, end_conn in self.connection_list:

            # Track info for horizontal sections
            layer = self._get_layer( start_conn )
            track = track_dictionary.setdefault( layer, 0 )

            netname = 'hypernet_'+str(net_id)

            # Get start point
            start_point = self.glue_points[start_conn]
            end_point   = self.glue_points[end_conn]
            
            # Prepare drawing object
            drawobj = Drawing_Object(name=netname,
                                     parent=self,
                                     label=netname,
                                     obj_type='hypernet')            
         
            drawobj.layer = layer       
            drawobj.hypernet_tree = [ start_point.x, start_point.y ]   
         
            # Midway point - this is the x co-ord for the horizontal section
            mid_x = ( ( ( end_point.x - start_point.x ) / 2 ) + start_point.x )
            mid_x += track * 5
            drawobj.hypernet_tree.append( mid_x )

            # End point
            drawobj.hypernet_tree.extend( [ end_point.y, end_point.x ] )
        
           
            # ...
            self.drawing_object_dict[netname] = drawobj  
            net_id += 1
            track_dictionary[layer] += 1

            if debug:
                print "FROM:", start_conn, " TO:", end_conn
                print "   X:", start_point.x, mid_x, end_point.x
                print "   ", drawobj.hypernet_tree

        
        

    def _get_layer(self, connection_point):
        """ Find out which layer a given connection point is on."""

        inst_name, pin_name = connection_point
        if inst_name is '_iport' or inst_name is '_oport': # it's a port...
            key_value = pin_name
        else: # it's an instance
            key_value = inst_name

        return self.layer_dict[key_value]


    def _count_crossovers(self):
        """ Count the crossovers in the diagram.
        """

        total_crossovers = 0
        num_layers = max(self.layered_drawing_object_dict.keys())

        for layer in range(0,num_layers ) :
            total_crossovers += self._count_crossovers_on_layer(layer)

        print "Crossovers:", total_crossovers


    def _count_crossovers_on_layer(self, layer=None, debug=True):
        """ Count crossovers between layer x and x+1.

        """

        crossover_count = 0

        drawobj_list = self.layered_connection_dict.get(layer,[])
        num_draw_objs = len(drawobj_list)
        if debug:
            print "================================================================"
            print len(drawobj_list), " nets on layer", layer


        for i in range( num_draw_objs-1 ):
            drawobj1 = drawobj_list[i]
            if not drawobj1: continue

            segment_gen1 = drawobj1.hypernet_generator()

            for segment1_start, segment1_end in segment_gen1:
    
                for j in range(i+1,num_draw_objs):
                    drawobj2 = drawobj_list[j]
                    if not drawobj2: continue
                    if drawobj1 == drawobj2: continue

                    segment_gen2 = drawobj2.hypernet_generator()

                    for segment2_start, segment2_end in segment_gen2:
                        if self._lines_cross( segment1_start, segment1_end,
                                              segment2_start, segment2_end ):
                            crossover_count += 1

        return crossover_count


    def _lines_cross(self, line1_start, line1_end, line2_start, line2_end, debug = True ):
        """ Determine if flightlines cross over eachother

        Construct the line eqn for each segment and then find the crossing
        point if one exists.  Then check that this crossing point is on both 
        line segments.

        """
        x1,y1 = line1_start
        x2,y2 = line1_end
        x3,y3 = line2_start
        x4,y4 = line2_end
        
        print line1_start, line1_end, line2_start, line2_end


#        if x1 == x2:
#            line1_direction = 'horizontal'
#        else:
#            line1_direction = 'vertical'

#        if x3 == x4:
#            line2_direction = 'horizontal'
#        else:
#            line2_direction = 'vertical'


#       if line1_direction == 'horizontal' and line2_direction == 'horizontal':
#            return self._overlaps(x1,x2,x3,x4)
#        elif line1_direction == 'vertical' and line2_direction == 'vertical':
#            return self._overlaps(y1,y2,y3,y4)          


        if self._overlaps(x1,x2,x3,x4) and self._overlaps(y1,y2,y3,y4):
            print " !!!!!!!!!! !!!!!! !!!!!! overlaps"
            return True
        else:
            print " don't cross"
            return False
            

    def _overlaps(self, y1,y2,y3,y4 ):
        
        ymax = max( y3, y4 )
        ymin = min( y3, y4 )

        if( ( (y1 >= ymin) and (y1 <= ymax) )
            or
            ( (y2 >= ymin) and (y2 <= ymax) )
          ):
            return True
        

        ymax = max( y1, y2 )
        ymin = min( y1, y2 )      
  
        if( ( (y3 >= ymin) and (y3 <= ymax) )
            or
            ( (y4 >= ymin) and (y4 <= ymax) )
          ):
            return True
        
        return False


    def _build_layered_connection_dict(self, debug=False):
        """ Layered Connection Dictionary.

        key = layer
        value = ordered list of connections, ordered by track.
        """

        self.layered_connection_dict = {}
        for drawobj in self.drawing_object_dict.values():

            if not drawobj.is_hypernet():
                continue

            self.layered_connection_dict.setdefault(drawobj.layer, []).append(drawobj)

        self._show_dictionary( "Layered Connection Dictionary",
                               self.layered_connection_dict,
                               debug )


    def _build_layered_drawing_object_dict(self, debug=False):
        """ Layered Drawing Object Dictionary.

        key = layer
        value = ordered list of drawing objects, ordered by y-position
        """

        self.layered_drawing_object_dict = {}

        for drawobj in self.drawing_object_dict.values():
    
            if drawobj.is_hypernet():
                continue

            layer = self.layer_dict[ drawobj.label ]
            drawobj.layer = layer
            self.layered_drawing_object_dict.setdefault(layer, []).append(drawobj)    
    
        self._show_dictionary( "Layered Drawing Object Dictionary",
                               self.layered_drawing_object_dict,
                               debug )
        



    def _show_dictionary(self, title, dictionary, debug=True ):
        """ Prettyprint a dictionary """

        if debug:
            print "\n\n###", title
            for key in dictionary.keys():
                name = dictionary[key]
                print "  %s : %s" % ( str(key).rjust(30), name )


