import snap7
from snap7.util import *
import time
import os
import json

class Smart7:

    def __init__(self):
        self.plc = snap7.client.Client()

    def set_comm_info(self, IP: str, RACK: int, SLOT: int):
        self.IP = IP
        self.RACK = RACK
        self.SLOT = SLOT

    def connect(self) -> str:
        try:
            self.plc.connect(self.IP, self.RACK, self.SLOT)
            if self.plc.get_connected():
                return "Connected to PLC successfully."

        except Exception as e:
            return f"Failed to connect to PLC: {e}"

    def set_db_data(self, db: int, start_byte: int, final_byte: int) -> str:
        
        self.db = db
        self.start_byte = start_byte
        self.final_byte = final_byte
        
    def get_db_data(self):
        return self.data
        
    def read_db_data(self):
        try:
            self.data = self.plc.db_read(self.db, self.start_byte, self.final_byte)
            return "reading DB success"
        except Exception as e:
            return f"Error reading DB: {e}"

    
    def replace_txt_file(self, path: str):
        try:
            with open("./db_temp_read.tmp" , "w") as file:
        
                file.write("nº ferr;" + str(snap7.util.get_int(self.data, 0)) + "\n")
                file.write("quant. peça;" + str(snap7.util.get_int(self.data, 2))+ "\n")
                file.write("peças lote;" + str(snap7.util.get_int(self.data, 4))+ "\n")
                file.write("peças turno;" + str(snap7.util.get_int(self.data, 6))+ "\n")
                file.write("maquina produzindo;" + str(snap7.util.get_bool(self.data, 8, 0))+ "\n")

                nome_ferramenta = ""

                for i in range(self.db_size - 9):
                    nome_ferramenta += snap7.util.get_char(self.data, i + 9)

                file.write("nome;" + str(nome_ferramenta)+ "\n")
                file.close()


        except Exception as e:
            print("Error writing the archive")
            print(e)
            time.sleep(5)
        
        try:
            os.replace("./db_temp_read.tmp", path)

        except Exception as e:
            if e != PermissionError:
                print("Error replacing files")
                print(e)
                time.sleep(5)

    def generate_settings_file(self, path: str):

        data = {
            "IP": self.IP,
            "RACK": self.RACK,
            "SLOT": self.SLOT,
            "db": self.db,
            "start_byte": self.start_byte,
            "final_byte": self.final_byte
        }

        try:
            with open(path, "w", encoding="utf-8") as file:
                json.dump(data, file, indent=4, ensure_ascii=False)

        except Exception as e:
            print("Error creating settings file")
            print(e)
            time.sleep(5)

    def get_settings(self, path: str):
        try:
            with open(path, "r") as file:
                data = json.load(file)

                self.IP = data["IP"]
                self.RACK = int(data["RACK"])
                self.SLOT = int(data["SLOT"])
                self.db = int(data["db"])
                self.start_byte = int(data["start_byte"])
                self.final_byte = int(data["final_byte"])

        except Exception as e:
            print("Error reading settings file")
            print(e)
            time.sleep(5)
