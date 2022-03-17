#from IPython.core.display import display, HTML
#display(HTML("<style>.container { width:100% !important; }</style>")) 
import random
from itertools import count
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np
from pathlib import Path
from clsNum import closestNumber as clsnum

#plt.style.use('fivethirtyeight')
plt.style.use('ggplot')

x_vals = []
y_vals = []
index = count()



def animate(i):
    data = pd.read_csv('data.csv')
    steps = len(data)
    samp_size = 5
    c_num = clsnum(steps,samp_size)
    
    def plotting(samp_size,arr_len):
        x = np.array(data['x_value'])[:arr_len]
        print(x.shape[0])
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
        plt.cla()
        
        #plt.plot(x_m,y1_m,label='Av 1')
        #if min(y1_m)<1000:
        #    plt.errorbar(x_m,y1_m,yerr=y1_s,label='SA-1',capsize=3,fmt='o',color='red')
        #    plt.errorbar(x_m,y2_m,yerr=y2_s,label='SA-2',capsize=3,fmt='o')
        #if min(y2_m)<1000:
        #    plt.errorbar(x_m,y1_m,yerr=y1_s,label='SA-1',capsize=3,fmt='o')
        #    plt.errorbar(x_m,y2_m,yerr=y2_s,label='SA-2',capsize=3,fmt='o',color='red')
        #if min(y2_m)<1000 and min(y1_m)<1000:
        #    plt.errorbar(x_m,y1_m,yerr=y1_s,label='SA-1',capsize=3,fmt='o',color='red')
        #    plt.errorbar(x_m,y2_m,yerr=y2_s,label='SA-2',capsize=3,fmt='o',color='red')
        #else:
        #    plt.errorbar(x_m,y1_m,yerr=y1_s,label='SA-1',capsize=3,fmt='o')
        #    plt.errorbar(x_m,y2_m,yerr=y2_s,label='SA-2',capsize=3,fmt='o')
        #plt.errorbar(x_m,y1_m,yerr=y1_s,label='SA-1',capsize=3,fmt='o')
        #plt.errorbar(x_m,y2_m,yerr=y2_s,label='SA-2',capsize=3,fmt='o')
        plt.plot(x_m,y1_m,label='1')
        plt.plot(x_m,y2_m,label='2')
        
        threshold = 1000
        # Add below threshold markers
        below_threshold = y1_m < threshold
        plt.scatter(x_m[below_threshold], y1_m[below_threshold], color='red')
        
        # Add above threshold markers
        above_threshold = np.logical_not(below_threshold)
        plt.scatter(x_m[above_threshold], y1_m[above_threshold])
        
        # Add below threshold markers
        below_threshold = y2_m < threshold
        plt.scatter(x_m[below_threshold], y2_m[below_threshold], color='red')
        # Add above threshold markers
        above_threshold = np.logical_not(below_threshold)
        plt.scatter(x_m[above_threshold], y2_m[above_threshold])        
        plt.legend(loc='upper left')
        plt.tight_layout()

    
    
    print(steps,c_num)
    if steps%samp_size==0:
        if c_num>steps:
            print("Go back ! ",c_num-samp_size)
            arr_len = c_num-samp_size
            plotting(samp_size,arr_len)
        elif c_num==0:
            pass
        else:
            print("Already perfect ! ",c_num)
            arr_len = c_num
            plotting(samp_size,arr_len)
    else:
        pass
    
    
    
ani = FuncAnimation(plt.gcf(), animate, interval=1000)
    
plt.tight_layout()
plt.show()

