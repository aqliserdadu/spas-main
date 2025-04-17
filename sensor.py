import serial
import struct
import time
from config import ambilConfig
#from rain import get_rainfall,cleanup

MAX_RETRIES = 3

def get_at500_data(parameter):

    (PORT, BAUDRATE, SLAVEID, FUNCTIONCODE, DATABITS, STOPBITS, PARITY,LENGTH, ADDRESS, CRC, METODE, PARAMETER, POST, PARSING, UNIT) = ambilConfig(parameter)
    for attempt in range(1, MAX_RETRIES + 1):
        try:

            baudrate = BAUDRATE
            parity = PARITY
            stopbits = STOPBITS
            bytesize = DATABITS
            timeout = 1
            port = PORT
            slaveid = SLAVEID
            functionCode=FUNCTIONCODE
            address=ADDRESS.split(",")
            length=LENGTH.split(",")
            parsing=PARSING.split(":")
            request = bytearray([slaveid,functionCode,address[0],address[1],length[0], length[1]])
            datacrc=CRC.split(",")
            crc = bytearray([datacrc[0], datacrc[1]])
            ser = serial.Serial(port, baudrate, bytesize, parity, stopbits, timeout)
            time.sleep(1)

            modbus_request = request + crc
            ser.write(modbus_request)
            time.sleep(1)  # Tunggu respons
            response = ser.read(256)

            if not response:
                print(f"Percobaan {attempt}/{MAX_RETRIES}: No response from {port}, retrying...")
                ser.close()
                time.sleep(2)  # Tunggu sebelum mencoba lagi
                continue

            if len(response) >= 7:  # Pastikan respons cukup panjang
                data = round(struct.unpack('>f', response[parsing[0]:parsing[1]])[0], 2)
                ser.close()
                return data
            else:
                print(f"Percobaan {attempt}/{MAX_RETRIES}: Incomplete response from {port}, retrying...")
                ser.close()
                time.sleep(2)
                continue

        except Exception as e:
            print(f"Percobaan {attempt}/{MAX_RETRIES}: Error reading Modbus Parameter {parameter} : {e}, retrying...")
            time.sleep(2)  # Tunggu sebelum mencoba lagi

    print(f"Gagal membaca data dari {port} setelah {MAX_RETRIES} percobaan.")
    return None  # Kembalikan None jika gagal membaca setelah 3 percobaan

def get_mace_data(parameter):
    (PORT, BAUDRATE, SLAVEID, FUNCTIONCODE, DATABITS, STOPBITS, PARITY,LENGTH, ADDRESS, CRC, METODE, PARAMETER, POST, PARSING, UNIT) = ambilConfig(parameter)   
    try:
        baudrate = BAUDRATE
        parity = PARITY
        stopbits = STOPBITS
        bytesize = DATABITS
        timeout = 1
        port = PORT
        slaveid = SLAVEID
        functionCode=FUNCTIONCODE
        address=ADDRESS.split(",")
        length=LENGTH.split(",")
        parsing=PARSING.split(":")
        request = bytearray([slaveid,functionCode,address[0],address[1],length[0], length[1]])
        datacrc=CRC.split(",")
        crc = bytearray([datacrc[0], datacrc[1]])
        ser = serial.Serial(port, baudrate, bytesize, parity, stopbits, timeout)
        time.sleep(1)
        
        modbus_request = request + crc
        ser.write(modbus_request)
        time.sleep(1)  
        response = ser.read(256)

        if not response:
            print("No response received from MACE sensor")
            ser.close()
            return None
        
        if len(response) >= 15:  
            data = round(struct.unpack('>f', response[parsing[0]:parsing[1]])[0], 2)
        else:
            print("Incomplete response received from MACE sensor")
            ser.close()
            return None

        ser.close()
        return data
    except Exception as e:
        print(f"Error in get_mace_data: {e}")
        return None

def get_rain_data_GPIO():
    
    tipping_count, total_rainfall = get_rainfall()
    cleanup()
    return tipping_count, total_rainfall

def get_rain_data(): #jika ada menggunakan sensor rain dari modbus
    tipping_count, total_rainfall=90,20
    return tipping_count, total_rainfall 

