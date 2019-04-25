from modules import server
from modules import config
from modules import mods

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
		config.setconfig('steamcmd')
		config.setconfig('arma3server')
		config.setconfig('mods')
	elif choice == 2:
		config.setconfig('username')
		config.setconfig('password')
	elif choice == 3:
		server.servermanagement( "start" )
	elif choice == 4:
		server.servermanagement( "stop" )
	elif choice == 5:
		server.servermanagement( "update" )
	elif choice == 6:
		server.servermanagement( "status")
	elif choice == 7:
		mods.mods('list')
	elif choice == 8:
		mods.mods( 'addSeveral' )
	elif choice == 9:
		mods.mods('addNonWorkshop')
	elif choice == 18:
		mods.mods('remove' )
	elif choice == 11:
		mods.listupdates()
	elif choice == 12:
		mods.updatemods()
	elif choice == 13:
		mods.forceupdateall()
	elif choice == 0:
		return
	else:
		print("Invalid input. Try again")
	menu()
