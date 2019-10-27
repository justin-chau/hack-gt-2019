#include <Wire.h>
#include <Adafruit_BNO055.h>
#include <utility/imumaths.h>
  
Adafruit_BNO055 bno = Adafruit_BNO055(55);
 
void setup(void) 
{
  Serial.begin(9600);
  
  /* Initialise the sensor */
  if(!bno.begin())
  {
    while(1);
  }
  
  delay(4000);

  bno.setExtCrystalUse(true);
}
 
void loop(void) 
{
  sensors_event_t event; 
  bno.getEvent(&event);
  
  /* Display the floating point data */
  Serial.print('<');
  Serial.print(event.orientation.x, 4);
  Serial.print(",");
  Serial.print(event.orientation.z, 4);
  Serial.println('>');

  delay(20);
}
