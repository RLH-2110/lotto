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
		return min(random.randrange(1,p1o10),maxValue-1) 	 # -1, because we added 1 before
	if (select <= 40):
		return min(random.randrange(p1o10,p2o10),maxValue-1) # -1, because we added 1 before
	if (select <= 55):
		return min(random.randrange(p2o10,p3o10),maxValue-1) # -1, because we added 1 before
	if (select <= 67):
		return min(random.randrange(p3o10,p4o10),maxValue-1) # -1, because we added 1 before
	if (select <= 77):
		return min(random.randrange(p4o10,p5o10),maxValue-1) # -1, because we added 1 before
	if (select <= 85):
		return min(random.randrange(p5o10,p6o10),maxValue-1) # -1, because we added 1 before
	if (select <= 91):
		return min(random.randrange(p6o10,p7o10),maxValue-1) # -1, because we added 1 before
	if (select <= 96):
		return min(random.randrange(p7o10,p8o10),maxValue-1) # -1, because we added 1 before
	if (select <= 99):
		return min(random.randrange(p8o10,p9o10),maxValue-1) # -1, because we added 1 before
	return min(random.randrange(p9o10,p10o10),maxValue-1) 	 # -1, because we added 1 before

def weightedRandomTest(i):
	counter = [0]*50

	while i > 0:
		rand = weightedRandom(49)
		counter[rand] = counter[rand] + 1
		i = i - 1

	i = 49
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
		              "f f f f f f f f"

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

	num49 = []
	num9 = []

	i = 1 # skip the integer for the total games
	while i < 49 + 1:
		num49.append(unpacked_data[i])
		i = i + 1

	while i < 9 + 1 + 49:
		num9.append(unpacked_data[i])
		i = i + 1


	# unsorted
	num49u = num49[:]
	num9u = num9[:]

	# sorted
	num49.sort(reverse=True)
	num9.sort(reverse=True)

	# indexes sorted by freqency
	num49r = []
	num9r = []

	i = 0
	while (i < len(num49)):
		index = num49u.index(num49[i])
		num49u[index] = None
		num49r.append(index)
		i = i + 1

	i = 0
	while (i < len(num9)):
		index = num9u.index(num9[i])
		num9u[index] = None
		num9r.append(index)
		i = i + 1


	biasedList.append(num49r)
	biasedList.append(num9r)
	



# get list if we want biased generation

if (cfg_biased == True):
	if (createBiasedList() == False):
		exit(-1)

# debug print
#print("biased list:")
#print(biasedList)



def generateNumbers():

	from49 = [0]*6
	from9 = [0]*1

	i = 0
	while i < len(from49):

		rand = 0

		# generate random number, untill its uniqe
		if (cfg_biased == False):
			rand = random.randrange(1,49+1)
		else:
			rand = weightedRandom(49)


		while checkUniqe(from49,rand) == False:
			if (cfg_biased == False):
				rand = random.randrange(1,49+1)
			else:
				rand = weightedRandom(49)


		from49[i] = rand
		i = i + 1

	i = 0
	while i < len(from9):

		rand = 0
		# generate random number, untill its uniqe
		if (cfg_biased == False):
			rand = random.randrange(1,9+1)
		else:
			rand = weightedRandom(9)

		while checkUniqe(from9,rand) == False:
			if (cfg_biased == False):
				rand = random.randrange(1,9+1)
			else:
				rand = weightedRandom(9)


		from9[i] = rand
		i = i + 1

	return from49,from9





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
					if (row == 1 and col >= 3):
						break
					fields[superI][1][row][col]["bg"] = "#d9d9d9"


			for row in range(5):
				for col in range(10):
					if (row == 4 and col >= 9):
						break
					fields[superI][0][row][col]["bg"] = "#d9d9d9"

			superI = superI + 1


	else: # field defined
		for row in range(2):
			for col in range(6):
				if (row == 1 and col >= 3):
					break
				fields[field][1][row][col]["bg"] = "#d9d9d9"

		for row in range(5):
			for col in range(10):
				if (row == 4 and col >= 9):
					break
				fields[field][0][row][col]["bg"] = "#d9d9d9"


def fix_old_result(index): #pads old_results till it contains index
	
	global old_results

	while len(old_results) <= index:
		old_results.append([])

		

def generate_body(fields,field):
	res = generateNumbers()
	from49 = res[0]
	from9 = res[1]

	if cfg_consoleOut == True:
		print(res)

	if not cfg_noWindow:
		from49s = ""
		i = 0
		while i < len(from49):
			from49s = from49s + str(from49[i])
			if (i < len(from49)-1):
				from49s = from49s + ", "
			i = i + 1

		from9s = ""
		i = 0
		while i < len(from9):
			from9s = from9s + str(from9[i])
			if (i < len(from9)-1):
				from9s = from9s + ", "
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

		from9Frame = tkinter.Frame(rootf)
		from9Field = [[],[]]

		from49Frame = tkinter.Frame(rootf)
		from49Field = [[],[],[],[],[]]

		fields.append([from49Field,from9Field])



		newline = tkinter.Label(rootf,text = "\nSchein "+str(superI+1))
		
		button = tkinter.Button(rootf,text = "Generieren",command=lambda i = superI: generate(fields,i))

		# 1 from 9
		i = 1
		while i <= 6:
			from9Field[0].append(tkinter.Label(from9Frame,text = "0"+str(i), relief=tkinter.GROOVE, borderwidth=5))
			i = i + 1
		while i <= 9:
			from9Field[1].append(tkinter.Label(from9Frame,text = "0"+str(i), relief=tkinter.GROOVE, borderwidth=5))
			i = i + 1


		for row in range(2):
			for col in range(6):
				if (row == 1 and col >= 3):
					break
				from9Field[row][col].grid(row=row, column=col)



		# 6 from 49

		i = 1
		while i < 10:
			from49Field[0].append(tkinter.Label(from49Frame,text = "0"+str(i), relief=tkinter.GROOVE, borderwidth=5))
			i = i + 1
		from49Field[0].append(tkinter.Label(from49Frame,text = "10", relief=tkinter.GROOVE, borderwidth=5))

		i = 11
		while i <= 49:
			from49Field[int((i-1)/10)].append(tkinter.Label(from49Frame,text = str(i), relief=tkinter.GROOVE, borderwidth=5))
			i = i + 1


		for row in range(5):
			for col in range(10):
				if (row == 4 and col >= 9):
					break
				from49Field[row][col].grid(row=row, column=col)

		newline.pack()
		button.pack()
		from49Frame.pack()

		newline2 = tkinter.Label(rootf,text = "\n")
		newline2.pack()

		from9Frame.pack()

		newline = tkinter.Label(rootf,text = "\n")
		newline.pack()

		rootf.pack()

		superI = superI + 1

	return fields



def setFields(result_array,fields,field):

	if (result_array == []):
		return;

	#print(result_array)

	i = 0
	while i < len(result_array[0]):
		j = result_array[0][i]
		#print(str(j) + ": " + str(int((j-1)/10)) + "," + str((j-1)%10))
		fields[field][0][int((j-1)/10)][(j-1)%10]["bg"] = "yellow"
		i = i + 1

	#print("next")

	i = 0
	while i < len(result_array[1]):
		j = result_array[1][i]
		#print(str(j) + ": " + str(int((j-1)/6)) + "," + str((j-1)%6))
		fields[field][1][int((j-1)/6)][(j-1)%6]["bg"] = "yellow"
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