#include "Main.h"

void init_photonics()
{
    //définition de sortie led
    pinMode(infrared, OUTPUT);
}

void led_on()
{
    digitalWrite(infrared, HIGH);
}

void led_off()
{
    digitalWrite(infrared, LOW);
}

void scan(int* scan_params)
{
    PC_COMMAND command = NONE;
    bool cancelled = false;
    int nb_steps = scan_params[0];
    int nb_angles = scan_params[1];
    int angle_max = scan_params[2];
    int value = 0;
    
    int small_nb_steps = small_step_rev/nb_angles;
    int big_nb_steps = big_nb_steps_max / nb_steps;
    if(angle_max == 180)
    {
        small_nb_steps /= 2;
    }

    led_on();
    enable_motors();
    
    //send_message("start");
    for(int i = 0; i < nb_angles; i++)
    {
        digitalWrite(dirPin, HIGH); //Raccourci : permet de démarrer en s'éloingnant du moteur
        send_message("angle");
        for(int j = 0; j < nb_steps; j++)
        {
            command = check_command();
            if(command == CANCEL)
            {
                cancelled = true;
                digitalWrite(dirPin, LOW);
                translation_steps(j*big_nb_steps, big_high_speed);
                i = nb_angles;
                j = nb_steps;
                send_message("cancelled");
            }
            else
            {
                for(int k = 0; k < 10; k++)
                {
                    value += analogRead(phototrans);
                }
                value /= 10;
                send_value(value);
                value = 0;
                
                translation_steps(big_nb_steps, big_low_speed);
            }
        }
        if(!cancelled)
        {
            digitalWrite(dirPin, LOW); //Raccourci : suite
            //translation_change_dir();
            translation_steps(big_nb_steps_max, big_high_speed);
            rotation_steps(small_nb_steps);
        }
    }
    send_message("end");
    disable_motors();
    led_off();
}

/*void pause(bool* cancelled)
{
    send_message("paused");
    bool paused = true;
    PC_COMMAND command = NONE;
    while(paused)
    {
        command = check_command();
        if(command == RESUME)
        {
            paused = false;
        }
        else if(command == CANCEL)
        {
            paused = false;
            *cancelled = true;
        }
    }
    send_message("resumed");
}*/

void calibration()
{
    send_message("led_off");
    led_off();
    delay(200);
    for(int i = 0; i < 100; i++)
    {
        send_value(analogRead(phototrans));
    }
    send_message("led_on");
    led_on();
    delay(200);
    for(int i = 0; i < 100; i++)
    {
        send_value(analogRead(phototrans));
    }
    send_message("end");
}

void monitor()
{
    PC_COMMAND command = NONE;
    bool monitoring = true;
    led_on();
    while(monitoring)
    {
        send_value(analogRead(phototrans));
        command = check_command();
        if(command == STOP)
        {
            monitoring = false;
        }
        else
        {
            delay(100);
        }
    }
    led_off();
}
