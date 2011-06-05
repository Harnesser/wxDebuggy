#! /usr/bin/env python
from wx import Point
from Drawing_Object import Drawing_Object

DEBUG = False

class Object_Factory:

    def __init__(self):
        self.module = None
        self.drawing_object_dict = {} 
        
    def build_object_dict(self, module, graph_edges_dict):
        """ Take a module data structure and make drawing objects for it. 
        At this point, build only instantiations and ports, we'll leave the
        traces til later.
        """
        self.drawing_object_dict = {} 
        self.module = module
        
        self._build_instn_objects()
        self._build_port_objects()
        self._build_passthru_objects(graph_edges_dict)
        
        return self.drawing_object_dict
        
        
    def _build_instn_objects(self):
        """ Build Drawing_Object()s for each of the instantiations in a module.
        Add them to the drawing object dictionary.
        """
        
        if self.module.inst_dict.values() :
            for iii,inst in enumerate(self.module.inst_dict.values()):
                drawobj = Drawing_Object( name=inst.module_ref.name,
                                           parent=None,
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
                                       parent=None,
                                       label='_here',
                                       obj_type='module')

            self.drawing_object_dict['_Nothing'] = drawobj



    def _build_port_objects(self):
        """ Build Drawing_Object()s for each of the ports in the current module.
        Add them to the drawing object dictionary.
        """

        if self.module.port_name_list:
            for port in self.module.port_dict.values():
                
                if port.direction == 'input':
                    key = '_iport'
                else:
                    key = '_oport'

                # Unitless positions for the meantime
                #x_pos += 2 # inst_col_dict[key]
                drawobj = Drawing_Object( name='port',
                                           parent=None,
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
                  self.module.name + " doesn't seem to have any!"

    
    def _build_passthru_objects(self, graph_edges_dict):
        """Add any passthrus as they are needed.
        These are vertice names in the graph dictionary which are not covered 
        by inst or port names.
        """
        
        passthru_id = 0
        for node in graph_edges_dict.keys():
            if not self.drawing_object_dict.get( node, None ):
                if node == '_iport':
                    continue

                if DEBUG: print "Found a new thang..", node
                drawobj = Drawing_Object( name=node + '_' + str(passthru_id),
                                          parent=None, 
                                          label=node,
                                          obj_type='passthru',
                                        )                

                drawobj.lhs_ports.append( '_i' )
                drawobj.rhs_ports.append( '_o' )
                drawobj.startpt = Point(0,0)
                drawobj.endpt   = Point(20,0)

                self.drawing_object_dict[node] = drawobj

                passthru_id += 1
           

  
