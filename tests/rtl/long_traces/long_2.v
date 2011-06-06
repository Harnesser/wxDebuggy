module long_2
  (
    input in1,
    output out1
  );


  one_in_three_out U1 ( .in(in1), .out1(n1), .out2(n2), .out3(n3) );
  
  one_in_one_out U2 ( .in(n3), .out(n4) );
  one_in_one_out U3 ( .in(n2), .out(n5) );
  one_in_one_out U4 ( .in(n4), .out(n6) );

  three_in_one_out U5 ( .in1(n1), .in2(n5), .in3(n6), .out(out1) );


endmodule

