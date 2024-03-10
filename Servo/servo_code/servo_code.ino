#include <Servo.h> // includes servo library
Servo servo1; // diferentiates between the two servos
Servo servo2; // diferentiates between the two servos

#define DELAY 2000   // 2 second delay


void setup() {
  Serial.begin(9600); // sets the baud rate, data rate in bits per second
  
  servo1.attach(9); // Attach servo to pin 9, bottom servo that turns left and right
  servo2.attach(10); // Attach another servo to pin 10, top servo that tilts back and forward

  servo1.write(90); // sets initial position in upright position for head
  servo2.write(90); // sets initial position facing forward
}

void loop() {
  
  // delay(DELAY); //  Hold the microcontroller for 2 seconds
    
  if (Serial.available() > 1) { //checks if there is any data available to be read from the serial buffer, if it is greater than one byte
    int angle1, angle2; // intergers named angle1 and angle2 that are then assigned values in the serial monitor
    angle1 = Serial.parseInt(); // Read the first angle value from serial monitor, serial.parseInt looks for the next valid integer in the incoming serial
    angle2 = Serial.parseInt(); // Read the second angle value from serial monitor, serial.parseInt looks for the next valid integer in the incoming serial
    
    angle1 = constrain(angle1, 0, 180); // Limit angles to between 0 and 180, if a value greater than 180 is entered than the servo is moved to the 180 position
    angle2 = constrain(angle2, 50, 180); // Limit angles to between 0 and 180, if a value greater than 180 is entered than the servo is moved to the 180 position
    
    servo1.write(angle1); // Move servo1 to specified angle
    servo2.write(angle2); // Move servo2 to specified angle
    
    Serial.print("Servo 1 angle: "); // Prints "Servo 1 angle: " to serial monitor
    Serial.println(servo1.read()); // Print current angle of servo 1 to serial monitor
    Serial.print("Servo 2 angle: "); // Print "Servo 2 angle: " to serial monitor
    Serial.println(servo2.read()); // Print current angle of servo 2 to serial monitor
  }
/*  
  else
    {   
    servo1.write(90); // upright position for head
    servo2.write(90); // faces forward
    delay(DELAY); //  Hold the microcontroller for 2 seconds
    }
  */  
}
