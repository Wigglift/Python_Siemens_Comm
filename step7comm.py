from smart7 import Smart7
import snap7
from snap7.util import *
import time
import os

#os.path.dirname(snap7.__file__)
#pyinstaller --onefile --add-binary="caminho dll;." arquivo
SETTINGS_FILE = "./settings.json"
smart7 = Smart7()

if(not os.path.exists(SETTINGS_FILE)):
    
    print("Settings file does not exist, creating a new one")

    DIRECTORY = input("Enter the destined directory: ")

    IP = (input("Enter the IP adress of PLC: "))
    RACK = int(input("Enter the RACK number: "))
    SLOT = int(input("Enter the SLOT number: "))

    smart7.set_comm_info(DIRECTORY,IP,RACK,SLOT)

    print(smart7.connect())

    db_number = int(input("Enter the DB number: "))
    start = int(input("Enter the start byte: "))
    size = int(input("Enter the size of the DB: "))

    smart7.set_db_data(db_number,start,size)

    print(smart7.get_status_db_data())

    smart7.generate_settings_file(SETTINGS_FILE)

else:
    print("Settings file exists, connecting to settings")
    
    smart7.get_settings(SETTINGS_FILE)

    print(smart7.connect())

    print(smart7.get_status_db_data())
    
print("The reading has started successfully")

execute = True

while execute == True:
    smart7.read_db_data()
    smart7.generate_txt_file()
    time.sleep(0.5)