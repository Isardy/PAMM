# Arma3ModManager
A python mod manager for Arma 3 dedicated servers, for Linux (tested on Debian 9 and Ubuntu 18.04.1 using Python 3.5.3)

Requirements :

	Python 3
	pip 3

	Python packages : (TODO install bash script)
		configparser
		lxml
		psutil

Usage :

The manager should work no matter where the files are placed but I recommend having them in the main Arma3Server directory.

$>python3 manager.py

On first use or if the manager.ini file doesn't exist, the script will prompt you for the basic information it need in order to work. There is no verification so make sure it's right when you enter it.

The ini file is pretty straight forward and can be edited manually if you made a mistake or changed something. You can also delete it and run manager.py again if you want to start again.

The tool assumes you don't mess with the mod files manually. It will not detect if you delete or add a mod without using it.
