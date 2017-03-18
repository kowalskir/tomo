#ifndef MAIN_INCLUDED
#define MAIN_INCLUDED

#include "Arduino.h"
#include "Consts.h"
#include "Motors.h"
#include "Com.h"

void init_photonics();
void led_on();
void led_off();
void scan(int* scan_params);
//void pause(bool* stopped);
void calibration();
void monitor();

#endif
