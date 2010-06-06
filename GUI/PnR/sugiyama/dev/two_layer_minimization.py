#! /usr/bin/env python
""" Sugiyama's 2-layer crossing minimization heuristic algorithm.

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

from matrix import *

# Set up the initial graph
V = [ list('abcd'), list('efghi') ]
edges = 'ae:af:be:bh:bi:cf:ch:ci:de:dg:di'
E = []
for edge in edges.split(':'):
    E.append( tuple(edge) )

# Inputs to the algorithm
I = 10
J = 10
print V[0]
print V[1]
print E
M0 = Matrix( V[0], V[1], E )

# 0
M_star = M0.copy()
C_star = M0.get_crossover_count()
j = 0

print "GO:"
print "=" * 50
print M0

def phase_1():

    global M_star
    global C_star
    global M0
    
    # 0
    i = 0
    prev_C = M0.get_crossover_count()
    # 1
    while i < I:
    
        print "-" * 50
        print "i", i
        
        M1 = M0.copy()
        M1.barycentre_row_reorder()
        
        M0 = M1.copy()
        M0.barycentre_col_reorder()


        C_M0 = M0.get_crossover_count()
        print prev_C, C_M0
        if C_M0 == prev_C:
            return
            
        if C_M0 < C_star:
            M_star = M0.copy()
            C_star = C_M0
            
        prev_C = C_M0
        print M_star 
        i += 1

# 1
phase_1()

# 2
while j < J:

    #print "=" * 50
    print "j", j
    
    # 2.1
    M1 = M0.copy()
    M1.row_reversion()
    M0 = M1.copy()
    
    # 2.2
    if not M0.col_barycenters_are_monotonic():
        phase_1()
        
    # 2.3
    M1 = M0.copy()
    M1.col_reversion()
    M0 = M1.copy()
    
    # 2.4
    if not M0.row_barycenters_are_monotonic():
        phase_1()
    else:
        break
            
    print M_star 
    j += 1
    
print "="*50
print "Final Answer:"
print M_star
    
