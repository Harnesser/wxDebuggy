module spider
  (
    input leg_left1,
    input leg_left2,
    input leg_left3,
    input leg_left4,
    output leg_right1,
    output leg_right2,
    output leg_right3, 
    output leg_right4

  );



  one_in_one_out U1 ( .in(leg_left1), .out(seg1) );
  one_in_one_out U2 ( .in(leg_left2), .out(seg2) );
  one_in_one_out U3 ( .in(leg_left3), .out(seg3) );
  one_in_one_out U4 ( .in(leg_left4), .out(seg4) );

  two_in_two_out U5 ( .in1(seg1), .in2(seg2), .out1(seg5), .out2(seg6) );
  two_in_two_out U6 ( .in1(seg3), .in2(seg4), .out1(seg7), .out2(seg8) );

  four_in_four_out U7 ( 
    .in1(seg5),
    .in2(seg6),
    .in3(seg7),
    .in4(seg8),
    .out1(seg9),
    .out2(seg10),
    .out3(seg11),
    .out4(seg12)
    );

  two_in_two_out U8 ( .in1(seg9), .in2(seg10), .out1(seg13), .out2(seg14) );
  two_in_two_out U9 ( .in1(seg11), .in2(seg12), .out1(seg15), .out2(seg16) );
    
  one_in_one_out U10 ( .out(leg_right1), .in(seg13) );
  one_in_one_out U11 ( .out(leg_right2), .in(seg14) );
  one_in_one_out U12 ( .out(leg_right3), .in(seg15) );
  one_in_one_out U13 ( .out(leg_right4), .in(seg16) );



endmodule

