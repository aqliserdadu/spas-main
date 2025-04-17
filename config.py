import mysql.connector
from dotenv import load_dotenv
import os
import pytz
import time
from datetime import datetime


# Load environment variables
env_path = "/var/www/html/project/spas-main/config/.env"  # .env file path
if not load_dotenv(dotenv_path=env_path):
    print(f"Error: .env file not found at {env_path}")
    exit(1)


HOST = os.getenv('HOST')
USER = os.getenv('USERS')
PASSWORD = os.getenv('PASSWORD')
DATABASE = os.getenv('DATABASE')
TIMEZONA = os.getenv('TIMEZONA')

# MySQL connection configuration
MYSQL_CONFIG = {
    'host': HOST,
    'user': USER,
    'password': PASSWORD,
    'database': DATABASE
}

# Timezone configuration
tz = pytz.timezone(TIMEZONA)
def ambilDateAll():
    timestamp = datetime.now(tz).strftime("%Y-%m-%d %H:%M:%S")
    return timestamp

def ambilDate():
    date = datetime.now(tz).strftime("%Y-%m-%d")
    return date

def ambilDateTime():
    Interval_Timestamp = datetime.strptime(ambilDateAll(), '%Y-%m-%d %H:%M:%S')
    unix_dt = int(time.mktime(Interval_Timestamp.timetuple()))
    return unix_dt

def ambilConfig(*parameter):
    try:
        # Membuka koneksi
        conn = mysql.connector.connect(**MYSQL_CONFIG)
        cursor = conn.cursor()

        # Buat placeholder sebanyak jumlah parameter (misal: %s, %s, %s, ...)
        placeholders = ', '.join(['%s'] * len(parameter))

        query = f'''
            SELECT 
                A.port,
                A.baudrate,
                A.slaveid,
                A.functioncode,
                A.databits,
                A.stopbits,
                A.parity,
                A.length,
                A.address,
                A.crc,
                A.metode,
                B.name AS parameter,
                B.post,
                B.parsing,
                B.unit 
            FROM tbl_sensor AS A
            JOIN tbl_parameter AS B ON A.id = B.idsensor
            WHERE B.name IN ({placeholders})
        '''
        cursor.execute(query, parameter)
        result = cursor.fetchone()

        # Jika data ditemukan
        if result:
            (port, baudrate, slaveid, functioncode, databits, stopbits, parity,
             length, address, crc, metode, parameter, post, parsing, unit) = result

            return (port, baudrate, slaveid, functioncode, databits, stopbits, parity,
                    length, address, crc, metode, parameter, post, parsing, unit)
        else:
            print("Data tidak ditemukan.")
            return (None, None, None, None, None, None, None,
                    None, None, None, None, None, None, None, None)

    except Exception as e:
        print(f"Terjadi kesalahan: {e}")
        return (None, None, None, None, None, None, None,
                    None, None, None, None, None, None, None, None)

    finally:
        # Tutup koneksi
        if 'cursor' in locals(): cursor.close()
        if 'conn' in locals(): conn.close()

def ambilParameterDb():
    
    try:
        # Membuka koneksi
        conn = mysql.connector.connect(**MYSQL_CONFIG)
        cursor = conn.cursor()

        # Query SQL
        query = '''
            SELECT   
                parameter
            FROM tbl_listparameter
        '''

        # Jalankan query
        cursor.execute(query)
        result = [row[0] for row in cursor.fetchall()]  # Ambil nilai langsung
        return result

    except Exception as e:
        print(f"Terjadi kesalahan: {e}")
        return None

    finally:
        # Tutup koneksi
        if 'cursor' in locals(): cursor.close()
        if 'conn' in locals(): conn.close()
        
def cekParameterDb(parameter):
    
    try:
        # Membuka koneksi
        conn = mysql.connector.connect(**MYSQL_CONFIG)
        cursor = conn.cursor()

        # Query SQL
        query = '''
            SELECT   
                name
            FROM tbl_parameter WHERE name = %s
        '''

        # Jalankan query
        cursor.execute(query,(parameter,))
        result = cursor.fetchone() # Ambil nilai langsung
        if result:
            print(f"Parameter {parameter} Terdaftar ")
            return True
        else:
            print(f"Parameter {parameter} Tidak Terdaftar")
            return False

    except Exception as e:
        print(f"Terjadi kesalahan: {e}")
        return False

    finally:
        # Tutup koneksi
        if 'cursor' in locals(): cursor.close()
        if 'conn' in locals(): conn.close()
        
def cekRainTipe():  #cek apakah sensor rain di GPIO apa di Modbus
    try:
        # Membuka koneksi
        conn = mysql.connector.connect(**MYSQL_CONFIG)
        cursor = conn.cursor()

        # Query SQL
        query = '''
            SELECT   
                tipe
            FROM tbl_parameter WHERE name = %s
        '''

        # Jalankan query
        cursor.execute(query,("Rainfall",))
        result = cursor.fetchone() # Ambil nilai langsung
        if result:
            print("Parameter Tipe :",result[0])
            return result[0]
        else:
            print("Parameter Tipe tidak di ketahui")
            return None

    except Exception as e:
        print(f"Terjadi kesalahan: {e}")
        return None

    finally:
        # Tutup koneksi
        if 'cursor' in locals(): cursor.close()
        if 'conn' in locals(): conn.close()
        
        
def ambilResolution():
    try:
        conn = mysql.connector.connect(**MYSQL_CONFIG)
        cursor = conn.cursor()
        query = "SELECT resolution FROM tbl_parameter Where tipe='GPIO'"
        cursor.execute(query)
        result = cursor.fetchone() # Ambil nilai langsung
        if result:
            data = result
        return data
    except Exception as e:
        print(f"[ERROR] Gagal memasukkan data ke database: {e}")    
        return 0
    finally:
        # Tutup koneksi
        if 'cursor' in locals(): cursor.close()
        if 'conn' in locals(): conn.close()
        
    
def cekAutoMeasure():
    try:
        # Membuka koneksi
        conn = mysql.connector.connect(**MYSQL_CONFIG)
        cursor = conn.cursor()

        # Query SQL
        query = "SELECT `automeasure` FROM `tbl_setting`"

        # Jalankan query
        cursor.execute(query)
        result = cursor.fetchone() # Ambil nilai langsung
        if result:
            automeasure =int(result[0])
            print("Auto Measure :",automeasure)
            return automeasure
        else:
            print("Parameter Tipe tidak di ketahui")
            return int(0)

    except Exception as e:
        print(f"Terjadi kesalahan: {e}")
        return int(0)

    finally:
        # Tutup koneksi
        if 'cursor' in locals(): cursor.close()
        if 'conn' in locals(): conn.close()

def insert_data(ph, tss, nh3n, cod, depth, debit, rainfall, temperature, waterpressure):
    status_auto = cekAutoMeasure()
    if status_auto:  # hanya berjalan insert jika automeasure aktif
        date = ambilDate()
        dateall = ambilDateAll()
        datetimelokal = ambilDateTime()
        
        query = """
        INSERT INTO tbl_sensor_data (date, dateall, datetime, ph, tss, nh3n, cod, depth, debit, rainfall, temperature, waterpressure)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
        """
        
        try:
            conn = mysql.connector.connect(**MYSQL_CONFIG)
            cursor = conn.cursor()

            values = (
                date, dateall, datetimelokal,
                ph, tss, nh3n, cod, depth, debit,
                rainfall, temperature, waterpressure
            )
            #values = tuple("NULL" if v is None else v for v in values) # ganti jika None menjadi 0
            cursor.execute(query, values)
            conn.commit()
            cursor.close()
            conn.close()

            print(f"[INFO] Data berhasil dimasukkan: {values}")
        except Exception as e:
            print(f"[ERROR] Gagal memasukkan data ke database: {e}")
    else:
        print("[INFO] Penyimpanan ke database dimatikan karena Auto Measure tidak aktif")
        

def insert_manual_reading(ph, tss, nh3n, cod, depth, debit, rainfall, temperature, waterpressure):
    date = ambilDate()
    dateall = ambilDateAll()
    datetimelokal = ambilDateTime()
        
    query = """
    INSERT INTO tbl_sensor_data (date, dateall, datetime,tipe ,ph, tss, nh3n, cod, depth, debit, rainfall, temperature, waterpressure)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
    """
       
    try:
        conn = mysql.connector.connect(**MYSQL_CONFIG)
        cursor = conn.cursor()
        values = (
                date, dateall, datetimelokal,"manual",
                ph, tss, nh3n, cod, depth, debit,
                rainfall, temperature, waterpressure
        )
        cursor.execute(query, values)
        conn.commit()
        cursor.close()
        conn.close()

        print(f"[INFO] Data berhasil dimasukkan: {values}")
    except Exception as e:
        print(f"[ERROR] Gagal memasukkan data ke database: {e}")
    
def data_kalibrasi(parameter):
    
    try:
        # Membuka koneksi
        conn = mysql.connector.connect(**MYSQL_CONFIG)
        cursor = conn.cursor()

        # Query SQL
        query = "SELECT `offset` FROM `tbl_kalibrasi` WHERE `name`=%s"

        # Jalankan query
        cursor.execute(query,(parameter,))
        result = cursor.fetchone() # Ambil nilai langsung
        if result:
            offset = result[0]
            return float(offset)
        else:
            print("Kalibrasi Parameter tidak di ketahui")
            return int(0)

    except Exception as e:
        print(f"Terjadi kesalahan: {e}")
        return int(0)

    finally:
        # Tutup koneksi
        if 'cursor' in locals(): cursor.close()
        if 'conn' in locals(): conn.close()