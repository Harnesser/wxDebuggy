#! /usr/bin/env python

import pprint
from numpy import *

print """
### ========================================================================
###
###  Section II: BASIC DEFINITIONS
###
### ========================================================================
"""

## -------------------------------------------------------------------------
##  A: n-Level Hierarchy and Map
## -------------------------------------------------------------------------
V = [ list('ab') , list('cdef'), list('ghij'), list('klm') ]
E = [  [('a','c'), ('a','d'), ('a','e'), ('a','f'), ('b','c'), ('b','f') ],
       [('c','g'), ('d','h'), ('d','i'), ('d','j'), ('e','g'), ('e','j') ],
       [('g','k'), ('i','k'), ('i','m'), ('j','k'), ('j','l') ]
    ]
    
levels  = len(V)

print """
## -------------------------------------------------------------------------
##  B: Matrix Realisation of n-Level Hierarchies
## -------------------------------------------------------------------------
"""
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
       
print """
## -------------------------------------------------------------------------
##  C: The Number of Crossings of n-Level Hierarchies
## -------------------------------------------------------------------------
"""
def calc_k(i,j,k):
    """ Calculate the crossings between an ordered pair of vertex rows.
    Calculates k( r(u,v), r(v,u) ) """
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
    
def calc_crossings(M):
    crossings = 0
    for i in xrange(levels-1):
        crossings += calc_layer_crossings(i)
    return crossings
            
for i in xrange(levels-1):
    print "Layer", i, calc_layer_crossings(M,i)
print "Total Crossings:", calc_crossings(M)


print """
## -------------------------------------------------------------------------
##  D: Connectivity
## -------------------------------------------------------------------------
"""
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
        
        
print """
## -------------------------------------------------------------------------
##  E: Barycentres
## -------------------------------------------------------------------------
"""
def vector_barycentre( vector ):

    barycentre = 0.0
    for j in xrange( len(vector) ):
        barycentre += j * vector[j]
    
    total = sum(vector)
    if total:
        barycentre /= total 
    else:
        barycentre = 0.0
        
    return barycentre
    
print "Vector Barycentres:"
for m in M:
    for v in m:
        print "%s: %f" % ( v, vector_barycentre(v) )


def row_barycentres( layer ):
    
    barycentres = []
  
    p = len( V[layer] )
    q = len( V[layer+1] )
    m = M[layer]
    
    for k in xrange(p):
        numer = 0.0
        denom = 0.0
        
        for l in xrange(q):
            numer += l * m[k][l]
            denom += m[k][l]
            
        if denom:
            barycentre = numer / denom
        else:
            barycentre = 0.0
            
        barycentres.append(barycentre)
        
    return barycentres
     
          
print "\nRow Barycentres:"   
for i in xrange(levels-1):
    print row_barycentres(i)
    

def col_barycentres( layer ):

    barycentres = []
  
    p = len( V[layer] )
    q = len( V[layer+1] )
    m = M[layer]
    
    for l in xrange(q):
        numer = 0.0
        denom = 0.0
        
        for k in xrange(p):
            numer += k * m[k][l]
            denom += m[k][l]
            
        if denom:
            barycentre = numer / denom
        else:
            barycentre = 0.0
            
        barycentres.append(barycentre)
        
    return barycentres

print "\nColumn Barycentres:"
for i in xrange(levels-1):
    print col_barycentres(i)
    

def get_x_pos(i, j):
    return 0.0
    
def upper_barycentres(i):
    
    barycentres = []
    
    p = len( V[layer-1] )
    m1 = M[layer-1]
    
    for k in xrange( len( V[i] ) ):
    
        numer = 0.0        
        for j in xrange(p):
            numer += get_x_pos(i-1,j) * m1[j][k]
            
        denom = calc_upper_connectivity(i,k)
        if denom:
            barycentre = numer / denom
        else:
            barycentre = 0.0
            
        barycentres.append(barycentre)
        
    return barycentres   
    
    
def lower_barycentres(i):
    
    barycentres = []

    q = len( V[layer+1] )
    m = M[layer]
    
    for k in xrange( len( V[i] ) ):
    
        numer = 0.0        
        for l in xrange(q):
            numer += get_x_pos(i-1,j) * m[k][l]
            
        denom = calc_upper_connectivity(i,k)
        if denom:
            barycentre = numer / denom
        else:
            barycentre = 0.0
            
        barycentres.append(barycentre)
        
    return barycentres   
         
print """
### ========================================================================
###
###  Section III: REDUCTION OF THE NUMBER OF CROSSINGS
###
### ========================================================================
"""

V = [ list('12345678'), list('abcdefgh') ]
edges = '1c:1d:1e:1h:2c:2e:3a:3e:3f:3h:4e:5c:5g:6f:7b:7d:8b:8f:8g'
E1 = []
for edge in edges.split(':'):
    E1.append( tuple(edge) )
E = [ E1 ]

levels = len(V)

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
    print "Crossings:",calc_crossings()
            
            
print """
## -------------------------------------------------------------------------
##  A: Algorithms for Two-Level Hierarchies
## -------------------------------------------------------------------------
"""            

def penalty_digraph( M ):
    """ Calculate the penalty digraph for a 2-layer graph
    ... NOT COMPLETE ... """
    
    for i in xrange( len(M) ) :
        print "Layer",i
        m = M[i]
        p = len( V[i] )
        q = len( V[i+1] )
        
        F = []
        for j in xrange(0,p-1):
            for k in xrange(j+1,p):
                k_uv = calc_k(i, j, k )  
                k_vu = calc_k(i, k, j )  
                
                if k_uv < k_vu:
                    edge = ( V[i][j], V[i][k] )
                else:
                    edge = ( V[i][k], V[i][j] )
                F.append( edge )
                
                print "  (%s,%s) vs (%s,%s) : %d vs %d : %s" % (
                    V[i][j], V[i][k], V[i][k], V[i][j],
                    k_uv, k_vu, edge )
            
        print "F:", F
            
print "## Penalty Minimization Method (PM method)"
penalty_digraph(M)           

V = [ list('abcd'), list('efghi') ]
edges = 'ae:af:be:bh:bi:cf:ch:ci:de:dg:di'
E1 = []
for edge in edges.split(':'):
    E1.append( tuple(edge) )
E = [ E1 ]

levels = len(V)

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
    print "Crossings:",calc_crossings()
            
print "## Barycentric method"

print """## Barycentric method
Method:
 0.M* := M0, C* := C(M0), j := 0;
 1.Carry out PHASE 1;
 2.Carry out the following until j = J; {[PHASE 2]}
 1.M1 := ROR(M0), M0 := M1;
 2.If the column barycenters are not in monotonous increase order for M0, carry out PHASE 1;
 3.M1 := ROC(M0), M0 := M1;
 4.If the row barycenters are not in monotonous increase order for M0, carry out PHASE 1;
 5.j := j + 1;
[PHASE 1]
 0.i := 0;
 1.Carry out the following until i = I;
 1.M1 := BOR(M0),  M0 := BOC(M1);
 2.If C(M0)<C*, then M* := M0 and C* := C(M0);
 3. := i + 1;
"""

def barycentre_row_reorder(M):
    """ Reorder the rows of matrix M on the barycentres. """
    
    barycentres = row_barycentres(M)
    
    return M_
    
    


def phase1(M0):
    
    M_star = list(M0)
    K_star = calc_crossings(M0)
    
    M1 = barycentre_row_reorder(M0)
    
    
def phase2():
    pass
    
def barycentric_method_2(M):
    """ Two-Layer Barycentric thingy."""
    
    M0 = list(M)
    
    
    

