#!/usr/bin/env python

import cv2
import numpy as np
import subprocess as sp
import time


import time
import picamera
import numpy as np
import io





class SplitFrames(object):
    def __init__(self, width, height):
        self.stream = io.BytesIO()
        self.count = 0
        self.width = width
        self.height = height
    def write(self, buf):
        self.stream.write(buf)
        print "buf", len(buf)

        #output = np.empty((self.width * self.height * 3,), dtype=np.uint8)
        output = np.fromstring(buf, dtype=np.uint8)
        output = output.reshape((self.height, self.width, 3))
        print output[0,:,0]
        
        cv2.imshow('curr', output)
        cv2.waitKey(1)

        

def streamPi():
    width = 320
    height = 240
    try:
        output = SplitFrames(width, height)
        with picamera.PiCamera(resolution=(width,height), framerate=24) as camera:
            time.sleep(2)
            start = time.time()
            #camera.iso = 100
            #time.sleep(2)

            #camera.shutter_speed = camera.exposure_speed
            #camera.exposure_mode = 'off'
            g = camera.awb_gains
            print "gain", g
            print "analog gain", camera.analog_gain
            print "awb", camera.awb_mode

            #camera.awb_mode = 'off'
            #camera.awb_gains = g
            

            camera.start_recording(output, format='rgb')
            camera.wait_recording(30)
            camera.stop_recording()
    finally:
        finish = time.time()
    print('Sent %d images in %d seconds at %.2ffps' % (
        output.count, finish-start, output.count / (finish-start)))

                                                                                                                                                                                                                
def streamPiStill():
    print "making cameraa"
    with picamera.PiCamera() as camera:
        while True:
            camera.resolution = (100, 100)
            camera.framerate = 24
            output = np.empty((112 * 128 * 3,), dtype=np.uint8)
            camera.capture(output, 'rgb')
            output = output.reshape((112, 128, 3))
            output = output[:100, :100, :]
            cv2.imshow('curr', output)
            cv2.waitKey(1)



def stream():
    WIDTH = 320
    HEIGHT = 256

    raspividcmd = ['raspivid', '-fps', '20', '-t', '0', '-w', str(WIDTH), '-h',
                   str(HEIGHT), '-r', '-', '--raw-format', 'gray', '-o', '/dev/null', '-n',
                   '-drc', 'off', '-ex', 'fixedfps', '-fl', '-awb', 'auto', '-ifx', 'none', '-md', '7', '-mm', 'average',]
    print "cmd: ", " ".join(raspividcmd)

    stream = None


    try:
        stream = sp.Popen(raspividcmd, stdout = sp.PIPE, universal_newlines = True)
        while stream.returncode == None:
            
            #test = stream.stdout.read(WIDTH * HEIGHT + (WIDTH * HEIGHT / 2))[0:WIDTH * HEIGHT]
            #test = stream.stdout.read(WIDTH * HEIGHT * 3)
            test = stream.stdout.read(WIDTH * HEIGHT)
            
            print "test: %d '%s'" % (len(test), test[0])
            curr = np.fromstring(test, dtype=np.uint8).reshape(HEIGHT, WIDTH)
            print "curr: ", curr[0]
            cv2.imshow('curr', curr[0:WIDTH*HEIGHT])
            cv2.waitKey(1)
            stream.poll()
            
    finally:
        if stream != None:
            stream.terminate()
            stream.kill()



def main():
    #stream()
    streamPi()
    #streamPiStill()


if __name__ == "__main__":
        main()