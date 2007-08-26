//
// A Simple Module declaration
//
// $Id: ports_only.v,v 1.1 2007-08-15 23:47:37 marty Exp $

module ports_only
  (
   input resetb,
   input mclk,
   input [3:0] din,
   output [6:0] dout,   // a comment to throw things
   output do_something
   );

endmodule // ports_only
