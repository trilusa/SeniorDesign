import serial
import keyboard

# Replace 'COM3' with the port where your Arduino is connected
ser = serial.Serial('COM3', 9600, timeout=1)
# Define a list of angle pairs
angle_pairs = [(0, 0), (90, 90), (180, 180), (45, 45), (135, 135)]

def send_angles(angle_pair):
    """Send a pair of angles to the Arduino."""
    # Convert the tuple to a string and encode it to bytes
    data = f"{angle_pair[0]},{angle_pair[1]}\n".encode()
    ser.write(data)
    print(f"Sent angles: {angle_pair}")

# Main loop
print("Press any key to send the next set of angles from the list...")
index = 0
while True:
    try:
        if keyboard.read_key():  # Wait for a key press
            send_angles(angle_pairs[index])
            index = (index + 1) % len(angle_pairs)  # Move to next pair or loop back
    except KeyboardInterrupt:
        break  # Exit the loop if Ctrl+C is pressed

ser.close()  # Close the serial connection when done
