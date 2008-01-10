module gates2 ( 
  input in1,
  input in2,
  input in3,
  output wire out1
  );
 
and2 U1 ( .A(in1), .B(in2), .Y(marty) );
and2 U2 ( .A(marty), .B(in3), .Y(out1) );
 
 
endmodule

