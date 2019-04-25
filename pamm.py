from modules import server
from modules import config
from modules import mods
from modules import cli

print("Isardy's Arma 3 Dedicated Server Mod Manager.")
print()
config.checkconfigfile()
cli.menu()