##Some AutoLISP tools I've been working on while teaching myself LISP.

These are primarily useful for processing files for laser cutting. Some CNC software handles polyines really slowly, especially the one I use regularly: UCP (Universal Control Panel from Universal Laser Systems). As it divides up curves into an arbitrarily large number of segments, it will take 2-3 times as long as it needs to doing tiny precise motions. I was originally just looking for a single command to break polylines into segments, but things got kind of out of hand, and now I have a small suite of custom tools. 

Functions

### gexp
Split all selected polylines into segments and explode them individually. Will slightly reduce resolution of cut but \~double speed.

###gseg
Split all polylines into segments, but not explode, so you can alter more easily before exploding

##gext
Will extend all selected segments to the given length, useful for smoothing

###gminext
Same as gext, but will not shrink lines, only extend