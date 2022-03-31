# tutorial p8
from IPython.core.display import display, HTML
display(HTML("<style>.container { width:100% !important; }</style>"))
import tkinter as tk
import pandas as pd
import numpy as np
import matplotlib
from matplotlib import style
style.use('ggplot')
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
import matplotlib.animation as animation

import tkinter as tk
from tkinter import ttk
from tkinter import *
from tkinter import filedialog
from clsNum import closestNumber as clsnum


LARGE_FONT= ("Verdana", 12)
style.use("ggplot")


f = Figure(figsize=(5,5), dpi=100)
a = f.add_subplot(1,1,1)
def animate(i):
    data = pd.read_csv('data.csv')
    steps = len(data)
    samp_size = 30
    c_num = clsnum(steps,samp_size)
    
    def plotting(samp_size,arr_len):
        x = np.array(data['x_value'])[:arr_len]
        #print(x.shape[0])
        x_mean = x.reshape(int(x.shape[0]/samp_size),samp_size)
        x_m = np.mean(x_mean,axis=1)

        y1 = np.array(data['total_1'])[:arr_len]
        y1_mean = y1.reshape(int(y1.shape[0]/samp_size),samp_size)
        y1_m = np.mean(y1_mean,axis=1)
        y1_s = np.std(y1_mean,axis=1)

        y2 = np.array(data['total_2'])[:arr_len]
        y2_mean = y2.reshape(int(y2.shape[0]/samp_size),samp_size)
        y2_m = np.mean(y2_mean,axis=1)
        y2_s = np.std(y2_mean,axis=1)
        a.clear()
        a.plot(x_m,y1_m,label='channel-1',color='green')
        a.errorbar(x_m,y1_m,yerr=y1_s,color='green',capsize=3,elinewidth=1)
        a.plot(x_m,y2_m,label='channel-2',color='blue') 
        a.errorbar(x_m,y2_m,yerr=y2_s,color='blue',capsize=3,elinewidth=1)
        threshold = 1000
        # Add below threshold markers
        below_threshold = y1_m < threshold
        a.scatter(x_m[below_threshold], y1_m[below_threshold], color='red',s=45)
        
        # Add above threshold markers
        above_threshold = np.logical_not(below_threshold)
        a.scatter(x_m[above_threshold], y1_m[above_threshold],color='green')
        
        # Add below threshold markers
        below_threshold = y2_m < threshold
        a.scatter(x_m[below_threshold], y2_m[below_threshold], color='red',s=45)
        # Add above threshold markers
        above_threshold = np.logical_not(below_threshold)
        a.scatter(x_m[above_threshold], y2_m[above_threshold],color='blue')        
        
        
        a.fill_between(x_m, 0, 1000, facecolor='yellow', alpha=0.5,
                label='Threshold')
        if min(y1)<min(y2) and max(y2)<max(y1):
            a.set_ylim(min(y1),max(y1))
        elif min(y1)<min(y2) and max(y1)<max(y2):
            a.set_ylim(min(y1),max(y2))
        elif min(y2)<min(y1) and max(y2)<max(y1):
            a.set_ylim(min(y2),max(y1))
        elif min(y2)<min(y1) and max(y1)<max(y2):
            a.set_ylim(min(y2),max(y2))
            
        a.set_xlabel('time')
        a.set_ylabel('count')
        a.legend(bbox_to_anchor=(0, 1.02, 1, .102), loc=3,
                 ncol=2, borderaxespad=0)
        #a.tight_layout()
    #print(steps,c_num)
    if steps%samp_size==0:
        if c_num>steps:
            #print("Go back ! ",c_num-samp_size)
            arr_len = c_num-samp_size
            plotting(samp_size,arr_len)
        elif c_num==0:
            pass
        else:
            #print("Already perfect ! ",c_num)
            arr_len = c_num
            plotting(samp_size,arr_len)
    else:
        pass



f1 = Figure(figsize=(5,5), dpi=100)
# https://stackoverflow.com/questions/54508045/how-the-add-subplotnrows-ncols-index-works
a1 = f1.add_subplot(1,2,1)#(row, col, index)
a2 = f1.add_subplot(1,2,2)
def animate1(i):
    data = pd.read_csv('data.csv')
    x = np.array(data['x_value'])
    
    y1 = np.array(data['total_1'])#[:arr_len]
    y2 = np.array(data['total_2'])#[:arr_len]
    
    a1.clear()
    a1.plot(x, y1, label='channel-1',color='green')
    a1.plot(x, y2 , label='channel-2',color='blue')
    a1.set_xlabel('time')
    a1.set_ylabel('count')
    a1.legend(bbox_to_anchor=(0, 1.02, 1, .102), loc=3,
             ncol=2, borderaxespad=0)
    
    a2.clear()
    #a2.bar(x, y1, label='channel-1',color='green')
    #a2.bar(x, y2 , label='channel-2',color='blue')
    data = {'ch-1':np.sum(y1), 'ch-2':np.sum(y2)}
    chnls = list(data.keys())
    vals = list(data.keys())
    a2.bar(['ch-1'], np.sum(y1), yerr=np.std(y1), align='center', alpha=0.5, ecolor='black', capsize=10)
    a2.bar(['ch-2'], np.sum(y2), yerr=np.std(y2), align='center', alpha=0.5, ecolor='black', capsize=10)
    a2.set_xlabel('time')
    a2.set_ylabel('count')
    a2.legend(bbox_to_anchor=(0, 1.02, 1, .102), loc=3,
             ncol=2, borderaxespad=0)

class LivePlot(tk.Tk):

    def __init__(self, *args, **kwargs): 
        tk.Tk.__init__(self, *args, **kwargs)
        tk.Tk.wm_title(self, "Plotting")
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand = True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        self.frames = {}
        for F in (StartPage, Plot_page):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        self.show_frame(StartPage)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

        
class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)
        label = tk.Label(self, text="""This Std plotting.""", font=LARGE_FONT)
        label.pack(pady=10,padx=10)
        button1 = ttk.Button(self, text="Visualize",
                            command=lambda: controller.show_frame(Plot_page))
        button1.pack()
        
        button2 = ttk.Button(self, text="Quit",
                            command=quit)
        button2.pack()

class PageOne(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Page One!!!", font=LARGE_FONT)
        label.pack(pady=10,padx=10)
        button1 = ttk.Button(self, text="Back to Home",
                            command=lambda: controller.show_frame(StartPage))
        button1.pack()

class Plot_page(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Graph Page!", font=LARGE_FONT)
        label.pack(pady=10,padx=10)
        button1 = ttk.Button(self, text="Back to Home",
                            command=lambda: controller.show_frame(StartPage))
        button1.pack()
        canvas = FigureCanvasTkAgg(f, self)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)
        toolbar = NavigationToolbar2Tk(canvas, self)
        toolbar.update()
        canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        
        canvas1 = FigureCanvasTkAgg(f1, self)
        canvas1.draw()
        canvas1.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)
        toolbar = NavigationToolbar2Tk(canvas1, self)
        canvas1._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
app = LivePlot()
ani = animation.FuncAnimation(f, animate, interval=1000)
ani1 = animation.FuncAnimation(f1, animate1, interval=1000)
app.mainloop()
