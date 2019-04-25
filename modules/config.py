import configparser
import os

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