#include "Com.h"

char buffer[BUFFER_LEN_MAX + 1];
char idx = 0;
STATE state = WAIT;
Stream* pStream = NULL;
int scan_params[3];

void prot_clear()
{
    state = WAIT;
    idx = 0;
}

void prot_setup(Stream* arg)
{
  pStream = arg;
  prot_clear();
}

//Fonction appelée dans le loop de l'arduino, check si il y a des données
//sur le port série et les met dans le buffer
void prot_loop()
{
    char c;
    bool process = true;
    
    if(pStream->available())
    {
      while(pStream->available() && process)
      {
          c = pStream->read();
          if(state == WAIT)
          {
              if(c == '<')
              {
                //Caractère de début de message, passage en mode receiving
                state = RECEIVING;
              }
          }
          else if(state == RECEIVING)
          {
              if(c == '<')
              {
                  //caractère de début en mileu de message : ne doit pas se produire
                  //normalement donc on annule la réception du message
                  prot_clear();
              }
              else if(c == '>')
              {
                  //caractère de fin, on ajoute le symbole de fin de chaine au buffer
                  //on passe en mode received et on arrête la boucle
                  buffer[idx] = '\0';
                  state = RECEIVED;
                  process = false;
              }
              else if(idx >= BUFFER_LEN_MAX)
              {
                  //Longeur du message plus grande que la taille maximum du buffer
                  //On annule la réception du message
                  prot_clear();
              }
              else
              {
                  //Cas normal, on ajoute le caractère au buffer
                  buffer[idx] = c;
                  idx += 1;
              }
          }
      }
    }
}

void send_message(char* message)
{
    pStream->print("<");
    pStream->print(message);
    pStream->print(">");
}

bool str_equal(const char* a, const char* b)
{
    int l = strlen(a);
    if(l == strlen(b))
    {
        if(strncmp(a, b, l) == 0)
            return true;
        else
            return false;
    }
    else
        return false;
}

PC_COMMAND message_to_command(const char* str)
{
    PC_COMMAND command = NONE;
    if(str_equal(str, "scan"))
        command = SCAN;
    else if(str_equal(str, "calibration"))
        command = CALIBRATION;
    else if(str_equal(str, "stop"))
        command = STOP;
    else if(str_equal(str, "resume"))
        command = RESUME;
    else if(str_equal(str, "pause"))
        command = PAUSE;
    else if(str_equal(str, "monitor"))
        command = MONITOR;
    else if(str_equal(str, "cancel"))
        command = CANCEL;
    else
        command = NONE;
    return command;
}

PC_COMMAND wait_command()
{
    bool wait = true;
    PC_COMMAND command = NONE;
    while(command == NONE)
    {
        prot_loop();
        if(state == RECEIVED)
        {
            command = message_to_command(buffer);
            prot_clear();
        }
    }
    return command;
}

PC_COMMAND check_command()
{
    PC_COMMAND command = NONE;
    char* token = NULL;
    int i = 0;
    prot_loop();
    if(state == RECEIVED)
    {
        if(strchr(buffer, ',') != NULL)
        {
            token = strtok(buffer, ",");
            command = message_to_command(token);
            while(token != NULL && i < 3)
            {
                token = strtok(NULL, ",");
                scan_params[i++] = atoi(token);
            }
        }
        else
        {
            command = message_to_command(buffer);
        }
        prot_clear();
    }
    return command;
}

int* get_scan_params()
{
    return scan_params;
}

void send_value(int value)
{
  //value supposé entre 0 et 1023
  pStream->print("<value:");
  pStream->print(value);
  pStream->print(">");
}

