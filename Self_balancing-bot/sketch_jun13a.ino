#include <Adafruit_MPU6050.h>
#include <Adafruit_Sensor.h>
#include <Wire.h>

double PAa,RAa,PAg,RAg;
unsigned long curr, prev=0, LoopTime;
Adafruit_MPU6050 mpu;
float accy,accx,accz;
float gx,gy,gz;
float accxc,accyc,acczc,gxc,gyc,gzc;
float sumr,sump,ct=0;
float anglePercent;
float angle = 0;
float inputSpeed = 0;
float pPart = 0;
float dPart = 0;
float i_part = 0;
float iPart = 0;
float ipart = 0;
float p = 0.5;
float i = 0.000002;
float d = 1.2;
float prevInput = 0; 
float array[50];
int k=0;
float PID_speed = 0;

float KalmanAngleRoll=0, KalmanUncertaintyAngleRoll=2*2;
float KalmanAnglePitch=0, KalmanUncertaintyAnglePitch=2*2;
float Kalman1DOutput[]={0,0};

int motor1Pin1 = 27; 
int motor1Pin2 = 26; 
int enable1Pin = 34; 
int motor2Pin1 = 33;
int motor2Pin2 = 32;
int enable2Pin = 14;
// Setting PWM properties
const int freq = 30000;
const int pwmChannel1 = 0;
const int pwmChannel2 = 1;
const int resolution = 8;
int dutyCycle = 150;

void kalman_1d(float KalmanState, float KalmanUncertainty, float KalmanInput, float KalmanMeasurement) {
  KalmanState=KalmanState+0.004*KalmanInput;
  KalmanUncertainty=KalmanUncertainty + 0.004 * 0.004 * 4 * 4;
  float KalmanGain=KalmanUncertainty * 1/(1*KalmanUncertainty + 3 * 3);
  KalmanState=KalmanState+KalmanGain * (KalmanMeasurement-KalmanState);
  KalmanUncertainty=(1-KalmanGain) * KalmanUncertainty;
  Kalman1DOutput[0]=KalmanState; 
  Kalman1DOutput[1]=KalmanUncertainty;
}

void setup() {
  // sets the pins as outputs:
  pinMode(motor1Pin1, OUTPUT);
  pinMode(motor1Pin2, OUTPUT);
  pinMode(enable1Pin, OUTPUT);
  pinMode(motor2Pin1, OUTPUT);
  pinMode(motor2Pin2, OUTPUT);
  pinMode(enable2Pin, OUTPUT);
  
  // configure LED PWM functionalitites
  ledcSetup(pwmChannel1, freq, resolution);
  ledcSetup(pwmChannel2, freq, resolution);
  
  // attach the channel to the GPIO to be controlled
  ledcAttachPin(enable1Pin, pwmChannel1);
  ledcAttachPin(enable2Pin, pwmChannel2);

  for (int i=0;i<50;i++){
  array[i]=0;
  }

  Serial.begin(115200);

   if (!mpu.begin()) {
    Serial.println("Failed to find MPU6050 chip");
    while (1) {
      delay(10);
    }
  }
  Serial.println("MPU6050 Found!");
  sensors_event_t a, g, temp;
  mpu.getEvent(&a, &g, &temp);
  accxc = a.acceleration.x;
  accyc = a.acceleration.y;
  acczc = a.acceleration.z - 9.81;
  gxc = g.gyro.x;
  gyc = g.gyro.y;
  gzc = g.gyro.z;
  mpu.setAccelerometerRange(MPU6050_RANGE_8_G);
  mpu.setGyroRange(MPU6050_RANGE_500_DEG);
  mpu.setFilterBandwidth(MPU6050_BAND_21_HZ);
  delay(100);
}

void loop() {

  curr=millis();
  LoopTime= curr-prev;
  prev=curr;
  /* Get new sensor events with the readings */ 
  sensors_event_t a, g, temp;
  mpu.getEvent(&a, &g, &temp);

  /* Print out the values */
  accx = a.acceleration.x;
  accy = a.acceleration.y;
  accz = a.acceleration.z;
  gx = g.gyro.x ;
  gy = g.gyro.y ;
  
  PAa = atan((-1*accx/(sqrt(accy*accy + accz*accz)))) *180/PI;
  RAa = (atan2(accy,accz))*180/PI +90;
  delay(100);


  //PID
  anglePercent = map(RAa, -90, 90, -100, 100);
  pPart = -1*p * anglePercent;

  dPart = d*(anglePercent - prevInput);
  prevInput = anglePercent;

  ipart-=array[k];
  array[k]=anglePercent;
  ipart+=array[k];
  if (k==0){
    k=49;
  }
  else{
    k-=1;
  }
  i_part = map(ipart, -4500, 4500, -100, 100);
  iPart = i*i_part;
  
  PID_speed = pPart + dPart + iPart;
  inputSpeed = map(PID_speed, -1*p*100-1*d*200-i*100, p*100+d*200+i*100, -100, 100);

  Serial.print("Pitch angle = ");
  Serial.print(PAa);
  Serial.print("Roll angle = ");
  Serial.print(RAa);
  Serial.print("Input Speed = ");
  Serial.println(inputSpeed);
  
  //control function
  if (inputSpeed >= 0){
    digitalWrite(motor1Pin1, LOW);
    digitalWrite(motor1Pin2, HIGH);
    digitalWrite(motor2Pin1, LOW);
    digitalWrite(motor2Pin2, HIGH);
    dutyCycle = map(inputSpeed, 0, 100, 210, 255);
    ledcWrite(pwmChannel2, dutyCycle);
  }else{
    int inputPositive = -1*inputSpeed;
    digitalWrite(motor1Pin1, HIGH);
    digitalWrite(motor1Pin2, LOW);
    digitalWrite(motor2Pin1, HIGH);
    digitalWrite(motor2Pin2, LOW);
    dutyCycle = map(inputPositive, 0, 100, 180, 255);
    ledcWrite(pwmChannel2, dutyCycle);
    }
  dutyCycle = 150;
}
