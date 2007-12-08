# placement_ga.py 
#
""" Placement of instanciations.

  Instantiations are placed in the x-axis using a recursive algorithm which
sorts out the signal path thru the design to be displayed.
  Y-axis placement is achieved using a Genetic Algorithm, because I couldn't
think of a way of doing it otherwise...

"""

import ga

drawing_object_dict_ref = None
connection_list_ref = None
inst_col_dict_ref = None

drawing_object_name_list = []

# GA parameters
BITS_PER_GENE = 4
    
def columnize( driver_dict, inst, col_dict, load = [], debug = False ):
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
                    #print inst,port,"LHS:", draw_ref.position
                    # X placement. 2*col for inputs, 2*col+1 for inouts and outputs
                    x = inst_col_dict[inst] * 2
                    y = draw_ref.position.y + draw_ref.lhs_ports.index(port)


                elif port in draw_ref.rhs_ports:
                    #print inst,port,"RHS:", draw_ref.position
                    # X placement. 2*col for inputs, 2*col+1 for inouts and outputs
                    x = inst_col_dict[inst] * 2 + 1
                    y = draw_ref.position.y + draw_ref.rhs_ports.index(port)

                else:
                    print "Warning: cannot find %s in the port lists of %s" % ( port, inst )
                     
                #print ":", x,y
            connection_point_coord_list[(inst,port)] = (x,y)
                
    if debug:
        print "Connection Dictionary"
        for a in connection_point_coord_list.keys():
            print "%s ::: %s" % ( a, connection_point_coord_list[a] )
        print "--------------------------------------------"


    find_crossovers( connection_list, connection_point_coord_list )

    return connection_point_coord_list



def find_crossovers( connection_list, connection_point_coord_list, debug=False ):
    """ Find the number of flightline crossovers
    
    Given the current y placements of the instantiations in the module to display,
    calculate how many flightline crossovers there are.
    """

    sum_of_gradients = 0
    
    num_crossovers = 0

    num_connections = len(connection_list)
    for i in range( num_connections ):
        conn1,conn2 = connection_list[i]
        
        flightline1 = ( connection_point_coord_list[conn1],
                        connection_point_coord_list[conn2] )

        sum_of_gradients += abs( gradient( flightline1 ) )

        
        for j in range( i+1, num_connections ): 
            conn3,conn4 = connection_list[j]

            flightline2 = ( connection_point_coord_list[conn3],
                            connection_point_coord_list[conn4] )
            
            if is_crossover( flightline1, flightline2, debug=False ):
                num_crossovers += 1

    if debug:
        print "Crossovers:", num_crossovers

    # normalise the sum of gradients for the fitness function
    p = 3000
    sum_of_gradients = ( 1.0 * (p - sum_of_gradients ) ) / p
    assert sum_of_gradients >= 0
    
    return num_crossovers, sum_of_gradients



def is_crossover( flightline1, flightline2, debug=False ):
    """ Determine if flightlines cross over eachother

    Construct the line eqn for each segment and then find the crossing
    point if one exists.  Then check that this crossing point is on both 
    line segments.

    flightline1 & flightline2 are tuples eg: ( (x1,y1),(x2,y2) )
    I've littered the place with 1.0 to invoke decimal maths
    Line Eqn: y = mx + c
    """
    xc,yc = (None,None)
    crosses = False

    (x1,y1),(x2,y2) = flightline1
    (u1,v1),(u2,v2) = flightline2

    # Gradients of lines
    m1 = gradient(flightline1)
    m2 = gradient(flightline2)

    # Line offsets: c = y - mx
    c1 = y1 - ( m1 * x1 )
    c2 = v1 - ( m2 * u1 )

    if m1 == m2: # lines are parallel, therefore don't cross
        crosses = False
    else:
        # Calc crossover point
        xc = 1.0 * ( c2 - c1 ) / ( m1 - m2 )
        yc = 1.0 * ( c1 * m2 - c2 * m1 ) / ( m2 -m1 )

        # Is it in range?
        if ( xc >= min(x1,x2) and xc <= max(x1,x2) and
             xc >= min(u1,u2) and xc <= max(u1,u2) and
             yc >= min(y1,y2) and yc <= max(y1,y2) and
             yc >= min(v1,v2) and yc <= max(v1,v2)
            ):
            crosses = True


    if debug:
        print "-----------------------------------------------"
        print "Line1", flightline1, " gradient:", m1, " offset:", c1
        print "Line2", flightline2, " gradient:", m2, " offset:", c2
        print "Crossing point", (xc,yc)," - crosses?",crosses


    
    return crosses


def gradient( flightline ):
    """ Find gradient of flightline """

    (x1,y1),(x2,y2)  = flightline

    if x1 < x2:
        gradient = 1.0 * (y2-y1) / (x2-x1)
    else:
        gradient = 1.0 * (y1-y2) / (x1-x2)

    return gradient
    
    

#drawing_object_dict_ref = None
#drawing_object_name_list = None

def layout_fitness_function( soul , display=False):
    """Determine the fitness of the genotype for positioning blocks.
    
    Fitness:
    * Least crossovers
    * No bounding box incursions
    
    """
    CRUNCH_WEIGHTING = 0.0   # how crunched up to 0 on the y-axis?
    XOVER_WEIGHTING = 1.0    # crossover weighting
    GRAD_WEIGHTING  = 2.0
    
    #  Fuck. How do I access the drawing object dictionary from in here?
    # Ugly global variable for this module, that's how.  So check that
    # it has been set
    assert drawing_object_dict_ref is not None
    
    # Set the y-placement of each block, using genes on the genome.
    y_values = set_y_placement( soul )
    
    # Calculate the fitness of the layout, and hence the genome.
    connection_point_coord_list = find_pin_coords(connection_list_ref,
                                                  drawing_object_dict_ref,
                                                  inst_col_dict_ref)
    num_crossovers, sum_of_gradients = find_crossovers( connection_list_ref,
                                                        connection_point_coord_list)

    crossover_fitness = (300.0-num_crossovers)/300
    
    y_pos_fitness = ( 128 - ( 1.0 * sum(y_values)/len(y_values) ) ) / 128
   
    fitness = ( ( y_pos_fitness * CRUNCH_WEIGHTING )  + 
                ( crossover_fitness * XOVER_WEIGHTING ) +
                ( sum_of_gradients * GRAD_WEIGHTING ) 
              )
              
    return fitness
     
    
def set_y_placement( soul, debug=False ):
    """ """
    y_values = []
    
    # Split the genome up into bytes, and 
    index = 0
    if debug:
        print "Genome:"
        print "".join( [ str(a) for a in soul ] )
        
    assert drawing_object_name_list
    for drawing_object_name in drawing_object_name_list:
        
        bits = soul[ index*BITS_PER_GENE : index*BITS_PER_GENE+BITS_PER_GENE ]
        number = int( "".join( [ str(a) for a in bits ] ), 2)
        
        if debug:
            print drawing_object_name
            print "bits", bits
            print "number", number
        
        #print drawing_object_dict_ref[drawing_object_name].position.y
        drawing_object_dict_ref[drawing_object_name].position.y = number
        #print ";;", drawing_object_dict_ref[drawing_object_name].position.y
        index += 1
        y_values.append(number)
        
    return y_values
    
def yplacement( drawing_object_dict, connection_list, inst_col_dict ):
    """ Place the instanciations of the current module in the y-axis.

    At the minute, this is pure combinatorial.  Will take ages for big ccts. 
    """
    global drawing_object_dict_ref
    global inst_col_dict_ref
    global connection_list_ref
    global drawing_object_name_list
    
    # Determine the number of objects to place so that we can set up the GA
    num_drawing_objects = len( drawing_object_dict )
    
    # Set up references to the drawing object dictionary
    drawing_object_dict_ref = drawing_object_dict 
    inst_col_dict_ref = inst_col_dict
    connection_list_ref = connection_list
    
    # A sorted list of block names is needed so that we can assign genes
    # by position to y-axis settings of the blocks.
    drawing_object_name_list = drawing_object_dict.keys()
    drawing_object_name_list.sort()

    # Configure the Genetic Algorithm    
    placement_ga = ga.ga(
        fitness_function = layout_fitness_function, 
        bits_per_gene = BITS_PER_GENE,  # num of bit for y-axis
        num_genes = num_drawing_objects,
        num_generations = 25,
        population_size = 200,
        num_crossovers = 1,
        num_parents = 120,
        mutation_rate = 0.19
        )
        
    #  Run the GA, then choose the fittest member of the DGA population as
    # the final layout values
    best_layout = placement_ga.evolve()
    
    # 
    
    
    return


   
    
