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
i=0
# angle_pairs = [(85, 85), (80,80),(75, 75), (70,70),(60,60)]  # Example angle pairs
angle_pairs = [(azimuth, elevation) for azimuth in range(0, 181, 15) for elevation in range(60, 121, 15)]
print(angle_pairs)
for angle_pair in angle_pairs:
    input("Press Enter to send angle pairs...")
    send_angles(angle_pair)
    time.sleep(5) 
# try:
#     while True:
#         #input("Press Enter to send angle pairs...")
#         # Define your angle pairs here
#         send_angles(angle_pairs[i])
#         i=i+1
#         time.sleep(0.05)  # Optional delay to avoid flooding the Arduino
# except KeyboardInterrupt:
#     print("Program terminated by user.")
# finally:
#     ser.close()  # Close the serial connection when done
