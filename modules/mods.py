import os
import configparser
import requests
from lxml import html

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