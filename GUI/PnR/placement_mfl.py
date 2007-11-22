# placement_mfl.py 
#
# Placement of instanciations in the current module view based on the minimisation of flight lines.
#


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


    
