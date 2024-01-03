#####
# Rain, a graphical display of audio input
#
#
# THE BEER-WARE LICENSE" (Revision 42, Poul-Henning Kamp):
#   <eel.josh@gmail.com> wrote this file.  
#   As long as you retain this notice 
#   you can do whatever you want with this stuff. 
#   If we meet some day, and you think this stuff is worth it, 
#   you can buy me a beer in return. - Joshua B. Mehlman
#
# Theeel December 2023
#####
version = 1.0

## TODO ### set up git

## TODO ## Entery arguments for which display to show.

## TODO ## # audio output for Ugo

# Python Libs
import time
import sys

#Third Party
import numpy
import matplotlib.pyplot as plt
from   matplotlib.animation import FuncAnimation

## Internal libs
import audioIn
import jFFT

## Settings
# fMin_Hz ## TODO ##
# fMax_Hz ## TODO ##
# freqRes (deltaF) ## TODO ##

# nAve ## TODO ##
fftWindow="Hanning"
# Animation Speed (Hz) ## TODO ##

## Comes out of settings
# dT_ms = 
# dF_Hz
sRate_Hz = 44100
nSampels = 2048 #Should be a power of 2
# nFreques = nSamples/2 + 1 (the +1 is for 0Hz)
# animation update time (ms)

## Init
print("Starting Rain v{}".format(version))
print("Block Size = {}".format(nSampels))
print("")

print("start audio from main")
audioClass = audioIn.audioIn_cl(blockSize=nSampels, sRate=sRate_Hz, fakeACCouple=True)
#print("Sample rate = {}Hz, Sample Len = {}ms\n".format(sRate_Hz, audioClass.blockLen_ms))
audioClass.startAudio()

yDataTime = audioClass.getAudioBlock(debug=False) # Get the audio
xDataTime = audioClass.getTimeAxis()
#xDataTime = numpy.arange(0, nSampels)*audioClass.deltaT_ms
#    print("yDataTime = {}".format(yDataTime)) # for debuging
#    time.sleep(100/1000) # for debuging

print("Initilize fft")
fftClass =  jFFT.jFFT_cl()
yDataTime_window = fftClass.appWindow(yDataTime, window=fftWindow)
freqData_mf = fftClass.calcFFT(yDataTime_window)

yDataFreq = list(freqData_mf[0]) ##TODO## Plot the numpy matrix, not two lists
freqDataPoints = len(yDataFreq)

xDataFreq = fftClass.getFreqs(sRate=sRate_Hz, tBlockLen=audioClass.blockSize)
print("")

#print("data mag{}{}  ".format(type(yDataFreq), freqDataPoints))
#print("data freqs {}{}  ".format(type(xDataFreq), freqDataPoints))
#print("len ydatatime = {}".format(len(yDataTime)))
#print("data mag/phase {}{} = {} ".format(type(yDataFreq), yDataFreq.shape, yDataFreq))

#while True: # for debuging
#audioClass.stopAudio()
#sys.exit() ## Exit here for debug

# Bring up plots 
## TODO ##  Put in a class, but note, is our timing
plt.rcParams['toolbar'] = 'None'

fig, (timeAx, freqAx) = plt.subplots(nrows=2,ncols=1)
fig.suptitle('Audio Data from Mic')

## Time D 
timeDataLine, = timeAx.plot(xDataTime, yDataTime)
#timeAx.set_title("Time Plot")
timeAx.set_xlabel("Time (ms)")
timeAx.set_ylabel("Ampidude (fo)")
timeAx.set_xlim(0,audioClass.blockLen_ms)
timeAx.set_ylim(-10000,10000)

## Freq D
freqDataLine, = freqAx.plot(xDataFreq, yDataFreq)
freqAx.set_xlabel("Frequency (Hz)")
freqAx.set_ylabel("Ampidude (foo)")
freqAx.set_xlim(0,fftClass.fMax)
freqAx.set_ylim(0,300000)

#subplots_adjust(left=None, bottom=None, right=None, top=None, wspace=None, hspace=None)

def update(frame):
    global xDataTime, yDataTime
    # Get the audio
    yDataTime = audioClass.getAudioBlock(debug=False)
    timeDataLine.set_data(xDataTime, yDataTime)

    yDataTime_window = fftClass.appWindow(yDataTime, window=fftWindow)
    freqData_mf = fftClass.calcFFT(yDataTime_window)
    yDataFreq = list(freqData_mf[0])
    freqDataLine.set_data(xDataFreq, yDataFreq)

    ##TODO ## Only do this if the layout or window size has changed
    fig.tight_layout() #tightent up the layout with this setup

    #fig.gca().relim()
    #fig.gxa().autoscale_view()
    return timeDataLine,
# interval is delay in ms between frames
animation = FuncAnimation(fig=fig, func=update, interval=100, cache_frame_data=False)

## TODO ### Display it in a cool way
# total RMS --> how many circles and background color?
# each circle
#   freqency --> color
#   amplidued --> speed

try:
    plt.show()
except:
    print("No plot, assume exit")

audioClass.stopAudio()
print("Exit rain")
