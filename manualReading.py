
from config import ambilParameterDb,cekParameterDb,cekRainTipe,insert_manual_reading
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
    ph = value if value is not None else 0 # merubah jika nilai None maka 0 jika ada value, value dari return di pakai

if "TSS" in listParameter:
    value = get_at500_data("TSS")
    tss = value if value is not None else 0

if "NH3-N" in listParameter:
    value = get_at500_data("NH3-N")
    nh3n = value if value is not None else 0

if "COD" in listParameter:
    value = get_at500_data("COD")
    cod = value if value is not None else 0

if "Temperature" in listParameter:
    value = get_at500_data("Temperature")
    temperature = value if value is not None else 0

if "Water Pressure" in listParameter:
    value = get_at500_data("Water Pressure")
    waterpressure = value if value is not None else 0

if "Depth" in listParameter:
    value = get_mace_data("Depth")
    depth = value if value is not None else 0
    
if "Debit" in listParameter:
    value = get_mace_data("Debit")
    debit = value if value is not None else 0
    
    
if "Rainfall" in listParameter:
    rain_tipe = cekRainTipe()
    if rain_tipe == "GPIO":
        #tipping_count, rainfall_val = get_rain_data_GPIO()
        tipping_count, rainfall_val = get_rain_data()
    elif rain_tipe == "modbus":
        tipping_count, rainfall_val = get_rain_data()
    else:
        rainfall_val = 0

    rainfall = rainfall_val if rainfall_val is not None else 0


insert_manual_reading(ph, tss, nh3n, cod, depth, debit, rainfall, temperature, waterpressure)

