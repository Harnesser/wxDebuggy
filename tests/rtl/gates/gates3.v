module gates3 ( 
  input in1,
  input in2,
  input in3,
  input in4,
  output wire out1
  );
 
and2 U1 ( .A(in1), .B(in2), .Y(gx) );
and2 U2 ( .A(in3), .B(in4), .Y(gy) );
and2 U3 ( .A(gx), .B(gy), .Y(out1) );
 
endmodule

