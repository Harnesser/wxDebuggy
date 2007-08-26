//
// A Simple Module declaration
//
// $Id: hendrix.v,v 1.1 2007-08-15 23:47:37 marty Exp $

module hendrix
  (
   input resetb,
   input mclk,
   input purple,
   input electric,
   input haze,   // a comment to throw things
   output [2:0] midnight_oil,
   output ladyland
   );

   marty me2 ( /*AUTOINST*/
	      // Outputs
	      .nothing_of_note		(ladyland),
	      // Inputs
	      .clk			(clk),
	      .resetb			(resetb),
	      .disconnection		(purple),
	      .gossamer			({electric,purple}),
	      .two_guitars		(haze));

   assign midnight_oil = { ladyland, ladyland };

endmodule // ports_only
