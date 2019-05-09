import os
import configparser
import subprocess
import signal
import psutil

from modules.config import *
from modules.mods import *

def getstatus():
	for pid in psutil.pids():
		process = psutil.Process(pid)
		if process.name() == "arma3server":
			return True
		else:
			return False

def start(profile):
	arma3path = getpath('arma3server')
	modspath = getpath('mods')
	modlist = listmods(profile)
	modstring = '"'
	for mod in modlist:
			modstring = modstring + modsdir + '/' + mod + ';'
	modstring = modstring[:-1] + '"'
	startcommmand = arma3path + '/' + "arma3server -config=server.cfg -mod=" + modstring + " >>server.rpt 2>&1 &"
	subprocess.call(startcommmand, shell=True, stdout=subprocess.PIPE)
	return getstatus()

def stop():
	if getstatus():
		process = subprocess.Popen(['pgrep', 'arma3server'], stdout=subprocess.PIPE)
		for pid in process.stdout:
			os.kill(int(pid), signal.SIGTERM)
		if getstatus():
			return False
		else:
			return True
	else:
		return True

def update():
	arma3path = config.getpath('arma3server')
	steampath = config.getpath('steamcmd')
	username = config.getcreds('username')
	password = config.getcreds('password')
	command = steampath + "/steamcmd.sh +login " + username + ' ' + password + " +force_install_dir " + arma + " +app_update 233780 validate +quit"
	subprocess.call(command, shell=True)
	return True