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
       
## -------------------------------------------------------------------------
##  The Number of Crossings of n-Level Hierarchies
## -------------------------------------------------------------------------
def calc_k(i,j,k):
    """ Calculate the crossings between an ordered pair of vertex rows. """
    q = len( V[i+1] )
    k_jk = 0
    
    for a in xrange(0,q-1):  # 0 ... q-2
        for b in xrange(a+1, q): # a+1 ... q-1
            k_jk += M[i][j][b] * M[i][k][a]
    
    return k_jk

def calc_layer_crossings(i):
    p = len( V[i] )
    K_M = 0
    
    for j in xrange(0,p-1):
        for k in xrange(j+1,p):
            K_M += calc_k(i, j, k )
    
    return K_M
    
for i in xrange(levels-1):
    print "Layer", i, calc_layer_crossings(i)
    
       
      
