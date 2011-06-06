module long_1
  (
    input in1,
    output out1
  );

  one_in_two_out U1 ( .in(in1), .out1(n1), .out2(n2) );
  one_in_one_out U2 ( .in(n2), .out(n3) );
  two_in_one_out U3 ( .in1(n1), .in2(n3), .out(out1) );

endmodule

