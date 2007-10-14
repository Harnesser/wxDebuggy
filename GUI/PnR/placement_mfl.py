# placement_mfl.py 
#
# Placement of instanciations in the current module view based on the minimisation of flight lines.
#


def columnize( driver_dict, inst, col_dict, load = [], debug = True ):
    """ Find the drivers of the current inst, and set their
    column numbers to one less than the current.

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



def place_instanciations( module, driver_dict, col_dict ):
    """ Place the instanciations of the current module by minimizing the total length of 
    all the connection flight lines.

    At the minute, this is pure combinatorial.  Will take ages for big ccts. 
    """

    for col in col_dict.values():

        for other_col in col_dict.values():
            pass


    
