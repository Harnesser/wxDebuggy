module gates1 ( 
  input in1,
  input in2,
  input in3,
  input in4,
  output wire out1,
  output wire out2
  );
 
and2 U1 ( .A(in1), .B(in2), .Y(out1) );
and2 U2 ( .A(in3), .B(in4), .Y(out2) );
 
 
endmodule

