module spider_2
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

  two_in_one_out U5 ( .in1(seg1), .in2(seg2), .out(seg5) );
  two_in_one_out U6 ( .in1(seg3), .in2(seg4), .out(seg6) );

  two_in_two_out U7 ( 
    .in1(seg5),
    .in2(seg6),
    .out1(seg7),
    .out2(seg8)
    );

  one_in_two_out U8 ( .in(seg7), .out1(seg9), .out2(seg10) );
  one_in_two_out U9 ( .in(seg8), .out1(seg11), .out2(seg12) );
    
  one_in_one_out U10 ( .out(leg_right1), .in(seg9) );
  one_in_one_out U11 ( .out(leg_right2), .in(seg10) );
  one_in_one_out U12 ( .out(leg_right3), .in(seg11) );
  one_in_one_out U13 ( .out(leg_right4), .in(seg12) );



endmodule

