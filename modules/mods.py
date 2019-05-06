import os
import shutil
import configparser
import requests
from lxml import html

from module import config

def getmodinfo( modid ):
	url = "https://steamcommunity.com/sharedfiles/filedetails/?id=" + str(modid)
	page = requests.get(url)
	tree = html.fromstring(page.content)

	data_type = tree.xpath('//a[@href="https://steamcommunity.com/workshop/browse/?appid=107410&browsesort=toprated&section=readytouseitems&requiredtags%5B%5D=Mod"]/text()')
	if data_type != []:
		if data_type[0] == 'Mod':
			last_update = tree.xpath('//div[@class="detailsStatRight"]/text()')
			title = tree.xpath('//div[@class="workshopItemTitle"]/text()')
			if len(last_update)==2:
				last_update.append("1 Jan @ 8:00am")	#placeholder for the case where a mod has never been updated
			modinfo = [modid, title[0], last_update[2].replace(",", "")]
			return modinfo
		else:
			return False
	else:
		return False

def listmods( profile ):
	config_file = configparser.ConfigParser(delimiters=':')
	config_file.read(profile + '.ini')
	workshopmods = config_file.items('WORKSHOP_MODS')
	nonworkshopmods = config_file.items('NON_WORKSHOP_MODS')
	return [workshopmods, nonworkshopmods]

def addworkshopmod( profile, modid ):
	config_file = configparser.ConfigParser(delimiters=':')
	config_file.read(profile + '.ini')
	modinfo = getmodinfo(modid)
	if modinfo:
		modname = str(modinfo[1])
		modupdate = str(modinfo[2])
		value = modname + ',' + modupdate
		config_file.set('WORKSHOP_MODS', modid, value)
		config_file.write(open(profile + '.ini', 'w'))
		return True
	else:
		return False

def addnonworkshopmod( profile, modname, directory ):
	config_file = configparser.ConfigParser(delimiters=':')
	config_file.read(profile + '.ini')
	arma3path = config.getpath('arma3server')
	modspath = config.getpath('mods')
	path = arma3path + '/' + modspath + '/' + directory
	if os.path.exists(path):
		config_file.set('NON_WORKSHOP_MODS', directory, modname)
		config_file.write(open(profile + '.ini', 'w'))
		return True
	else:
		return False

def removemod( profile, ws, mod ):
	config_file = configparser.ConfigParser(delimiters=':')
	config_file.read(profile + '.ini')
	if ws:
		config_file.remove_option('WORKSHOP_MODS', mod)
		config_file.write(open(profile + '.ini', 'w'))
		arma3path = config.getpath('arma3server')
		modspath = config.getpath('mods')
		realpath = arma3path + "/" + modspath + "/steamapps/workshop/content/107410/" + mod
		sympath = arma3path + "/" + modspath + "/" + mod
		os.unlink(sympath)
		shutil.rmtree(realpath)
	else:
		directory = config_file.get('NON_WORKSHOP_MODS', mod)
		config_file.remove_option('NON_WORKSHOP_MODS', mod)
		config_file.write(open(profile + '.ini', 'w'))
		path = arma3path + "/" + modspath + "/" + directory
		shutil.rmtree(path)
	return True

def modneedsupdate( profile, modid ):
	config_file = configparser.ConfigParser(delimiters=':')
	config_file.read(profile + '.ini')
	mod = config_file.get('WORKSHOP_MODS', mod)
	if (getmodinfo(modid)[2] == config_file.get('WORKSHOP_MODS',modid).split(',')[1]):
		return False
	else:
		return True

def modexists(modid):
	arma3path = config.getpath('arma3server')
	modspath = config.getpath('mods')
	realpath = arma3path + "/" + modspath + "/steamapps/workshop/content/107410/" + modid
	sympath = arma3path + "/" + modspath + "/" + modid
	if os.path.exists(realpath) and os.path.exists(sympath):
		return 1
	elif os.path.exists(realpath):
		return 2
	else:
		return False

def downloadmod( profile, modid )
	config_file = configparser.ConfigParser(delimiters=':')
	config_file.read(profile + '.ini')
	steam = config.getpath('steamcmd')
	arma3path = config.getpath('arma3server')
	modspath = config.getpath('mods')
	username = config.getcreds('username')
	password = config.getcreds('password')
	#TODO Function to generate steamcmd commands ?
	realpath = arma + "/" + modspath + "/steamapps/workshop/content/107410/" + modid
	sympath = arma + "/" + modspath + "/" + modid
	command = steam + "/steamcmd.sh " + "+login " + username + " " + password + " +force_install_dir " + arma3path + "/" + modspath + " +workshop_download_item 107410 " + modid + " +quit"
	subprocess.call(command, shell=True, stdout=subprocess.PIPE)
	if modexists(modid):
		lowerize(modid)
		return True
	else:
		os.symlink(realpath, sympath)
		lowerize(modid)
		return True

def lowerize (modid)
	if modexists(modid):
		arma3path = config.getpath('arma3server')
		modspath = config.getpath('mods')
		realpath = arma + "/" + modspath + "/steamapps/workshop/content/107410/" + modid +"/"
		lowerize = "find " + realpath + r" -depth -exec rename 's/(.*)\/([^\/]*)/$1\/\L$2/' {} \;"
		subprocess.call(lowerize, shell=True)
		return True
	elif modid == "all"
		realpath = arma + "/" + modspath + "/steamapps/workshop/content/107410/"
		lowerize = "find " + realpath + r" -depth -exec rename 's/(.*)\/([^\/]*)/$1\/\L$2/' {} \;"
		subprocess.call(lowerize, shell=True)
		return True
	else:
		return False