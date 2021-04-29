## Homemade useful or interesting Autocad scripts

### AutoLisp_Tools
A set of tools for for processing files for laser cutting
### SpiralGen
A cool bit of pattern generation using autocad. 
### ImageConv
Experiments with generating CAD files from images. 

 

## AutoLisp_Tools Functions

Some CNC software handles polyines really slowly, especially the one I use regularly: UCP (Universal Control Panel from Universal Laser Systems). As it divides up curves into an arbitrarily large number of segments, it will take 2-3 times as long as it needs to doing tiny precise motions. I was originally just looking for a single command to break polylines into segments, but things got kind of out of hand, and now I have a small suite of custom tools. 

Load with (load "s"). You will have to place files in a location in AutoCAD's search path, or make a new one.

### gexp
Split all selected polylines into segments and explode them individually. Will slightly reduce resolution of cut but \~double speed.

### gseg
Split all polylines into segments, but not explode, so you can alter more easily before exploding

### gext
Will extend all selected segments to the given length, useful for smoothing

### gminext
Same as gext, but will not shrink lines, only extend


## ImageConv
A handful of python scripts to convert images to DXFs designed to be laser engraved. Mostly not super useful, but fun. It's pretty slow, as I used Python to make it easier to tweak between runs. Each run outputs a DXF, an image containing the map of dots, and a file with run details in a folder. 

To set up folders run ./cleanup. It will also clean your existing out & dump folders, if already set up. To run python scripts, simple run with the name of the desired output as the an argument. Save input images under img or in ImageConv. 

### pointilism.py
Converts greyscale images into dots. Can be tweaked to do a lot to do interesting things, the variables to play with are at the top of the file. It's simply a more interesting way of rastering images. 


### connectDots.py
Connects dots from pointilism to fill in better and engrave faster. Has 2 settings, default is rolling sum. Default settings work well on 1500-1500px images. 
