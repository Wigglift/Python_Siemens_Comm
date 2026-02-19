import snap7
from snap7.util import *
import time
import os

#os.path.dirname(snap7.__file__)
#pyinstaller --onefile --add-binary="caminho dll;." arquivo
SETTINGS_FILE = "./settings.txt"
TEMPORARY_FILE = "F:/testeComm/teste.tmp" 
FILE = "F:/testeComm/teste.txt"
plc = snap7.client.Client()

if(not os.path.exists('./settings.txt')):
    print("Settings file does not exist, creating a new one:")
    IP = input("Enter the IP address of the PLC: ")
    RACK = int(input("Enter the rack number: "))
    SLOT = int(input("Enter the slot number: "))

    try:
        plc.connect(IP, RACK, SLOT)
        print("Connected to PLC successfully.")

    except Exception as e:
        print(f"Failed to connect to PLC: {e}")
        time.sleep(5)

    print(f"plc.get_connected() = {plc.get_connected()}")
    time.sleep(1)

    db_number = int(input("Enter the DB number: "))
    start = int(input("Enter the start byte: "))
    size = int(input("Enter the size of the DB: "))

    try:
        data = plc.db_read(db_number, start, size)
        print("DB reading success")

        try:
            with open(SETTINGS_FILE, "w") as file:
                file.write(IP + "\n")
                file.write(str(RACK) + "\n")
                file.write(str(SLOT) + "\n")
                file.write(str(db_number) + "\n")
                file.write(str(start) + "\n")
                file.write(str(size) + "\n") 
                print("Settings file created with actual settings")
                file.close()

        except Exception as e:
            print("Error creating settings file")
            print(e)
            time.sleep(5)

    except Exception as e:
        print(f"Error reading DB {e}")
        time.sleep(5)
else:
    print("Settings file exists, connecting to settings")
    try:
        with open(SETTINGS_FILE, "r") as file:
            IP = file.readline().strip()
            RACK = int(file.readline().strip())
            SLOT = int(file.readline().strip())
            db_number = int(file.readline().strip())
            start = int(file.readline().strip())
            size = int(file.readline().strip())
            file.close()
    except Exception as e:
        print("Error reading settings file")
        print(e)
        time.sleep(5)

    try:
        plc.connect(IP, RACK, SLOT)
        print("Connected to PLC successfully.")

    except Exception as e:
        print(f"Failed to connect to PLC: {e}")
        time.sleep(5)

    print(f"plc.get_connected() = {plc.get_connected()}")
    time.sleep(1)

    try:
        data = plc.db_read(db_number, start, size)
        print("DB reading success")

    except Exception as e:
        print(f"Error reading DB {e}")
        time.sleep(5)
    
print("The reading has started successfully")

execute = True

while execute == True:
    try:
        data = plc.db_read(db_number, start, size)

    except Exception as e:
        print("DB reading failure: ")
        print(e)

    try:
        with open(TEMPORARY_FILE, "w") as file:
    
            file.write("nº ferr;" + str(snap7.util.get_int(data, 0)) + "\n")
            file.write("velocidade;" + str(snap7.util.get_int(data, 2))+ "\n")
            file.write("quant. peça;" + str(snap7.util.get_int(data, 4))+ "\n")

            nome_ferramenta = ""

            for i in range(32):
                nome_ferramenta += snap7.util.get_char(data, i + 6)

            file.write("nome;" + str(nome_ferramenta)+ "\n")
            file.close()


    except Exception as e:
        print("Error writing the archive")
        print(e)
        time.sleep(5)

    try:
        os.replace(TEMPORARY_FILE, FILE)
    except Exception as e:
        if e != PermissionError:
            print("Error replacing files")
            print(e)

    time.sleep(0.5)