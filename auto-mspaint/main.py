import numpy as np
import ctypes
import time
import json
import cv2
import os

from PIL import ImageGrab
from pynput.mouse import Button, Controller as MController
from pynput.keyboard import Key, Controller as KController


mouse = MController()
keybrd = KController()
MessageBox = ctypes.windll.user32.MessageBoxW


with open('settings.json', 'r') as f:
    conf = json.load(f)


with open(conf['INPUT_FILES'], 'r') as f:
    image_list = f.read().split('\n')

print(image_list)

class Prog:
    exitnow       : bool  = False
    program_start : float
    program_end   : float


completed = [1]

paintbrush_position = conf['PAINT_POSITION']
draw_rect =           conf['DRAW_REGION']
ss_directory =        conf['SCREENGRAB_DIRECTORY']
ss_region =           conf['SCREENGRAB_REGION']


def mmap(x, in_min, in_max, out_min, out_max):
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

def main():
    Prog.exitnow = False
    mouse.position = (draw_rect[0], draw_rect[1])
    mouse.click(Button.left)

    Prog.program_start = time.perf_counter()

    for imdir in range(len(image_list)):

        image = image_list[imdir]
        # Uncomment me if you get assertion errors :)
        # image = os.path.join(os.path.dirname(__file__), image_list[imdir]).replace('\\','/')

        try:
            im = cv2.imread(image, -1)
        except:
            continue

        imgray = cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)
        ret,thresh = cv2.threshold(imgray,127,255,cv2.THRESH_BINARY)

        # Find the contours (outlines) of the image
        contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

        last = time.perf_counter()

        # Draw the image
        for data in range(len(contours)):
            for point in range(len(contours[data])):
                if point != 0: mouse.press(Button.left) # Fixes the weird lines from everywhere

                pos = (contours[data][point][0][0], contours[data][point][0][1])

                mouse.position = (
                    mmap(pos[0], 0, im.shape[1], draw_rect[0], draw_rect[2]),
                    mmap(pos[1], 0, im.shape[0], draw_rect[1], draw_rect[3])
                )
                mouse.release(Button.left)
            time.sleep(0.1)


        # Select all; will also render the frame because sometimes some parts of the image doesn't show up.
        keybrd.press(Key.ctrl_l);keybrd.tap('a');keybrd.release(Key.ctrl_l)


        # Another safety feature, will place mouse on the terminal (if your terminal inside of the point ofcourse) so that you can CTRL+C (Keyboard-Interrupt) out of it.
        mouse.position = (1000, 300)


        # Will sleep depending on how long it took to draw the image, so that mspaint will have time to process the input (+1.2 sec to make sure that it actually renders)
        time.sleep(((time.perf_counter() - last) * 2.5) + 1.2)


        # A safety feature.
        # IT DOESNT WORKSS DOSJFHADFHIDFJKLFJSLHdssIUODHJDd HELP ME FIX IT PLEASE SEPAESL PSLEPAEPLSLAELPLESPL

        # TODO:
        # -FIXME FIXME FIXME FIXME FIXME FIXME FIXME FIXME FIXME FIXME FIXME FIXME 
        # if mouse.position == (0, 0): exitnow = True


        mouse.position = (draw_rect[0], draw_rect[1])
        mouse.click(Button.left)

        now = time.perf_counter()

        # Process Logger
        print(f'Process: {image}, Estimated Finish Time: {round(np.mean(np.array(completed)) * len(image_list))}s, Render Time: {round(now - last)}s')
        completed.append(now - last)


        # Screenshotting and saving
        ss_img = ImageGrab.grab(ss_region)
        ss_img.save(ss_directory+'/'+image.split('/')[-1])


        # Delete Frame
        keybrd.tap(Key.delete)


        # Paint Tool
        mouse.position = paintbrush_position
        mouse.click(Button.left)

        mouse.position = tuple(draw_rect)
    Prog.program_end = time.perf_counter()


if __name__ == '__main__':
    MessageBox(0, 'Starting in 5 seconds...', 0x40)
    time.sleep(5)

    try:
        main()
    except Exception as ex:
        print(ex)
        Prog.exitnow = True
    print(f"\nFinished in: {Prog.program_end-Prog.program_start}s\n")
    MessageBox(0, 'Succesfully Rendered Frames...' if not Prog.exitnow else 'Program Force Quit', 'Done', 0x40)