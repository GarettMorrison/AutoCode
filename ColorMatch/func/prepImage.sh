#!/bin/bash
echo Converting $1 Image
file=$1

maxWidth=1000
maxHeight=1000

imgWidth=$(identify -format "%w" $file)
imgHeight=$(identify -format "%h" $file)

if [ "$imgWidth" -gt "$maxWidth" ];
then
	mogrify -resize "$maxWidth"x $file
fi
if [ "$imgHeight" -gt "$maxHeight" ];
then
	mogrify -resize "$maxWidth"x $file
fi
mogrify -format png -rotate 90 $file
rm $file
echo done!