#ifndef COM_INCLUDED
#define COM_INCLUDED

#define BUFFER_LEN_MAX 50

#include "Arduino.h"
//#include <cstring>

enum PC_COMMAND
{
    NONE,
    SCAN,
    CALIBRATION,
    MONITOR,
    PAUSE,
    RESUME,
    CANCEL,
    STOP
};

enum STATE
{
    WAIT,
    RECEIVING,
    RECEIVED
};

void prot_clear();
void prot_setup(Stream* arg);
void prot_loop();
void send_message(char* message);
void send_value(int value);
bool str_equal(const char* a, const char* b);
PC_COMMAND message_to_command(const char* str);
PC_COMMAND wait_command();
PC_COMMAND check_command();
int* get_scan_params();

#endif
