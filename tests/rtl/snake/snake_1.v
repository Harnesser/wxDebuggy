module snake_1 ( input in1, output out1 );
   
   one_in_four_out U1( .in1(in1),                        .out1(n1), .out2(n2), .out3(n3), .out4(n4) );
   
   two_in_three_out U2( .in1(n1), .in2(n2),                  .out1(n5), .out2(n6), .out3(n7) );
   
   two_in_two_out U3 ( .in1(n3), .in2(n4) ,                  .out1(n8), .out2(n9));
   
   two_in_three_out U4( .in1(n6), .in2(n7),                       .out1(n10), .out2(n11), .out3(n12) );
   
   two_in_two_out U5( .in1(n8),.in2(n9),                      .out1(n13),   .out2(    n14 
    ) );
   
   three_in_one_out U6 ( .in1(n10), .in2(n11) ,  .in3(n12) ,            .out(n15) );
   
   three_in_one_out U7 ( .in1(n13), .in2(n5),  .in3(n14),             .out(n16));
   
   two_in_one_out U8 ( .in1(n15), .in2(n16),                        .out(out1) );
   
   
endmodule
   
