# placement_ga.py 
#
""" Placement of instanciations.

  Instantiations are placed in the x-axis using a recursive algorithm which
sorts out the signal path thru the design to be displayed.
  Y-axis placement is achieved using a Genetic Algorithm, because I couldn't
think of a way of doing it otherwise...

"""


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



def find_pin_coords(connection_list, drawing_object_dict, inst_col_dict, debug=False):
    """ Determine the coordinates of each of the connection points for each net.
    
    The co-ordinates of each net hang-point is, for the purpose of the layout GA,
    is unitless.  For example, if a module's y axis origin is (2,4) then its input
    pins are at (2*2,4+1), (2*2,4+2), ..., (2*2,4+n) where n is the number of input
    pins.  Its outputs are at (2*2+1,4+1), (2*2+1,4+2), ..., (2*2+1,4+m) where m 
    is the number of outputs + inouts.    
    
    The pin y-axis number is determined by the order of their declaration.

    """    

    if drawing_object_dict is None:
        print 'Warning: Call "find_pin_coords" after creating drawing_object_dict'
        
    connection_point_coord_list = {} # conection_point_coord_list[('U3', 'in1')] = (3, 5)

    for connections in connection_list:

        for inst,port in connections:

            # Get a handle on the drawing object
            if inst is '_oport' or inst is '_iport' :
                
                # Port?
                draw_ref = drawing_object_dict[port]
                x = inst_col_dict[inst] * 2
                y = draw_ref.position.y        
                connection_point_coord_list[(inst,port)] = (x,y)

            else:

                # Module?
                draw_ref = drawing_object_dict[inst]
                if draw_ref is None:
                    print "Warning: Cannot find drawing object for inst \"%s\"" % ( inst )

                # go thru the ports and place them.
                if port in draw_ref.lhs_ports:
                    print inst,port,"LHS:", draw_ref.position
                    # X placement. 2*col for inputs, 2*col+1 for inouts and outputs
                    x = inst_col_dict[inst] * 2
                    y = draw_ref.position.y + draw_ref.lhs_ports.index(port)


                elif port in draw_ref.rhs_ports:
                    print inst,port,"RHS:", draw_ref.position
                    # X placement. 2*col for inputs, 2*col+1 for inouts and outputs
                    x = inst_col_dict[inst] * 2 + 1
                    y = draw_ref.position.y + draw_ref.rhs_ports.index(port)

                else:
                    print "Warning: cannot find %s in the port lists of %s" % ( port, inst )
                     
                print ":", x,y
            connection_point_coord_list[(inst,port)] = (x,y)
                
    if debug:
        print "Connection Dictionary"
        for a in connection_point_coord_list.keys():
            print "%s ::: %s" % ( a, connection_point_coord_list[a] )
        print "--------------------------------------------"


    find_crossovers( connection_list, connection_point_coord_list )

    return connection_point_coord_list



def find_crossovers( connection_list, connection_point_coord_list ):
    """ Find the number of flightline crossovers
    
    Given the current y placements of the instantiations in the module to display,
    calculate how many flightline crossovers there are.
    """

    num_crossovers = 0

    num_connections = len(connection_list)
    for i in range( num_connections ):
        for j in range( i+1, num_connections ): 

            conn1,conn2 = connection_list[i]
            conn3,conn4 = connection_list[j]

            flightline1 = ( connection_point_coord_list[conn1],
                            connection_point_coord_list[conn2] )

            flightline2 = ( connection_point_coord_list[conn3],
                            connection_point_coord_list[conn4] )
            
            if is_crossover( flightline1, flightline2, True ):
                num_crossovers += 1

    return num_crossovers



def is_crossover( flightline1, flightline2, debug=False ):
    """ Determine if flightlines cross over eachother
    """
    
    crosses = False


    # First




    if debug:
        print flightline1, gradient(flightline1)
        print flightline2, gradient(flightline2)


    
    return crosses


def gradient( flightline ):
    """ Find gradient of flightline """

    (a,b),(c,d)  = flightline

    if a < c:
        gradient = 1.0 * (b-d) / (c-a)
    else:
        gradient = 1.0 * (d-b) / (a-c)

    return gradient
    

def yplacement( inst_col_dict, drawing_object_dict, driver_dict ):
    """ Place the instanciations of the current module in the y-axis.

    At the minute, this is pure combinatorial.  Will take ages for big ccts. 
    """

   
    
