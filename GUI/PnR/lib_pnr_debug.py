#! /usr/bin/env python
""" Functions to help debug
"""

def show_dictionary( title, dictionary ):
    """ Prettyprint a dictionary """

    print "\n\n###", title
    for key in dictionary.keys():
        name = dictionary[key]
        print "  %s : %s" % ( str(key).rjust(30), name )




        
        
