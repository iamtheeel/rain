#####
# Audio Input to an array on request using pyaudio
#
# Non-Blocking, if you cant keep up with the audio, you will skip that block
# getAudioBlock will wait if the next block is not ready
#
## TODO ## Calibration
#
# THE BEER-WARE LICENSE" (Revision 42, Poul-Henning Kamp)
#   <iamtheeel> wrote this file.
#   As long as you retain this notice
#   you can do whatever you want with this stuff.
#   If we meet some day, and you think this stuff is worth it,
#   you can buy me a beer in return. - Joshua B. Mehlman
#
# Theeel December 2023
#####
version = 1.0

# Third Party
import pyaudio
import numpy

# Python Libs
import time

class audioIn_cl:
    def __init__(self,blockSize=1024, sRate=44100,fakeACCouple = False):
        print("audioIn.__init__: version = {} blockSize = {}".
                                 format(version, blockSize))
        self.fakeACCouple = fakeACCouple

        ## Set Values
        self.blockSize = blockSize
        self.CHANNELS = 1
        self.sRate_Hz = sRate
        self.FORMAT = pyaudio.paInt16

        ## Calculated values
        self.deltaT_ms = 1000/self.sRate_Hz
        self.blockLen_ms = self.blockSize*self.deltaT_ms

        print("Sample rate = {}Hz, Sample Len = {}ms\n".format(
                      self.sRate_Hz, self.blockLen_ms))

        ## the input stream
        self.dataBlock = None
        self.pyAu = pyaudio.PyAudio()
        self.stream = self.pyAu.open(format=self.FORMAT, 
                                     channels=self.CHANNELS, 
                                     rate=self.sRate_Hz, 
                                     input=True,
                                     frames_per_buffer=self.blockSize,
                                     stream_callback=self.getCallback(
                                                            debug = False) )

    #Note: del gets caught up on the audio running
    def __del__(self):
        print("audioIn.__del__")

    def getCallback(self, debug = False):
        ## Return pointer to the audio callback
        def audioCallBack(in_data, frame_count, time_info, status):
            if debug:
                if self.dataBlock is not None:
                    print("not keeping up")
            self.dataBlock = numpy.frombuffer(in_data, dtype=numpy.int16)
            #print("yData = {}".format(self.dataBlock))
            return (in_data, pyaudio.paContinue)

        return audioCallBack

    def startAudio(self):
        print("audioIn.startAuidio:")
        self.stream.start_stream()

    def stopAudio(self):
        print("audioIn.stopAuidio:")
        self.stream.stop_stream()
        self.stream.close()
        self.pyAu.terminate()

    def getTimeAxis(self):
        time = numpy.arange(0, self.blockSize)*self.deltaT_ms
        print(time)
        return time

    def getAudioBlock(self, debug=False):
        while self.dataBlock is None:
            #if debug:
            print("audioIn.getAudioBlaock waiting for data")
            time.sleep(100/1000)

        if debug:
            print("audioIn.getAudioBlock yData = {}".format(self.dataBlock))

        data = numpy.copy(self.dataBlock)
        self.dataBlock = None #wipe so we don't reuse

        if self.fakeACCouple:
            ave = round(numpy.average(data)) ## TODO ## make dependant on type
            data -= ave

        return data
