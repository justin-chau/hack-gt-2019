#include "TeensyStep.h"

#define SPR_1 800
#define SPR_2 800

#define W_MAX_1 18
#define W_MAX_2 26

#define STEPPER_1_STEP_PIN 2
#define STEPPER_1_DIRECTION_PIN 3
#define STEPPER_2_STEP_PIN 4
#define STEPPER_2_DIRECTION_PIN 5
#define YAW_LIM_PIN 31
#define PITCH_LIM_PIN 32

#define YAW_OFFSET 840
#define PITCH_OFFSET 350

#define YAW_MIN -10000
#define YAW_MAX 10000

#define PITCH_MIN -2000
#define PITCH_MAX 10000

#define DEG2STEP 2.2222
#define PITCH_RATIO 2.57142
#define YAW_RATIO 4

#define HOMING_STATE 0
#define TRACKING_STATE 1

#define Kp_1 0.01
#define Kp_2 0.01
#define MIN_ERROR 2
#define YAW_DIR 1
#define PITCH_DIR 1

double input_1, input_2, output_1, output_2, error_1, error_2;
double setpoint_1 = 0;
double setpoint_2 = 0;

Stepper stepper_1(STEPPER_1_STEP_PIN, STEPPER_1_DIRECTION_PIN);
Stepper stepper_2(STEPPER_2_STEP_PIN, STEPPER_2_DIRECTION_PIN);

RotateControl speedController_1, speedController_2;
StepControl homingController;

//Genearl Vars
int count = 0;
int state;

//Serial vars
const byte numChars = 32;
char receivedChars[numChars];
char tempChars[numChars];
boolean newData = false;

//Stepper vars
float yaw_deg_center = 0.0;
float yaw_deg = 0.0;
float pitch_deg = 0.0;

bool yawStop = false;
bool pitchStop = false;

bool running_2 = false;
bool stopping_2 = false;
bool prev_Running_2 = false;

bool running_1 = false;
bool stopping_1 = false;
bool prev_Running_1 = false;

void setup() {
  Serial.begin(9600);

  pinMode(YAW_LIM_PIN, INPUT_PULLUP);
  pinMode(PITCH_LIM_PIN, INPUT_PULLUP);
  pinMode(LED_BUILTIN, OUTPUT);

  state = HOMING_STATE;
  delay(5000);
}

void loop() {
  switch (state) {

    case 4:
      stepper_1.setPosition(0);
      stepper_2.setPosition(0);

      state = TRACKING_STATE;
      while (!newData) {
        digitalWrite(LED_BUILTIN, HIGH);
        recvWithStartEndMarkers();
        if (newData == true) {
          strcpy(tempChars, receivedChars);
          parseSerialInputs();
          yaw_deg_center = yaw_deg;
        }
      }
      digitalWrite(LED_BUILTIN, LOW);
      state = TRACKING_STATE;
      break;

    case 3:
      readLimitSwitches();
      Serial.print(digitalRead(YAW_LIM_PIN));
      Serial.print(' ');
      Serial.println(digitalRead(PITCH_LIM_PIN));
      break;

    case HOMING_STATE:
      readLimitSwitches();

      stepper_1
      .setMaxSpeed(-RPMTS(30, 1))
      .setAcceleration(10000);
      speedController_1.rotateAsync(stepper_1);

      while (!yawStop) {
        readLimitSwitches();
      }
      speedController_1.emergencyStop();

      stepper_1.setMaxSpeed(RPMTS(15, 1));
      speedController_1.rotateAsync(stepper_1);

      delay(500);
      speedController_1.emergencyStop();

      stepper_1
      .setMaxSpeed(-RPMTS(5, 1));
      speedController_1.rotateAsync(stepper_1);

      readLimitSwitches();
      while (!yawStop) {
        readLimitSwitches();
      }
      speedController_1.emergencyStop();
      stepper_1.setPosition(-YAW_OFFSET);

      stepper_1
      .setMaxSpeed(RPMTS(30, 1))
      .setTargetAbs(0);

      stepper_2
      .setMaxSpeed(-RPMTS(30, 2))
      .setAcceleration(10000);
      speedController_2.rotateAsync(stepper_2);

      while (!pitchStop) {
        readLimitSwitches();
      }
      speedController_2.emergencyStop();

      stepper_2.setMaxSpeed(RPMTS(15, 2));
      speedController_2.rotateAsync(stepper_2);

      delay(500);
      speedController_2.emergencyStop();

      stepper_2
      .setMaxSpeed(-RPMTS(5, 2));
      speedController_2.rotateAsync(stepper_2);

      readLimitSwitches();
      while (!pitchStop) {
        readLimitSwitches();
      }
      speedController_2.emergencyStop();
      stepper_2.setPosition(-PITCH_OFFSET);

      stepper_2
      .setMaxSpeed(RPMTS(30, 2))
      .setTargetAbs(0);
      homingController.move(stepper_1, stepper_2);

      homingController.stop();

      state = TRACKING_STATE;
      while (!newData) {
        recvWithStartEndMarkers();
        if (newData == true) {
          strcpy(tempChars, receivedChars);
          parseSerialInputs();
          yaw_deg_center = yaw_deg;
          setpoint_2 = yaw_deg_center;
        }
      }
      break;

    case TRACKING_STATE:

      readLimitSwitches();
      recvWithStartEndMarkers();
      if (newData == true) {
        strcpy(tempChars, receivedChars);
        parseSerialInputs();
        newData = false;
      }

      input_1 = stepper_1.getPosition();
      if ((abs(yaw_deg - yaw_deg_center) < 160)) {
        setpoint_1 = -(yaw_deg - yaw_deg_center) * YAW_RATIO * DEG2STEP;
      }

      input_2 = stepper_2.getPosition();
      setpoint_2 = (pitch_deg) * PITCH_RATIO * DEG2STEP;
      if (pitch_deg > 120) {
        setpoint_2 = 120 * PITCH_RATIO * DEG2STEP;
      }
      else if (pitch_deg < -60) {
        setpoint_2 = -60 * PITCH_RATIO * DEG2STEP;
      }

      error_1 = setpoint_1 - input_1;
      error_2 = setpoint_2 - input_2;

      /**************** YAW STEPPER CONTROL ****************/

      running_1 = abs(error_1) > MIN_ERROR;

      if (!stopping_1 && !prev_Running_1 && running_1) {
        stepper_1
        .setMaxSpeed(RPMTS(W_MAX_1, 1))
        .setAcceleration(8000);
        speedController_1.rotateAsync(stepper_1);
      }

      if (stopping_1) {
        speedController_1.stopAsync();
        if (!speedController_1.isRunning()) {
          stopping_1 = false;
        }
      }
      else if (running_1) {
        output_1 = Kp_1 * YAW_DIR * (setpoint_1 - input_1);
        if (abs(output_1) > W_MAX_1)
          output_1 = output_1 / abs(output_1);
        speedController_1.overrideSpeed(output_1);
      }
      else {
        stopping_1 = true;
      }

      prev_Running_1 = running_1;

      /**************** PITCH STEPPER CONTROL ****************/

      running_2 = abs(error_2) > MIN_ERROR;

      if (!stopping_2 && !prev_Running_2 && running_2) {
        stepper_2
        .setMaxSpeed(RPMTS(W_MAX_2, 2))
        .setAcceleration(8000);
        speedController_2.rotateAsync(stepper_2);
      }

      if (stopping_2) {
        speedController_2.stopAsync();
        if (!speedController_2.isRunning()) {
          stopping_2 = false;
        }
      }
      else if (running_2) {
        output_2 = Kp_2 * PITCH_DIR * (setpoint_2 - input_2);
        if (abs(output_2) > W_MAX_2)
          output_2 = output_2 / abs(output_2);
        speedController_2.overrideSpeed(output_2);
      }
      else {
        stopping_2 = true;
      }

      prev_Running_2 = running_2;

      break;
  }
}

float RPMTS(float w, int i) {
  if (i == 1)
    return round(w * SPR_1 / 60);
  else if (i == 2)
    return round(w * SPR_2 / 60);
  else
    return round(w * SPR_1 / 60);
}

void readLimitSwitches() {
  yawStop = digitalRead(YAW_LIM_PIN) == HIGH;
  pitchStop = digitalRead(PITCH_LIM_PIN) == HIGH;
}

void parseSerialInputs() {
  char * strtokIndx; // this is used by strtok() as an index
  strtokIndx = strtok(tempChars, ",");
  yaw_deg = atof(strtokIndx);
  strtokIndx = strtok(NULL, ",");
  pitch_deg = atof(strtokIndx);
}

void recvWithStartEndMarkers() {
  static boolean recvInProgress = false;
  static byte ndx = 0;
  char startMarker = '<';
  char endMarker = '>';
  char rc;

  while (Serial.available() > 0 && newData == false) {
    rc = Serial.read();

    if (recvInProgress == true) {
      if (rc != endMarker) {
        receivedChars[ndx] = rc;
        ndx++;
        if (ndx >= numChars) {
          ndx = numChars - 1;
        }
      }
      else {
        receivedChars[ndx] = '\0'; // terminate the string
        recvInProgress = false;
        ndx = 0;
        newData = true;
      }
    }
    else if (rc == startMarker) {
      recvInProgress = true;
    }
  }
}
