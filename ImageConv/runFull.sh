#!/bin/bash
echo Running pointilism and connectDots #
python3 pointilism.py "$1" #
echo " " #
python3 connectDots.py "$1" #
#
#