//
// Me
// $Id: marty.v,v 1.1 2007-08-15 23:47:37 marty Exp $
module marty
  (
   input wire clk,
   input wire resetb,
   input wire disconnection,
   input wire [1:0] gossamer,
   output reg nothing_of_note,
   input wire two_guitars
   );

   wire  temp = |( gossamer && { disconnection, two_guitars});

//   always @( posedge clk or negedge resetb )
//     if( !resetb )
//       nothing_of_note = 1'b0;
//     else
//       nothing_of_note = temp;

   

endmodule // marty
