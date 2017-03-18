import numpy as np
import skimage.transform as tr
import skimage.transform as tr
from skimage.io import imsave

import time
import math
from threading import Thread

from Gui import ScanWin, CalibrationWin, MonitorWin, RecWin, ConnectWin
from Com import Com

class Tomo :
    def __init__(self, win, com) :
        
        self.win = win
        self.com = com
        self.reset()
        
        self.win.but_start_scan.configure(command=self.scan)
        self.win.but_start_rec.configure(command=self.reconstruction)
        self.win.but_calibration.configure(command=self.calibration)
        self.win.but_reset.configure(command=self.reset)
        self.win.but_centering.configure(command=self.centering)
        self.win.but_save.configure(command=lambda:self.save(self.sino))
        self.win.but_cancel_scan.configure(command=self.cancel_scan)
        self.win.but_monitor.configure(command=self.monitor)
    
    def reset(self) :
        self.calibrated = False
        self.cancelled = False
        self.sino = []
        self.value_min = -1
        self.value_max = -1
        self.log_value_max = -1
        self.nb_angles = 0
        self.nb_steps = 0
        self.angle_max = 0
        self.win.reset()
        
    def scan(self) :
        if not self.calibrated :
            self.win.not_calibrated()
            return False
        
        self.nb_angles = int(self.win.nb_angles_value.get())
        self.nb_steps = int(self.win.nb_steps_value.get())
        self.angle_max = int(self.win.revolution_value.get())
        
        self.sino = np.zeros((self.nb_steps, self.nb_angles))
        self.win.reset()
        self.win.init_sino(self.sino, 0.,self.log_value_max, self.angle_max)
        self.win.start_scan()
        
        Thread(target=self.process_scan).start()

        
    def process_scan(self) :
        i = 0
        j = 0
        elapsed = time.time()
        t = elapsed
        processing = True
        self.com.send("scan,"+str(self.nb_steps)+","+str(self.nb_angles)+","+str(self.angle_max))
        
        while processing and not self.cancelled :
            message, value = self.com.check_message()
            if message == Com.SIGNAL :
                if value == "end" :
                    processing = False
                elif value == "angle" :
                    i += 1
                    j = 0
            elif message == Com.VALUE :
                self.sino[j,i - 1] = self.value_adjustment(value)
                j += 1
                if time.time() - t >= 0.1 :
                    self.win.update_sino(self.sino)
                    t = time.time()
            else :
                pass
                
        self.win.update_sino(self.sino)
        elapsed = time.time()-elapsed
        
        if self.cancelled :
            self.cancelled = False
            self.win.cancel_scan()
            print("Scan cancelled")
        else :
            self.win.end_scan()
            print("Scan ended")
        print("Time elapsed (s) : " + str(elapsed))
    
    def cancel_scan(self) :
        self.com.send("cancel")
        self.cancelled = True

    def value_adjustment(self, value) :
        value = (1023./(self.value_max - self.value_min)) * (value - self.value_min)
        if value <= 0. :
            value = self.log_value_max
        elif value >= self.value_max :
            value = 0.
        else :
            value = self.log_value_max - math.log(value)
        return value

    def reconstruction(self) :
        
        rec_win = RecWin()
        Thread(target=lambda:self.process_reconstruction(rec_win)).start()
    
    def process_reconstruction(self, rec_win) :
        
        algo = self.win.rec_algo_value.get()
        fbp_filter = self.win.fbp_filter_value.get()
        theta = np.linspace(0, self.angle_max, self.nb_angles, endpoint=False)
        if algo == "sart" :
            image = tr.iradon_sart(self.sino, theta)
        elif algo == "fbp" :
            if fbp_filter == "None" :
                fbp_filter = None
            image = tr.iradon(self.sino, theta, circle = True, filter=fbp_filter)

        rec_win.show_image(image)
        rec_win.but_save.configure(command=lambda:self.save(image))
        
    def calibration(self) :
        calib_win = CalibrationWin()
        Thread(target=lambda:self.process_calibration(calib_win)).start()
    
    def process_calibration(self, calib_win) :
        nb_vmin = 0
        nb_vmax = 0
        vmin = 0
        vmax = 0
        state = ""
        processing = True
        self.com.send("calibration")
        while processing :
            message, value = self.com.check_message()
            if message == Com.SIGNAL :
                if value == "end" :
                    processing = False
                elif value == "led_on" :
                    state = "vmax"
                elif value == "led_off" :
                    state = "vmin"
            elif message == Com.VALUE :
                if state == "vmin" :
                    vmin += value
                    nb_vmin += 1
                elif state == "vmax" :
                    vmax += value
                    nb_vmax += 1
        self.value_min = vmin / nb_vmin
        self.value_max = vmax / nb_vmax
        self.log_value_max = math.log(self.value_max)
        self.calibrated = True
        calib_win.end(self.value_max, self.value_min)
    
    def monitor(self) :
        
        mon_win = MonitorWin()
        mon_win.but_start.configure(command=lambda:Thread(target=lambda:self.start_monitor(mon_win)).start())
        mon_win.but_stop.configure(command=self.stop_monitor)
    
    def start_monitor(self, mon_win) :
        self.monitoring = True
        self.com.send("monitor")
        t = time.time()
        while self.monitoring :
            message, value = self.com.check_message()
            if message == Com.VALUE :
                mon_win.add_value(value)
            if time.time() - t >= 0.1 :
                mon_win.update_graph()
                t = time.time()

    def stop_monitor(self) :
        self.monitoring = False
        self.com.send("stop")
        
    def centering(self) :
        h = self.sino.shape[0]
        l = self.sino.shape[1]
        new_sino = np.zeros((h, l))
        nonzero = self.sino.nonzero()
        inf = min(nonzero[0])
        sup = max(nonzero[0])
        size = sup - inf
        i = math.floor((h-(sup-inf))/2)
        new_sino[i:i+size,0:l] = self.sino[inf:sup,0:l]
        self.sino = new_sino
        self.win.update_sino(self.sino)
    
    def save(self, data) :
        try:
            imsave(ScanWin.save_path(), np.uint16(data), plugin="freeimage") #DOES NOT WORK !!!!!
        except Exception as e:
            print(e)
