#!/bin/bash

F_INPUT="surface"

python3 move_collimator.py -swipe_file $F_INPUT 0 20 10 0 20 10
python3 move_collimator.py -file_xy $F_INPUT 

echo temp.$F_INPUT.scan

while [ -f temp.$F_INPUT.scan ]; do  
	python3 move_collimator.py
done
