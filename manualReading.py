
from config import ambilParameterDb,cekParameterDb,cekRainTipe,insert_manual_reading,data_kalibrasi
from sensor import get_at500_data,get_mace_data,get_rain_data,get_rain_data_GPIO

data = ambilParameterDb()
listParameter = []  #parameter yang bener-bener terdaftar atau sedang digunakan akan di tampung
for row in data:
    cekParameter = cekParameterDb(row)
    if cekParameter:
        listParameter.append(row)

#niai default adalah none
ph = tss = nh3n = cod = depth = debit = rainfall = temperature = waterpressure = tipping_count = None

#jika terdapat parameter yang digunakan sama di lisparameter maka fungsi dijalankan 

if "pH" in listParameter: #cek paramter terdatar apa tidak jika terdaftar akan jalan
    value = get_at500_data("pH") # return ketika dijalnkan script jika ada salah atau maka nilai default None
    nilai = value if value is not None else 0 # merubah jika nilai None maka 0 jika ada value, value dari return di pakai
    kalibrasi = data_kalibrasi("pH")
    ph = float(nilai) + float(kalibrasi)
    
    
if "TSS" in listParameter:
    value = get_at500_data("TSS")
    nilai = value if value is not None else 0 # merubah jika nilai None maka 0 jika ada value, value dari return di pakai
    kalibrasi = data_kalibrasi("TSS")
    tss = float(nilai) + float(kalibrasi)

if "NH3-N" in listParameter:
    value = get_at500_data("NH3-N")
    nilai = value if value is not None else 0 # merubah jika nilai None maka 0 jika ada value, value dari return di pakai
    kalibrasi = data_kalibrasi("NH3-N")
    nh3n = float(nilai) + float(kalibrasi)

    

if "COD" in listParameter:
    value = get_at500_data("COD")
    nilai = value if value is not None else 0 # merubah jika nilai None maka 0 jika ada value, value dari return di pakai
    kalibrasi = data_kalibrasi("COD")
    cod = float(nilai) + float(kalibrasi)


if "Temperature" in listParameter:
    value = get_at500_data("Temperature")
    nilai = value if value is not None else 0 # merubah jika nilai None maka 0 jika ada value, value dari return di pakai
    kalibrasi = data_kalibrasi("Temperature")
    temperature = float(nilai) + float(kalibrasi)


if "Water Pressure" in listParameter:
    value = get_at500_data("Water Pressure")
    nilai = value if value is not None else 0 # merubah jika nilai None maka 0 jika ada value, value dari return di pakai
    kalibrasi = data_kalibrasi("Water Pressure")
    waterpressure = float(nilai) + float(kalibrasi)

if "Depth" in listParameter:
    value = get_mace_data("Depth")
    nilai = value if value is not None else 0 # merubah jika nilai None maka 0 jika ada value, value dari return di pakai
    kalibrasi = data_kalibrasi("Depth")
    depth = float(nilai) + float(kalibrasi)
    
if "Debit" in listParameter:
    value = get_mace_data("Debit")
    nilai = value if value is not None else 0 # merubah jika nilai None maka 0 jika ada value, value dari return di pakai
    kalibrasi = data_kalibrasi("Debit")
    ddebit = float(nilai) + float(kalibrasi)
    

if "Rainfall" in listParameter:
    rain_tipe = cekRainTipe()
    if rain_tipe == "GPIO":
        tipping_count, rainfall_val = get_rain_data()
    elif rain_tipe == "modbus":
        tipping_count, rainfall_val = get_rain_data()
    else:
        rainfall_val = 0

    nilai = rainfall_val if rainfall_val is not None else 0
    kalibrasi = data_kalibrasi("Rainfall")
    rainfall = float(nilai) + float(kalibrasi)


insert_manual_reading(ph, tss, nh3n, cod, depth, debit, rainfall, temperature, waterpressure)

