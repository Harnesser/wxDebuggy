//
// Angus Young
//
// $Id: young.v,v 1.1 2007-08-15 23:47:37 marty Exp $

module young
  (
   input wire clk,
   input wire resetb,
   input wire [1:0] rosie,
   input wire back_in_black,
   input wire about_to_rock,
   input wire thunderstruck,
   output reg [3:0] moneytalks
   );

   wire   this_wwire;
   reg [3:0] that_reg;
   
   
   slash guns_n_roses (/*AUTOINST*/
		       // Outputs
		       .sweet		(moneytalks[3]),
		       .jungle		(moneytalks[2]),
		       .rocket		(),
		       .child		(),
		       .mine		(moneytalks[1:0]),
		       .crazy		(),
		       // Inputs
		       .clk		(clk),
		       .resetb		(resetb),
		       .paradise	(back_in_black),
		       .city		(about_to_rock),
		       .locomotion	(thunderstruck),
		       .welcome		(rosie));

   
endmodule 
