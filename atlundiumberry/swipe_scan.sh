#!/bin/bash

F_INPUT="test"

python3 move_collimator.py -swipe_file $F_INPUT 1 3 1 1 3 1
python3 move_collimator.py -file_xy $F_INPUT 

echo temp.$F_INPUT.scan

while [ -f temp.$F_INPUT.scan ]; do  
	python3 move_collimator.py
done
