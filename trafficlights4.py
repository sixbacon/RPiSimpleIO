# draft of a prgram to drive a simple Raspberry Pi interface board
# board will have traffic light leds, push buttons, trimmers and a temperature sensor 
# 1/1/13 using billboard module - works
# 1/1/13 starting talking to the board - leds working
# 2/1/13 switches now work - note have to set them up unlike outputs on chip
# 3/1/13 temperature display working
# 9/1/13 trimmer display now working
# 9/1/13 checkd works with board disconnected and connected again

import bb1
from bb1 import *
import i2cdevices2
from i2cdevices2 import *

#led patterns for traffic lights
redlight     = (RED,   BLACK,  BLACK)
redoranlight = (RED,   ORANGE, BLACK)
greenlight   = (BLACK, BLACK,  GREEN)
orangelight  = (BLACK, ORANGE, BLACK)

# tell computer what is connected to the digital i/o pins of chip
switch1=0
switch2=1
ledr1=2
ledo1=3
ledg1=4
ledr2=5
ledo2=6
ledg2=7
temperatureChannel=1
trimmer1Channel = 0
trimmer2Channel = 3

def readtemperature():
    # just a bodge for now
    return (3.0*(anaport.ADCread(1)-45))

def readtrimmer(channel):
    return anaport.ADCread(channel)

def setupbbhardware():
    #see if bb is attached
    global digport,anaport
    digport=pcf8574(0x20)
    anaport=pcf8591(0x48)
    if digport.ChipPresent & anaport.ChipPresent:
        bb1.bbpresent = True
    else:
        bb1.bbpresent = False
      
    if bb1.bbpresent == True : #set up ports to drive leds and read switches
        #switch all leds off
        digport.writeall(0)
        #enable the inputs for the switches
        digport.setinput(switch1)
        digport.setinput(switch2)
       
def switchled(block,lights):
    if block == 1: #block1
        if lights == redlight:
            digport.writeport(ledr1,1)
            digport.writeport(ledo1,0)
            digport.writeport(ledg1,0)
        if lights == redoranlight:
            digport.writeport(ledr1,1)
            digport.writeport(ledo1,1)
            digport.writeport(ledg1,0)
        if lights == greenlight:
            digport.writeport(ledr1,0)
            digport.writeport(ledo1,0)
            digport.writeport(ledg1,1)
        if lights == orangelight:
            digport.writeport(ledr1,0)
            digport.writeport(ledo1,1)
            digport.writeport(ledg1,0)
    else: #block2
        if lights == redlight:
            digport.writeport(ledr2,1)
            digport.writeport(ledo2,0)
            digport.writeport(ledg2,0)
        if lights == redoranlight:
            digport.writeport(ledr2,1)
            digport.writeport(ledo2,1)
            digport.writeport(ledg2,0)
        if lights == greenlight:
            digport.writeport(ledr2,0)
            digport.writeport(ledo2,0)
            digport.writeport(ledg2,1)
        if lights == orangelight:
            digport.writeport(ledr2,0)
            digport.writeport(ledo2,1)
            digport.writeport(ledg2,0)

def setledblock1(lights):
    for ind in range((len(bb1.ledBlock1))):
        bb1.ledBlock1[ind].colour=lights[ind]
    if bb1.bbpresent:
        switchled(1,lights)
        
def setledblock2(lights):
    for ind in range((len(bb1.ledBlock2))):
        bb1.ledBlock2[ind].colour=lights[ind]
    if bb1.bbpresent:
        switchled(2,lights)
        
def runlightsequence():
    #a pedestriam button has been pressed so start setting both sets of traffic lights to red
    setledblock1(orangelight)
    setledblock2(orangelight)
    updatescreen()
    pygame.time.wait(2000) #wait for 2000 ms or 3 sec
    setledblock1(redlight)
    setledblock2(redlight)
    updatescreen()
    pygame.time.wait(8000) #wait for 8000 ms or 15 sec
    setledblock1(redoranlight)
    setledblock2(redoranlight)
    updatescreen()
    pygame.time.wait(2000) #wait for 2000 ms or 3 sec
    setledblock1(greenlight)
    setledblock2(greenlight)
    updatescreen()
    pygame.event.clear
            
def main():
    setupbbhardware()
    initialisegraphics() #note have to have set up hardware first to read the status
    # set led intial colours
    setledblock1(greenlight)
    setledblock2(greenlight)  
    updatescreen()#update the screen with new objects
    while True: # main loop
       # update temperature
       if bb1.bbpresent:
           bb1.temperature = readtemperature()
           TempDisplay(bb1.temperature)
           bb1.trimmer1.angle=readtrimmer(trimmer1Channel)
           bb1.trimmer2.angle=readtrimmer(trimmer2Channel)
           bb1.trimmer1.draw()
           bb1.trimmer2.draw()
           # check for switch press on the board
           if digport.readport(switch1) == 1 :
               bb1.button1.pressed = True
           if digport.readport(switch2) == 1 :
               bb1.button2.pressed = True
       # check for keypress
       for event in pygame.event.get():
           if event.type == QUIT:
               #switch all leds off
               if bb1.bbpresent:
                   digport.writeall(0)
               #close window
               pygame.quit()
               #stop program
               sys.exit()
           elif event.type == MOUSEBUTTONDOWN:
               if bb1.button1.buttonPressed(pygame.mouse.get_pos()):
                   bb1.button1.pressed= True
               if bb1.button2.buttonPressed(pygame.mouse.get_pos()):
                   bb1.button2.pressed= True
       if bb1.button1.pressed  :
            updatescreen()
            pygame.time.wait(FPS)
            bb1.button1.pressed= False
            updatescreen()
            runlightsequence()
       if bb1.button2.pressed  :    
            updatescreen()
            pygame.time.wait(FPS)
            bb1.button2.pressed= False
            updatescreen()
            runlightsequence()

if __name__ == '__main__':
    main()

