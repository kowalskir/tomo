#from serial.tools.list_ports import comports as serial_comports
from Com import Com
from Tomo import Tomo
from Gui import ScanWin

try :
    com = Com("/dev/ttyUSB0")
except Exception as e:
    print(e)
    com = None
finally :
    win = ScanWin()
    Tomo(win, com)
    win.mainloop()
