#Lets Randomize Relics
#Made by setz

#@splixel on twitter
#twitch.tv/skiffain

#too lazy for licenses, pretend I attached WTFPL
#(do what the fuck you want with this)

#error_recalc comes from https://www.romhacking.net/utilities/1264/

#Conditions for flight are one of the following
	#Soul of Bat (ez mode)
	#Gravity Boots + Leap Stone (chaining gravity jumps)
	#Form of Mist + Power of Mist (fly as mist)

#Requirements for accessing castle 2 are
	#Flight
	#Jewel of Open
	#Mist

import random
from subprocess import call
from binascii import hexlify
from datetime import datetime


FileName = "Castlevania - Symphony of the Night (USA) (Track 1).bin"
#RandomizeBossRelics = False #Not Supported

ShowItemPlacements = True #Print out a log of when items are placed

#RandoSeed = 1234567890
RandoSeed = 0


#Ability Checks
HasLeapStone = False
HasGravityBoots = False
HasJewelOfOpen = False
HasMist = False
HasPowerOfMist = False
HasBat = False
HasWolf = False
HasSonar = False
HasMermanStatue = False
InvertedCastleOK = False

#TODO
	#accept args
	#args: Player Seed input
	#args for other options
	#Options to not randomize boss relics	
	#Copy files instead of just overwriting
	#do a hash check to ensure its editing the right file
	#possibly make a small frontend for it?

#Known Bugs
	#need to trace relics from left/right as well as up/down because of how sotn loads entities
		#List of known delinquents
		#Cube Of Zoe
		#Spirit Orb
		#Farie Scroll
		#Leap Stone
	#if Jewel of Open is collected, you can no longer buy the random relic from the Librarian, potentially causing a softlock.
        #location ID text is inaccurate
        #medusa fails to spawn a relic
	
#Some relics have doubles, so..
	#Relic ID/Name 			#RelicLocation ID 	#Cant Be Behind 			RL ID No-Gos
	#00	Soul of Bat 		00					
	#01	Fire of Bat 		01					
	#02	Echo of Bat 		02					Castle 2 					18 19 1a 1b 1c
	#03	Force of Echo 		03					
	#04	Soul of Wolf 		04					
	#05	Power of Wolf  		05					
	#05	Power of Wolf 		05					
	#06	Skill of Wolf 		06					
	#07	Form of Mist 		07					Castle 2, Mist Gates 		18 19 1a 1b 1c 00
	#08	Power of Mist 		08					
	#09	Gas Cloud 			09					
	#0A	Cube of Zoe 		0a					
	#0A Cube of Zoe  		0a					
	#0B	Spirit Orb			0b					
	#0C	Gravity Boots		0c					
	#0D	Leap Stone			0d					
	#0E	Holy Symbol			0e					
	#0F	Faerie Scroll		0f					
	#10	Jewel of Open		10					Castle 2, Jewel Doors 		18 19 1a 1b 1c 0d 0e 11 15
	#11	Merman Statue		11					Holy Snorkel Location 		0e
	#12	Bat Card			12					
	#13	Ghost Card			13					
	#14	Faerie Card			14					
	#15	Demon Card			15					
	#16	Sword Card			16					
	#17	Sprite Card			--					
	#18	Nosedevil Card 		--					
	#19	Heart of Vlad		17					
	#19	Heart of Vlad		17					
	#1A	Tooth of Vlad		18					
	#1A	Tooth of Vlad		18					
	#1B	Rib of Vlad			19					
	#1B	Rib of Vlad			19					
	#1C	Ring of Vlad		1a					
	#1C	Ring of Vlad		1a					
	#1D Eye of Vlad			1b					
	#1D Eye of Vlad			1b
NamedRelics = ["Soul of Bat","Fire of Bat","Echo of Bat","Force of Echo","Soul of Wolf","Power of Wolf",
               "Skill of Wolf","Form of Mist","Power of Mist","Gas Cloud","Cube of Zoe","Spirit Orb","Gravity Boots",
               "Leap Stone","Holy Symbol","Faerie Scroll","Jewel of Open","Merman Statue","Bat Card","Ghost Card",
               "Faerie Card","Demon Card","Sword Card","Heart of Vlad","Tooth of Vlad","Rib of Vlad","Ring of Vlad","Eye of Vlad"]
NamedLocations = ["Entrance","Castle Keep (Upper Left)","Colosseum","The Creature","Clock Tower",
                  "Alchemy Laboratory (Ceiling)","Reverse Caverns","Underground Caverns (Left)",
                  "Castle Keep (Upper Right)","Medusa","Alchemy Laboratory (Pedestal)","Marble Gallery, Lower",
                  "Alchemy Laboratory (Boss Room)","Underground Caverns (Right)","Olrox's Quarters (Ceiling)",
                  "Long Library (Books)","Long Library (Librarian)","Olrox's Quarters (Boss Room)","Outer Wall",
                  "Long Library (Upper Left)","Darkwing Bat","Death","Marble Gallery (Clock Room)",
                  "Long Library (Boss Room)","Abandoned Mine","Floating Catacombs","Castle Keep (Lower)","Akmodan II"]
RelicLocation = [0x047a5b66, 0x0557535e, 0x04aa4156, 0x0526e6a8, 0x049d6596, 0x04b6b9b4, 0x054b1d5a, 0x043c578a, 
	0x05610db8, 0x04cfcb16, 0x04b6b946, 0x048fd1fe, 0x048fc9ba, 0x05610dc2, 0x04c34ee6, 0x047a5720, 
	0x047a321c, 0x04c35174, 0x054b1d58, 0x05611958, 0x047a5784, 0x045ea95e, 0x04aa3f76, 0x06306ab2, 
	0x05051d52, 0x069d2b1e, 0x059bdb30, 0x04da65f2]
DoubleLocation = [0, 0, 0, 0, 0, 0x053f971c, 0, 0, 
	0x0561142C, 0, 0x053F969A, 0, 0, 0, 0, 0,
	0, 0, 0, 0x0561127c, 0, 0, 0, 0x04e335b4, 
	0x067d1630, 0x050fa914, 0x059ee2e4, 0x0662263a]
TripleLocation = [0, 0, 0, 0, 0, 0, 0, 0, 
	0, 0, 0x04b6b08a, 0x048fe280, 0, 0, 0, 0,
	0, 0, 0, 0, 0, 0, 0, 0, 
	0, 0, 0, 0]
QuadrupleLocation = [0, 0, 0, 0, 0, 0, 0, 0, 
	0, 0, 0x053f8e2e, 0, 0, 0, 0, 0,
	0, 0, 0, 0, 0, 0, 0, 0, 
	0, 0, 0, 0]
RelicList = []
RelicList = [bytearray([0x00]),
	bytearray([0x01]),
	bytearray([0x02]),
	bytearray([0x03]),
	bytearray([0x04]),
	bytearray([0x05]),
	bytearray([0x06]),
	bytearray([0x07]),
	bytearray([0x08]),
	bytearray([0x09]),
	bytearray([0x0a]),
	bytearray([0x0b]),
	bytearray([0x0c]),
	bytearray([0x0d]),
	bytearray([0x0e]),
	bytearray([0x0f]),
	bytearray([0x10]),
	bytearray([0x11]),
	bytearray([0x12]),
	bytearray([0x13]),
	bytearray([0x14]),
	bytearray([0x15]),
	bytearray([0x16]),
	bytearray([0x19]),
	bytearray([0x1a]),
	bytearray([0x1b]),
	bytearray([0x1c]),
	bytearray([0x1d])]

RelicsUsed = []
LocationsUsed = []
for i in range(0, len(RelicList)):
	RelicsUsed.append(False)
	LocationsUsed.append(False)

def ReplaceByte(ByteLocation, NewByte): 
	with file(FileName, "r+b") as HackThisRom: #Comment these out during testing.
		HackThisRom.seek(ByteLocation) #Comment these out during testing.
		HackThisRom.write(NewByte) #Comment these out during testing.
	return True

def PlaceItem(Item, Location):
	if ShowItemPlacements:
		print("Placing Item: "+str(NamedRelics[Item])) #DEBUG
		#print("Location a: "+str(hex(RelicLocation[Location])))
	ReplaceByte(RelicLocation[Location], RelicList[Item])

	if (DoubleLocation[Location] != 0):
		#if ShowItemPlacements:
			#print("Location b: "+str(hex(DoubleLocation[Location])))
		ReplaceByte(DoubleLocation[Location], RelicList[Item])		

	if (TripleLocation[Location] != 0):
		#if ShowItemPlacements:
			#print("Location c: "+str(hex(DoubleLocation[Location])))
		ReplaceByte(TripleLocation[Location], RelicList[Item])		

	if (QuadrupleLocation[Location] != 0):
		#if ShowItemPlacements:
			#print("Location d: "+str(hex(DoubleLocation[Location])))
		ReplaceByte(QuadrupleLocation[Location], RelicList[Item])		
	
	#Check abilities if possible
	global HasJewelOfOpen 
	global HasLeapStone
	global HasMist
	global HasPowerOfMist
	global HasGravityBoots
	global HasBat
	global HasWolf
	global HasSonar
	global HasMermanStatue

	if Item == 0x10:
		HasJewelOfOpen = True
	elif Item == 0xd:
		HasLeapStone = True
	elif Item == 0x7:
		HasMist = True
	elif Item == 0x8:
		HasPowerOfMist = True
	elif Item == 0xc:
		HasGravityBoots = True
	elif Item == 0x4:
		HasWolf = True
	elif Item == 0x0:
		HasBat = True
	elif Item == 0x2:
		HasSonar = True
	elif Item == 0x11:
		HasMermanStatue = True

	#Mark as used
	RelicsUsed[Item] = True
	LocationsUsed[Location] = True
	return True

def FindUnplacedRelic():
	RandIndex = random.randint(0, len(RelicList)-1)
	if RelicsUsed[RandIndex]:		
		return FindUnplacedRelic()
	else:
		return RandIndex

def FindUnplacedLocation(InputArray):
	if ShowItemPlacements:
		print("Valid Locations remaining: "+str(len(InputArray))+"\n") #DEBUG
	if len(InputArray)>0:
		RandIndex = InputArray[random.randint(0, len(InputArray)-1)]
	else: #DEBUG
		print("\nNo valid locations. Figuring out what went wrong...") #DEBUG
		print("\nUnplaced Items:") #DEBUG
		for i in range(0, 28): #DEBUG
			if not RelicsUsed[i]: #DEBUG
				print(NamedRelics[i]) #DEBUG
		print("\nUnused Locations:") #DEBUG
		for i in range(0, 28): #DEBUG
			if not LocationsUsed[i]:
				print(NamedLocations[i])
	if LocationsUsed[RandIndex]:
		return FindUnplacedLocation(InputArray)
	else:
		return RandIndex

def SoftUnlock():
	#print(str(HasJewelOfOpen)+" | "+str(HasLeapStone)+" | "+str(HasMist)+" | "+str(HasPowerOfMist)+" | "+str(HasGravityBoots)+" | "+str(HasBat)+" | "+str(HasSonar)+" | "+str(HasMermanStatue))
	#List of available locations
	LocationsAvailable = []

	global InvertedCastleOK #Global check for the Inverted Castle requirements. For use to narrow softlock prevention mechanisms and allow for more complex seeds.
	global LoopPrevention #DEBUG
	
	
	#Starting Areas
	if LocationsUsed[0x04] == False:
		LocationsAvailable.append(0x04)
	if LocationsUsed[0x0a] == False:
		LocationsAvailable.append(0x0a)
	if LocationsUsed[0x0b] == False:
		LocationsAvailable.append(0x0b)
	if LocationsUsed[0x0f] == False:
		LocationsAvailable.append(0x0f)
	if LocationsUsed[0x10] == False:
		LocationsAvailable.append(0x10)
	
	#Restricted Areas
	if ShowItemPlacements:
		print("***Placement Restrictions***") #DEBUG
	if HasMist and (HasLeapStone or HasGravityBoots or HasBat):
		#Soul of Bat Vanilla
		if LocationsUsed[0x00] == False:
			LocationsAvailable.append(0x00)
	else:
		if ShowItemPlacements:
			print("No Mist | No Leap Stone/Gravity Boots/Bat") #DEBUG
	if HasBat or (HasGravityBoots and HasLeapStone) or (HasMist and HasPowerOfMist):
		#Flight only
		if LocationsUsed[0x01] == False:
			LocationsAvailable.append(0x01)
		if LocationsUsed[0x05] == False:
			LocationsAvailable.append(0x05)
		if LocationsUsed[0x08] == False:
			LocationsAvailable.append(0x08)
		if LocationsUsed[0x0c] == False:
			LocationsAvailable.append(0x0c)
		if LocationsUsed[0x13] == False:
			LocationsAvailable.append(0x13)
		if LocationsUsed[0x16] == False:
			LocationsAvailable.append(0x16)
	else:
		if ShowItemPlacements:
			print("No Flight") #DEBUG
	if (HasBat or (HasMist and HasPowerOfMist) or (HasGravityBoots and HasLeapStone)) and (HasMist or HasWolf or HasBat):
		if LocationsUsed[0x02] == False: #Olrox's Prize
			LocationsAvailable.append(0x02)
	else:
		if ShowItemPlacements:	
			print("Cannot get to Olrox") #DEBUG
	if HasGravityBoots or HasBat or (HasMist and HasPowerOfMist):
		#Gravity Boots or better
		if LocationsUsed[0x06] == False:
			LocationsAvailable.append(0x06)
		if LocationsUsed[0x12] == False:
			LocationsAvailable.append(0x12)
		if LocationsUsed[0x14] == False:
			LocationsAvailable.append(0x14)
	else:
		if ShowItemPlacements:	
			print("No GravityBoots/Bat/PowerOfMist") #DEBUG
	if HasLeapStone or HasGravityBoots or HasBat or (HasMist and HasPowerOfMist):
		#Leapstone or better
		if LocationsUsed[0x07] == False:
			LocationsAvailable.append(0x07)
		if LocationsUsed[0x0d] == False:
			LocationsAvailable.append(0x0d) #Colosseum - only required if leap stone?
	else:
		if ShowItemPlacements:	
			print("No Leap Stone/GravityBoots/Bat/PowerOfMist") #DEBUG
	if HasJewelOfOpen:
		#Bottom of the castle
		if LocationsUsed[0x11] == False:
			LocationsAvailable.append(0x11)
	else:
		if ShowItemPlacements:	
			print("No Jewel of Open") #DEBUG
	if HasJewelOfOpen and HasLeapStone or HasBat or (HasMist and HasPowerOfMist):
		if LocationsUsed[0x15] == False: #Demon card a bitch
			LocationsAvailable.append(0x15)
	else:
		if ShowItemPlacements:
			print("No Jewel of Open | No Leap Stone/Bat/PowerOfMist") #DEBUG
	if (HasMermanStatue and HasJewelOfOpen) or RelicsPlaced == 27:
		#holy snorkel vanilla
		if LocationsUsed[0x0e] == False:
			LocationsAvailable.append(0x0e)
	else:
		if ShowItemPlacements:
			print("No Jewel of Open | No Merman Statue") #DEBUG


	
	if HasJewelOfOpen and HasMist and (HasBat or HasPowerOfMist or (HasLeapStone and HasGravityBoots)) and ((HasBat and HasSonar) or HasPowerOfMist):
		#Castle 2 - Jewel of Open, Mist, Flight, and one of the two relic combinations that can pass the Spike Breaker room.
		InvertedCastleOK = True
		if LocationsUsed[0x03] == False:
			LocationsAvailable.append(0x03)
		if LocationsUsed[0x09] == False:
			LocationsAvailable.append(0x09)
		if LocationsUsed[0x17] == False:
			LocationsAvailable.append(0x17)
		if LocationsUsed[0x18] == False:
			LocationsAvailable.append(0x18)
		if LocationsUsed[0x19] == False:
			LocationsAvailable.append(0x19)
		if LocationsUsed[0x1a] == False:
			LocationsAvailable.append(0x1a)
		if LocationsUsed[0x1b] == False:
			LocationsAvailable.append(0x1b)
	else:
		if ShowItemPlacements:
			print("Castle 2 Unavailable") #DEBUG
	if ShowItemPlacements:
		print
	ThisRel = FindUnplacedRelic()
	if (InvertedCastleOK == False and len(LocationsAvailable) == 2 and RelicsPlaced >= 16) or len(LocationsAvailable) == 1:
		#Only one location left.
                #Two locations while Castle2 requirements have not been met and most items have been placed.
		#Check to see if its the last item in the game. If not, give an item that will unlock more items
		if ShowItemPlacements:
			print("Running out of valid locations -"), #DEBUG
		if RelicsPlaced == 26: #Prevents Mist or Jewel from being the last relic placed, to avoid softlocks where they are put behind their own requirement.
			if HasMist == False:
				ThisRel = 0x07
				if ShowItemPlacements:
					print("Forcing placement of Form of Mist") #DEBUG
			elif HasJewelOfOpen == False:
				ThisRel = 0x10
				if ShowItemPlacements:
					print("Forcing placement of Jewel of Open") #DEBUG                      
		elif HasMist == False and RelicsPlaced >= 16: #Force placement of Mist if near the Castle2 cutoff. Prevents softlock.
			ThisRel = 0x07
			if ShowItemPlacements:
				print("Forcing placement of Form of Mist") #DEBUG
		elif HasJewelOfOpen == False or HasLeapStone == False or HasGravityBoots == False:
			TempRNG = random.randint(0,2) #Randomizes between Jewel of Open, Leap Stone, and Gravity Boots.
			while TempRNG is not None:
				if TempRNG == 0 and HasJewelOfOpen == False:
					if ShowItemPlacements:
						print("Forcing placement of Jewel of Open") #DEBUG
					ThisRel = 0x10
					TempRNG = None #Found a valid item. Escaping loop.
				elif TempRNG == 1 and HasLeapStone == False:
					ThisRel = 0x0D
					TempRNG = None #Found a valid item. Escaping loop.
					if ShowItemPlacements:
						print("Forcing placement of Leap Stone") #DEBUG
				elif TempRNG == 2 and HasGravityBoots == False:
					ThisRel = 0x0C
					TempRNG = None #Found a valid item. Escaping loop.
					if ShowItemPlacements:
						print("Forcing placement of Gravity Boots") #DEBUG
				else:
					TempRNG = random.randint(0,2) #Reroll if the RNG picks an item already placed.

		elif HasMist == False or HasMermanStatue == False:
			TempRNG = random.randint(0,1) #Randomizes between Form of Mist or Merman Statue.
			while TempRNG is not None:
				if TempRNG == 0 and HasMist == False:
					ThisRel = 0x07
					TempRNG = None #Found a valid item. Escaping loop.
					if ShowItemPlacements:
						print("Forcing placement of Form of Mist") #DEBUG
				elif TempRNG == 1 and HasMermanStatue == False:
					ThisRel = 0x11
					TempRNG = None #Found a valid item. Escaping loop.
					if ShowItemPlacements:
						print("Forcing placement of Merman Statue") #DEBUG
				else:
					TempRNG = random.randint(0,1) #Reroll if the RNG picks an item already placed.
		elif HasBat == False or HasPowerOfMist == False:
			TempRNG = random.randint(0,1) #Randomizes between Soul of Bat and Power of Mist.
			while TempRNG is not None:
				if TempRNG == 0 and HasBat == False:
					ThisRel = 0x00
					if ShowItemPlacements:
						print("Forcing placement of Soul of Bat") #DEBUG
					TempRNG = None #Found a valid item. Escaping loop.
				elif TempRNG == 1 and HasPowerOfMist == False:
					ThisRel = 0x08
					if ShowItemPlacements:
						print("Forcing placement of Power of Mist") #DEBUG
					TempRNG = None #Found a valid item. Escaping loop.
				else:
					TempRNG = random.randint(0,2) #Reroll if the RNG picks an item already placed.
		elif HasSonar == False or HasPowerOfMist == False:
			TempRNG = random.randint(0,1) #Randomizes between Echo of Bat and Power of Mist.
			while TempRNG is not None:
				if TempRNG == 0 and HasSonar == False:
					ThisRel = 0x02
					if ShowItemPlacements:
						print("Forcing placement of Echo of Bat") #DEBUG
					TempRNG = None #Found a valid item. Escaping loop.
				elif TempRNG == 1 and HasPowerOfMist == False:
					ThisRel = 0x08
					if ShowItemPlacements:
						print("Forcing placement of Power of Mist") #DEBUG
					TempRNG = None #Found a valid item. Escaping loop.
				else:
					TempRNG = random.randint(0,1) #Reroll if the RNG picks an item already placed.
		else: #DEBUG
			if ShowItemPlacements:
				print("Last relic") #DEBUG
	else:
		ThisRel = FindUnplacedRelic()
	ThisLoc = FindUnplacedLocation(LocationsAvailable)
	if ShowItemPlacements:
		print("Attempting to place item in location (currently inaccurate): "+NamedLocations[ThisLoc]) #DEBUG
	#Items are never allowed in these locations
	if ThisRel == 0x02 and LoopPrevention < 8 and RelicsPlaced < 21: #Echo of Bat
		if ThisLoc == 0x18 or ThisLoc == 0x19 or ThisLoc == 0x1a or ThisLoc == 0x1b or ThisLoc == 0x1c:
			if ShowItemPlacements:
				print("Invalid placement of Echo of Bat. Retrying...") #DEBUG
			LoopPrevention += 1
			return SoftUnlock()
	elif ThisRel == 0x07 and LoopPrevention < 8: #Form of Mist
		if ThisLoc == 0x18 or ThisLoc == 0x19 or ThisLoc == 0x1a or ThisLoc == 0x1b or ThisLoc == 0x1c or ThisLoc == 0x00:
			if ShowItemPlacements:
				print("Invalid placement of Form of Mist. Retrying...") #DEBUG
			LoopPrevention += 1
			return SoftUnlock()
	elif ThisRel == 0x10 and LoopPrevention < 8: #Jewel of Open
		if ThisLoc == 0x18 or ThisLoc == 0x19 or ThisLoc == 0x1a or ThisLoc == 0x1b or ThisLoc == 0x1c or ThisLoc == 0x0d or ThisLoc == 0x0e or ThisLoc == 0x11 or ThisLoc == 0x15:
			if ShowItemPlacements:
				print("Invalid placement of Jewel of Open. Retrying...") #DEBUG
			LoopPrevention += 1
			return SoftUnlock()
	elif ThisRel == 0x11 and LoopPrevention < 8 and RelicsPlaced < 27: #Merman Statue
		if ThisLoc == 0x0e:
			if ShowItemPlacements:
				print("Invalid placement of Merman Statue. Retrying...") #DEBUG
			LoopPrevention += 1
			return SoftUnlock()
	elif LoopPrevention >= 8:
		raw_input("Unable to place item into its own restriction. Seed is broken...")
		exit()
	else:
		LoopPrevention = 0
	retval = [ThisRel, ThisLoc]
	
	return retval

def SetSeed():
	Seed = 0 #Initialize return variable.
	while Seed == 0: #Keep running until a valid seed is set.
		try:
			AskForSeed = int(raw_input("Enter a seed number (up to 12 digits), or enter 0 to generate one randomly.\n?"))
			if int(AskForSeed) == 0: #User wants to generate a random seed.
				print("Generating Random Seed...")
				Seed = int(datetime.time(datetime.now()).strftime("%H%M%S%f")) #Set return variable to current system time, as 12 digit integer.
				random.seed(Seed) #Initializes RNG to the generated timestamp.
				Seed = random.randint(1,999999999999) #Advances the RNG by one step and generates a 12 digit integer.
			elif (type(AskForSeed) == int or type(AskForSeed) == long) and len(str(AskForSeed)) <= 12 and AskForSeed > 0: #User entered a seed.
				Seed = AskForSeed #Pass user-entered seed to return variable.
			else: #User entered a negative number.
				print("Invalid input value.")
		except ValueError: #User entered a non-integer.
			print("Invalid input type.")
	AskForSeed = None #Garbage collection.
	return Seed

def main():
	print("Sotn Relic Randomizer")
	print("Your file name should be \""+FileName+"\"")
	print("To show spoilers, edit the script and set ShowItemPlacements to True")
	print("If this is your first time running, you will need to download error_recalc.exe and put it in the same directory as this script. You can grab it here: https://www.romhacking.net/utilities/1264/")
	print("")

	global RelicsPlaced #Tracked to allow the randomizer to "look ahead" when running out of locations, to avoid softlocks when multiple items must be placed to open a new area.
	global LoopPrevention #DEBUG
	LoopPrevention = 0 #DEBUG

	'''
	##############################################################################################################
	#DEBUG - Bulk Seed Testing for Crashes
	##############################################################################################################

	while True:
		
		RelicList = []
		RelicList = [bytearray([0x00]),
	bytearray([0x01]),
	bytearray([0x02]),
	bytearray([0x03]),
	bytearray([0x04]),
	bytearray([0x05]),
	bytearray([0x06]),
	bytearray([0x07]),
	bytearray([0x08]),
	bytearray([0x09]),
	bytearray([0x0a]),
	bytearray([0x0b]),
	bytearray([0x0c]),
	bytearray([0x0d]),
	bytearray([0x0e]),
	bytearray([0x0f]),
	bytearray([0x10]),
	bytearray([0x11]),
	bytearray([0x12]),
	bytearray([0x13]),
	bytearray([0x14]),
	bytearray([0x15]),
	bytearray([0x16]),
	bytearray([0x19]),
	bytearray([0x1a]),
	bytearray([0x1b]),
	bytearray([0x1c]),
	bytearray([0x1d])]
		for i in range(0, len(RelicList)):
			RelicsUsed[i] = False
			LocationsUsed[i] = False
		HasLeapStone = False
		HasGravityBoots = False
		HasJewelOfOpen = False
		HasMist = False
		HasPowerOfMist = False
		HasBat = False
		HasWolf = False
		HasSonar = False
		HasMermanStatue = False
		InvertedCastleOK = False
		RelicsPlaced = 0
              
		Seed = int(datetime.time(datetime.now()).strftime("%H%M%S%f")) #Set return variable to current system time, as 12 digit integer.
		random.seed(Seed) #Initializes RNG to the generated timestamp.
		Seed = random.randint(1,999999999999) #Advances the RNG by one step and generates a 12 digit integer.
		random.seed(Seed) #Initializes RNG to the generated seed.
		print("Seed is \""+format(int(Seed),'012d')+"\"") #Displays seed number as 12 digit integer.
		for i in range(0, len(RelicList)):
			print("\n---------------------\nRelics Placed:"+str(i)) #DEBUG
			LoopPrevention = 0 #DEBUG
			RelicsPlaced = i #Sets global variable.
			PlsNoSoftlock = SoftUnlock()
			ThisRelic = PlsNoSoftlock[0]
			ThisLocation = PlsNoSoftlock[1]
			PlaceItem(ThisRelic, ThisLocation)
		print("Done")

	##############################################################################################################
	'''

	RandoSeed = SetSeed() #Returns random or user-entered integer, up to 12 digits.
	random.seed(RandoSeed) #Initializes RNG to the generated seed.
	print("Seed is \""+format(int(RandoSeed),'012d')+"\"") #Displays seed number as 12 digit integer.
	raw_input("Press Enter to continue...") #Gives user time to write down the seed number.
	
	#Do some shuffling things, make sure things arent impossible to access
	#Make things always possible later
	print("Shuffling Relics..")

	#Place the rest of the items
	for i in range(0, len(RelicList)):
		if ShowItemPlacements:
			print("---------------------\nRelics Placed:"+str(i)+"\n") #DEBUG
		else:
			print("Relics Placed:"+str(i))
		RelicsPlaced = i #Sets global variable.
		PlsNoSoftlock = SoftUnlock()
		ThisRelic = PlsNoSoftlock[0]
		ThisLocation = PlsNoSoftlock[1]
		PlaceItem(ThisRelic, ThisLocation)
	print("Relics Placed:28\n")

	print("Bytes Written, Fixing ECC..")

	#Windows
	#call(["error_recalc.exe", FileName, "1"])

	#Not Windows
	call(["wine", "error_recalc.exe", FileName, "1"]) #comment these out during testing

	print("Done")

if __name__ == '__main__':
	main()
