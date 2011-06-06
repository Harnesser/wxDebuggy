module feedback_2
  (
    input in1,
    output out1
  );

  two_in_two_out U1 ( .in1(in1), .in2(n3), .out1(n1), .out2(n2) );
  two_in_two_out U2 ( .in1(n1), .in2(n2), .out1(out1), .out2(n3) );

endmodule

