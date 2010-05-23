#! /usr/bin/env python

import pprint
from numpy import *

## -------------------------------------------------------------------------
##  A: n-Level Hierarchy and Map
## -------------------------------------------------------------------------
V = [ list('ab') , list('cdef'), list('ghij'), list('klm') ]
E = [  [('a','c'), ('a','d'), ('a','e'), ('a','f'), ('b','c'), ('b','f') ],
       [('c','g'), ('d','h'), ('d','i'), ('d','j'), ('e','g'), ('e','j') ],
       [('g','k'), ('i','k'), ('i','m'), ('j','k'), ('j','l') ]
    ]
    
levels  = len(V)


## -------------------------------------------------------------------------
##  B: Matrix Realisation of n-Level Hierarchies
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
##  C: The Number of Crossings of n-Level Hierarchies
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
    
def calc_crossings():
    crossings = 0
    for i in xrange(levels-1):
        crossings += calc_layer_crossings(i)
    return crossings
            
for i in xrange(levels-1):
    print "Layer", i, calc_layer_crossings(i)
print "Total Crossings:", calc_crossings()


## -------------------------------------------------------------------------
##  D: Connectivity
## -------------------------------------------------------------------------
def calc_upper_connectivity( i, k ):
    lim = len( V[i-1] )
    C_U = 0
    
    for j in xrange(0, lim ):
        C_U += M[i-1][j][k]
        
    return C_U


def calc_lower_connectivity( i, k ):
    lim = len( V[i+1] )
    C_L = 0
    
    for l in xrange(0, lim ):
        C_L += M[i][k][l]
        
    return C_L

print "Upper connectivities:"
for i in xrange(1,levels):
    for k in xrange( len( V[i] ) ): 
        print "  %s : %d" % ( V[i][k], calc_upper_connectivity(i, k) )
        
print "Lower connectivities:"
for i in xrange(levels-1):
    for k in xrange( len( V[i] ) ): 
        print "  %s : %d" % ( V[i][k], calc_lower_connectivity(i, k) )
        
## -------------------------------------------------------------------------
##  E: Barycentres
## -------------------------------------------------------------------------

   
      
