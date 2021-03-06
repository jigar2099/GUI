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

LARGE_FONT= ("Verdana", 12)
style.use("ggplot")



f = Figure(figsize=(5,5), dpi=100)
a = f.add_subplot(111)
def animate(i):
    data = pd.read_csv('data.csv')
    x = np.array(data['x_value'])
    y1 = np.array(data['total_1'])#[:arr_len]
    y2 = np.array(data['total_2'])#[:arr_len]
    a.clear()
    a.plot(x, y1,label='channel-1')
    a.plot(x, y2,label='channel-2')
    a.set_xlabel('time')
    a.set_ylabel('count')
    a.legend(bbox_to_anchor=(0, 1.02, 1, .102), loc=3,
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
        label = tk.Label(self, text="""This GUI is created for live plotting only.""", font=LARGE_FONT)
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
app = LivePlot()
ani = animation.FuncAnimation(f, animate, interval=1000)
app.mainloop()
        