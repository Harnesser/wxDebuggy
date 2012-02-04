#! /usr/bin/env python
""" Sugiyama Layer Reordering Operations"""

import pprint
import graph_test_base
#import reordering
            
DEBUG = False

class SugiyamaLayerReordering( graph_test_base.Graph_Test_Base ):
       
    def get_graph_gates1(self):
        """ Build the graph for this cct:
        
                        +------+
            in_a O------#      #------O out_a
                        |      | 
            in_b O------#  U1  #------O out_b
                        |      |
                    +---#      #---+
                    |   +------+   |
                    |              |
                    |   +------+   |
                    +---#  U0  #---+
                        +------+                                             
        """

        vertices = [  [ 'in_b', 'in_a' ],         
                      [ 'U0', 'U1' ]
                      [ 'out_b', 'out_a' ] 
                   ]
        str_ = [ 'in_a.o_1:U0.i_1;in_b.o_1:U0.i_2;in_c.o_1:U1.i_1;in_d.o_1:U1.i_2',
            'U0.o_1:U2.i_1;U1.o_1:U2.i2' ] 
        
        str_ = '\n'.join(str_, vertices)
        G = self.build_multilayer_graph_from_shorthand(str_)
        
        return G
        

    def test__reorder_gates1_phase1(self):
        G = self.get_graph_gates1()

        print G.display()
        #eng = reordering.Reordering_Engine()
        #eng.set_graph(G)
        #self.show_conn_matrices(eng.G, 'I N I T I A L')
        #        
        #self.assertEquals( eng.G.get_crossover_count(), 3)
        #for x in eng.gen_phase1():
        #    self.show_conn_matrices(eng.G)
        #        
        #self.assertEquals( eng.G.get_crossover_count(), 0)
        #
        #self.show_conn_matrices(eng.G, 'F I N A L   R E S U L T')
        
        

        

        

