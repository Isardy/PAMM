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

def menu(choice):
	try:
		choice = int(choice)
	except:
		mainmenu()
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
		mainmenu()
	return

def pammmenu():
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
		pammmenu()
	if choice not in [1, 2, 3, 4, 5, 9, 0]:
		pammmenu()
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
			mainmenu()
		elif choice == 0:
			sys.exit()
		else:
			pammmenu()
		pammmenu()
	return

def servermenu():

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
		servermenu()
	if choice not in [1, 2, 3, 9, 0]:
		servermenu()
	else:
		if choice == 1:
			start(getactivelist())
		elif choice == 2:
			stop()
		elif choice == 3:
			update()
		elif choice == 9:
			mainmenu()
		elif choice == 0:
			sys.exit()
		else:
			servermenu()
		servermenu()
	return

def modsmenu():
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
	print("8	Repair Mods (Lowerize mod file names")
	print()
	print("9	Back to Main Menu")
	print("0	Exit")
	choice = input("Your choice : ")
	try:
		choice = int(choice)
	except:
		modsmenu()
	if choice not in [1, 2, 3, 4, 5, 6, 7, 8, 9, 0]:
		modsmenu()
		if choice == 1:
			os.system('clear')
			print(header)
			print()
			print("####Mods Management####")
			print()
			print("Active profile : " + getactivelist())
			print()
			print("##Mod Profile##")
			print()
			i = 0
			j=0
			profiles = getlists()
			for profile in profiles:
				print(i + '	: ' + profile[0])
				i+=1
			print()
			ch = input("Select profile to set as active (leave empty to keep current) : ")
			if ch == '':
				modsmenu()
			else:
				try:
					for profile in profiles:
						if not i == j:
							j+=1
						else:
							selectlist(profile)
				except:
					modsmenu()
'''
		elif choice == 2:

		elif choice == 3:

		elif choice == 4:

		elif choice == 5:

		elif choice == 6:

		elif choice == 7:

		elif choice == 8:

	elif choice == 9:
		mainmenu()
	elif choice == 0:
		sys.exit()
	else:
		modsmenu()
	return
'''
if __name__ == "__main__":

	if not checkconfigfile():
		print("No manager.ini found.")
		print("Creating new manager.ini file.")
		generateconfigfile()

	mainmenu()