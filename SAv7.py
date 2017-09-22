
from matplotlib.figure import Figure

import numpy as np
import matplotlib.pyplot as plt
import rtlsdr 
from matplotlib.mlab import psd

import tkinter as Tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
import rtlsdr



root = Tk.Tk()
root.wm_title("RF signal tracker")

root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

sdr = rtlsdr.RtlSdr()

# configure device

sdr.sample_rate = 2.048e6
sdr.center_freq = 1300e6-.3e6
sdr.gain = 40.2
cindex=600;
bw=50;
ilow=2400
ihigh=2500
timelength=1001;

#tsdata[:]=np.nan;

 
NFFT = 256*4
NUM_SAMPLES_PER_SCAN = NFFT*64
centerindex=int(NFFT/2)

fc=sdr.fc;
rs=sdr.rs;
findex=np.arange(0,NFFT)
freq=((fc-rs/2)+findex*(rs/NFFT))/1e6
#run twice to loose bad starting data
samples = sdr.read_samples(NUM_SAMPLES_PER_SCAN)
samples = sdr.read_samples(NUM_SAMPLES_PER_SCAN) 
psd_scan, f = psd(samples, NFFT=NFFT)
psd_scan[centerindex-3:centerindex+3]=np.nan
graphdata=10*np.log10(psd_scan)-sdr.gain
graphdatasmoothed=graphdata

plt.minorticks_on();
fig, axarr = plt.subplots(2)
ax=axarr[0];
ax2=axarr[1];
ax.grid(True)
ax.set_title("RF Intensity")
ax.set_xlabel("Frequency (MHz)")
ax.set_ylabel("Signal (dB)")

ax2.minorticks_on();
ax2.grid(b=True,which='major')
ax2.grid(b=True,which='minor')
ax2.set_xlabel("sample #")
ax2.set_ylabel("Peak Signal (dB)")

fig.subplots_adjust(hspace=.5)

vline=ax.axvline(x=freq[cindex],color="#f0a0a0")
lindex=max(0,cindex-bw)
rindex=min(NFFT-1,cindex+bw)
vlinel=ax.axvline(x=freq[lindex],color='#b0b0b0')
vliner=ax.axvline(x=freq[rindex],color='#b0b0b0')


tsdata=[]

line2,=ax.plot(freq,graphdatasmoothed,color="#b0b0b0")
line1,=ax.plot(freq,graphdata)
tsplot=tsdata[0:10]
line3,=ax2.plot(np.zeros(timelength))
point, =ax.plot(freq[cindex],graphdata[cindex],'rx')
ax.ticklabel_format(useOffset=False)
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.show()
canvas.get_tk_widget().grid(row=0,columnspan=6,sticky=Tk.NSEW)

#toolbar = NavigationToolbar2TkAgg( canvas, root )
#toolbar.update()
canvas._tkcanvas.grid(row=0,columnspan=8)




var1 = Tk.StringVar(root,"")
var2 = Tk.StringVar(root,"")
var3 = Tk.StringVar(root,"")
var4 = Tk.StringVar(root,"")
var5 = Tk.StringVar(root,"")
var6 = Tk.StringVar(root,"")

def __init__(self, master):
    master.columnconfigure(0, weight=1)
    master.rowconfigure(0, weight=1)

def click(event):
	global cindex,lindex,rindex
	x=event.x
	y=event.y
	
	inv = ax.transData.inverted()
	datapos = inv.transform((x,y))
	cindex = np.argmin(np.abs(freq - datapos[0]))
	lindex=max(0,cindex-bw)
	rindex=min(NFFT-1,cindex+bw)
	vline.set(xdata=freq[cindex])
	
def left(event):
	global cindex,bw,rindex,lindex
	cindex=cindex-1
	lindex=max(0,cindex-bw)
	rindex=min(NFFT-1,cindex+bw)
	vline.set(xdata=freq[cindex])
	vlinel.set(xdata=freq[lindex])
	vliner.set(xdata=freq[rindex])
	
def right(event):
	global cindex,bw,rindex,lindex
	cindex=cindex+1
	lindex=max(0,cindex-bw)
	rindex=min(NFFT-1,cindex+bw)
	vline.set(xdata=freq[cindex])
	vlinel.set(xdata=freq[lindex])
	vliner.set(xdata=freq[rindex])
	
def uparrow(event):
	global sdr,NFFT,NUM_SAMPLES_PER_SCAN,freq
	sdr.fc=sdr.fc+50e6
	fc=sdr.fc;
	rs=sdr.rs;
	findex=np.arange(0,NFFT)
	freq=((fc-rs/2)+findex*(rs/NFFT))/1e6
	line1.set_xdata(freq)
	line2.set_xdata(freq)
	ax.autoscale()
	
def downarrow(event):
	global sdr,NFFT,NUM_SAMPLES_PER_SCAN,freq
	sdr.fc=sdr.fc-50e6
	
	fc=sdr.fc;
	rs=sdr.rs;
	findex=np.arange(0,NFFT)
	freq=((fc-rs/2)+findex*(rs/NFFT))/1e6
	line1.set_xdata(freq)
	line2.set_xdata(freq)
	
def shiftdownarrow(event):
	global sdr,NFFT,NUM_SAMPLES_PER_SCAN,freq
	sdr.fc=sdr.fc-2e6
	
	fc=sdr.fc;
	rs=sdr.rs;
	findex=np.arange(0,NFFT)
	freq=((fc-rs/2)+findex*(rs/NFFT))/1e6
	line1.set_xdata(freq)
	line2.set_xdata(freq)

def shiftuparrow(event):
	global sdr,NFFT,NUM_SAMPLES_PER_SCAN,freq
	sdr.fc=sdr.fc+3e6
	
	fc=sdr.fc;
	rs=sdr.rs;
	findex=np.arange(0,NFFT)
	freq=((fc-rs/2)+findex*(rs/NFFT))/1e6
	line1.set_xdata(freq)
	line2.set_xdata(freq)	
	
def GetData():
	global tsdata,graphdata,graphdatasmoothed,f,sdr,NUM_SAMPLES_PER_SCAN,NFFT,centerindex,tsplot,lindex,rindex
	samples = sdr.read_samples(NUM_SAMPLES_PER_SCAN)
	psd_scan, f = psd(samples, NFFT=NFFT)
	psd_scan[centerindex-3:centerindex+3]=np.nan
	graphdata=10*np.log10(psd_scan)-sdr.gain
	graphdatasmoothed=graphdatasmoothed*.8+graphdata*.2
	window=10**(graphdata[lindex:rindex]/10)
	
	bw=wBW.get()
	lindex=max(0,cindex-bw)
	rindex=min(NFFT-1,cindex+bw)
	BWpower=10*np.log10(sum(window))
	#y=max(graphdata[lindex:rindex])
	tsdata.append(BWpower);
	#tsdata.append(lindex);
	tsplot=tsdata[-timelength:];
	tsplot = tsplot + [0]*(timelength - len(tsplot))
	root.after(wScale2.get(),GetData)

def RealtimePlottter():
	global graphdata,line1,point,bw,tsdata,line3
	bw=wBW.get()
	freq_template = 'mark freq = %.4f MHz'
	v2_template = 'mark = %.2f dB, '
	v3_template = 'ave = %.2f dB'
	v4_template = 'peak = %.2f dB, '
	v5_template = 'ave = %.2f dB'
	v6_template = 'BW power = %.2f dB'
	ax.set_ylim([wVbottom.get(),wVtop.get()])
	ax2.set_ylim([wVbottom.get(),wVtop.get()])
	
	ax.set_xlim([min(freq),max(freq)])
	ax2.set_xlim([0,timelength-1])
	line1.set_ydata(graphdata)
	line2.set_ydata(graphdatasmoothed)
	
	line3.set_ydata(tsplot);
	lindex=max(0,cindex-bw)
	rindex=min(NFFT-1,cindex+bw)
	vline.set(xdata=freq[cindex]) 
	vlinel.set(xdata=freq[lindex])
	vliner.set(xdata=freq[rindex])

	var1.set(freq_template % (freq[cindex]))
	var2.set(v2_template % (graphdata[cindex]))
	var3.set(v3_template % (graphdatasmoothed[cindex]))
	var4.set(v4_template % (max(graphdata[lindex:rindex])))
	var5.set(v5_template % (max(graphdatasmoothed[lindex:rindex])))
	
	var6.set(v6_template % (tsdata[-1]))
		
	point.set_data(freq[cindex],graphdata[cindex])
	canvas.draw()
	root.after(25,RealtimePlottter)
	
def cleardata():
	global tsdata
	tsdata=[]

def _quit():
    root.quit()     # stops mainloop
    np.savetxt('SAdata.txt', tsdata)
    root.destroy()  # this is necessary on Windows to prevent
                    # Fatal Python Error: PyEval_RestoreThread: NULL tstate

canvas._tkcanvas.bind('<Button-1>',click)

button = Tk.Button(master=root, text='Quit', command=_quit)

clearbutton= Tk.Button(master=root, text='Clear data',command=cleardata)

wVtop = Tk.Scale(master=root,label="Signal Max", from_=0, to=-100,orient="vertical")
wVtop.set(-10)
wVbottom = Tk.Scale(master=root,label="Signal Min", from_=0, to=-100,orient="vertical")
wVbottom.set(-80)

wScale2 = Tk.Scale(master=root,label="Delay:", from_=1, to=200,sliderlength=30,orient=Tk.HORIZONTAL)
wScale2.set(10)
wBW = Tk.Scale(master=root,label="Bandwidth:", from_=1, to=128,sliderlength=20,length=200,orient=Tk.HORIZONTAL)
wBW.set(10)

root.bind('<Left>',left)
root.bind('<Right>',right)
root.bind('<Up>',uparrow)
root.bind('<Down>',downarrow)
root.bind('<Shift-Up>',shiftuparrow)
root.bind('<Shift-Down>',shiftdownarrow)

wValue1= Tk.Label(master=root,textvariable=var1,font=("Helvetica", 24))
wValue2= Tk.Label(master=root,textvariable=var2,font=("Helvetica", 36))
wValue3= Tk.Label(master=root,textvariable=var3,font=("Helvetica", 36))
wValue4= Tk.Label(master=root,textvariable=var4,font=("Helvetica", 36))
wValue5= Tk.Label(master=root,textvariable=var5,font=("Helvetica", 36))

wValue6= Tk.Label(master=root,textvariable=var6,font=("Helvetica", 36))


#figure is in 0,0
wScale2.grid(row=1,column=0)

wBW.grid(row=1,column=1,columnspan=2)
wVtop.grid(row=2,column=1)
wVbottom.grid(row=2,column=2)
wValue1.grid(row=1,column=3)
wValue2.grid(row=2,column=3)
wValue3.grid(row=2,column=4)
wValue4.grid(row=3,column=3)
wValue5.grid(row=3,column=4)
wValue6.grid(row=4,column=3)
button.grid(row=5,column=3) #quit button
clearbutton.grid(row=3,column=1)

root.protocol("WM_DELETE_WINDOW", _quit) 
root.after(100,GetData)
root.after(100,RealtimePlottter)
Tk.mainloop()

