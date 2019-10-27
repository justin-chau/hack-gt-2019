#include <Wire.h>
#include <Adafruit_BNO055.h>
#include <utility/imumaths.h>

Adafruit_BNO055 bno = Adafruit_BNO055(55);

float x = 0;
float prev_x = x;
float temp_x = x;
float base_x = 3600;
float diff_x;

void setup(void)
{
  Serial.begin(9600);

  /* Initialise the sensor */
  if (!bno.begin())
  {
    while (1);
  }

  delay(4000);

  bno.setExtCrystalUse(true);
}

void loop(void)
{
  sensors_event_t event;
  bno.getEvent(&event);

  temp_x = event.orientation.x;

  diff_x = temp_x - prev_x;

  if (abs(diff_x) > 180) {
    if (diff_x / abs(diff_x) == -1) {
      base_x = base_x + 360;
    }
    else {
      base_x = base_x - 360;
    }
  }
  x = base_x + temp_x;

  /* Display the floating point data */

  Serial.print('<');
  Serial.print(round(x));
  Serial.print(",");
  Serial.print(round(event.orientation.z));
  Serial.println('>');

  delay(20);
  prev_x = temp_x;

}
