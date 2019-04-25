import os
import configparser
import subprocess
import signal
import psutil

from modules import mods

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
		modlist = mods.mods('quietlist')
		modstring = '"'

		#TODO manage empty mod list


		for mod in modlist:
			modstring = modstring + modsdir + '/' + mod + ';'
		modstring = modstring[:-1] + '"'
		startstring = serverpath + '/' + 'arma3server -config=server.cfg -mod=' + modstring + " >>server.rpt 2>&1 &"
		subprocess.call(startstring, shell=True, stdout=subprocess.PIPE)
		#print(startstring)
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