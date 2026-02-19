import snap7
from snap7.util import *
import time
import os


print(snap7.__file__)

#os.path.dirname(snap7.__file__)
#pyinstaller --onefile --add-binary="caminho dll;." arquivo

IP = input("Enter the IP address of the PLC: ")
RACK = int(input("Enter the rack number: "))
SLOT = int(input("Enter the slot number: "))
TEMPORARY_FILE = "F:/testeComm/teste.tmp" 
FILE = "F:/testeComm/teste.txt"

plc = snap7.client.Client()

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


    except Exception as e:
        print("Error writing the archive")
        print(e)
        time.sleep(5)

    try:
        os.replace(TEMPORARY_FILE, FILE)
    except:
        print("Error replacing the TMP file")
        time.sleep(5)
    time.sleep(0.5)