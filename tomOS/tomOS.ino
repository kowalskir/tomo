#include "Main.h"
#include "Com.h"
//#include <cmath>

PC_COMMAND command = NONE;

void setup()
{
    Serial.begin(19200);
    prot_setup(&Serial);
    init_motors();
    init_photonics();
}

void loop()
{
    //send_message("ready");
    command = check_command();
    
    //int angle_steps = round( (float)((ANGLE_STOP-ANGLE_START)*ROTATION_STEPS_REVOLUTION) / (float)(360*NB_ANGLES) );
    
    if(command == SCAN)
    {
        scan(get_scan_params());
    }
    else if(command == CALIBRATION)
    {
        calibration();
    }
    else if(command == MONITOR)
    {
        monitor();
    }
}
