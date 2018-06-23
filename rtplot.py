import serial
import numpy as np
from matplotlib import pyplot as plt
from time import time

# If you're not using Linux, you'll need to change this
# check the Arduino IDE to see what serial port it's attached to
ser = serial.Serial('/dev/ttyUSB0', 115200)

# set plot to animated
plt.ion() 

start_time = time()
timepoints = []
ydataX = []
ydataY = []
ydataZ = []
ydataGX = []
ydataGY = []
ydataGZ = []
ydataT = []
yrange = [-20000,20000]
view_time = 60 # seconds of data to view at once
duration = 24 # total seconds to collect data

fig1 = plt.figure()
# http://matplotlib.org/users/text_props.html
fig1.suptitle('Received Data', fontsize='18', fontweight='bold')
plt.xlabel('time, seconds', fontsize='14', fontstyle='italic')
plt.ylabel('acceleration', fontsize='14', fontstyle='italic')
plt.axes().grid(True)
lineX, = plt.plot(ydataX,marker='.',markersize=4,linestyle='--',markerfacecolor='red')
lineY, = plt.plot(ydataY,marker='.',markersize=4,linestyle='--',markerfacecolor='blue')
lineZ, = plt.plot(ydataZ,marker='.',markersize=4,linestyle='--',markerfacecolor='green')
lineGX, = plt.plot(ydataGX,marker='.',markersize=4,linestyle='--',markerfacecolor='red')
lineGY, = plt.plot(ydataGY,marker='.',markersize=4,linestyle='--',markerfacecolor='blue')
lineGZ, = plt.plot(ydataGZ,marker='.',markersize=4,linestyle='--',markerfacecolor='green')
lineT, = plt.plot(ydataT,marker='.',markersize=4,linestyle='--',markerfacecolor='green')

plt.ylim(yrange)
plt.xlim([0,view_time])

# flush any junk left in the serial buffer
ser.flushInput()
# ser.reset_input_buffer() # for pyserial 3.0+
run = True

# collect the data and plot a moving frame
while run:
    ser.reset_input_buffer()
    data = ser.readline().split(' ')
    print data
    
    # sometimes the incoming data is garbage, so just 'try' to do this
    try:
        # store the entire dataset for later
        ydataX.append(float(data[0]))
        ydataY.append(float(data[1]))
        ydataZ.append(float(data[2]))
        ydataGX.append(float(data[3]))
        ydataGY.append(float(data[4]))
        ydataGZ.append(float(data[5]))
        ydataT.append(float(data[6].rstrip()))
        # print float(data[6].rstrip())


        timepoints.append(time()-start_time)
        current_time = timepoints[-1]
        
        # update the plotted data
        lineX.set_xdata(timepoints)
        lineX.set_ydata(ydataX)

        lineY.set_xdata(timepoints)
        lineY.set_ydata(ydataY)

        lineZ.set_xdata(timepoints)
        lineZ.set_ydata(ydataZ)

        lineGX.set_xdata(timepoints)
        lineGX.set_ydata(ydataGX)

        lineGY.set_xdata(timepoints)
        lineGY.set_ydata(ydataGY)
        
        lineGZ.set_xdata(timepoints)
        lineGZ.set_ydata(ydataGZ)

        lineT.set_xdata(timepoints)
        lineT.set_ydata(ydataT)

        # slide the viewing frame along
        if current_time > view_time:
            plt.xlim([current_time-view_time,current_time])
            
        # when time's up, kill the collect+plot loop
        # if timepoints[-1] > duration: run=False
    
    # if the try statement throws an error, just do nothing
    except: pass
    
    # update the plot
    fig1.canvas.draw()

# plot all of the data you collected
fig2 = plt.figure()
# http://matplotlib.org/users/text_props.html
fig2.suptitle('complete data trace', fontsize='18', fontweight='bold')
plt.xlabel('time, seconds', fontsize='14', fontstyle='italic')
plt.ylabel('potential, volts', fontsize='14', fontstyle='italic')
plt.axes().grid(True)

plt.plot(timepoints, ydataX,marker='o',markersize=4,linestyle='--',markerfacecolor='red')
plt.plot(timepoints, ydataY,marker='o',markersize=4,linestyle='--',markerfacecolor='red')
plt.plot(timepoints, ydataZ,marker='o',markersize=4,linestyle='--',markerfacecolor='red')
plt.plot(timepoints, ydataGX,marker='o',markersize=4,linestyle='--',markerfacecolor='red')
plt.plot(timepoints, ydataGY,marker='o',markersize=4,linestyle='--',markerfacecolor='red')
plt.plot(timepoints, ydataGZ,marker='o',markersize=4,linestyle='--',markerfacecolor='red')
plt.plot(timepoints, ydataT,marker='o',markersize=4,linestyle='--',markerfacecolor='red')

plt.ylim(yrange)
fig2.show()

ser.close()