//Test to read 4 analog values on Teensy 3.6
// The 4 analog values are read, post-processed, then sent to computer
//2 photodiodes, 2 PSDs
//Limited to 3.3 V into Teensy ADC input
//Scanenr 1: Al mirror, Scanner 2: Gold mirror
//Ran at 5 Hz
//This version will start the scan and read whenever PSD is in certain range
//Both mirrors are ran with same signal
//Uses Teensy ADC library

#include <ADC.h>
#include <ADC_util.h>
#include <math.h>


const int READPIN1 = A14; //Pin 33 ADC0
const int READPIN2 = A15; //Pin 34 ADC0
const int READPIN3 = A16; //Pin 35 ADC1
const int READPIN4 = A17; //Pin 36 ADC1

const float DEG2RAD = PI / 180.0f;
const float RAD2DEG = 180.0f / PI;

//locating constants (in mm, not m or cm due since want to prevent the use of float)
const word X_1 = 925;
const word Y_1 = 0;
const word X_2 = 0;
const word Y_2 = 0;
const byte BETA1 = 108.76;
const byte BETA2 = 66.85;
const byte THRESHOLD = 3; // number of data points collected in one collectnLocate (depends on the n value) to count as retroreflector detection
const word PHTHRESH1 = 500;
const word PH1TRIG = 500;
const word PHTHRESH2 = 150;
word reading[4];

unsigned long time0, time1, time2, timedelta1, timedelta2;
long a1, a2; //this is the global variable average angle value manipulated and used by multiple functions and main loop

int test = 0;

ADC *adc = new ADC(); // adc object;

void setup() {

  pinMode(READPIN1, INPUT);
  pinMode(READPIN2, INPUT);
  pinMode(READPIN3, INPUT);
  pinMode(READPIN4, INPUT);


  //teensy defaults to serial usb if connected via usb?
  SerialUSB.begin(115200);
  //Serial.begin(2000000);
  

  // ADC0
  adc->adc0->setAveraging(20); // set number of average
  adc->adc0->setResolution(16); // set bits of resolution, 13 bit resolution max for teensy 3.6? This auto sets it to 12 bits.. no 13 bit default?!
  adc->adc0->setConversionSpeed(ADC_CONVERSION_SPEED::VERY_HIGH_SPEED); // change the conversion speed
  adc->adc0->setSamplingSpeed(ADC_SAMPLING_SPEED::VERY_HIGH_SPEED); // change the sampling speed
  

  // ADC1
  adc->adc1->setAveraging(20); // set number of averages
  adc->adc1->setResolution(16); // set bits of resolution
  adc->adc1->setConversionSpeed(ADC_CONVERSION_SPEED::VERY_HIGH_SPEED); // change the conversion speed
  adc->adc1->setSamplingSpeed(ADC_SAMPLING_SPEED::VERY_HIGH_SPEED); // change the sampling speed

  //Serial.println("Setup done");
  delay(100);
  
}

void loop() {
 
  //time0 = micros();


  // this number can be even smaller to make faster, but there is a point (when n is less than number points per half cycle)
  // probably better when at least one cycle, so can average the angle to compensate for the phase shift of driving signal
  collectnLocate(1644); //1645 ~1 scan (1 cycle at 5 Hz)

  // float ang1 = PSDToAngle1(a1)*RAD2DEG;
 // float ang2 = PSDToAngle2(a2)*RAD2DEG;

      
  Serial.print(a1);
  // Serial.print(ang1);
  Serial.print(" ");
  Serial.println(a2);
 // Serial.println(ang2);
  // time2 = micros();

  // timedelta1 = time1-time0;
  //timedelta2 = time2-time1;

  //Serial.print ("timedelta1: ");
  // Serial.println (timedelta1);
  // Serial.print ("timedelta2: ");
  // Serial.println (timedelta2);


  /*
    gather();
    Serial.print (reading[0]);
    Serial.print (" ");
    Serial.print (reading[1]);
    Serial.print (" ");
    Serial.print (reading[2]);
    Serial.print (" ");
    Serial.println (reading[3]);
  */

  /*
    if (a1 != -1 && a2 != -1){

      // angles in degrees converted to radians
     // float ang1 = (drivingToAngle1(a1) + BETA1)*DEG2RAD;
      //float ang2 = (drivingToAngle2(a2) + BETA2)*DEG2RAD;
      float ang1 = PSDToAngle1(a1) + BETA1*DEG2RAD;
      float ang2 = PSDToAngle2(a2) + BETA2*DEG2RAD;
      // in mm
      float locationx = (Y_2-Y_1+X_1*tan(ang1)-X_2*tan(ang2))/(tan(ang1)-tan(ang2));
      float locationy = (locationx-X_1)*tan(ang1)+Y_1;

      Serial.print(locationx);
      Serial.print(" ");
      Serial.println(locationy);
    }

    else{
      Serial.println ("-1 -1");
    }
  
*/

  //time1 = micros();

  //timedelta = time1-time0;
  //Serial.println (timedelta);
  // delayMicroseconds(300);

}


// gathers data from ADC and update the global variables
void gather(void) {
  
  reading[0] = adc->adc0->analogRead(READPIN1); 
  reading[1] = adc->adc0->analogRead(READPIN2); 
  reading[2] = adc->adc1->analogRead(READPIN3); 
  reading[3] = adc->adc1->analogRead(READPIN4); 

}

// collectnLocate function will run loop n times, changes the values of globals a1, a2 that are used for locating
void collectnLocate(word n) {
    
  int angle1average[n / 2] = {};
  int angle2average[n / 2] = {};
  long average1 = 0;
  long average2 = 0;
  word n1 = 0;
  word n2 = 0;
  bool trig = true;

  do {
    reading[1] = adc->adc0->analogRead(READPIN2);
    
    //if (reading[2] >= PH1TRIG){
    if (reading[1] < 22250 && reading[1] > 22000) {
      for (word i = 0; i < n; i++) {
        // int time0 = micros();
        gather();

        // here less than thresh because use retroreflective background
        if (reading[0] < PHTHRESH1) {
          angle1average[n1] = reading[1];
          // Serial.print(i);
          // Serial.print(" ");
          // Serial.println(angle1average[n1]);
          n1++;
        }

        if (reading[2] > PHTHRESH2) {
          angle2average[n2] = reading[3];
          n2++;
        }
        // int time1 = micros();
        // int timedelta = time1 - time0;
        // Serial.print ("Time: ");
        // Serial.println(timedelta);
      }
      /*
        Serial.println("Test: ");

        for (word i = 0; i<n1; i++){
        Serial.println(angle1average[i]);
        }*/

      trig = false;
    }
  } while (trig);

  /*
    for (word i = 0; i<n1; i++){
      average1 = average1 + angle1average[i];
    }
    for (word i = 0; i<n2; i++){
      average2 = average2 + angle2average[i];
    }
  */
  if (n1 >= THRESHOLD && n2 >= THRESHOLD) {
    for (word i = 0; i < n1; i++) {
      average1 = average1 + angle1average[i];
    }
    for (word i = 0; i < n2; i++) {
      average2 = average2 + angle2average[i];
    }
    //average1 = average1/n1;
    // average2 = average2/n2;
    a1 = average1 / n1;
    a2 = average2 / n2;
    
  }
  else if (n1 >= THRESHOLD && n2 < THRESHOLD) {
    for (word i = 0; i < n1; i++) {
      average1 = average1 + angle1average[i];
    }
    //average1 = average1/n1;
    a1 = average1 / n1;
    a2 = -1;
  }
  else if (n1 < THRESHOLD && n2 >= THRESHOLD) {
    for (word i = 0; i < n2; i++) {
      average2 = average2 + angle2average[i];
    }
    //average2 = average2/n2;
    a1 = -1;
    a2 = average2 / n2;
  }
  else {
    a1 = -1;
    a2 = -1;
  }
}
/*
  // Converts ADC angle 1 value to angle, returns angle in degrees
  float drivingToAngle1(word data){
  float ADCavg1 = 4381.5; //channged from 4105
  float ADCrange1 = 5373.0; //changed from 5031
  float Anglerange1 = 38.95; // angle at 4.7 Vpp 5 Hz (width = 79.5, length = 112.4, angle = 38.95, changed from 34.767
  // float k = 2.35; // Vpp(driving signal)/Vpp(mock reading signal), this is only used when angle range is defaulted to the driving signal
  // float Angle1 = k * (data - ADCavg1) * (Anglerange1 / ADCrange1);
  float Angle1 = (data - ADCavg1) * (Anglerange1 / ADCrange1);

  return Angle1;
  }

  // Converts ADC angle 2 value to angle
  float drivingToAngle2(word data){
  float ADCavg2 = 4358.0; //changed from 4011
  float ADCrange2 = 5150.0; //changed from 5150
  float Anglerange2 = 40.53; // angle at 8.4 Vpp 5 Hz (width = 83, length = 112.4, angle = 40.53, changed from 43.50
  //  float k = 4.2;
  // float Angle2 = k * (data - ADCavg2) * (Anglerange2 / ADCrange2);
  float Angle2 = (data - ADCavg2) * (Anglerange2 / ADCrange2);

  return Angle2;
  }
*/

// Returns angle of PSD1 in RADIANS
float PSDToAngle1(word data) {
  float ADCavg1 = 22875.0;  // found by putting in the centre of scan
  float ADCrange1 = 5486.0; //found by placing retroreflector on ends and measuring. corresponds to the Xrange value
  float Xrange1 = 725; // in mm ***usually Xrange/ADCrange is constant, so shouldnt need to change those..
  float d1 = 1104.0; //distance from mirror to calibration surface in mm, this value directly correlates to Xrange1
  float Angle1 = atan(Xrange1 * (data - ADCavg1) / d1 / ADCrange1);

  return Angle1;
}

// Returns angle of PSD2 in RADIANS
float PSDToAngle2(word data) {
  float ADCavg2 = 22820.5;
  float ADCrange2 = 3545.0;
  float Xrange2 = 525.0; // in mm
  float d2 = 1104.0; //distance from mirror to calibration surface in mm
  float Angle2 = atan(Xrange2 * (data - ADCavg2) / d2 / ADCrange2);

  return Angle2;
}


/*
  // Converts PSD 1 value to angle, returns angle in degrees
  float PSDToAngle1(word data){
  float ADCavg1 = 4660.5;
  float ADCrange1 = 1219.0;
  float Anglerange1 = 34.767;
  float Angle1 = (data - ADCavg1) * (Anglerange1 / ADCrange1);

  return Angle1;
  }

  // Converts PSD 2 value to angle
  float PSDToAngle2(word data){
  float ADCavg2 = 4538.0;
  float ADCrange2 = 1070.0;
  float Anglerange2 = 43.50;
  float Angle2 = (data - ADCavg2) * (Anglerange2 / ADCrange2);

  return Angle2;
  }
*/
