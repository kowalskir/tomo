#ifndef CONSTS_INCLUDED
#define CONSTS_INCLUDED

//Small stepper
const int small_pin1 = 8;    // Blue   - 28BYJ48 pin 1
const int small_pin2 = 9;    // Pink   - 28BYJ48 pin 2
const int small_pin3 = 10;    // Yellow - 28BYJ48 pin 3
const int small_pin4 = 11;    // Orange - 28BYJ48 pin 4
const int small_speed = 1200;  //variable to set stepper speed
const int small_step_rev = 512; // number of steps per full revolution
const int small_lookup[8] = {B01000, B01100, B00100, B00110, B00010, B00011, B00001, B01001};


//Pin definition
const int small_disable = 2;//éteint le contrôlleur du petit moteur
//déclaration des sorties de l'Arduino, dirPin définissant la direction de rotation et stepPin la commande de rotation pour le grand moteur
//Big Stepper
const int stepPin = 3;
const int dirPin = 4;
const int big_high_speed = 100; //Delai entre HIGH-LOW-HIGH
const int big_low_speed = 150;
const int big_nb_steps_max = 8000;
const int disable = 7;//éteint le controlleur du grand moteur


//déclaration des variables relative au système led-senseur
const int infrared = 12; 
const int phototrans = 0;


#endif
