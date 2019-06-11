#!/usr/bin/env python
import os, sys
from modules.config import *
from modules.server import *
from modules.mods import *

header = '\
8888888b.     d8888 888b     d888 888b     d888\n\
888   Y88b   d88888 8888b   d8888 8888b   d8888\n\
888    888  d88P888 88888b.d88888 88888b.d88888\n\
888   d88P d88P 888 888Y88888P888 888Y88888P888\n\
8888888P" d88P  888 888 Y888P 888 888 Y888P 888\n\
888      d88P   888 888  Y8P  888 888  Y8P  888\n\
888     d8888888888 888   "   888 888   "   888\n\
888    d88P     888 888       888 888       888\n'

def mainmenu():
	while True:
		if getstatus():
			status = 'Online'
		else:
			status = 'Offline'
		os.system('clear')
		print(header)
		print()
		print("####Python Arma 3 Mod Manager####")
		print()
		print("Server state : " + status)
		print("Active profile : " + getactivelist())
		print()
		print("Please choose one of the options below : ")
		print()
		print("1	PAMM Settings")
		print("2	Arma 3 Server Settings")
		print("3	Mods Management")
		print()
		print("0 	Exit")
		choice = input("Your choice : ")
		menu(choice)

def menu(choice): #TODO rewrite similarly to modsmenu
	while True:
		try:
			choice = int(choice)
		except:
			break
		if choice == 0:
			os.system('clear')
			sys.exit()
		elif choice == 1:
			pammmenu()
		elif choice == 2:
			servermenu()
		elif choice == 3:
			modsmenu()
		else :
			break
		return

def pammmenu():
	while True:
		while True:
			os.system('clear')
			print(header)
			print()
			print("####PAMM Settings####")
			print()
			print("##Steam##")
			print()
			print("Path to steamcmd : " + getpath('steamcmd'))
			print("Steam user : " + getcreds('username'))
			print()
			print("1	Set path to steamcmd")
			print("2	Change Steam user")
			print("3	Change Steam password")
			print()
			print("##Arma##")
			print()
			print("Path to arma3server : " + getpath('arma3server'))
			print()
			print("4	Change path to arma3server")
			print()
			print("##Mods##")
			print()
			print("Path to mods : " + getpath('mods'))
			print()
			print("5	Change path to mods")
			print()
			print("9	Back to Main Menu")
			print("0	Exit")
			choice = input("Your choice : ")
			try:
				choice = int(choice)
			except:
				break
			if choice not in [1, 2, 3, 4, 5, 9, 0]:
				break
			else:
				if choice == 1:
					setconfig('steamcmd')
				elif choice == 2:
					setconfig('username')
				elif choice == 3:
					setconfig('password')
				elif choice == 4:
					setconfig('arma3server')
				elif choice == 5:
					setconfig('mods')
				elif choice == 9:
					break
				elif choice == 0:
					sys.exit()
				else:
					break
		break

def servermenu():
		while True:
			if getstatus():
				status = 'Online'
			else:
				status = 'Offline'
			os.system('clear')
			print(header)
			print()
			print("####Arma 3 Server Settings####")
			print()
			print("Server state : " + status)
			print("Active profile : " + getactivelist())
			print()
			print("1	Start Server")
			print("2	Stop Server")
			print("3	Update Server")
			print()
			print("9	Back to Main Menu")
			print("0	Exit")
			choice = input("Your choice : ")
			try:
				choice = int(choice)
			except:
				break
			if choice not in [1, 2, 3, 9, 0]:
				break
			else:
				if choice == 1:
					start(getactivelist())
				elif choice == 2:
					stop()
				elif choice == 3:
					update()
				elif choice == 9:
					break
				elif choice == 0:
					sys.exit()
				else:
					break

def modsmenu():
	while True:
		os.system('clear')
		print(header)
		print()
		print("####Mods Management####")
		print()
		print("Active profile : " + getactivelist())
		print()
		print("##Mod Profile##")
		print()
		print("1	Change active profile")
		print("2	Create profile")
		print("3	Delete profile")
		print()
		print("##Mod Management##")
		print()
		print("4	List Mods")
		print("5	Update Mods")
		print("6	Add Mod")
		print("7	Remove Mod")
		print("8	Repair Mods (Lowerize mod file names)")
		print()
		print("9	Back to Main Menu")
		print("0	Exit")
		choice = input("Your choice : ")
		try:
			choice = int(choice)
		except:
			input("Wrong choice")
			break
		if choice == 9:
			break
		elif choice == 0:
			sys.exit()
		elif choice in [1, 2, 3, 4, 5, 6, 7, 8]:
			modsmenuaction(choice)
		else:
			pass

def modsmenuaction( choice ):
	while True:
		if choice == 1:
			os.system('clear')
			print(header)
			print()
			print("####Mods Management####")
			print()
			print("Active profile : " + getactivelist())
			print()
			print("##Mod Profiles##")
			print()
			i = 0
			j = 0
			profiles = getlists()
			for profile in profiles:
				print(str(i) + '	: ' + profile[0])
				i+=1
			print()
			chosenprofile = input("Select profile to set as active (leave empty to keep current) : ")
			try:
				selectlist(profiles[int(chosenprofile)][0])
				break
			except:
				break

		elif choice == 2:
			os.system('clear')
			print(header)
			print()
			print("####Mods Management####")
			print()
			print("Active profile : " + getactivelist())
			print()
			print("##New Profile##")
			print()
			profilename = input("New Profile name : ")
			try:
				createlist(profilename)
				selectlist(profilename)
				break
			except:
				break

		elif choice == 3:
			os.system('clear')
			print(header)
			print()
			print("####Mods Management####")
			print()
			print("Active profile : " + getactivelist())
			print()
			print("##Mod Profiles##")
			print()
			i = 0
			j = 0
			profiles = getlists()
			for profile in profiles:
				print(str(i) + '	: ' + profile[0])
				i+=1
			print()
			chosenprofile = input("Select profile to delete : ")
			try:
				confirm = input("Are you sure you want to delete " + profiles[int(chosenprofile)][0] + " [y/n] ?")
				if confirm in ['y', 'Y', 'yes', 'Yes']:
					deletelist(profiles[int(chosenprofile)][0])
					break
				else:
					break
			except:
				break


		elif choice == 4:
			os.system('clear')
			print(header)
			print()
			print("####Mods Management####")
			print()
			print("Active profile : " + getactivelist())
			print()
			print("##Mod List##")
			print()
			for mod in listmods(getactivelist())[0]:
				print(mod[0] + " : " + mod[1].split(',')[0] + ' (' + mod[1].split(',')[1] + ')')
			for mod in listmods(getactivelist())[1]:
				print(mod[0] + " : " + mod[1].split(',')[0] + ' (' + mod[1].split(',')[1] + ')')
			input("Press enter to go back.")
			break

		elif choice == 5:
			os.system('clear')
			activelist = getactivelist()
			print(header)
			print()
			print("####Mods Management####")
			print()
			print("Active profile : " + activelist)
			print()
			print("##Mod updates##")
			print()
			print("Querying Steam workshop for updates...")
			toupdate = []
			i = 0
			for mod in listmods(activelist):
				if modneedsupdate(activelist, mod[0]):
					toupdate.append(mod[0], mod[1].split(',')[0])
					i+=1
			print(str(i) + " mod update(s) available : ")
			for mod in toupdate :
				print(mod[0] + ' : ' + mod[1])
			confirm = input("Proceed with updates ? [yes/no]")
			if confirm in ['y', 'Y', 'yes', 'Yes']:
				for mod in toupdate:
					print("Updating " + mod[1])
					dowloadmod(activelist, mod[0])
					print("Done.")
				print("Updates completed. Lowerizing file names. This can take a few minutes...")
				for mod in toupdate:
					lowerize(mod[0])
				input("Done. Press enter to go back the menu.")
				break
			else:
				break


if __name__ == "__main__":

	if not checkconfigfile():
		print("No manager.ini found.")
		print("Creating new manager.ini file.")
		generateconfigfile()

	mainmenu()
