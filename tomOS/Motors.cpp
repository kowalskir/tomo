#include "Motors.h"

//Stepper small_stepper;
//Stepper small_stepper(ROTATION_STEPS_REVOLUTION, 8, 10, 9, 11);

void small_anticlockwise()
{
    for(int i = 0; i < 8; i++)
    {
        small_setOutput(i);
        delayMicroseconds(small_speed);
    }
}

void small_clockwise()
{
    for(int i = 7; i >= 0; i--)
    {
        small_setOutput(i);
        delayMicroseconds(small_speed);
    }
}

void small_setOutput(int out)
{
    digitalWrite(small_pin1, bitRead(small_lookup[out], 0));
    digitalWrite(small_pin2, bitRead(small_lookup[out], 1));
    digitalWrite(small_pin3, bitRead(small_lookup[out], 2));
    digitalWrite(small_pin4, bitRead(small_lookup[out], 3));
}

void init_motors()
{
    //Init rotation motor
    //small_stepper = Stepper(ROTATION_STEPS_REVOLUTION, 8, 10, 9, 11);
    pinMode(small_pin1, OUTPUT);
    pinMode(small_pin2, OUTPUT);
    pinMode(small_pin3, OUTPUT);
    pinMode(small_pin4, OUTPUT);
    pinMode(small_disable, OUTPUT);
    
    //Init translation motor
    pinMode(stepPin,OUTPUT);
    pinMode(dirPin,OUTPUT);
    pinMode(disable, OUTPUT);
    //digitalWrite(dirPin, HIGH);
    //pinMode(disable, OUTPUT);
}

void disable_motors()
{
    //HIGH OR LOW ???
    digitalWrite(disable, LOW);
    digitalWrite(small_disable, LOW);
}

void enable_motors()
{
    digitalWrite(disable, HIGH);
    digitalWrite(small_disable, HIGH);
    //digitalWrite(dirPin, HIGH);
}

void translation_change_dir()
{
    if(digitalRead(dirPin) == HIGH)
        digitalWrite(dirPin, LOW);
    else
        digitalWrite(dirPin, HIGH);
}

void translation_steps(int n, int speed)
{
    for(int i = 0; i < n; i++)
    {
        digitalWrite(stepPin, HIGH);
        delayMicroseconds(speed);
        digitalWrite(stepPin, LOW);
        delayMicroseconds(speed);
    }
}

void rotation_steps(int n)
{
    for(int i = 0; i < n; i++)
    {
        small_anticlockwise();
    }
}
