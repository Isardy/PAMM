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
import psutil
import shutil

##########################Server Management###############################

def servermanagement( action ):
	if action == "stop":
		process = "arma3server"
		process = subprocess.Popen(["pgrep", process], stdout=subprocess.PIPE)
		for pid in process.stdout:
			os.kill(int(pid), signal.SIGTERM)
		input("Server stopped.")
	elif action == "start":
		print("Starting Arma 3 server.")
		config_file = configparser.ConfigParser(delimiters=':')
		config_file.read("manager.ini")
		serverpath = config_file.get('PATHS', 'arma3server')
		modsdir = config_file.get('PATHS', 'mods')
		modlist = mods('quietlist')
		modstring = '"'
		for mod in modlist:
			modstring = modstring + modsdir + '/' + mod + ';'
		modstring = modstring[:-1] + '"'
		startstring = serverpath + '/' + 'arma3server -config=server.cfg -mod=' + modstring + " >>server.rpt 2>&1 &"
		#subprocess.call(startstring, shell=True, stdout=subprocess.PIPE)
		print(startstring)
		input("Arma 3 server started.")
	elif action == "update":
		config_file = configparser.ConfigParser(delimiters=':')
		config_file.read("manager.ini")
		steam = config_file.get('PATHS', 'steamcmd')
		arma = config_file.get('PATHS', 'arma3server')
		username = config_file.get('STEAM_CREDENTIALS', 'username')
		password = config_file.get('STEAM_CREDENTIALS', 'password')
		command = steam + "/steamcmd.sh " + "+login " + username + " " + password + " +force_install_dir " + arma + " +app_update 233780 validate +quit"
		subprocess.call(command, shell=True)
		input("Arma 3 Server is up to date.")
	elif action == "status":
		for pid in psutil.pids():
			process = psutil.Process(pid)
			if process.name()=="arma3server":
				input("Arma 3 server is running.")
				return
		input("Arma 3 server is down.")

##########################Config Management###############################

def generateconfigfile():
	print("Generating config file...")
	config_file = ("manager.ini")
	config_file = configparser.ConfigParser(delimiters=':')
	config_file.add_section('PATHS')
	config_file.add_section('STEAM_CREDENTIALS')
	config_file.add_section('MODS')
	config_file.add_section('NON_WORKSHOP_MODS')
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
	input("Configuration file 'manager.ini' has been created.")

def checkconfigfile():
	config_file = configparser.ConfigParser(delimiters=':')
	config_file = ("manager.ini")
	if not os.path.isfile(config_file):
		input("manager.ini not found.")
		generateconfigfile()
	else:
		input("manager.ini found.")

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

def getmodinfo( modid ):
	url = "https://steamcommunity.com/sharedfiles/filedetails/?id=" + str(modid)
	page = requests.get(url)
	tree = html.fromstring(page.content)
	last_update = tree.xpath('//div[@class="detailsStatRight"]/text()')
	title = tree.xpath('//div[@class="workshopItemTitle"]/text()')
	if len(last_update)==2:
		last_update.append("1 Jan @ 8:00am")	#placeholder for the case where a mod has never been updated
	modinfo = [modid, title[0], last_update[2].replace(",", "")]
	return modinfo

def mods( action, modid=0 ):
	config_file = configparser.ConfigParser(delimiters=':')
	config_file.read("manager.ini")
	if action == "list":
		print("Liste des mods :")
		modlist = config_file.items('MODS')
		nwmodlist = config_file.items('NON_WORKSHOP_MODS')
		for mod in modlist:
			print(mod)
		for mod in nwmodlist:
			print(mod)
		input("Press 'Enter' to go back to the Menu.")
	elif action == "quietlist":
		wmods = config_file.options('MODS')
		nwmods = config_file.options('NON_WORKSHOP_MODS')
		return wmods + nwmods
	elif action == "add":
		if modid==0:
			modid = input("Enter mod Workshop id :")
		mod = getmodinfo(modid)
		id = str(mod[0])
		title = str(mod[1])
		date = str(mod[2])
		value = title + ',' + date 
		config_file.set('MODS', id, value )
		config_file.write(open('manager.ini', 'w'))
	elif action == "addSeveral":
		if modid==0:
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
			mods( 'addSeveral' )
		else:
			return
	elif action == 'addNonWorkshop':
		title = input("Mod title : (ex : Star Wars Opposition) ")
		directory = input("Mod directory in lowercase : (ex: @swop) ")
		config_file.set('NON_WORKSHOP_MODS', directory, title)
		config_file.write(open('manager.ini', 'w'))
		return
	elif action == "remove":
		modid = input("Enter mod Workshop id :")
		config_file.remove_option('MODS', str(modid))
		config_file.write(open('manager.ini', 'w'))
		arma3path = config_file.get('PATHS', 'arma3server')
		modspath = config_file.get('PATHS', 'mods')
		realpath = arma3path + "/" + modspath + "/steamapps/workshop/content/107410/" + str(modid)
		sympath = arma3path + "/" + modspath + "/" + str(modid)	
		shutil.rmtree(realpath)
		os.unlink(sympath)
		more = input("Do you want to remove more mods [yes/no] ?")
		while more not in [ 'yes', 'Yes', 'no', 'No', 'y', 'n', 'Y', 'N']:
			print("Invalid answer.")
			more = input("Do you want to remove more mods [yes/no] ?")
		if more in ['yes', 'Yes', 'y']:
			mods( 'remove' )
		else:
			return

def checkmodupdate( modid ): #True if needs update
	config_file = configparser.ConfigParser(delimiters=':')
	config_file.read("manager.ini")
	arma3path = config_file.get('PATHS', 'arma3server')
	modpath = config_file.get('PATHS', 'mods')
	modpath = arma3path + "/" + modpath + "/" + modid
	if os.path.islink(modpath):
		if config_file.get('MODS', modid).split(',')[1] == getmodinfo(modid)[2]:
			return False
		else:
			return True
	else:
		return True	

def listupdates():
	print("Checking workshop for updates...")
	config_file = configparser.ConfigParser(delimiters=':')
	config_file.read("manager.ini")
	updatecounter = 0
	modcounter = 0
	for mod in config_file.options('MODS'):
		if checkmodupdate(mod):
			updatecounter += 1
			modcounter += 1
			print(config_file.get('MODS', mod).split(',')[0] + " needs an update.")
		else:
			modcounter += 1
			print(config_file.get('MODS', mod).split(',')[0] + " is up to date.")
	summary = str(updatecounter) + "/" + str(modcounter) + " mods need an update :"
	print(summary)
	if (updatecounter > 0):
		update = input("Proceed with update ? (Yes/No)")
		if (update in [ 'yes', 'Yes','y','Y']):
			updatemods();
	else:
		input("Press 'Enter' to continue.")

def updatemods():
	print("Update")
	config_file = configparser.ConfigParser(delimiters=':')
	config_file.read("manager.ini")
	for mod in config_file.options('MODS'):
		print("Checking update availability for " + config_file.get('MODS', mod).split(',')[0])
		if checkmodupdate(mod):
			print("Update available. Updating mod...")
			steam = config_file.get('PATHS', 'steamcmd')
			arma = config_file.get('PATHS', 'arma3server')
			modspath = config_file.get('PATHS', 'mods')
			username = config_file.get('STEAM_CREDENTIALS', 'username')
			password = config_file.get('STEAM_CREDENTIALS', 'password')
			command = steam + "/steamcmd.sh " + "+login " + username + " " + password + " +force_install_dir " + arma + "/" + modspath + " +workshop_download_item 107410 " + mod + " +quit"
			subprocess.call(command, shell=True, stdout=subprocess.PIPE)
			mods('add', mod)
			realpath = arma + "/" + modspath + "/steamapps/workshop/content/107410/" + mod
			sympath = arma + "/" + modspath + "/" + mod
			if not os.path.islink(sympath):
				os.symlink(realpath, sympath)
			print("Converting mod file names to Lowercase. This operation may take some time.")
			lowerize = "find " + arma + "/" + modspath + "/" + mod + r" -depth -exec rename 's/(.*)\/([^\/]*)/$1\/\L$2/' {} \;"
			subprocess.call(lowerize, shell=True)
			print("Mod updated.")
		else:
			print("Mod up to date.")

def forceupdateall():
	print("Forcing update for all mods")
	config_file = configparser.ConfigParser(delimiters=':')
	config_file.read("manager.ini")
	steam = config_file.get('PATHS', 'steamcmd')
	arma = config_file.get('PATHS', 'arma3server')
	modspath = config_file.get('PATHS', 'mods')
	username = config_file.get('STEAM_CREDENTIALS', 'username')
	password = config_file.get('STEAM_CREDENTIALS', 'password')
	nbMod = 0
	modCounter = 0
	for mod in config_file.options('MODS'):
		nbMod += 1 
	print("Updating " + str(nbMod) + " mods.")
	for mod in config_file.options('MODS'):
		modCounter += 1
		modTitle = config_file.get('MODS', mod).split(',')[0]
		print("Updating " + modTitle + " (" + str(modCounter) + "/" + str(nbMod) +")" )
		command = steam + "/steamcmd.sh " + "+login " + username + " " + password + " +force_install_dir " + arma + "/" + modspath + " +workshop_download_item 107410 " + mod + " +quit"
		subprocess.call(command, shell=True, stdout=subprocess.PIPE)
		mods('add', mod)
		realpath = arma + "/" + modspath + "/steamapps/workshop/content/107410/" + mod
		sympath = arma + "/" + modspath + "/" + mod
		if not os.path.islink(sympath):
			os.symlink(realpath, sympath)
		print(modTitle + " updated.")
	print("Converting mod file names to Lowercase. This operation may take some time.")
	lowerize = "find " + arma + "/" + modspath + r" -depth -exec rename 's/(.*)\/([^\/]*)/$1\/\L$2/' {} \;"
	subprocess.call(lowerize, shell=True)
	print("All mods have been updated.")

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
	print("6	Server Status")
	print()
	print("Mods Management :")
	print("7	List Mods")
	print("8	Add Mods")
	print("9	Add Non-Workshop Mods")
	print("10	Remove Mods")
	print("11	Check Mods for Updates")
	print("12	Update Mods")
	print("13	Force update Mods")
	print()
	print("0	Abort")
	print()

	while True:
		try:
			choice = int(input('Enter your choice [0-12] : '))
			break
		except :
			print("Invalid input. Try again.")
	if choice == 1:
		setconfig('steamcmd')
		setconfig('arma3server')
		setconfig('mods')
	elif choice == 2:
		setconfig('username')
		setconfig('password')
	elif choice == 3:
		servermanagement( "start" )
	elif choice == 4:
		servermanagement( "stop" )
	elif choice == 5:
		servermanagement( "update" )
	elif choice == 6:
		servermanagement( "status")
	elif choice == 7:
		mods('list')
	elif choice == 8:
		mods( 'addSeveral' )
	elif choice == 9:
		mods('addNonWorkshop')
	elif choice == 18:
		mods('remove' )
	elif choice == 11:
		listupdates()
	elif choice == 12:
		updatemods()
	elif choice == 13:
		forceupdateall()
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