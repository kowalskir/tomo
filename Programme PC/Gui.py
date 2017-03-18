import tkinter as tk
from tkinter import ttk, messagebox, filedialog

from matplotlib import use as matplotlib_use
matplotlib_use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure
from matplotlib import ticker

import numpy as np

class ConnectWin(tk.Tk) :
    def __init__(self) :
        tk.Tk.__init__(self, port_list, callback)
        self.title("Connection")
        
        self.active = tk.StringVar()
        self.active.set(port_list[0].device)
        for port in port :
            text=port.name + " : " + port.description
            ttk.Radiobutton(self, text=text, variable=self.active, value=port.device).pack(side=tk.TOP)
        self.button = ttk.Button(self, text="Connect", command=callback)
        self.button.pack(side=tk.TOP)
        
    @staticmethod
    def no_port(self) :
        messagebox.showerror(message="No serial port found")
    
    def get_active(self) :
        return self.active

class CalibrationWin(tk.Toplevel) :
    def __init__(self) :
        tk.Toplevel.__init__(self)
        
        self.grab_set()
        self.title("Calibration")
        
        ttk.Label(self,text="Calibration in progress..").pack()
    
    def end(self, max_value, min_value) :
        message = "maximum value = " + str(max_value) + " ; minimum value = " + str(min_value)
        messagebox.showinfo(message=message)
        self.destroy()
        
class MonitorWin(tk.Toplevel) :
    def __init__(self) :
        tk.Toplevel.__init__(self)
        
        self.grab_set()
        self.title("Monitor")
        
        frame = tk.Frame(self)
        frame.pack()
        
        self.values = []
        self.x_values = []
        
        self.figure = Figure(figsize=(6,6), frameon=False)
        self.canvas = FigureCanvasTkAgg(self.figure, master=frame)
        toolbar = NavigationToolbar2TkAgg(self.canvas, frame)
        toolbar.update()
        self.canvas.get_tk_widget().pack(fill=tk.BOTH)
        self.graph = self.figure.gca().plot(self.values, "+")
        self.figure.gca().set_xlim(0,300)
        self.figure.gca().set_ylim(0,1023)
        
        but_frame = tk.Frame(frame)
        but_frame.pack(side=tk.TOP, fill=tk.X)
        self.but_start=ttk.Button(but_frame, text="Start")
        self.but_start.pack(side=tk.LEFT)
        self.but_stop=ttk.Button(but_frame, text="Stop")
        self.but_stop.pack(side=tk.LEFT)
        ttk.Button(but_frame, text="Quit", command=self.destroy).pack(side=tk.RIGHT)

    def add_value(self, value) :
        if len(self.values) >= 300 :
            del self.values[0]
        else :
            self.x_values.append(len(self.x_values))
            
        self.values.append(value)
    
    def update_graph(self) :
        self.graph[0].set_data(self.x_values, self.values)
        self.canvas.draw()
    
class RecWin(tk.Toplevel) :
    def __init__(self) :
        tk.Toplevel.__init__(self)
        
        self.grab_set()
        self.title("Reconstruction")

        self.label = ttk.Label(self,text="Reconstruction in progress..")
        self.label.pack()
        
        frame = tk.Frame(self)
        frame.pack()
        
        self.figure_image = Figure(figsize=(6,6), frameon=False)
        self.canvas_image = FigureCanvasTkAgg(self.figure_image, master=frame)
        self.canvas_image.get_tk_widget().pack(fill=tk.BOTH)
        toolbar = NavigationToolbar2TkAgg(self.canvas_image, frame)
        toolbar.update()
        
        but_frame = tk.Frame(frame)
        but_frame.pack(side=tk.TOP, fill=tk.X)
        self.but_save = ttk.Button(but_frame, text="Save as PNG")
        self.but_save.pack(side=tk.LEFT)
        ttk.Button(but_frame, text="Quit", command=self.destroy).pack(side=tk.RIGHT)
    
    def show_image(self, data) :
        self.label.destroy()
        self.figure_image.gca().imshow(data, cmap="gray_r", interpolation="nearest", extent=(0,data.shape[1],0,data.shape[0]), aspect="auto", origin="lower")
        self.canvas_image.draw()
        self.figure_image.gca().xaxis.set_major_formatter(ticker.FuncFormatter(lambda x, pos:"{}".format(x*80/data.shape[1])))
        self.figure_image.gca().xaxis.set_major_locator(ticker.LinearLocator(9))
        self.figure_image.gca().yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, pos:"{}".format(x*80/data.shape[0])))
        self.figure_image.gca().yaxis.set_major_locator(ticker.LinearLocator(9))
        #self.figure_image.gca().set_title("Reconstruction")

class ScanWin(tk.Tk) :
    
    def __init__(self) :
        tk.Tk.__init__(self)
        #self.root = root
        self.title("Tomography")
        
        self.draw_widgets()
    
    def draw_widgets(self) :
        
        #Sinogram zone
        frame = ttk.Labelframe(self, text="Sinogram")
        frame.pack(side=tk.LEFT,fill=tk.BOTH)
        self.figure_sino = Figure(figsize=(6,6), frameon=False)
        self.canvas_sino = FigureCanvasTkAgg(self.figure_sino, master=frame)
        toolbar = NavigationToolbar2TkAgg(self.canvas_sino, frame)
        toolbar.update()
        self.canvas_sino.get_tk_widget().pack(fill=tk.BOTH)

        
        right_frame = tk.Frame(self)
        right_frame.pack(side=tk.LEFT,fill=tk.BOTH, expand=1)
        
       
        #Scan options
        frame_scan = ttk.Labelframe(right_frame, text="Scan")
        frame_scan.pack(side=tk.TOP, fill=tk.X)

        ttk.Label(frame_scan, text="Number of angles").grid(row=0,column=0)
        ttk.Label(frame_scan, text="Number of steps").grid(row=1,column=0)
        self.nb_angles_value = tk.StringVar()
        self.nb_angles_value.set("64")
        ttk.Combobox(frame_scan, textvariable=self.nb_angles_value, values=["4","8","16","32","64","128","256"], state="readonly").grid(row=0,column=1)
        self.nb_steps_value = tk.StringVar()
        self.nb_steps_value.set("400")
        ttk.Combobox(frame_scan, textvariable=self.nb_steps_value, values=["100","200","400","800"], state="readonly").grid(row=1,column=1)
        self.revolution_value = tk.StringVar()
        self.revolution_value.set("360")
        ttk.Radiobutton(frame_scan, text="Complete revolution", variable=self.revolution_value, value="360").grid(row=2,column=0,columnspan=2)
        ttk.Radiobutton(frame_scan, text="Half revolution", variable=self.revolution_value, value="180").grid(row=3,column=0,columnspan=2)
        
        but_frame = tk.Frame(frame_scan)
        but_frame.grid(row=4,column=0,columnspan=2)
        self.but_start_scan = ttk.Button(but_frame, text="Start")
        self.but_start_scan.pack(side=tk.LEFT)
        self.but_cancel_scan = ttk.Button(but_frame, text="Cancel")
        self.but_cancel_scan.pack(side=tk.LEFT)
        
        #Reconstruction options
        frame_rec= ttk.Labelframe(right_frame, text="Reconstruction")
        frame_rec.pack(side=tk.TOP, fill=tk.X)
        
        self.rec_algo_value = tk.StringVar()
        self.rec_algo_value.set("sart")
        ttk.Radiobutton(frame_rec, text="Algebraic method", variable=self.rec_algo_value, value="sart").grid(row=0,column=0,columnspan=2)
        ttk.Radiobutton(frame_rec, text="Filtered backprojection", variable=self.rec_algo_value, value="fbp").grid(row=1,column=0,columnspan=2)
        ttk.Label(frame_rec, text="FBP filter").grid(row=2,column=0)
        self.fbp_filter_value = tk.StringVar()
        self.fbp_filter_value.set("ramp")
        ttk.Combobox(frame_rec, textvariable=self.fbp_filter_value, values=["None","ramp","shepp-logan","cosine","hamming","hann"], state="readonly").grid(row=2,column=1)
        
        but_frame = tk.Frame(frame_rec)
        but_frame.grid(row=3,column=0,columnspan=2)
        self.but_centering = ttk.Button(but_frame, text="Centering")
        self.but_centering.pack(side=tk.LEFT)
        self.but_start_rec = ttk.Button(but_frame, text="Reconstruct", command=lambda:RecWin())
        self.but_start_rec.pack(side=tk.LEFT)
        
        #Buttons
        but_frame = tk.Frame(right_frame)
        but_frame.pack(side=tk.TOP,fill=tk.X)
        
        self.but_save = ttk.Button(but_frame, text="Save sinogram as PNG", command=lambda:self.im_sino.imsave(filedialog.asksaveasfilename(defaultextension=".png", filetypes=[["Image",".png"]]),cmap="gray_r"))
        self.but_save.grid(row=0,column=0)
        self.but_reset = ttk.Button(but_frame, text="Reset")
        self.but_reset.grid(row=0,column=1)
        self.but_calibration = ttk.Button(but_frame, text="Calibration")
        self.but_calibration.grid(row=1,column=0)
        self.but_monitor = ttk.Button(but_frame, text="Monitor", command=lambda:MonitorWin())
        self.but_monitor.grid(row=1,column=1)
        self.but_quit = ttk.Button(but_frame, text="Quit", command=self.destroy)
        self.but_quit.grid(row=2,column=0)
    
    def init_sino(self, sino, vmin, vmax, angle_max) :
        self.im_sino = self.figure_sino.gca().imshow(sino, cmap="gray_r", vmin=vmin,vmax=vmax, interpolation="nearest", extent=(0,sino.shape[1],0,sino.shape[0]), aspect="auto", origin="lower")
        self.figure_sino.gca().xaxis.set_major_formatter(ticker.FuncFormatter(lambda x, pos:"{}".format(x*angle_max/sino.shape[1])))
        self.figure_sino.gca().xaxis.set_major_locator(ticker.LinearLocator(5))
        self.figure_sino.gca().yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, pos:"{}".format(x*80/sino.shape[0])))
        self.figure_sino.gca().yaxis.set_major_locator(ticker.LinearLocator(9))
        self.figure_sino.gca().set_xlabel("Angle (deg)")
        self.figure_sino.gca().set_ylabel("Distance (mm)")
        #self.figure_sino.gca().set_title("Sinogram")
        #self.figure_sino.gca().set_ylim(0,sino.shape[0)
        self.canvas_sino.draw()
        
    def update_sino(self, data) :
        self.im_sino.set_data(data)
        self.canvas_sino.draw()
    
    def reset(self) :
        self.figure_sino.clf()
        self.canvas_sino.draw()
        self.but_cancel_scan.configure(state="disabled")
        self.but_start_rec.configure(state="disabled")
        self.but_centering.configure(state="disabled")
        self.but_save.configure(state="disabled")

    def cancel_scan(self) :
        self.but_start_scan.configure(state="normal")
        self.but_cancel_scan.configure(state="disabled")
        self.but_reset.configure(state="normal")
    
    def start_scan(self) :
        self.but_start_scan.configure(state="disabled")
        self.but_cancel_scan.configure(state="normal")
        self.but_reset.configure(state="disabled")
    
    def end_scan(self) :
        self.but_start_scan.configure(state="enabled")
        self.but_cancel_scan.configure(state="disabled")
        self.but_start_rec.configure(state="normal")
        self.but_centering.configure(state="normal")
        self.but_save.configure(state="normal")
        self.but_reset.configure(state="normal")
    
    
    @staticmethod
    def save_path() :
        return filedialog.asksaveasfilename(defaultextension=".png", filetypes=[["Image",".png"]])
    
    def not_calibrated(self) :
        messagebox.showwarning(message="You must calibrate before doing a scan")

