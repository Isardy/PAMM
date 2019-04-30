import os
import shutil
import configparser
import requests
from lxml import html

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
	config_file.read('manager.ini')

	#TODO config.py funtions to get paths
	arma3path = config_file.get('PATHS', 'arma3server')
	modspath = config_file.get('PATHS', 'mods')

	path = arma3path + '/' + modspath + '/' + directory
	if os.path.exists(path):
		config_file.read(profile + '.ini')
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
		config_file.read('manager.ini')

		arma3path = config_file.get('PATHS', 'arma3server')
		modspath = config_file.get('PATHS', 'mods')
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

def checkmodupdate( profile ):
	config_file = configparser.ConfigParser(delimiters=':')
	config_file.read(profile + '.ini')
	for mod in config_file.items('WORKSHOP_MODS'):
		latestupdate = getmodinfo(mod[0])[2]


