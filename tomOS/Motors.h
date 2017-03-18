#ifndef MOTORS_INCLUDED
#define MOTORS_INCLUDED

#include "Arduino.h"
#include "Consts.h"

void init_motors();
void disable_motors();
void enable_motors();
void translation_change_dir();
void translation_steps(int n, int speed);
void rotation_steps(int n);
void small_anticlockwise();
void small_clockwise();
void small_setOutput(int out);

#endif
