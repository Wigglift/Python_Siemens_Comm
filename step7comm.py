from smart7 import Smart7
import snap7
from snap7.util import *
import time
import os

#os.path.dirname(snap7.__file__)
#pyinstaller --onefile --add-binary="caminho dll;." arquivo
SETTINGS_FILE = "./settings.json"
TEMPORARY_FILE = "F:/testeComm/teste.tmp" 
FILE = "F:/testeComm/teste.txt"
plc = snap7.client.Client()

if(not os.path.exists(SETTINGS_FILE)):

    print("Settings file does not exist, creating a new one")

    IP = (input("Enter the IP adress of PLC: "))
    RACK = int(input("Enter the RACK number: "))
    SLOT = int(input("Enter the SLOT number: "))

    Smart7.set_comm_info(IP,RACK,SLOT)

    print(Smart7.connect())

    db_number = int(input("Enter the DB number: "))
    start = int(input("Enter the start byte: "))
    size = int(input("Enter the size of the DB: "))

    Smart7.set_db_data(db_number,start,size)

    print(Smart7.read_db_data())

    Smart7.generate_settings_file(SETTINGS_FILE)

else:
    print("Settings file exists, connecting to settings")
    
    Smart7.get_settings()

    print(Smart7.connect())

    print(Smart7.read_db_data())
    
print("The reading has started successfully")

execute = True

while execute == True:
    Smart7.replace_txt_file(FILE)

    time.sleep(0.5)
