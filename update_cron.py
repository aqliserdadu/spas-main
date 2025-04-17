import os
import mysql.connector
from dotenv import load_dotenv

# Load environment variables
env_path = "config/.env"  # Path ke .env
if not load_dotenv(dotenv_path=env_path):
    print(f"Error: .env file not found at {env_path}")
    exit(1)

# Ambil env variable
HOST = os.getenv('HOST')
USER = os.getenv('USERS')  # perhatikan nama variabel di .env juga
PASSWORD = os.getenv('PASSWORD')
DATABASE = os.getenv('DATABASE')

# Validasi env
if not all([HOST, USER, PASSWORD, DATABASE]):
    print("Error: Some environment variables are missing.")
    exit(1)

# Koneksi ke MySQL
conn = mysql.connector.connect(
    host=HOST,
    user=USER,
    password=PASSWORD,
    database=DATABASE
)

cursor = conn.cursor()

# Ambil interval (dalam menit) dari database
cursor.execute("SELECT interval FROM tbl_setting LIMIT 1")
row = cursor.fetchone()
interval = int(row[0]) if row else 2  # default ke 2 menit jika tidak ada data

cursor.close()
conn.close()

# Baris cron baru
cron_line = f"*/{interval} * * * * python3 /opt/SPAS-MAIN/main.py"

# Ambil isi crontab saat ini
current_crontab = os.popen("crontab -l").read().splitlines()

# Buang baris yang sudah mengandung main.py
new_crontab = [line for line in current_crontab if "main.py" not in line]
new_crontab.append(cron_line)

# Simpan ke file sementara
with open("new_cron.txt", "w") as f:
    f.write("\n".join(new_crontab) + "\n")

# Apply ke crontab
os.system("crontab new_cron.txt")
os.remove("new_cron.txt")
