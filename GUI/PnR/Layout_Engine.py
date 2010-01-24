#! /usr/bin/env python

""" Building a graph from a circuit description.

Edges on a graph are specified as (u,v) where u and v are verticesbul in the graph.
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
import wx
from Drawing_Object import *
import pickle
import graph_builder
import lib_pnr_debug as libdb
import pprint

#import Routing_Engine
#import Ordering_Engine

class Layout_Engine:
    """ Schematic Layout Engine.
    
    This module extracts the graph information from the module to draw
    then delegates to other classes to do the layout."""
    
    def __init__(self, use_pickled_module=False):
        self.module = None    # The Module to draw
        self.use_pickled_module = use_pickled_module
            
        self.graph = None
        self.graph_edges = {}
        self.layer_dict = {}    
        self.connection_list = []
        self.glue_points = {}
        self.drawing_object_dict = {}
        #self.routing_engine = PnR.Routing_Engine()
        #self.ordering_engine = PnR.Ordering_Engine()

        self.layered_connection_dict = {} # key = layer, value = list of hypernet drawing objects
        self.layered_drawing_object_dict = {} # key = layer, value = list of objects
        
	    # Hypernet track dictionary
        self.track_dict = {} # key = layer, values = tracks used. 	
    

        
    def place_and_route(self, module, animate=False, debug=False ):
        """ Place and Route a Module."""
        
        self.module = module # should I type-check?
        
        # Get graph representation of the circuit
        self.graph = graph_builder.Graph_Builder()
        self.graph_edges     = self.graph.extract_graph( self.module )
        self.layer_dict      = self.graph.get_layer_dict()
        self.connection_list = self.graph.get_conn_list()
        
        #  Build a list of the module and port blocks that we have to place
        # Connections will be added later  
        self._build_drawing_object_dict()

        # Update the x-position of the blocks depending on what layer they've
        # been placed on.
        self.glue_points = {}  
        # Layered dictionaries
        self._build_layered_drawing_object_dict()
        self._build_layered_connection_dict()
        self._update_block_x_positions()
        
        # Route
        if animate:
            print "Animating"
            for c_crossovers in self._run_egb_pnr_generator( change_direction = True ):
                print "pnr yielding..."
                yield self._flatten_dicts()
        else :       
            self._run_egb_pnr_algorithm( change_direction=True )
            yield self._flatten_dicts()
         
    def _flatten_dicts(self,debug=False):
        """ """

        # Drawing objects
        drawing_objects = {}
        
        # Add blocks to list
        for layer in self.layered_drawing_object_dict.keys():
            for drawing_obj in self.layered_drawing_object_dict[layer]:
                if debug: print "Block Name:", drawing_obj.label
                drawing_objects[drawing_obj.label] = drawing_obj
                
        # Add hypernets to drawing object_dict...
        for layer in self.layered_connection_dict.keys():
            for drawing_obj in self.layered_connection_dict[layer]:
                if debug: print "Hypernet Name:", drawing_obj.label
                drawing_objects[drawing_obj.label] = drawing_obj
            
        # In full GUI mode, pickle the RTL module for unit testing this Python module
        #if not self.use_pickled_module:
        #    self._pickle_module_for_tests() 
       
        # We're done. The GUI will draw these objects
        return drawing_objects
        
        
    ## =============================================================================
    ##
    ## PRIVATE METHODS
    ##
    ## =============================================================================

    def _update_block_x_positions(self, debug=False):
        """ Update the blocks' x positions dependant on their layering."""
        

        if debug:
            print ":::: Update Block X Positions"
            print 'Layered Drawing Object_Dict Keys\n', self.layered_drawing_object_dict.keys()
            print
        
        for layer in self.layered_drawing_object_dict.keys():
            y_pos = 10
            for drawing_obj in self.layered_drawing_object_dict[layer]:
                position = wx.Point( layer * 200, y_pos )
                drawing_obj.setPosition( position ) 
                y_pos += 50
        
      
    def _update_block_y_positions(self, layer, debug=False):
        """ Update the blocks' y positions depending on their position in the layer list."""
        
        if debug:
            print ":::: Update Block Y Positions, Layer:", layer
            
            print 'Drawing Object_Dict Keys\n', self.drawing_object_dict.keys()
            print '\nLayer Dictionary Keys\n', self.layer_dict.keys()
            print
            
        y_pos = 10
        drawing_objs = self.layered_drawing_object_dict[layer]
        for drawing_obj in drawing_objs:
            if debug: print "--- ", drawing_obj.label
            position = drawing_obj.getPosition()
            if debug: print "---- ", position
            position.y = y_pos
            drawing_obj.setPosition( position )
            if debug: print "---- ", drawing_obj.getPosition()
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
                                       obj_type='module')

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
        passthru_id = 0
        for node in self.graph_edges.keys():
            if not self.drawing_object_dict.get( node, None ):
                if node == '_iport':
                    continue

                if debug: print "Found a new thang..", node
                drawobj = Drawing_Object( name=node + '_' + str(passthru_id),
                                          parent=self,  #hmmm, for flightlines only! FIXME
                                          label=node,
                                          obj_type='passthru',
                                        )                

                drawobj.lhs_ports.append( '_in' )
                drawobj.rhs_ports.append( '_out' )
                drawobj.startpt = wx.Point(0,0)
                drawobj.endpt   = wx.Point(20,0)

                self.drawing_object_dict[node] = drawobj

                passthru_id += 1
           
        if debug:     
            libdb.show_dictionary( "Drawing Object Dictionary",
                                   self.drawing_object_dict )



    def _determine_glue_points(self, debug=False):
        """ Find glue Points for pins on instantiations."""
        
        self.glue_points = {}

        for layer in self.layered_drawing_object_dict.keys():
            for drawing_obj in self.layered_drawing_object_dict[layer]:
                drawing_obj.build_glue_points_dict()
            
                if drawing_obj.obj_type == 'hypernet':
                    print "Woops - shouldn't have hypernets at this stage..."
             
                for pin,position in drawing_obj.glue_points.iteritems():
                    self.glue_points[pin] = position
                
        if debug:
            libdb.show_dictionary( "Glue Point Dictionary",
                                   self.glue_points)
        



    def _assign_hypernet_tracks(self, hypernets, debug=False):
        """ Assign horizontal net segments to tracks.
        
        Based on the ordered list of connections...
        """

        track = 0
        for net in hypernets:
            net.track = track
            net.update_horizontal_position()
            track += 1                
 
 
    def _assign_tracks_in_layer(self, layer, debug=False):
        """ Assign horizontal net segments to tracks.
        
        Based on the ordered list of connections...
        """

        nets = self.layered_connection_dict[layer]
        self._assign_hypernet_tracks( nets, debug )
                   
              
    def _update_hypernets(self, layer, debug=False):
        """ """
       
        #  Keep track on which tracks we're routing the horizontal
        # sections of the nets on.  Forcing each horizontal section
        # to be on a unique track will prevent them from running on 
        # top of each other.  Consult this dictionary before assigning
        # horizontal tracks.
        #  Keys are horizontal routing channel ids, '0' is the channel 
        # between the inputs and the first layer of modules.  The 
        # value is the next available track.
        track_dictionary = {}
        
        if debug : print "Updating hypernets...."
        for hypernet in self.layered_connection_dict[layer]:

            # Track info for horizontal sections
            track = track_dictionary.setdefault( layer, 0 )

            # Get start point
            start_point = self.glue_points[hypernet.start_conn]
            end_point   = self.glue_points[hypernet.end_conn]

            # Midway point - this is the x co-ord for the horizontal section
            hypernet.horizontal_origin = ( ( ( end_point.x - start_point.x ) / 2 ) 
                                           + start_point.x )

            hypernet.hypernet_tree = [ start_point.x, start_point.y, 
                                      0,  # horizontal section position
                                      end_point.y, end_point.x ]
                                      
            hypernet.track = track
            hypernet.update_horizontal_position()
             
            # ...
            track_dictionary[layer] += 1

            if debug:
                print "Hypernet:", hypernet.label
                print "   FROM:", hypernet.start_conn, " TO:", hypernet.end_conn
                print "   X:", start_point.x, end_point.x
                print "   ", hypernet.hypernet_tree
                print "   Layer:", layer

        
    def _get_crossover_count(self, layer, debug=False ):
        """ Crossover count
        Recalculates the hypernet start and stop co-ords.
        """
  
        self._determine_glue_points()
        self._update_hypernets(layer)
        self._optimize_hypernet_tracks( self.layered_connection_dict[layer] )
        c_crossovers = self._count_crossovers_on_layer( layer )
        
        if debug:
            print "New crossover count for layer", layer, " : ", c_crossovers
        return c_crossovers        
        
        
    def _build_layered_connection_dict( self, debug=False ):
        """ First cut routing of the nets.
        
        This works layer by layer.  The space between the layers is
        divided into tracks and only one net section may be on a track.
        """
        self.layered_connection_dict = {}
        
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
            drawobj.track = track
            drawobj.start_conn = start_conn
            drawobj.end_conn = end_conn
            
            # Midway point - this is the x co-ord for the horizontal section
            drawobj.horizontal_origin = ( ( ( end_point.x - start_point.x ) / 2 ) 
                                           + start_point.x )

            drawobj.hypernet_tree = [ start_point.x, start_point.y, 
                                      0,  # horizontal section position
                                      end_point.y, end_point.x ]

            drawobj.update_horizontal_position()
        
           
            # ...
            self.layered_connection_dict.setdefault( layer, [] ).append( drawobj ) 
            net_id += 1
            track_dictionary[layer] += 1

            if debug:
                print "FROM:", start_conn, " TO:", end_conn
                print "   X:", start_point.x, end_point.x
                print "   ", drawobj.hypernet_tree

        
        

    def _get_layer(self, connection_point):
        """ Find out which layer a given connection point is on."""

        inst_name, pin_name = connection_point
        if inst_name is '_iport' or inst_name is '_oport': # it's a port...
            key_value = pin_name
        else: # it's an instance
            key_value = inst_name

        return self.layer_dict[key_value]


    def _reord( self, old_list, _from, _to ):
        """ """
       
        assert _from < len(old_list)
        assert _to   < len(old_list)
        
        list_ = old_list[:]
        mover = list_[_from]#; print list_, mover
        del( list_[_from] )#; print list_
        list_.insert( _to, mover)#; print list_

        return list_
        


    def _minimize_crossovers(self):
        """ """
        
        num_layers = len( self.layered_connection_dict.keys() )
        for layer in range(1,num_layers+1):
            self._assign_horizontal_sections_to_tracks(layer)
            
        
    def _optimize_hypernet_tracks(self, hypernets, debug=False):
        """ Assign the horizontal sections to tracks.

        Greedy assign as described in [Eschbach et al].
        
        First assign each horizontal section to a unique track.  
        Then we see which net will cause the least crossovers on the top track.
        Then we see which of the other nets causes the least crossovers on the 2nd track.
        And so on until all nets are assigned to a track.
        """
    
        c_tracks = len(hypernets)
        layer_list = hypernets[:] # copy it.
        for track_index in range(c_tracks):
        
            min_cost = 10000000 # inf if i could...
            best_net = None
            
            for net_index in range(track_index, c_tracks):
                
                if debug: self._print_hypernets('before', hypernets)
                # Move the net to the track and 
                new_layer_list = self._reord( layer_list, _from=net_index, _to=track_index )
                hypernets = new_layer_list
                self._assign_hypernet_tracks(hypernets)
                if debug: self._print_hypernets('after', hypernets)
                
                # Count the crossovers and keep an eye on the best performers
                crossover_count = self._count_hypernet_crossovers(hypernets)
                if crossover_count < min_cost:
                    min_cost = crossover_count
                    best_net = net_index
                    
                if debug:
                    print "Track:%d, Net:%d, Crossovers:%d" % (track_index,
                                                               net_index, 
                                                               crossover_count)
                    
            # update the net ordered list to the best so far
            layer_list = self._reord( layer_list, _from=best_net, _to=track_index)        
        
        return layer_list
        
    def _print_hypernets( self, title, hypernets ):
        
        print "Hypernet dump", title
        for hypernet in hypernets:
            print "  ", hypernet.label, hypernet.hypernet_tree
            
        
    def _assign_horizontal_sections_to_tracks(self, layer, debug=False):
        """ Assign the horizontal sections to tracks.

        Greedy assign as described in [Eschbach et al].
        
        First assign each horizontal section to a unique track.  
        Then we see which net will cause the least crossovers on the top track.
        Then we see which of the other nets causes the least crossovers on the 2nd track.
        And so on until all nets are assigned to a track.
        """
    
        if debug:
            libdb.show_dictionary( "Layered Connection Dictionary",
                                    self.layered_connection_dict )
        
        self._optimize_hypernet_tracks( self.layered_connection_dict[layer], debug )


    def _run_egb_pnr_algorithm(self, change_direction=False, debug=False):
        """ Call the PnR generator until it's done. """
        
        for c_crossovers in self._run_egb_pnr_generator( change_direction, debug ):
            pass
            
            
    def _run_egb_pnr_generator(self, change_direction=False, debug=False ):
        """ Optimize the placement of the blocks to reduce overall crossovers.
        
                       =-----=     =-----=     =-----= 
              A  o-----+     +-----+     +-----+     +------o  Y
                       =-----=     =-----=     =-----=
                     
        Block index:
                [1]      [2]         [3]         [4]       [5]
        
        Hypernet index
                    [1]        [2]         [3]         [4]         
        """
        
        c_layers = max(self.layered_drawing_object_dict.keys())
        print self.layered_drawing_object_dict.keys()
        c_crossovers_prev = 1000000
        inputs_to_outputs = True

        MAX_TRIES = 30
        c_tries = 0
                
        # First, make sure everything is in place
        for layer in self.layered_drawing_object_dict.keys():
            self._update_block_x_positions()
            self._update_block_y_positions(layer)
            
        if debug: 
            self._print_debug_info()
            pprint.pprint( self.layered_drawing_object_dict )


        # Now optimize - layers start from [1], not [0]
        c_crossovers = self._count_crossovers()
        print "Initial crossover count", c_crossovers
        
        while True:
                       
            if inputs_to_outputs:
                start_ = 2
                end_   = c_layers + 1
                inc_   = 1
                if debug : print "---->  Forwards"
            else:
                start_ = c_layers - 1
                end_   = 0
                inc_   = -1
                if debug : print "<---- Backwards"
                
            # Loop thru all layers except the input pin layer and optimize.
            for layer in xrange( start_, end_, inc_ ):
                print "[]:", self._count_crossovers()
                drawing_objects = self.layered_drawing_object_dict[layer]
                if drawing_objects == None:
                    continue
                    
                if inputs_to_outputs:
                    hypernet_layer = layer - 1
                else :
                    hypernet_layer = layer
                    if hypernet_layer == 0 :
                        hypernet_layer = 1
                                                               
                c_removed = self._optimize_layer( layer,
                                                  hypernet_layer,
                                                  drawing_objects)
                                                  
                c_crossovers -= c_removed
                print "Layer %d: Xovers:%d removed:%d" %( layer, c_crossovers, c_removed )
                print "<>:", self._count_crossovers()
                
                
            # Break if no crossovers
            print c_crossovers, c_crossovers_prev
            if ( c_crossovers == 0 ) or ( c_crossovers_prev == c_crossovers ):
                break
                        
            if change_direction :
                inputs_to_outputs = False
            else:
                inputs_to_outputs = True
                               
            print "Crossovers:", c_crossovers
            c_crossovers_prev = c_crossovers  
            yield c_crossovers
            
        print "Crossovers:", self._count_crossovers()
        yield c_crossovers
        
        
    def _optimize_layer( self, layer, hypernet_layer, 
                               drawing_objects_in_layer, 
                               debug=True):
        """ Optimizes the crossvers in the layer.
        Returns the number of crossovers it removed."""
                              
        c_objects = len(drawing_objects_in_layer)  
        c_removed = 0
        
        # Bail out early if there's nothing to optimize
        c_crossovers_now = self._get_crossover_count( hypernet_layer ) 
        if ( c_objects <= 1 ) or ( c_crossovers_now == 0 ):
            return c_removed
                       
        # Swap each block with its neighbour in turn to see if it reduces crossovers
        for i in xrange( c_objects-1 ): # -1 because ...           
            c_crossovers_before = self._get_crossover_count( hypernet_layer )
            
            self._swap_drawing_object(layer, i) # ... this swaps i with i+1, 
            self._update_block_y_positions(layer)
            
            c_crossovers_after = self._get_crossover_count( hypernet_layer )
            
            if c_crossovers_after > c_crossovers_before:
                self._swap_drawing_object(layer, i) 
                self._update_block_y_positions(layer)
            else :
                c_removed += ( c_crossovers_before - c_crossovers_after ) 
                
            if debug:
                print "Layer %d, object %d - before:%d; after:%d" % ( layer, i,
                    c_crossovers_before, c_crossovers_after)
    
            #if debug: self._print_debug_info()

        return c_removed


    def _print_debug_info(self):
        """ """
        print self._get_debug_info_text()
        
    def _write_debug_info_text(self, directory='./'):
        """ """
        hLOG = open( directory + '/' + self.module.name + '.dat' , 'w')
        hLOG.write( self._get_debug_info_text() )
        hLOG.close()       
        
    def _get_debug_info_text(self):
        """ Make a string of the debug info """
                
        indent = '  '
        text_list = []
        
        
        text_list.append( '-*' * 50 )
        text_list.append( "Drawing Objects" )
        for layer in self.layered_drawing_object_dict.keys():
            text_list.append( ( indent * 2 ) + "Layer %d" % layer )
            for drawing_obj in self.layered_drawing_object_dict[layer]:
                text_list.append( ( indent * 3 ) + "Object '%s'" % drawing_obj.label )
                text_list.append( ( indent * 4 ) + "Position: %s" % drawing_obj.getPosition() )
                for gp in drawing_obj.glue_points.keys():
                    text_list.append( "%s %s %s" % ( ( indent * 4 ),
                                      gp, drawing_obj.glue_points[gp] ) )
                    
        text_list.append( "Hypernets" )
        for layer in self.layered_connection_dict.keys():
            text_list.append( ( indent * 2 ) + "Layer %d" % layer )
            for drawing_obj in self.layered_connection_dict[layer]:
                text_list.append( ( indent * 3 ) + "Hypernet '%s'" % drawing_obj.label )
                
                segment_gen1 = drawing_obj.hypernet_generator()
                coords = []
                for segment1_start, segment1_end in segment_gen1:
                    coords.append( "(%s,%s)" % ( segment1_start, segment1_end ) )
                text_list.append( ( indent * 4 ) + ', '.join(coords) )
                         
                         
        return '\n'.join(text_list)                                                       
                                
                                         
    def _swap_drawing_object( self, layer, drawing_obj_index, debug=False):
        """ Swap a drawing object with it's neighbour. """
        
        drawing_objects = self.layered_drawing_object_dict[layer] # really an alias...
        if len(drawing_objects) <= 1:
            return # no point in doing this...
            
        tmp_drawing_obj_1 = drawing_objects[drawing_obj_index]
        
        if debug:
            _list = []
            for drawing_obj in drawing_objects:
                _list.append( drawing_obj.label )
            print 'Before: ' + ','.join(_list)
            
        # Do the swap
        drawing_objects[drawing_obj_index] = drawing_objects[drawing_obj_index+1]
        drawing_objects[drawing_obj_index+1] = tmp_drawing_obj_1
        
        if debug:
            _list = []
            for drawing_obj in drawing_objects:
                _list.append( drawing_obj.label )
            print 'After: ' + ','.join(_list)
            
           
            
    def _count_crossovers(self):
        """ Count the crossovers in the diagram.
        """

        total_crossovers = 0
        num_layers = max(self.layered_drawing_object_dict.keys())

        for layer in range(0,num_layers) :
            total_crossovers += self._count_crossovers_on_layer(layer)

        return total_crossovers
        

    def _count_hypernet_crossovers(self, hypernets, debug=False):
        """ Count crossovers between hypernets

        """

        c_crossovers = 0
        
        c_hypernets = len(hypernets)
        if debug:
            print "================================================================"
            print c_hypernets, " hypernets on layer"


        for i in range( c_hypernets-1 ):
            drawobj1 = hypernets[i]
            if not drawobj1: 
                continue

            segment_gen1 = drawobj1.hypernet_generator()

            for segment1_start, segment1_end in segment_gen1:
    
                for j in range(i+1,c_hypernets):
                    drawobj2 = hypernets[j]
                    if not drawobj2: continue
                    if drawobj1 == drawobj2: continue

                    segment_gen2 = drawobj2.hypernet_generator()
                        
                    for segment2_start, segment2_end in segment_gen2:
                        if self._lines_cross( segment1_start, segment1_end,
                                              segment2_start, segment2_end ):
                            c_crossovers += 1

        return c_crossovers
        

    def _count_crossovers_on_layer(self, layer=None, debug=False):
        """ Count crossovers between layer x and x+1.

        """

        hypernets = self.layered_connection_dict.get(layer,[])
        crossover_count = self._count_hypernet_crossovers( hypernets, debug )
        
        return crossover_count


    def _lines_cross(self, line1_start, line1_end, line2_start, line2_end, debug = False ):
        """ Determine if flightlines cross over eachother

        Construct the line eqn for each segment and then find the crossing
        point if one exists.  Then check that this crossing point is on both 
        line segments.

        """
        x1,y1 = line1_start
        x2,y2 = line1_end
        x3,y3 = line2_start
        x4,y4 = line2_end
     
        if self._overlaps(x1,x2,x3,x4) and self._overlaps(y1,y2,y3,y4):
            return True
        else:
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


    def _build_layered_drawing_object_dict(self, debug=False):
        """ Layered Drawing Object Dictionary.

        Hypernets are *not* included...
        
        key = layer
        value = ordered list of drawing objects, ordered by y-position
        """

        self.layered_drawing_object_dict = {}

        for drawobj in self.drawing_object_dict.values():
    
            if drawobj.is_hypernet(): # skip hypernets
                continue

            layer = self.layer_dict[ drawobj.label ]
            drawobj.layer = layer
            self.layered_drawing_object_dict.setdefault(layer, []).append(drawobj)    
    
        if debug:
            print "Layered Drawing Object Dictionary"
            for layer in self.layered_drawing_object_dict.keys():
                print "Layer: ", layer
                for drawing_obj in self.layered_drawing_object_dict[layer]:
                    print "    ", drawing_obj.label
                    
        
    def _pickle_module_for_tests(self):
        """ Pickle an RTL module data structure for unittesting this module. 
        
        Only executed in full GUI mode.
        """       
        
        filename = self.module.name + '.dat'
        hPICKLE = open('./tests/module_pickles/' + filename,'wb')
        pickle.dump( self.module, hPICKLE )
        hPICKLE.close()
        print 'Pickling: "%s"' % filename

        
        
    
    ###
    ### Methods for Unit Tests
    ###
    def get_number_of_layers(self):
        """ Return the number of layers in the layout. """
        return( len( self.layered_drawing_object_dict.keys() ) )
        
    def get_blocks_per_layer(self,layer):
        """ Return a list of blocks in the given layer """
        return len( self.layered_drawing_object_dict[layer] )
                    
    def get_hypernets_per_layer(self, layer):
        """ Return the nets in the given layer. """
        return len( self.layered_connection_dict[layer] )
        
        

        
if __name__ == '__main__':

    import sys
    sys.path.append('../../')
    import pprint
    
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
    eng = Layout_Engine( use_pickled_module=True )
    for stuff in eng.place_and_route(module):
        pass
    
    eng._write_debug_info_text()    
    print eng._get_debug_info_text()
    print '\n\n' + ( '=8' * 30 )
    print '  Module "%s"' % module_name
    print '  * Crossovers: %d' % eng._count_crossovers()
    print ( '=8' * 30 )

    
