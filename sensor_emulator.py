# TEST PERSISTENCE
import requests
import random
import time
import math
import json

# Configuration
SERVER_URL = "https://roboreactor.com"  # Update with your server's IP/port
EMAIL = "kornbot380@hotmail.com"      # Example email
PROJECT = "Smart_Robots"

def post_sensor_data(sensor_payload):
    url = f"{SERVER_URL}/sensor_postdata"
    data = {
        "email": EMAIL,
        "project_name": PROJECT,
        "sensor_payload": sensor_payload
    }
    try:
        response = requests.post(url, json=data)
        if response.status_code == 200:
            print(f"Update Success: {response.json()}")
        else:
            print(f"Error {response.status_code}: {response.text}")
    except Exception as e:
        print(f"Failed to connect: {e}")

# 🔋 BMS (Battery Management)
def emulate_bms():
    soc = random.uniform(20.0, 100.0)
    post_sensor_data({"BMS_sensor": {"main_pack": soc, "aux_cell_1": soc-2, "temp_sensor_5": 35.5}})

# 🌬️ Environment
def emulate_environment():
    temp = random.uniform(22.0, 28.0)
    hum = random.uniform(40.0, 60.0)
    post_sensor_data({
        "Environment_sensor": {
            "temp_hum_1": temp,
            "pressure": random.uniform(1013, 1025),
            "air_quality": random.randint(10, 50)
        }
    })

# 🏎️ Motion (IMU)
def emulate_motion():
    post_sensor_data({
        "Motion_sensor": {
            "imu_1": {
                "x": random.uniform(-0.1, 0.1),
                "y": random.uniform(-0.1, 0.1),
                "z": random.uniform(0.95, 1.05)
            },
            "radar_2": random.uniform(0, 5)
        }
    })

# ❤️ Biometric
def emulate_biometric():
    hr = random.randint(60, 100)
    post_sensor_data({
        "Biometric_sensor": {
            "heart_rate": hr,
            "body_temp": random.uniform(36.0, 37.5),
            "skin_conductance": random.uniform(0.1, 5.0)
        }
    })

# 🛰️ Position (GPS/RTK)
def emulate_position():
    post_sensor_data({
        "Position_sensor": {
            "gps_rtk": {
                "x": random.uniform(10.0, 10.1),
                "y": random.uniform(105.0, 105.1),
                "z": 1.2
            }
        }
    })

# 🧪 Chemical
def emulate_chemical():
    post_sensor_data({
        "Chemical_sensor": {
            "gas_analyzer": random.randint(300, 500),
            "ph_level": random.uniform(6.8, 7.4)
        }
    })

# 📊 Array Sensor (Heatmap)
def emulate_array():
    # 10x10 Heatmap Grid
    grid = []
    peak_x, peak_y = random.randint(2, 7), random.randint(2, 7)
    for x in range(10):
        row = []
        for y in range(10):
            val = 8.5 + 0.5 * math.exp(-((x - peak_x)**2 + (y - peak_y)**2) / 8)
            row.append(round(val, 4))
        grid.append(row)
    
    post_sensor_data({
        "Array_sensor": {
            "Tactile_finger_sensor_1": grid,
            "sensor_2": grid # or generate a different one
        }
    })

# 🎵 Audio Sensor (Waveform)
def emulate_audio():
    # Generate a simple waveform (50 samples)
    samples = [round(math.sin(i * 0.5) * 0.05 + random.uniform(-0.01, 0.01), 4) for i in range(50)]
    post_sensor_data({
        "Audio_sensor": {
            "mic_1": samples,
            "mic_2": samples,
            "soundcard_3": samples

        }
    })

if __name__ == "__main__":
    print(f"Starting Multi-Sensor Emulation for {EMAIL}...")
    print(f"Targeting server: {SERVER_URL}")
    
    try:
        while True:
            # Emulate all sensor groups
            emulate_bms()
            emulate_environment()
            emulate_motion()
            emulate_biometric()
            emulate_position()
            emulate_chemical()
            emulate_array()
            emulate_audio()
            
            print("--- Cycle complete. Waiting 1 second. ---")
            time.sleep(1)
            
    except KeyboardInterrupt:
        print("\nEmulation stopped by user.")
