#!/usr/bin/python
#Isardy's Arma 3 Dedicated Server Mod Manager
#Author : Isardy
#
#This program aims to make mod management for Arma 3 Dedicated Servers easier.
#It will replace the present bash script suite and be more practical and Windows compatible.

##########################################################################

import os
import configparser

##########################################################################


def servermanagement( str ):
	if str == "stop":
		print("stop server")
		menu()
	elif str == "start":
		print("start server")
	elif str == "update":
		print("update server")
	else:
		print("Server Management error")

##########################################################################

def generateconfigfile():
	print("Generating config file...")

	config_file = ("manager.ini")
	config_file = configparser.ConfigParser()

	config_file.add_section('PATHS')
	config_file.add_section('STEAM_CREDENTIALS')
	str = input("Enter path to steamcmd directory (exemple : /home/user/steamcmd) :")
	config_file.set('PATHS','steamcmd', str)
	str = input("Enter path to arma 3 server directory (exemple : /home/user/arma3) :")
	config_file.set('PATHS','arma3server', str)
	str = input("Enter path where you want the mods to be installed (exemple : /home/user/arma3/mods) :")
	config_file.set('PATHS','mods', str)

	str = input("Enter your steam user name :")
	config_file.set('STEAM_CREDENTIALS','username', str)
	str = input("Enter your steam password :")
	config_file.set('STEAM_CREDENTIALS','password', str)

	config_file.write(open('manager.ini', 'w+'))

	print("Configuration file 'manager.ini' has been created.")

def checkconfigfile():
	
	config_file = configparser.ConfigParser()
	config_file = ("manager.ini")

	if not os.path.isfile(config_file):
		print("manager.ini not found.")
		generateconfigfile()
	else:
		print("manager.ini found.")

def setconfig( str ):
	config_file = configparser.ConfigParser()
	config_file.read("manager.ini")

	if str == "steamcmd" or str == "arma3server" or str == "mods" :
		value = config_file.get('PATHS', str)
		print("Setting new path for ", str, " directory.")
		print("Path presently set to : ", value)
		input_prompt = "New path to " + str + " (leave empty to keep present path) :"
		new = input(input_prompt)
		if not str:
			print("Keeping present value.")
		else:
			config_file.set('PATHS', str, new)
			print("New ", str, " path set to ", new)

	elif str == "username":
		value = config_file.get('STEAM_CREDENTIALS', 'username')
		print("Setting new Steam user name.")
		print("User name presently set to : ", value)
		str = input("New Steam user name (leave empty to keep present path) :")
		if not str:
			print("Keeping present value.")
		else:
			config_file.set('STEAM_CREDENTIALS','username', str)
			print("New Steam username set to ", str)

	elif str == "password":
		value = config_file.get('STEAM_CREDENTIALS', 'password')
		print("Setting new Steam password.")
		str = input("New Steam password (leave empty to keep present password) :")
		if not str:
			print("Keeping present value.")
		else:
			config_file.set('STEAM_CREDENTIALS','password', str)
			print("New Steam password set.")

	config_file.write(open('manager.ini', 'w'))


##########################################################################

def menu():

	print("######MAIN MENU######")
	print()
	print("Manager Configuration :")
	print("1	Set Paths")
	print("2	Set Steam Credentials")
	print()
	print("Arma 3 Server Management :")
	print("3	Start Server")
	print("4	Stop Server")
	print("5	Update Server")
	print()
	print("Mods Management :")
	print("6	List Mods")
	print("7	Add Mods")
	print("8	Remove Mods")
	print("9	Check Mods for Updates")
	print("10	Update Mods")
	print()
	print("0	Abort")
	print()

	choice = input('Enter your choice [0-10] : ')
	choice = int(choice)
	if choice == 1:
		setconfig('steamcmd')
		setconfig('arma3server')
		setconfig('mods')
		menu()
	elif choice == 2:
		setconfig('username')
		setconfig('password')
		menu()
	elif choice == 3:
		print()
		#Start Server
		servermanagement( "start" )
	elif choice == 4:
		#Stop Server
		servermanagement( "stop" )
	elif choice == 5:
		#Update Server
		servermanagement( "update" )
	elif choice == 6:
		print()
		#List Mods
	elif choice == 7:
		print()
		#Add Mods
	elif choice == 8:
		print()
		#Remove Mods
	elif choice == 9:
		print()
		#Check Mods for Update
	elif choice == 10:
		print()
		#Update Mods
	elif choice == 0:
		return
	else:
		print("Invalid input. Try again")
		menu()



##########################################################################


print("Isardy's Arma 3 Dedicated Server Mod Manager.")
print()
checkconfigfile()
menu()
