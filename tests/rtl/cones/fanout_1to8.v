module fanout_1to8
  (
    output a,
    output b,
    output c,
    output d,
    output e,
    output f,
    output g,
    output h,
    input y    

  );

  one_in_two_out hendrix ( .in(seven),    .out1(b), .out2(d) );
  one_in_two_out slash   ( .in(eleventy), .out1(a), .out2(f) );
  one_in_two_out king    ( .in(forty),    .out1(h), .out2(c) );
  one_in_two_out hammet  ( .in(pi),       .out1(e), .out2(g) );
  
  one_in_two_out clapton ( .in(four),     .out1(seven), .out2(pi) );
  one_in_two_out young   ( .in(zero),     .out1(forty), .out2(eleventy) );
  
  one_in_two_out marty   ( .in(y), .out1(young), .out2(clapton) );

endmodule

