import serial

class Com :
    
    WAIT = 1
    RECEIVING = 2
    RECEIVED = 3

    NONE = 0
    SIGNAL = 1
    VALUE = 3
    
    def __init__(self, port) :
        self.ser = serial.Serial(port, baudrate = 19200)
        if not self.ser :
            print("Erreur lors de l'ouverture du port série")
            exit()
        
        if self.ser.in_waiting > 0 :
            self.ser.reset_input_buffer()
        
        self.clear()
    
    def clear(self) :
        self.state = Com.WAIT
        self.message = ""
    
    def loop(self) :
        
        if self.ser.in_waiting > 0 :
            while self.ser.in_waiting > 0 and not self.state == Com.RECEIVED :
                c = self.ser.read().decode("utf-8")
                if self.state == Com.WAIT :
                    if c == '<' :
                        self.state = Com.RECEIVING
                elif self.state == Com.RECEIVING :
                    if c == '<' :
                        self.clear()
                    elif c == '>' :
                        self.state = Com.RECEIVED
                    else :
                        self.message += c
            #print(self.message)
    
    def check_message(self) :
        
        m_type = False
        m_value = False
        
        self.loop()
        
        if self.state == Com.RECEIVED :
            l = self.message.split(':')
            if len(l) <= 1 :
                m_type = Com.SIGNAL
                m_value = self.message
            else :
                if l[0] == "value" :
                    m_type = Com.VALUE
                    m_value = int(l[1])
                else :
                    m_type = l[0]
                    m_value = l[1]
            self.clear()
        
        return m_type, m_value
    
    def send(self, message) :
        string = "<" + message + ">"
        self.ser.write(string.encode("utf-8"))
