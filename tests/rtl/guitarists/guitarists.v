//
// Guitarists
//
// $Id: guitarists.v,v 1.1 2007-08-15 23:47:37 marty Exp $

module guitarists
  (
   input mclk,
   input resetb,
   input riff,
   input groove,
   input solo,
   output wire [1:0] keelar_tune
   );

   assign welcome = 1'b0;

   wire   this_wwire;
   reg [3:0] that_reg;
   
   
   young acdc (/*AUTOINST*/
	       // Outputs
	       .moneytalks		({2'b00,keelar_tune[1:0]}),
	       // Inputs
	       .clk			(clk),
	       .resetb			(resetb),
	       .rosie			({riff,groove}),
	       .back_in_black		(riff),
	       .about_to_rock		(riff),
	       .thunderstruck		(groove));

   hendrix experience (/*AUTOINST*/
		       // Outputs
		       .midnight_oil	(midnight_oil[2:0]),
		       .ladyland	(ladyland),
		       // Inputs
		       .resetb		(resetb),
		       .mclk		(mclk),
		       .purple		(groove),
		       .electric	(riff),
		       .haze		(groove));

   ports_only i0 ( /*AUTOINST*/
		  // Outputs
		  .dout			(dout[6:0]),
		  .do_something		(do_something),
		  // Inputs
		  .resetb		(resetb),
		  .mclk			(mclk),
		  .din			(din[3:0]));
   
   
endmodule 
