#include <ESP32Servo.h> // ESP32Servo library installed by Library Manager
#include "ESC.h" // RC_ESP library installed by Library Manager
#include "BluetoothSerial.h"

#define ESC_PIN(15) // connected to ESC control wire
// Note: the following speeds may need to be modified for your particular hardware.
#define MIN_SPEED 1040 // speed just slow enough to turn motor off
#define MAX_SPEED 1240 // speed where my motor drew 3.6 amps at 12v.

ESC myESC(ESC_PIN, 1000, 2000, 500); // ESC_Name (PIN, Minimum Value, Maximum Value, Arm Value)

long int val; // variable to read the value from the analog pin

const char * pin = "1234";
String device_name = "ESP32-BT-Slave";

BluetoothSerial SerialBT;

void setup() {
  Serial.begin(115200);
  SerialBT.begin(device_name);
  pinMode(ESC_PIN, OUTPUT);
  myESC.arm(); // Send the Arm command to ESC
  delay(5000); // Wait a while

  // the following loop turns on the motor slowly, so get ready
  for (int i = 0; i < 350; i++) { // run speed from 840 to 1190
    myESC.speed(MIN_SPEED - 200 + i); // motor starts up about half way through loop
    delay(10);
  }
} // speed will now jump to pot setting

void loop() {
  if (SerialBT.available()) {
    val = atol(SerialBT.read());
    Serial.println(val)
  }
  delay(20);
  val = map(val, 0, 100, MIN_SPEED, MAX_SPEED); // scale pot reading to valid speed range
  myESC.speed(val); // sets the ESC speed
  delay(10); // Wait for a while
}
