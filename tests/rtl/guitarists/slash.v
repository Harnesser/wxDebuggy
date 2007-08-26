//
// A Simple Module declaration
//
// $Id: slash.v,v 1.1 2007-08-15 23:47:37 marty Exp $

module slash
  (
   input clk,
   input resetb,
   output sweet,
   input paradise,
   input city,
   input locomotion,
   input wire [1:0] welcome,
   output jungle,
   output rocket,
   output [2:0] child,
   output [1:0] mine
   output crazy
   );

   marty me (
	     /*AUTOINST*/
	     // Outputs
	     .nothing_of_note		(jungle),
	     // Inputs
	     .clk			(clk),
	     .resetb			(resetb),
	     .disconnection		(paradise),
	     .gossamer			(welcome),
	     .two_guitars		(city));
	      
endmodule // slash

