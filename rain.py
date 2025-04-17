import RPi.GPIO as GPIO
from config import ambilResolution
import time


RAIN_SENSOR_PIN = 18  # Pin GPIO untuk sensor tipping bucket
RESOLUTION = ambilResolution() # Resolusi curah hujan per tipping (mm)

GPIO.setmode(GPIO.BCM)
GPIO.setup(RAIN_SENSOR_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

tipping_count = 0

def tipping_callback(channel):
    global tipping_count
    tipping_count += 1
    print(f"Tipping terdeteksi! Jumlah saat ini: {tipping_count}")

GPIO.add_event_detect(RAIN_SENSOR_PIN, GPIO.FALLING, callback=tipping_callback, bouncetime=300)

def get_rainfall():
    global tipping_count
    tipping_count = 0
    start_time = time.time()

    while time.time() - start_time < 60:
        time.sleep(1)  # Tunggu untuk mengurangi beban CPU

    total_rainfall = tipping_count * RESOLUTION
    return tipping_count, total_rainfall

def cleanup():
    GPIO.cleanup()
