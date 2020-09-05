
#include <ADC.h>
#include <ADC_util.h>

const int readPin1 = A14; //Pin 33 ADC0
const int readPin2 = A15; //Pin 34 ADC0
const int readPin3 = A16; //Pin 35 ADC1
const int readPin4 = A17; //Pin 36 ADC1

unsigned long time0, time1, timedelta;
ADC *adc = new ADC(); // adc object;
word reading[4];


void setup() {

  pinMode(readPin1, INPUT);
  pinMode(readPin2, INPUT);
  pinMode(readPin3, INPUT);
  pinMode(readPin4, INPUT);

  SerialUSB.begin(115200);
  Serial.println("Begin setup");

  ///// ADC0 ////
  // reference can be ADC_REFERENCE::REF_3V3, ADC_REFERENCE::REF_1V2 (not for Teensy LC) or ADC_REFERENCE::REF_EXT.
  //adc->adc0->setReference(ADC_REFERENCE::REF_1V2); // change all 3.3 to 1.2 if you change the reference to 1V2

  adc->adc0->setAveraging(20); // set number of averages
  //16 bit resolution here is actually 13 bit limited by the hardware. The last 3 bits here are just noise
  adc->adc0->setResolution(16); // set bits of resolution, 13 bit resolution max for teensy 3.6? This auto sets it to 12 bits.. no 13 bit default?!

  // it can be any of the ADC_CONVERSION_SPEED enum: VERY_LOW_SPEED, LOW_SPEED, MED_SPEED, HIGH_SPEED_16BITS, HIGH_SPEED or VERY_HIGH_SPEED
  // see the documentation for more information
  // additionally the conversion speed can also be ADACK_2_4, ADACK_4_0, ADACK_5_2 and ADACK_6_2,
  // where the numbers are the frequency of the ADC clock in MHz and are independent on the bus speed.
  adc->adc0->setConversionSpeed(ADC_CONVERSION_SPEED::VERY_HIGH_SPEED); // change the conversion speed
  // it can be any of the ADC_MED_SPEED enum: VERY_LOW_SPEED, LOW_SPEED, MED_SPEED, HIGH_SPEED or VERY_HIGH_SPEED
  adc->adc0->setSamplingSpeed(ADC_SAMPLING_SPEED::VERY_HIGH_SPEED); // change the sampling speed

  // always call the compare functions after changing the resolution!
  //adc->adc0->enableCompare(1.0/3.3*adc->adc0->getMaxValue(), 0); // measurement will be ready if value < 1.0V
  //adc->adc0->enableCompareRange(1.0*adc->adc0->getMaxValue()/3.3, 2.0*adc->adc0->getMaxValue()/3.3, 0, 1); // ready if value lies out of [1.0,2.0] V

  // If you enable interrupts, notice that the isr will read the result, so that isComplete() will return false (most of the time)
  // adc->adc0->enableInterrupts(adc0_isr);

  ////// ADC1 /////

  adc->adc1->setAveraging(20); // set number of averages
  adc->adc1->setResolution(16); // set bits of resolution
  adc->adc1->setConversionSpeed(ADC_CONVERSION_SPEED::VERY_HIGH_SPEED); // change the conversion speed
  adc->adc1->setSamplingSpeed(ADC_SAMPLING_SPEED::VERY_HIGH_SPEED); // change the sampling speed

  //adc->adc1->setReference(ADC_REFERENCE::REF_1V2);

  // always call the compare functions after changing the resolution!
  //adc->adc1->enableCompare(1.0/3.3*adc->adc1->getMaxValue(), 0); // measurement will be ready if value < 1.0V
  //adc->adc1->enableCompareRange(1.0*adc->adc1->getMaxValue()/3.3, 2.0*adc->adc1->getMaxValue()/3.3, 0, 1); // ready if value lies out of [1.0,2.0] V


  // If you enable interrupts, note that the isr will read the result, so that isComplete() will return false (most of the time)
  // adc->adc1->enableInterrupts(adc1_isr);


  delay(100);
}


void loop() {

  //  time0 = micros();


  reading[0] = adc->adc0->analogRead(readPin1);
  reading[1] = adc->adc0->analogRead(readPin2);
  reading[2] = adc->adc1->analogRead(readPin3);
  reading[3] = adc->adc1->analogRead(readPin4);
  // time1 = micros();

  Serial.print (reading[0]);
  Serial.print (" ");
  Serial.print (reading[1]);
  Serial.print (" ");
  Serial.print (reading[2]);
  Serial.print (" ");
  Serial.println (reading[3]);



  //Serial.println(timedelta = time1-time0);


  /*
      // Print errors, if any.
      if(adc->adc0->fail_flag != ADC_ERROR::CLEAR) {
        Serial.print("ADC0: "); Serial.println(getStringADCError(adc->adc0->fail_flag));
      }
      #ifdef ADC_DUAL_ADCS
      if(adc->adc1->fail_flag != ADC_ERROR::CLEAR) {
        Serial.print("ADC1: "); Serial.println(getStringADCError(adc->adc1->fail_flag));
      }
      #endif
  */
  // delay(1000);
}

/*
  // If you enable interrupts make sure to call readSingle() to clear the interrupt.
  void adc0_isr() {
        adc->adc0->analogReadContinuous();
  }

  void adc1_isr() {
        adc->adc1->analogReadContinuous();
  }
*/
