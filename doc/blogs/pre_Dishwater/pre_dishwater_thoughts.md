State of the Viewer
-------------------
Things are progressing slightly well with wxDebuggy, it now does a half-decent job of drawing some verilog modules and the wiring between them -- and all this while limiting the number of crossovers!

![Screenshot from the latest RTL Viewer version] (Screenshot-spider-for-blog.png)

As mentioned before, I wasn't too happy with the wire-crossing reduction results when using a straight version of the Sugiyama et al algorithm. The current revision of the verilog viewer improves the crossover reduction using two techniques:

1. The layer reordering stage of the Sugiyama et al algorithm was tweaked using ideas found [here (SFvHM09)] [SFvHM09]. With this tweak, the layout algorithm now knows that modules have ports and that these ports are in a fixed order.

2. The orthogonal wire routing algorithm use 'Greedy Assign' to place the vertical line segments of each wire to a unique track between the layers. This idea comes from (EGB04). 

Stuff to Fix for 'Dishwater' Tag
--------------------------------
* Y co-ordinate assignment of the modules should be improved.
* Long dummy edges should be kept straight.
* Clock/reset-like signals that go to multiple modules in multiple layers need to be handled better.
* Feedback wires are not drawn all that well.

Misc worries
------------
* RTL parser is very slow. The files I test on have basic RTL and wiring, and there are only about 12 of them, but it takes around 3 seconds for my desktop to parse them and build the necessary data structures.
* Greedy assign may not be enough for more involved circuits - I may need to add the 'Sifting' bit too.

References
----------

* SFvHM09 [Port Constraints in Hierarchical Layout of Data Flow Diagrams] [SFvHM09]
* EGB04 Orthogonal Circuit Visualization Improved by Merging the Placement and Routing Phases (no link)

[SFvHM09]: http://rtsys.informatik.uni-kiel.de/~biblio/downloads/papers/gd09.pdf
