
""" Evaluating the steps necessary to invoke to move the new position. """
def pos_eval(new_x, new_y):
	with open('move_data/.position.xy', 'r') as f:
		x, y = map(float, f.readline().split())

	print("Current position is:", x, y)
	line_prepender('move_data/.position.xy', str(new_x)+" "+str(new_y))
	return 0, 0

def line_prepender(filename, line):
	with open(filename, 'r+') as f:
		content = f.read()
		f.seek(0, 0)
		f.write(line.rstrip('\r\n') + '\n' + content)

def deleteContent(fName):
	with open(fName, "w"):
		pass
