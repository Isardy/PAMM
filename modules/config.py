import configparser
import os

def checkconfigfile():

	config_file = configparser.ConfigParser(delimiters=':')
	config_file = ("manager.ini")
	if not os.path.isfile(config_file):
		input("manager.ini not found.")
		generateconfigfile()
	else:
		input("manager.ini found.")

def generateconfigfile():

	print("Generating config file...")
	config_file = ("manager.ini")
	config_file = configparser.ConfigParser(delimiters=':')
	config_file.add_section('PATHS')
	str = input("Enter path to steamcmd directory (exemple : \033[1;41m/home/user/steamcmd\033[1;m) :")
	config_file.set('PATHS','steamcmd', str)
	str = input("Enter path to arma 3 server directory (exemple : \033[1;41m/home/user/arma3\033[1;m) :")
	config_file.set('PATHS','arma3server', str)
	str = input("Enter path, relative to the main Arma 3 directory, where you want the mods to be installed (exemple : \033[1;41mmods\033[1;m) :")
	config_file.set('PATHS','mods', str)	
	config_file.add_section('STEAM_CREDENTIALS')
	config_file.set('STEAM_CREDENTIALS','username', str)
	str = input("Enter your steam password :")
	config_file.set('STEAM_CREDENTIALS','password', str)
	config_file.add_section('MOD_LISTS')
	config_file.write(open('manager.ini', 'w+'))
	input("Configuration file 'manager.ini' has been created.")

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

def createlist( listname ):

	if listname not in getlists():		
		config_file = listname + ".ini"
		config_file = configparser.ConfigParser(delimiters=':')
		config_file.add_section('WORKSHOP_MODS')
		config_file.add_section('NON_WORKSHOP_MODS')
		config_file.write(open(listname + '.ini', 'w+'))
		config_file.read('manager.ini')
		config_file.set('MOD_LISTS', listname, "False")
		config_file.write(open('manager.ini', 'w+'))
		return True
	else:
		return False

def getlists():
	config_file = configparser.ConfigParser(delimiters=':')
	config_file.read("manager.ini")
	lists = config_file.items('MOD_LISTS')
	return lists

def deletelist( modlist ):
	config_file = configparser.ConfigParser(delimiters=':')
	config_file.read("manager.ini")
	config_file.remove_option('MOD_LISTS', modlist)
	config_file.write(open('manager.ini', 'w'))
	os.remove(modlist + '.ini')
	return True

def selectlist( modlist ):
	config_file = configparser.ConfigParser(delimiters=':')
	config_file.read("manager.ini")
	lists = getlists()
	listnames = []
	for item in lists:
		listnames.append(item[0])
	if modlist in listnames:
		for item in lists:
			config_file.set('MOD_LISTS', item[0], 'False')
		config_file.set('MOD_LISTS', modlist, 'True')
		config_file.write(open('manager.ini', 'w'))
		return True
	else :
		return False

def getpath(path):
	config_file = configparser.ConfigParser(delimiters=':')
	config_file.read("manager.ini")
	if path == 'steamcmd' or path == 'arma3server' or path == 'mods':
		return config_file.get('PATHS', path)
	else:
		return False

def getcreds(cred):
	config_file = configparser.ConfigParser(delimiters=':')
	config_file.read("manager.ini")
	if cred == 'username' or cred == 'password':
		return config_file.get('STEAM_CREDENTIALS', cred)
	else:
		return False