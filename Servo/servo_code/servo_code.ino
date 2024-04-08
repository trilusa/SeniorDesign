#include <Servo.h> // includes servo library
Servo servo1; // diferentiates between the two servos
Servo servo2; // diferentiates between the two servos

#define STEP_SIZE 1    // Change this value to make the movement step bigger or smaller
#define INITIAL_DELAY 15  // Initial delay in milliseconds between each servo movement step
#define FINAL_DELAY 15    // Final delay in milliseconds for a slower ending movement
#define ACCELERATION_STEPS 5 // Number of steps to incrementally increase/decrease delay (simulate acceleration/deceleration)


void setup() {
  Serial.begin(9600); // sets the baud rate, data rate in bits per second
  
  servo1.attach(9); // Attach servo to pin 9, bottom servo that turns left and right
  servo2.attach(10); // Attach another servo to pin 10, top servo that tilts back and forward
  moveServo(servo1, servo1.read(), 90);
  moveServo(servo2, servo2.read(), 90);
}

void loop() {    
  if (Serial.available() > 1) { //checks if there is any data available to be read from the serial buffer, if it is greater than one byte
    int angle1, angle2; // intergers named angle1 and angle2 that are then assigned values in the serial monitor
    angle1 = Serial.parseInt(); // Read the first angle value from serial monitor, serial.parseInt looks for the next valid integer in the incoming serial
    angle2 = Serial.parseInt(); // Read the second angle value from serial monitor, serial.parseInt looks for the next valid integer in the incoming serial
    
    angle1 = constrain(angle1, 0, 180); // Limit angles to between 0 and 180, if a value greater than 180 is entered than the servo is moved to the 180 position
    angle2 = constrain(angle2, 50, 180); // Limit angles to between 0 and 180, if a value greater than 180 is entered than the servo is moved to the 180 position
    
    moveServo(servo1, servo1.read(), angle1);
    moveServo(servo2, servo2.read(), angle2);

    // Serial.print("Servo 1 angle: "); // Prints "Servo 1 angle: " to serial monitor
    // Serial.println(servo1.read()); // Print current angle of servo 1 to serial monitor
    // Serial.print("Servo 2 angle: "); // Print "Servo 2 angle: " to serial monitor
    // Serial.println(servo2.read()); // Print current angle of servo 2 to serial monitor
  } 
}

void moveServo(Servo servo, int fromAngle, int toAngle) {
  int step = (toAngle > fromAngle) ? STEP_SIZE : -STEP_SIZE;
  int delayTime = INITIAL_DELAY;
  int delayStep = (INITIAL_DELAY - FINAL_DELAY) / ACCELERATION_STEPS;

  for (int angle = fromAngle; (step > 0) ? angle <= toAngle : angle >= toAngle; angle += step) {
    servo.write(angle);
    delay(delayTime);
    if (angle - fromAngle < ACCELERATION_STEPS * STEP_SIZE || toAngle - angle < ACCELERATION_STEPS * STEP_SIZE) {
      delayTime -= delayStep; // Decrease delay to speed up
    } else {
      delayTime = FINAL_DELAY; // Keep constant speed
    }
    delayTime = max(delayTime, FINAL_DELAY); // Ensure delay never goes below FINAL_DELAY
  }
}
