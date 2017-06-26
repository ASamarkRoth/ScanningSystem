#!/bin/bash

F_INPUT="surface"

python3 move_collimator.py -swipe_file $F_INPUT 0 20 10 0 20 10
python3 move_collimator.py -file_xy $F_INPUT 

echo temp.$F_INPUT.scan

while [ -f temp.$F_INPUT.scan ] && [ ON != "0" ]; do  
	python3 move_collimator.py
	ON="$(sed '2q;d' .scanning.xy | awk '{print $2}')"
done

mv stepper.log $F_INPUT_stepper.log
mv coords.log $F_INPUT_coords.log
mv power.log $F_INPUT_power.log
