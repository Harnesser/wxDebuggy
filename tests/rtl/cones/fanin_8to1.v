module fanin_8to1
  (
    input a,
    input b,
    input c,
    input d,
    input e,
    input f,
    input g,
    input h,
    output y    
  );

  two_in_one_out hendrix ( .out(seven),    .in1(b), .in2(d) );
  two_in_one_out slash   ( .out(eleventy), .in1(a), .in2(f) );
  two_in_one_out king    ( .out(forty),    .in1(h), .in2(c) );
  two_in_one_out hammet  ( .out(pi),       .in1(e), .in2(g) );
  
  two_in_one_out clapton ( .out(four),     .in1(seven), .in2(pi) );
  two_in_one_out young   ( .out(zero),     .in1(forty), .in2(eleventy) );
  
  two_in_one_out marty   ( .out(y), .in1(zero), .in2(four) );
endmodule

