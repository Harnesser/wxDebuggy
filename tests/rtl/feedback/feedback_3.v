module feedback_3
  (
    input in1,
    output out1
  );

  three_in_three_out U1 ( .in1(in1), .in2(n4), .in3(n5),
                          .out1(n1), .out2(n2), .out3(n3) );
  three_in_three_out U2 ( .in1(n1), .in2(n2), .in3(n3),
                          .out1(out1), .out2(n4), .out3(n5) );

endmodule

