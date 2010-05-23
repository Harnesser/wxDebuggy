#! /usr/bin/env python

import pprint
from numpy import *

## -------------------------------------------------------------------------
##  n-Level Hierarchy and Map
## -------------------------------------------------------------------------
V = [ list('ab') , list('cdef'), list('ghij'), list('klm') ]
E = [  [('a','c'), ('a','d'), ('a','e'), ('a','f'), ('b','c'), ('b','f') ],
       [('c','g'), ('d','h'), ('d','i'), ('d','j'), ('e','g'), ('e','j') ],
       [('g','k'), ('i','k'), ('i','m'), ('j','k'), ('j','l') ]
    ]
    
levels  = len(V)

## -------------------------------------------------------------------------
##  Matrix Realisation of n-Level Hierarchies
## -------------------------------------------------------------------------
M = []
for i in xrange(levels-1):
    m_shape = ( len( V[i] ), len( V[i+1] ) )
    m = zeros( m_shape )
   
    for e in E[i]:
        row = V[i].index( e[0] )
        col = V[i+1].index( e[1] )
        m[row][col] = 1
    
    M.append(m)
    
for i in xrange(levels-1):
    print "M(%0d)" % (i)
    print M[i]
    print 

   
       
      
