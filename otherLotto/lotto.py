import random
import tkinter
import pdb
import sys
import argparse
import os
import struct
from tkinter import messagebox

cfg_consoleOut = False
cfg_count = 1
cfg_noWindow = False
cfg_biased = False
biasedList = None

parser = argparse.ArgumentParser(
	prog='Lotto',
	description='generates Eurolotto sheets',
	epilog='')

parser.add_argument('-c', '--count', help="The count of Eurolotto sheets")      # option that takes a value
parser.add_argument('-p', '--print', action='store_true', help="prints the Eurolotto sheet values in the console")  # on/off flag
parser.add_argument('-nw', '--noWindow', action='store_true', help="does not start the window")  # on/off flag
parser.add_argument('-b', '--biased', action='store_true', help="if set, used statistics about the previous winning numbers as bias")  # on/off flag


args = parser.parse_args()
#print(args.count, args.print, agrs.noWindow)

# set cfgs via cmd parameters

cfg_consoleOut = args.print

cfg_noWindow = args.noWindow

cfg_biased = args.biased

if args.count != None:
	if not (args.count.isdigit()):
		print("The count argument must be a number!")
		exit()
	cfg_count = int(args.count)


def checkUniqe(array, number):
	i = 0
	while i < len(array):
		if (array[i] == number):
			return False
		i = i + 1
	return True



def weightedRandom(maxValue):
	if (maxValue < 10):
		print("weightedRandom maxValue must be 10 or more!")
		exit(-1)


	maxValue = maxValue + 1 # since rand is exlusive

	p1o10 = max(int(maxValue * 0.1),2)
	p2o10 = max(p1o10 + int(maxValue * 0.1),p1o10+1)
	p3o10 = max(p2o10 + int(maxValue * 0.1),p2o10+1)
	p4o10 = max(p3o10 + int(maxValue * 0.1),p3o10+1)
	p5o10 = max(p4o10 + int(maxValue * 0.1),p4o10+1)
	p6o10 = max(p5o10 + int(maxValue * 0.1),p5o10+1)
	p7o10 = max(p6o10 + int(maxValue * 0.1),p6o10+1)
	p8o10 = max(p7o10 + int(maxValue * 0.1),p7o10+1)
	p9o10 = max(p8o10 + int(maxValue * 0.1),p8o10+1)
	p10o10 = max(maxValue,p9o10+1)


	# 24% 1 1/10
	# 16% 2 1/10
	# 15% 3 1/10
	# 12% 4 1/10
	# 10% 5 1/10
	# 8%  6 1/10
	# 6%  7 1/10
	# 5%  8 1/10
	# 3%  9 1/10
	# 1% 10 1/10

	select = random.randrange(0,101) # 0 - 100

	if (select <= 24):
		return random.randrange(1,p1o10)
	if (select <= 40):
		return random.randrange(p1o10,p2o10)
	if (select <= 55):
		return random.randrange(p2o10,p3o10)
	if (select <= 67):
		return random.randrange(p3o10,p4o10)
	if (select <= 77):
		return random.randrange(p4o10,p5o10)
	if (select <= 85):
		return random.randrange(p5o10,p6o10)
	if (select <= 91):
		return random.randrange(p6o10,p7o10)
	if (select <= 96):
		return random.randrange(p7o10,p8o10)
	if (select <= 99):
		return random.randrange(p8o10,p9o10)
	return random.randrange(p9o10,p10o10)

def weightedRandomTest(i):
	counter = [0]*51

	while i > 0:
		rand = weightedRandom(50)
		counter[rand] = counter[rand] + 1
		i = i - 1

	i = 50
	while (i >= 0):
		print(str(i) + ": " + str(counter[i]))
		i = i - 1

#weightedRandomTest(0xFFFFF)


def createBiasedList():

	if (os.path.isfile("./freq.bin") == False):
		print("freq.bin does not exist, cant used Biased generation")
		return False
	# file exists

	global biasedList

	unpacked_data = None
	biasedList = []
	freqList = []

	try:
		with open("./freq.bin","rb") as file:

			data_format = "i " + \
		              "f f f f f f f f f f" + \
		              "f f f f f f f f f f" + \
		              "f f f f f f f f f f" + \
		              "f f f f f f f f f f" + \
		              "f f f f f f f f f f" + \
		              "f f f f f f f f f f" + \
		              "f f"

			data = file.read()

			# Unpack the data
			unpacked_data = struct.unpack(data_format, data)
	except IOError:
		print("Error: An I/O error occurred while handling freq.bin")
		return False
	except struct.error:
		print("Error: The data could not be unpacked. The file may be corrupted.")
		return False


	print("statistics for "+str(unpacked_data[0])+" games")

	#print(unpacked_data)

	num50 = []
	num12 = []

	i = 1 # skip the integer for the total games
	while i < 50 + 1:
		num50.append(unpacked_data[i])
		i = i + 1

	while i < 12 + 1 + 50:
		num12.append(unpacked_data[i])
		i = i + 1


	# unsorted
	num50u = num50[:]
	num12u = num12[:]

	# sorted
	num50.sort(reverse=True)
	num12.sort(reverse=True)

	# indexes sorted by freqency
	num50r = []
	num12r = []

	i = 0
	while (i < len(num50)):
		index = num50u.index(num50[i])
		num50u[index] = None
		num50r.append(index)
		i = i + 1

	i = 0
	while (i < len(num12)):
		index = num12u.index(num12[i])
		num12u[index] = None
		num12r.append(index)
		i = i + 1


	biasedList.append(num50r)
	biasedList.append(num12r)
	



# get list if we want biased generation

if (cfg_biased == True):
	if (createBiasedList() == False):
		exit(-1)

# debug print
#print("biased list:")
#print(biasedList)



def generateNumbers():

	from50 = [0]*5
	from12 = [0]*2

	i = 0
	while i < 5:

		rand = 0

		# generate random number, untill its uniqe
		if (cfg_biased == False):
			rand = random.randrange(1,50+1)
		else:
			rand = weightedRandom(50)


		while checkUniqe(from50,rand) == False:
			if (cfg_biased == False):
				rand = random.randrange(1,50+1)
			else:
				rand = weightedRandom(50)


		from50[i] = rand
		i = i + 1

	i = 0
	while i < 2:

		rand = 0
		# generate random number, untill its uniqe
		if (cfg_biased == False):
			rand = random.randrange(1,12+1)
		else:
			rand = weightedRandom(12)

		while checkUniqe(from12,rand) == False:
			if (cfg_biased == False):
				rand = random.randrange(1,12+1)
			else:
				rand = weightedRandom(12)


		from12[i] = rand
		i = i + 1

	return from50,from12





biasButtionText = "Bias Aktivieren"
if (cfg_biased == True):
	biasButtionText = "Bias Deaktivieren"

buttonSwitchBias = None

def biasButtionFunc():

	global biasButtionText
	global cfg_biased
	global biasedList
	global buttonSwitchBias

	if (biasedList == None):
		if (createBiasedList() == False):
			messagebox.showerror("Fehler", "Fehler beim laden der Warcheinlichkeiten!")
			return

	if (cfg_biased == False):
		cfg_biased = True
		biasButtionText = "Bias Deaktivieren"
	else:
		cfg_biased = False
		biasButtionText = "Bias Aktivieren"

	buttonSwitchBias.config(text=biasButtionText)

if not cfg_noWindow:

	root = tkinter.Tk()
	root.geometry("300x430")
	root.minsize(300,430)

	# Create a Canvas widget inside a Frame to hold your scrollable content
	canvas = tkinter.Canvas(root)
	scrollbar = tkinter.Scrollbar(root, orient="vertical", command=canvas.yview)
	roots = tkinter.Frame(canvas)

	roots.bind(
	    "<Configure>",
	    lambda e: canvas.configure(
	        scrollregion=canvas.bbox("all")
	    )
	)

	window_id = canvas.create_window((0, 0), window=roots, anchor="nw")
	canvas.configure(yscrollcommand=scrollbar.set)


	canvas.coords(window_id, 50, 0) # makes sure the thing is cented on start


	def update_scroll_region(event = None):
	    # Update the scroll region to encompass the frame
	    canvas.configure(scrollregion=canvas.bbox("all"))
	    
	    # get the frame size
	    frame_width = roots.winfo_width()
	    frame_height = roots.winfo_height()

	    # Calculate the coordinates to center the frame
	    x = (root.winfo_width() - frame_width) // 2
	    y = 0

	    #print("x: " + str(x) + " root: "+ str(root.winfo_width()) + " frame: " + str(frame_width))

	    # Update the window position within the canvas
	    canvas.coords(window_id, x, y)

		# Clear previous rectangles (if any)
	    #canvas.delete("debug")
	    
	    # Draw a rectangle around the roots frame
	    #canvas.create_rectangle(x, y, x + frame_width, y + frame_height, outline="red", tags="debug")

	roots.bind("<Configure>", update_scroll_region)
	canvas.bind("<Configure>", update_scroll_region)


	# Pack the scrollbar and canvas
	scrollbar.pack(side="right", fill="y")
	canvas.pack(side="left", fill="both", expand=True)

	rootf = tkinter.Frame(roots)

	update_scroll_region(None)




	def on_mouse_wheel(event):
	    # On Windows, event.delta is the amount of scrolling
	    if event.num == 5 or (event.num == 4 and event.delta < 0):  # Scroll down
	        canvas.yview_scroll(1, "units")
	    elif event.num == 4 or (event.num == 5 and event.delta > 0):  # Scroll up
	        canvas.yview_scroll(-1, "units")

	root.bind_all("<MouseWheel>", on_mouse_wheel)  # For Windows
	root.bind_all("<Button-4>", on_mouse_wheel)  # For Linux scroll up
	root.bind_all("<Button-5>", on_mouse_wheel)  # For Linux scroll down



	root.title("Eurolotto!")
	space = tkinter.Label(roots, text="\n", justify=tkinter.LEFT)
	space.pack()


	buttonSwitchBias = tkinter.Button(roots,text=biasButtionText,command=lambda: biasButtionFunc())
	buttonSwitchBias.pack()

	buttons = tkinter.Frame(roots)

	buttonAdd = tkinter.Button(buttons,text = "+",command=lambda: changeUI(True))
	buttonGen = tkinter.Button(buttons,text = "Alle Generieren",command=lambda: generate(fields))
	buttonSub = tkinter.Button(buttons,text = "-",command=lambda: changeUI(False))
	buttonAdd.pack(side = tkinter.LEFT)
	buttonGen.pack(side = tkinter.LEFT)
	buttonSub.pack(side = tkinter.LEFT)

	#buttonSwitchBias = tkinter.Button(buttons,text=biasButtionText,command=lambda: biasButtionFunc())
	#buttonSwitchBias.pack()

	buttons.pack()

# TODO - maximize + minize needs to reposition the thing - NOT POSSIBLE!


def clearFields(fields, field = None):
	
	if (field == None):
		superI = 0
		while superI < len(fields):

			for row in range(2):
				for col in range(6):
					fields[superI][1][row][col]["bg"] = "#d9d9d9"


			for row in range(5):
				for col in range(10):
					fields[superI][0][row][col]["bg"] = "#d9d9d9"

			superI = superI + 1


	else: # field defined
		for row in range(2):
				for col in range(6):
					fields[field][1][row][col]["bg"] = "#d9d9d9"

		for row in range(5):
			for col in range(10):
				fields[field][0][row][col]["bg"] = "#d9d9d9"


def fix_old_result(index): #pads old_results till it contains index
	
	global old_results

	while len(old_results) <= index:
		old_results.append([])

		

def generate_body(fields,field):
	res = generateNumbers()
	from50 = res[0]
	from12 = res[1]

	if cfg_consoleOut == True:
		print(res)

	if not cfg_noWindow:
		from50s = ""
		i = 0
		while i < len(from50):
			from50s = from50s + str(from50[i])
			if (i < len(from50)-1):
				from50s = from50s + ", "
			i = i + 1

		from12s = ""
		i = 0
		while i < len(from12):
			from12s = from12s + str(from12[i])
			if (i < len(from12)-1):
				from12s = from12s + ", "
			i = i + 1

			
			if not cfg_noWindow:
				setFields(res,fields,field)

	return res

def generate(fields, field = None):

	global old_results

	if (field == None): # if we generate all fields

		if not cfg_noWindow:
			clearFields(fields)

		old_results = []
		superI = 0
		while superI < len(fields):
			res = generate_body(fields,superI)

			old_results.append(res)
			superI = superI + 1

	else: # we selected a specific field
		clearFields(fields,field)
		fix_old_result(field)
		res = generate_body(fields,field)
		old_results[field] = res

def initUI(numFields):

	global roots
	global rootf
	rootf.destroy()
	rootf = tkinter.Frame(roots)

	fields = []

	superI = 0
	while superI < numFields:

		from12Frame = tkinter.Frame(rootf)
		from12Field = [[],[]]

		from50Frame = tkinter.Frame(rootf)
		from50Field = [[],[],[],[],[]]

		fields.append([from50Field,from12Field])



		newline = tkinter.Label(rootf,text = "\nSchein "+str(superI+1))
		
		button = tkinter.Button(rootf,text = "Generieren",command=lambda i = superI: generate(fields,i))

		# 2 from 12
		i = 1
		while i <= 6:
			from12Field[0].append(tkinter.Label(from12Frame,text = "0"+str(i), relief=tkinter.GROOVE, borderwidth=5))
			i = i + 1
		while i <= 12:
			if i >= 10:
				from12Field[1].append(tkinter.Label(from12Frame,text = str(i), relief=tkinter.GROOVE, borderwidth=5))
			else:
				from12Field[1].append(tkinter.Label(from12Frame,text = "0"+str(i), relief=tkinter.GROOVE, borderwidth=5))
			i = i + 1


		for row in range(2):
			for col in range(6):
				from12Field[row][col].grid(row=row, column=col)



		# 5 from 50

		i = 1
		while i < 10:
			from50Field[0].append(tkinter.Label(from50Frame,text = "0"+str(i), relief=tkinter.GROOVE, borderwidth=5))
			i = i + 1
		from50Field[0].append(tkinter.Label(from50Frame,text = "10", relief=tkinter.GROOVE, borderwidth=5))

		i = 11
		while i <= 50:
			from50Field[int((i-1)/10)].append(tkinter.Label(from50Frame,text = str(i), relief=tkinter.GROOVE, borderwidth=5))
			i = i + 1


		for row in range(5):
			for col in range(10):
				from50Field[row][col].grid(row=row, column=col)

		newline.pack()
		button.pack()
		from50Frame.pack()

		newline2 = tkinter.Label(rootf,text = "\n")
		newline2.pack()

		from12Frame.pack()

		newline = tkinter.Label(rootf,text = "\n")
		newline.pack()

		rootf.pack()

		superI = superI + 1

	return fields



def setFields(result_array,fields,field):

	if (result_array == []):
		return;

	i = 0
	while i < len(result_array[0]):
		j = result_array[0][i]
		#print(str(j) + ": " + str(int((j-1)/10)) + "," + str(j%10))
		fields[field][0][int((j-1)/10)][j%10]["bg"] = "yellow"
		i = i + 1

	#print("next")

	i = 0
	while i < len(result_array[1]):
		j = result_array[1][i]
		#print(str(j) + ": " + str(int((j-1)/6)) + "," + str(j%6))
		fields[field][1][int((j-1)/6)][j%6]["bg"] = "yellow"
		i = i + 1
	#print("done!")




fields = None
old_results = None


def changeUI(add):
	global fields
	global cfg_count

	if (add == True):
		cfg_count = cfg_count + 1
	else:
		if (cfg_count > 1):
			cfg_count = cfg_count - 1
		else:
			return

	fields = initUI(cfg_count)

	# resore old values
	i = 0
	while i < len(old_results) and i < cfg_count:
		setFields(old_results[i],fields,i)
		i = i + 1


if not cfg_noWindow:
	fields = initUI(cfg_count)
else:
	i = 0
	fields = []
	while i < cfg_count:
		fields.append(None) # we only need the right lenght, if we dont use the window
		i = i + 1

generate(fields)

if not cfg_noWindow:
	#root.after_idle(SizeManager)
	root.mainloop();