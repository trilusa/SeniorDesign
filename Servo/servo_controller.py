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

# angles = [(90, el) for el in range(50, 181)]
az_el_grid = [[(az, el) for az in range(0, 181)] for el in range(50, 181)]
az_el_90 = [t for sublist in az_el_grid for t in sublist if t[0] == 90]
angles= [(az, el) for az in range(10, 191, 1) for el in range(50, 151, 50)]
# angle_pairs = [(0, elevation) for elevat
# ion in range(-50, 90, 1)]
#center = (90,90)
print(az_el_90)
# angle_pairs = [((azimuth + 90) % 360, (elevation + 90) % 360) for azimuth, elevation in angle_pairs]

# print(angle_pairs)
send_angles((90,90))
time.sleep(5)

angles.reverse()
while True:
    for angle_pair in angles:
        # input("Press Enter to send angle pairs...")
        send_angles(angle_pair)
        time.sleep(2.8)
    # az_el_90.reverse()
        
    # for angle_pair in reversed(az_el_90):
    #     input("Press Enter to send angle pairs...")
    #     send_angles(angle_pair)
    #     # time.sleep(4)
