#!/bin/bash


F_INPUT="surface"

python3 move_collimator.py -swipe_file $F_INPUT 0 2 1 0 2 1
python3 move_collimator.py -file_xy $F_INPUT 

echo temp.$F_INPUT.scan

ON="$(sed '2q;d' .scanning.xy | awk '{print $2}')"
while [ -f temp.$F_INPUT.scan ] && [ "$ON" == "0" ]; do  
	python3 move_collimator.py
	ON="$(sed '2q;d' .scanning.xy | awk '{print $2}')"
done

if [ "$ON" == "1" ]; then
	echo "Emergency stop activated, exiting normally!"
fi

mv stepper.log "$F_INPUT"_stepper.log
mv coords.log "$F_INPUT"_coords.log
mv power.log "$F_INPUT"_power.log

python3 move_collimator.py -no_file
