import serial
import time

# Configure the serial port. You might need to change the port name.
ser = serial.Serial('/dev/ttyACM0', 9600)  # Change '/dev/ttyACM0' to your Arduino's port
ser.flush()  # Flush the serial buffer

def send_angles(angles):
    angles_str = ','.join(str(angle) for angle in angles)
    print(angles_str)
    ser.write((angles_str + '\n').encode())
    ser.flush()

angle_pairs = [(azimuth, elevation) for azimuth in range(-90, 91, 45) for elevation in range(-30, 90, 5)]
print(angle_pairs)
angle_pairs = [((azimuth + 90) % 360, (elevation + 90) % 360) for azimuth, elevation in angle_pairs]

print(angle_pairs)
send_angles(angle_pairs[0])
time.sleep(5)


while True:
    for angle_pair in angle_pairs:
        # input("Press Enter to send angle pairs...")
        send_angles(angle_pair)
        time.sleep(2)
    for angle_pair in angle_pairs:
        input("Press Enter to send angle pairs...")
        send_angles(angle_pair)
        # time.sleep(4)
