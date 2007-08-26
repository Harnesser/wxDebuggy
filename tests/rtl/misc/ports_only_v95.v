//
// A Simple Module declaration in Verilog-1995 Style
//
// $Id: ports_only_v95.v,v 1.1 2007-08-15 23:47:37 marty Exp $

module ports_only_v95
  (
   resetb,
   mclk,
   din,
   dout,   // a comment to throw things
   do_something
   );

   input   resetb;
   input   mclk;
   input  [3:0] din;
   output [6:0] dout;
   output do_something;   
   
endmodule // ports_only
