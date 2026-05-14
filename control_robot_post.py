import requests
import time
import json
import sys
import math

BASE_URL = sys.argv[1].rstrip("/") if len(sys.argv) > 1 else "https://roboreactor.com"  #"http://127.0.0.1:8095"
email = "kornbot380@hotmail.com"
project_name = "Smart_Robots"  #bd3  #Forklift #teslacoil358@gmail.com
def euler_to_quaternion(roll_deg, pitch_deg, yaw_deg):
    """
    Converts Euler angles (in degrees) to a Quaternion.
    Roll = rotation around X-axis
    Pitch = rotation around Y-axis
    Yaw = rotation around Z-axis
    """
    roll = math.radians(roll_deg)
    pitch = math.radians(pitch_deg)
    yaw = math.radians(yaw_deg)

    cy = math.cos(yaw * 0.5)
    sy = math.sin(yaw * 0.5)
    cp = math.cos(pitch * 0.5)
    sp = math.sin(pitch * 0.5)
    cr = math.cos(roll * 0.5)
    sr = math.sin(roll * 0.5)

    return {
        "x": sr * cp * cy - cr * sp * sy,
        "y": cr * sp * cy + sr * cp * sy,
        "z": cr * cp * sy - sr * sp * cy,
        "w": cr * cp * cy + sr * sp * sy
    }

def control_robot():
    url = f"{BASE_URL}/api/sim3/input"
    #angle_theta = math.arctan()
    # Payload containing position, steering angle, and joint controls
    x = 2.5
    z = 1.5
    steerangle = math.degrees(x/z)
    payload = {email: {project_name: {
        "target_position": {
            "x": x,
            "y": 0,
            "z": z
        },
        # Rotate the robot 45 degrees around the Z-axis (Yaw)
        "target_quaternion": euler_to_quaternion(roll_deg=0.0, pitch_deg=0.0, yaw_deg=45.0),
        "joint_targets": {
            #"S1": -1.3
            "shoulder":math.radians(40),
            "base":math.radians(45),
            "wrist":math.radians(20)
        },
        "steering_angle_deg": steerangle, #30.0,
        "timestamp": int(time.time() * 1000),
        "robot_name": "Robot_arm_01"  # Add or update this field for dynamic label
    }}}
    try:
        print(f"Sending POST request to {url}...")
        response = requests.post(url, json=payload, timeout=5)
        response.raise_for_status()
        print("Successfully sent control command.")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
    except requests.exceptions.RequestException as e:
        print(f"Error sending request: {e}")
        if hasattr(e, 'response') and e.response is not None:
            print(f"Response body: {e.response.text}")

if __name__ == "__main__":
    control_robot()
