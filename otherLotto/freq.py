import sys
import struct
import os.path


expectedArgsC = 1 + 1 +49 + 9 # progamm name + number total games + 49 numbers + 9 numbers

if len(sys.argv) != expectedArgsC and len(sys.argv) != expectedArgsC + 1 and len(sys.argv) != 2 and len(sys.argv) != 3:
	print("Usage: "+str(sys.argv[0]) + " [total games] [amount number 1] [amount number 2] ... [amount number 49] [amount extra number 1] [amount extra number 2] .. [amount extra number 9] (optional output filename)")
	print("\nAlternative Usage:"+str(sys.argv[0]) +" [file to load the other arguments from] (optional output filename)")
	exit()


print("parsing args")

totalGames = 0
numbersOffset = 2
outputFile = "./freq.bin"
argv = []



# set output file correctly
if (len(sys.argv) == 3):
	outputFile = sys.argv[2]
if (len(sys.argv) == expectedArgsC+1):
	outputFile = sys.argv[expectedArgsC]
	



if len(sys.argv) == 2:

	# if we load from args file
	with open(sys.argv[1],"r") as file:
		data = file.readline().split(' ')


		if len(data) < (49+9+1):
			print("not enough args in the args file!")
			exit()
		if len(data) > (49+9+1):
			print("too many args in the args file!")
			exit()

		if not data[0].isdigit():
			print ("please only input numbers and optional file paths, and dont mix them up!")
			exit()
		argv = [sys.argv[0],int(data[0])]
		totalGames = argv[1]

		i = 2
		while i <= len(data): # must be equals here or else we dont read all data!
			if not data[i-1].isdigit():
				print ("please only input numbers and optional file paths, and dont mix them up!")

			argv.append(int(data[i-1]))
			i = i + 1

		if len(argv) != expectedArgsC:
			print("args corruption! progammer error!")
			print(len(argv))
			print(expectedArgsC)
			print(argv)
			exit()
else:
	if not totalGames.isdigit():
		print ("please only input numbers and optional file paths, and dont mix them up!")
		exit()
	totalGames = int(sys.argv[1])

	i = 0
	while i < len(sys.argv):
		if not sys.argv[i].isdigit():
			print ("please only input numbers and optional file paths, and dont mix them up!")
			exit()
		argv.append(int(sys.argv[i]))
		i = i + 1

# all args are now in argv


print("setup calulation")

freq = []
i = 0
while i < (49+9+1): # THIS LINE IS WEIRD! IT SHOULD BE 49+9, but for some reason its off by 1
	freq.append(0)
	i = i + 1


print("calculating percentages")

i = 0
while i < len(freq) and i < (49+9):
	freq[i] = (argv[numbersOffset + i] / totalGames) * 100
	i = i + 1


print("checking if output file exists")

if os.path.isfile(outputFile) or os.path.isdir(outputFile):

	print(outputFile + " already exists. Overwrite y/n :", end = "")
	while True:
		choice = input().upper()
		if choice == "Y" or choice == "YES":
			try:
				os.remove("demofile.txt") 
			except:
				print("failed to remove old file!")
				exit();
			break
		if choice == "N" or choice == "NO":
			exit()
		print("\nInvalid choice!\nOverwrite Y/N: ")

print("packing data...")

print(len(freq))

data = struct.pack("i "+\
"f f f f f f f f f f" +\
"f f f f f f f f f f" +\
"f f f f f f f f f f" +\
"f f f f f f f f f f" +\
"f f f f f f f f f" +\
\
"f f f f f f f" +\
"f f",\
totalGames,\
freq[0],freq[1],freq[2],freq[3],freq[4],freq[5],freq[6],freq[7],freq[8],freq[9],\
freq[10],freq[11],freq[12],freq[13],freq[14],freq[15],freq[16],freq[17],freq[18],freq[19],\
freq[20],freq[21],freq[22],freq[23],freq[24],freq[25],freq[26],freq[27],freq[28],freq[29],\
freq[30],freq[31],freq[32],freq[33],freq[34],freq[35],freq[36],freq[37],freq[38],freq[39],\
freq[40],freq[41],freq[42],freq[43],freq[44],freq[45],freq[46],freq[47],freq[48],\
\
freq[50],freq[51],freq[52],freq[53],freq[54],freq[55],freq[56],freq[57],freq[58])


print("writing data")

with open(outputFile,"wb") as file:
	file.write(data)



