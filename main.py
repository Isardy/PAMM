#!/usr/bin/python3
#Isardy's Arma 3 Dedicated Server Mod Manager
#Author : Isardy
#
#This program aims to make mod management for Arma 3 Dedicated Servers easier.
#It will replace the present bash script suite and be more practical (and maybe  Windows compatible at some point).

##########################################################################

import os
import configparser
import requests
from lxml import html
import subprocess
import signal


##########################Server Management###############################
#
#	servermanagement(action)
#		arguments : (str) action : 'stop', 'start' or 'update'
#		function:
#			Starts, stops or updates the Arma 3 server
#		return : None
#
##########################################################################

def servermanagement( action ):
	if action == "stop":
		process = "arma3server"
		process = subprocess.Popen(["pgrep", process], stdout=suprocess.PIPE)
		for pid in process.stdout:
			os.kill(int(pid), signal.SIGTERM)
		print("Server stopped.")
	elif action == "start":
		config_file = configparser.ConfigParser(delimiters=':')
		config_file.read("manager.ini")
		serverpath = config_file.get('PATHS', 'arma3server')
		modsdir = config_file.get('PATHS', 'mods')
		modlist = mods('quietlist')
		#subprocess.call('/home/steam/arma/arma3server', shell=True)
		modstring = ''
		for mod in modlist:
			modstring = modstring + modsdir + '/' + mod + ';'
		modstring = modstring[:-1]
		#print(modstring)

		#TODO custom config file
		startstring = serverpath + 'arma3server -config=server.cfg -mod=' + modstring

		print(startstring)



	elif action == "update":
		print("update server")
	elif action == "status":
		print("server status")


##########################Config Management###############################
#
#	generateconfigfile()
#		arguments : None
#		function :
#			Generates a config file while prompting the user for each option 
#		return : None
#
#	checkconfigfile()
#		arguments : None
#		function :
#			Checks if the config file exists and calls generateconfigfile if not
#		return : None
#
#	setconfig(option)
#		arguments : (str) option : steamcmd, arma3server, mods, username, password
#		function :
#			Prompts user for the specified value to best set in manager.ini
#		return : None
#
##########################################################################

def generateconfigfile():
	print("Generating config file...")

	config_file = ("manager.ini")
	config_file = configparser.ConfigParser(delimiters=':')

	config_file.add_section('PATHS')
	config_file.add_section('STEAM_CREDENTIALS')
	config_file.add_section('MODS')

	str = input("Enter path to steamcmd directory (exemple : \033[1;41m/home/user/steamcmd\033[1;m) :")
	config_file.set('PATHS','steamcmd', str)
	str = input("Enter path to arma 3 server directory (exemple : \033[1;41m/home/user/arma3\033[1;m) :")
	config_file.set('PATHS','arma3server', str)
	str = input("Enter path, relative to the main Arma 3 directory, where you want the mods to be installed (exemple : \033[1;41mmods\033[1;m) :")
	config_file.set('PATHS','mods', str)

	str = input("Enter your steam user name :")
	config_file.set('STEAM_CREDENTIALS','username', str)
	str = input("Enter your steam password :")
	config_file.set('STEAM_CREDENTIALS','password', str)


	config_file.write(open('manager.ini', 'w+'))

	print("Configuration file 'manager.ini' has been created.")

def checkconfigfile():
	
	config_file = configparser.ConfigParser(delimiters=':')
	config_file = ("manager.ini")

	if not os.path.isfile(config_file):
		print("manager.ini not found.")
		generateconfigfile()
	else:
		print("manager.ini found.")

def setconfig( option ):
	config_file = configparser.ConfigParser(delimiters=':')
	config_file.read("manager.ini")

	if option == "steamcmd" or option == "arma3server" or option == "mods" :
		value = config_file.get('PATHS', option)
		print("Setting new path for ", option, " directory.")
		print("Path presently set to : \033[1;41m", value, "\033[1;m")
		input_prompt = "New path to " + option + " (leave empty to keep present path) :"
		new = input(input_prompt)
		if not option:
			print("Keeping present value.")
		else:
			config_file.set('PATHS', option, new)
			print("New ", option, " path set to \033[1;41m", new, "\033[1;m")

	elif option == "username":
		value = config_file.get('STEAM_CREDENTIALS', 'username')
		print("Setting new Steam user name.")
		print("User name presently set to : \033[1;41m", value, "\033[1;m")
		option = input("New Steam user name (leave empty to keep present path) :")
		if not option:
			print("Keeping present value.")
		else:
			config_file.set('STEAM_CREDENTIALS','username', option)
			print("New Steam username set to \033[1;41m", option, "\033[1;m")

	elif option == "password":
		value = config_file.get('STEAM_CREDENTIALS', 'password')
		print("Setting new Steam password.")
		option = input("New Steam password (leave empty to keep present password) :")
		if not option:
			print("Keeping present value.")
		else:
			config_file.set('STEAM_CREDENTIALS','password', option)
			print("New Steam password set.")

	config_file.write(open('manager.ini', 'w'))

##############################Mods Management#############################
#
#	getmodinfo(modid)
#	arguments : (int) modid
#	function :
#		Retrieves information about the specified mod from the Steam Workshop
#	returns : ( list ) modinfo [ <mod id>, <mod title>, <last update date>]
#
##########################################################################


def getmodinfo( modid ):
	print("Getting mod info from the Workshop.")
	url = "https://steamcommunity.com/sharedfiles/filedetails/?id=" + str(modid)
	page = requests.get(url)
	tree = html.fromstring(page.content)
	#TODO : handle invalid ID
	#print(page)
	last_update = tree.xpath('//div[@class="detailsStatRight"]/text()')
	title = tree.xpath('//div[@class="workshopItemTitle"]/text()')
	modinfo = [modid, title[0], last_update[2]]
	return modinfo

def mods( action, modid=0 ):
	config_file = configparser.ConfigParser(delimiters=':')
	config_file.read("manager.ini")
	if action == "list":
		print("Liste des mods :")
		print(config_file.items('MODS'))
		input("Press 'Enter' to go back to the Menu.")
		#TODO terminaltables
	elif action == "quietlist":
		return config_file.options('MODS')
	elif action == "add":
		modid = input("Enter mod Workshop id :")
		mod = getmodinfo(modid)
		id = str(mod[0])
		title = str(mod[1])
		date = str(mod[2])
		value = title + ',' + date 
		config_file.set('MODS', id, value )
		config_file.write(open('manager.ini', 'w'))
		more = input("Do you want to add more mods [yes/no] ?")
		while more not in [ 'yes', 'Yes', 'no', 'No', 'y', 'n', 'Y', 'N']:
			print("Invalid answer.")
			more = input("Do you want to add more mods [yes/no] ?")
		if more in ['yes', 'Yes', 'y']:
			mods( 'add' )
		else:
			return
	elif action == "remove":
		modid = input("Enter mod Workshop id :")
		config_file.remove_option('MODS', str(modid))
		config_file.write(open('manager.ini', 'w'))
		more = input("Do you want to remove more mods [yes/no] ?")
		while more not in [ 'yes', 'Yes', 'no', 'No', 'y', 'n', 'Y', 'N']:
			print("Invalid answer.")
			more = input("Do you want to remove more mods [yes/no] ?")
		if more in ['yes', 'Yes', 'y']:
			mods( 'remove' )
		else:
			return

def checkmodstatus( modid ):
	config_file = configparser.ConfigParser(delimiters=':')
	config_file.read("manager.ini")
	modid = str(modid)
	modinfo = config_file.get('MODS', modid)



def updatemods():
	print("Update")






##############################Main Menu###################################

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
	elif choice == 2:
		setconfig('username')
		setconfig('password')
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
		mods('list')
		#List Mods
	elif choice == 7:
		mods( 'add' )
		#Add Mods
	elif choice == 8:
		mods('remove' )
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
