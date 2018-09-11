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
		print()
		#Set Paths
	elif choice == 2:
		print()
		#Set Steam Credentials
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
print("Reading config file...")

config_file = ("./modmanager.ini")
if not os.path.isfile(config_file):

	print("Config file 'modmanager.ini' not found. Creating configuration file...")

	config_file = configparser.ConfigParser()

	config_file.add_section('PATHS')
	config_file.add_section('STEAM_CREDENTIALS')
	str = input("Enter path to steamcmd directory (exemple : /home/user/steamcmd) :")
	config_file.set('PATHS','steamcmd', str)
	str = input("Enter path to arma 3 server directory (exemple : /home/user/arma3) :")
	config_file.set('PATHS','arma3sever', str)
	str = input("Enter path where you want the mods to be installed (exemple : /home/user/arma3/mods) :")
	config_file.set('PATHS','mods', str)

	str = input("Enter your steam user name :")
	config_file.set('STEAM_CREDENTIALS','username', str)
	str = input("Enter your steam password :")
	config_file.set('STEAM_CREDENTIALS','password', str)

	config_file.write(open('manager.ini', 'w+'))

	print("Blank configuration file created.")
	print("Remember that you need to setup the Paths and Credentials using the following menu.")
	print()
	menu()

else:
	menu()