# need to install: "pip install pynput" to use this
# This python file contains class that takes locational input from serial port and uses it for controlling computer

import serial
import time
#from pynput.mouse import Button, Controller as MouseController
from tkinter import *
import pyautogui # use pyautogui because no "Button" keyword that interfers with tkinter "button"
from pynput.keyboard import Key, Controller as KeyboardController # use pynput keyboard, faster than pyautogui


class Interact:

    def __init__(self):

        # not necessary to initialize variables just have it here for formality
        self.ser = 0
        #self.mouse = MouseController()
        # mouse.position(x,y) sets the mouse on coordinate, mouse.move(x,y) moves relatively
        # mouse.click (Button.right, 1) clicks right button once
        # mouse.press (Button.right), mouse.release (Button.right) clicks and releases respectively
        self.keyboard = KeyboardController()

        self.root = Tk()
        self.root.wm_attributes("-topmost", 1)
        # screen by pixel (top left is 0,0),***NOTE: change this depending on the screen you are using***
        self.Xscreenmax = 1279
        self.Yscreenmax = 1023
        # scan dist by mm (bottom left is 0,0)
        self.Xscanmax = 925
        self.Yscanmax = 1104

        self.prevx = 0
        self.prevy = 0

        self.down = False



    # primes serial port for reading
    def initialize(self):


        self.ser = serial.Serial('COM9', baudrate=2000000, timeout=0.1)  # initialize serial port for comms, CHANGE to correct comm port
        #self.ser = serial.Serial('COM9', baudrate=115200, timeout=None, xonxoff=False, rtscts=False,dsrdtr=False)  # Tried with and without the last 3 parameters, and also at 1Mbps, same happens.
        time.sleep(0.2)
        self.ser.flushInput()
        self.ser.flushOutput()

    def collectData(self):
        #self.ser.flush()
       # print(self.ser.inWaiting())

        #b = self.ser.read_until(b'\n')  # read a byte string until byte char '\n'
        b = self.ser.readline()  # read a byte string (note that one byte is one character send in serial port)
        string_n = b.decode()  # decode byte string into Unicode string
        string = string_n.rstrip()  # remove \n and \r
        return string.split()  # returns array of string type

    # Takes in the 2 x,y coordinates and converts it/remaps it to the coordinates of the computer and returns
    def remap (self,x,y):

        xremap = x * self.Xscreenmax/self.Xscanmax
        yremap = self.Yscreenmax - (y * self.Yscreenmax/self.Yscanmax) # due to placement of origins

        return (xremap,yremap)

    def homecursor(self):
        self.prevx, self.prevy = pyautogui.position()

        pyautogui.moveTo(self.Xscreenmax/2, 0)
        #self.mouse.position = (self.Xscreenmax/2, 0)

    def mousePosition(self):

        #break out of the inf loop on windows with ctrl + c ? doesnt work, just use ctrl + F2
        try:
            while (True):
                position = pyautogui.position()
                #position = self.mouse.position
                print (position)

                time.sleep(0.2)

        finally:
            print("hi outside")


    # prints raw location from serial
    def printContinuous(self):
        self.initialize()
        while True:
            data = self.collectData()

            if len(data) == 2:
                x = float(data[0])
                y = float(data[1])

                print(x,y)



    # reads serial port for the location, converts, then moves mouse to that location
    def moveMouse(self):
        self.initialize()

        while(True):
            data = self.collectData()
            if (len(data) == 2):
                if (float(data[0]) != -1) & (float(data[1]) != -1):
                    x, y = self.remap(float(data[0]), float(data[1]))
                    print (x, y)

                    # move mouse to certain position, make sure you can close with keyboard interrupt..
                    #self.mouse.position = (x, y)
                    pyautogui.moveTo(x,y)
                else:
                    print ("No pen detected")
            else:
                print("Serial comms error!")

        print("hi outside")
        self.ser.close()

    # Reads the locations from serial port, converts it, if locate, move mouse to location and click & hold
    def pressAndHold(self):

        self.initialize()
        down = False

        while(True):
            data = self.collectData()
            if (len(data) == 2):
                if (float(data[0]) != -1) & (float(data[1]) != -1):
                    x, y = self.remap(float(data[0]), float(data[1]))
                    print(x, y)

                    # move mouse to certain position, make sure you can close with keyboard interrupt..
                   # self.mouse.position = (x, y)
                    pyautogui.moveTo(x, y)
                    #self.mouse.press(Button.left) # check what happens if press repeatedly
                    if not down:
                        pyautogui.mouseDown(button='left')
                        down = True
                else:
                    print("No pen detected")
                    #self.mouse.release(Button.left)
                    pyautogui.mouseUp(button='left')
                    down = False
                    # make sure to kno
                    #self.homecursor() #resets cursor on corner when no retroreflector is found
            else:
                print("Serial comms error!")

    # For buttonGUI function Use
    def pressAndHoldGUI(self):

        data = self.collectData()
        if (len(data) == 2):
            if (float(data[0]) != -1) & (float(data[1]) != -1):
                x, y = self.remap(float(data[0]), float(data[1]))
                print(x, y)

                # move mouse to certain position, make sure you can close with keyboard interrupt..
               # self.mouse.position = (x, y)
                pyautogui.moveTo(x, y)
                #self.mouse.press(Button.left) # check what happens if press repeatedly
                if not self.down:
                    pyautogui.mouseDown(button='left')
                    self.down = True
            else:
                print("No pen detected")
                #self.mouse.release(Button.left)
                pyautogui.mouseUp(button='left')
                self.down = False
                # make sure to kno
                #self.homecursor() #resets cursor on corner when no retroreflector is found
        else:
            print("Serial comms error!")

        self.root.after(50, self.pressandHoldGUI)  # this allows simultaneous running of root.mainloop(), not sure what the number is

    def clickReleaseTest(self):

        # move mouse to certain position, make sure you can close with keyboard interrupt.. use ctrl + F2
       # pyautogui.moveTo(500,500)
       # self.mouse.position = (500, 500)
      #  self.mouse.click(Button.right) # from tests, repeated press doesnt repress, only click does that
       # time.sleep(1)
       # pyautogui.moveTo(520, 300)
        #self.mouse.position = (520, 300)
       # self.mouse.click(Button.right)
      #  time.sleep(1)
       # pyautogui.moveTo(500, 490)
        #self.mouse.position = (500, 490)
       # self.mouse.press(Button.right)
        time.sleep(5)
      #  pyautogui.moveTo(510, 495)
        #self.mouse.position = (510, 495)
       # self.mouse.press(Button.right)
        pyautogui.mouseDown (button = 'left')

        time.sleep(1)
        pyautogui.moveTo(530, 500)
        time.sleep(1)

        pyautogui.mouseDown (button = 'left')


       # pyautogui.mouseUp (button = 'right')


       # self.mouse.release(Button.right)
       # self.mouse.click(Button.left)
        pyautogui.scroll(10)


    # This ex func allows continuous loop running along side with tkinter mainloop
    # put press and hold stuff in here
    def runningLoopFunc (self):
        #print ("hey Im loopin!")
        time.sleep(2)
        print("down1")
        pyautogui.mouseDown(button='left')

        time.sleep(2)
        print("UP")
        pyautogui.mouseUp(button='left')

        self.root.after(50, self.runningLoopFunc) # this allows simultaneous running of root.mainloop()

    # ex function called by gui, see keyboard press functions below
    def testbuttonaction(self):
        print("button pressed!")

    # ex function that creates the GUI with tkinter
    def buttontestgui(self):

        upButton = Button(self.root, text = "UP", padx = 50, pady = 50, command = self.keyup)
        downButton = Button(self.root, text = "DOWN", padx = 50, pady = 50, command = self.keydown)
        leftButton = Button(self.root, text="LEFT", padx=50, pady=50, command=self.keyleft)
        rightButton = Button(self.root, text="RIGHT", padx=50, pady=50, command=self.keyright)
        pgupButton = Button(self.root, text="PGUP", padx=50, pady=50, command=self.keypgup)
        pgdownButton = Button(self.root, text="PGDOWN", padx=50, pady=50, command=self.keypgdown)

        upButton.grid(row = 0, column = 1)
        downButton.grid(row = 1, column = 1)
        leftButton.grid(row=1, column=0)
        rightButton.grid(row=1, column=2)
        pgupButton.grid(row=0, column=2)
        pgdownButton.grid(row=0, column=0)
        print("Initialized!")

        # loopin
        self.runningLoopFunc()  # main running loop here
        self.root.mainloop()

        #while (1):
           # self.root.update_idletasks()
          #  self.root.update()

    # Function that runs GUI and controls mouse in background with press & hold function
    # Press ctrl + F2 to stop program, must be selected on pycharm window though!
    def buttonGUI(self):

        self.initialize()
        self.down = False # initialize this for pressAndHoldGUI

        upButton = Button(self.root, text = "UP", padx = 50, pady = 50, command = self.keyup)
        downButton = Button(self.root, text = "DOWN", padx = 50, pady = 50, command = self.keydown)
        leftButton = Button(self.root, text="LEFT", padx=50, pady=50, command=self.keyleft)
        rightButton = Button(self.root, text="RIGHT", padx=50, pady=50, command=self.keyright)
        pgupButton = Button(self.root, text="PGUP", padx=50, pady=50, command=self.keypgup)
        pgdownButton = Button(self.root, text="PGDOWN", padx=50, pady=50, command=self.keypgdown)

        upButton.grid(row = 0, column = 1)
        downButton.grid(row = 1, column = 1)
        leftButton.grid(row=1, column=0)
        rightButton.grid(row=1, column=2)
        pgupButton.grid(row=0, column=2)
        pgdownButton.grid(row=0, column=0)
        print("Initialized!")

        # loopin
        self.pressAndHoldGUI()  # main running loop here
        self.root.mainloop()

        #while (1):
           # self.root.update_idletasks()
          #  self.root.update()

    # just testing
    def keyboardTest(self):

        time.sleep (5)

        for x in range(10):

            for char in "Hey I am typing super fast and smooth. So fast and smooth that it seems fake lol!\n":
                self.keyboard.press (char)
                self.keyboard.release (char)
              #  pyautogui.press(char)
             #  time.sleep (0.005)

    # This section is the keyboard simulated key press functions

    # Mouse scroll vs the key up or key down depending on the program being used on
    def keyup(self):

        # This is to make sure select on the working window before issuing the key command
       # time.sleep(1)
        self.homecursor()
        pyautogui.click(button = 'left' )
        pyautogui.moveTo(self.prevx, self.prevy)
        pyautogui.vscroll(200)

       # self.keyboard.press(Key.up)
        #self.keyboard.release(Key.up)

    def keydown(self):

        self.homecursor()
        pyautogui.click(button='left')
        pyautogui.moveTo(self.prevx, self.prevy)
        pyautogui.vscroll(-200)

       # self.keyboard.press(Key.down)
        #self.keyboard.release(Key.down)

    def keyleft(self):

        self.homecursor()
        pyautogui.click(button='left')
        pyautogui.moveTo(self.prevx, self.prevy)

        self.keyboard.press(Key.left)
        self.keyboard.release(Key.left)

    def keyright(self):

        self.homecursor()
        pyautogui.click(button='left')
        pyautogui.moveTo(self.prevx, self.prevy)

        self.keyboard.press(Key.right)
        self.keyboard.release(Key.right)

    def keypgup(self):

        self.homecursor()
        pyautogui.click(button='left')
        pyautogui.moveTo(self.prevx, self.prevy)

        self.keyboard.press(Key.page_up)
        self.keyboard.release(Key.page_up)

    def keypgdown(self):

        self.homecursor()
        pyautogui.click(button='left')
        pyautogui.moveTo(self.prevx, self.prevy)

        self.keyboard.press(Key.page_down)
        self.keyboard.release(Key.page_down)

    # Press ctrl + F2 to stop program, must be selected on pycharm window though!
    # This only works when smoothly move mouse to left of right of screen
    def swipetest(self):

        prevx, prevy = pyautogui.position()
        rightcount = 0
        leftcount = 0

        while(True):
            positionx, positiony = pyautogui.position()
           # print(positionx)
            #print(positiony)
            time.sleep(0.4) # this imitates the incoming serial value timing


            # swipe right counter
            if (positionx - prevx) > 30:
                leftcount = 0
                rightcount = rightcount + 1
                print (rightcount)

                # swipe right detected
                if rightcount >= 2:
                    self.keyboard.press(Key.page_up)
                    self.keyboard.release(Key.page_up)
                    rightcount = 0

            # swipe left counter
            elif (positionx - prevx) < -30:
                rightcount = 0
                leftcount = leftcount + 1

                # swipe left detected
                if leftcount >= 2:
                    self.keyboard.press(Key.page_down)
                    self.keyboard.release(Key.page_down)
                    leftcount = 0

            else:
                rightcount = 0
                leftcount = 0

            prevx = positionx
           # prevy = positiony

    # Press ctrl + F2 to stop program, must be selected on pycharm window though!
    # This only works when smoothly move mouse to left of right of screen
    # Takes value from serial port then moves mouse and applies swipetest function code
    def swipe(self):

        self.initialize()
        prevx, prevy = pyautogui.position()
        rightcount = 0
        leftcount = 0

        while (True):
            data = self.collectData()
            if (len(data) == 2):
                if (float(data[0]) != -1) & (float(data[1]) != -1):
                    x, y = self.remap(float(data[0]), float(data[1]))
                    print(x, y)

                    # move mouse to certain position, make sure you can close with keyboard interrupt..
                    # self.mouse.position = (x, y)
                    pyautogui.moveTo(x, y)

                    # swipe right counter
                    if (x - prevx) > 30:   # change this value for sensitivity
                        leftcount = 0
                        rightcount = rightcount + 1

                        # swipe right detected
                        if rightcount >= 2:
                            self.keyboard.press(Key.page_up)
                            self.keyboard.release(Key.page_up)
                            rightcount = 0

                    # swipe left counter
                    elif (x - prevx) < -30:  # change this value for sensitivity
                        rightcount = 0
                        leftcount = leftcount + 1

                        # swipe left detected
                        if leftcount >= 2:
                            self.keyboard.press(Key.page_down)
                            self.keyboard.release(Key.page_down)
                            leftcount = 0

                    else:
                        rightcount = 0
                        leftcount = 0

                    prevx = x

                else:
                    rightcount = 0
                    leftcount = 0
                    print("No pen detected")
            else:
                rightcount = 0
                leftcount = 0
                print("Serial comms error")


if __name__ == "__main__":

    # interactivity class object 'test'
    test = Interact()
   # test.printContinuous()  # use this to read from the serial port to ensure correct data
   # test.mousePosition()   # use for calibration, shows the coordinate of the cursor in real time
   # test.moveMouse()   # uses serial data positions to move the cursor
    #test.clickReleaseTest()
   # test.keyboardTest()
   # test.pressAndHold() # uses serial data positions to move cursor and click when there is a retroreflector detected
   # test.buttontestgui()    # test gui creation and button
  #  test.buttonGUI() # actual gui function that takes inputs from serial to control mouse
    #test.swipetest()    # reads the mouse cursor position and when swipe left/right will activate certain commands
    test.swipe() # uses serial data positions and reads the swipes left/right will activate certain commands, no mouse press!