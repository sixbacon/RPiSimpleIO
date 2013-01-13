#handles sreen dsiplay of bill board
#1/1/13
import pygame, sys
from pygame.locals import *

#Constants
#timing
FPS = 400

#Window size - fixed to begin with
windowWidth = 800
windowHeight = 500

# location of top left of pcb
basex = 100
basey = 10

# pcb dimensions all in pixels
basew = 400
baseh = 300
#hole corner assume all same distance from edges
holed = 20
#hole radius
holer = 5

#set up size of leds
ledSize=20
#location of first block of leds relative to pcb
ledBlock1x = 40
ledBlock1y = 90
#location of second block of leds relative to pcb
ledBlock2x = 340
ledBlock2y = 90
#button details and locations relative to pcb
buttonSize = 40
button1x =  30
button1y = 160
button2x = 330
button2y = 160
#Trimmer details and locations relative to pcb
trimmerSize = 40
trimmer1x = 110
trimmer1y = 210
trimmer2x = 300
trimmer2y = 210
trimsector=270

#colour table  R    G    B
WHITE        = (255, 255, 255)
BLACK        = (  0,   0,   0)
RED          = (255,   0,   0)
GREEN        = (  0, 255,   0)
LIGHTGREEN   = (204, 255, 153)
DARKGREEN    = (  0, 155,   0)
DARKGRAY     = ( 40,  40,  40)
YELLOW       = (255, 255,   0)
BRIGHTGREEN  = (  0, 255,   0)
BRIGHTBLUE   = (  0,   0, 255)
BLUE         = (  0,   0, 155)
LIGHTGRAY    = (203, 212, 212)
ORANGE       = (255, 128,   0)
OFFWHITE     = (250, 250, 250)

#Variables - give current status for display
bbpresent = False
temperature = 20
angle1 = 40
angle2 = 100
   
def drawbaseboard():
    #pretty crude drawing to begin with
    #draw pcb in window
    base = pygame.Rect(basex,basey,basew,baseh)
    pygame.draw.rect(DISPLAYSURF, GREEN, base) 

    #put hole in each corner
    cx = basex +holed
    cy = basey +holed
    cr = holer
    colour = DARKGRAY
    pygame.draw.circle(DISPLAYSURF,colour,[cx,cy],cr)
    cx = basex + basew - holed
    cy = basey + holed
    cr = holer
    colour = DARKGRAY
    pygame.draw.circle(DISPLAYSURF,colour,[cx,cy],cr)
    cx = basex + holed
    cy = basey + baseh -holed
    cr = holer
    colour = DARKGRAY
    pygame.draw.circle(DISPLAYSURF,colour,[cx,cy],cr)
    cx = basex + basew - holed
    cy = basey + baseh - holed
    cr = holer
    colour = DARKGRAY
    pygame.draw.circle(DISPLAYSURF,colour,[cx,cy],cr)

def drawBillBoardAttached(attached):
    # draw box saying if interface board is connected
    bbx = basex + 180
    bby = basey + 50
    bbd = 12
    bbBox = pygame.Rect(bbx-5, bby-bbd, 70,bbd)
    pygame.draw.rect(DISPLAYSURF, WHITE, bbBox)
    font = pygame.font.Font(None, 16)
    bbhead=       '  Board     '
    text = font.render(bbhead, 1, BLACK)
    textpos =(bbx,bby-bbd)
    DISPLAYSURF.blit(text, textpos)
    if attached :
       bbstatus=  '  Present   '
    else:
       bbstatus = 'Not Attached'
    bbBox = pygame.Rect(bbx-5, bby, 70,bbd)
    pygame.draw.rect(DISPLAYSURF, BLACK, bbBox)
    text = font.render(bbstatus, 1, WHITE)
    textpos =(bbx,bby)
    DISPLAYSURF.blit(text, textpos)

def TempDisplay(temp):
    # draw box displaying the temperature of the sensor on the board
    tdx = basex + 190
    tdy = basey + 250
    tdd = 12
    tempBox = pygame.Rect(tdx-5, tdy-tdd, 40,tdd)
    pygame.draw.rect(DISPLAYSURF, YELLOW, tempBox)
    temphead=str("TEMP")  
    font = pygame.font.Font(None, 16)
    text = font.render(temphead, 1, BLUE)
    textpos =(tdx,tdy-tdd)
    DISPLAYSURF.blit(text, textpos)
    
    tempBox = pygame.Rect(tdx-5, tdy, 40,tdd)
    pygame.draw.rect(DISPLAYSURF, BLUE, tempBox)
    tempstr=str("{0:4.1f}".format(temp))
    text = font.render(tempstr, 1, YELLOW)
    textpos =(tdx,tdy)
    DISPLAYSURF.blit(text, textpos)   
    pygame.display.update()
    
class activeElement():
    #base class for objects draw on screen
    def __init__(self,x,y,w,h,colour):
        # change from pcb coordinates to window coordinates
        self.x=x + basex
        self.y=y + basey
        self.w=w
        self.h=h
        self.colour=colour

#functions for trimmer arrow manipulation
#the arrow is a sprite from pygame module so can easily redraw
# the immage is styored extermnally and has to be loaded
def load_image(name, colorkey=None):
    fullname =  name
    try:
        image = pygame.image.load(fullname)
    except pygame.error, message:
        print 'Cannot load image:', fullname
        raise SystemExit, message
    image = image.convert()
    if colorkey is not None:
        if colorkey is -1:
            colorkey = image.get_at((0,0))
        image.set_colorkey(colorkey, RLEACCEL)
    return image, image.get_rect()

class Arrow(pygame.sprite.Sprite):
    # rotates arrow
    def __init__(self):
        pygame.sprite.Sprite.__init__(self) #call Sprite intializer
        self.image, self.rect = load_image('tarrow1.bmp', -1)
        screen = pygame.display.get_surface()
        #self.area = screen.get_rect()
        self.original = self.image

    def rotate(self,angle,coord,angrange):         
        self.angle = angle
        center = coord
        #map angle onto  sector with centre at top
        rotation=self.angle+360-angrange/2
        # print "rotation", angle, rotation #for debug
        if rotation >= 360:
            rotation = rotation - 360
        rotate = pygame.transform.rotate
        self.image = rotate(self.original, -1*rotation) #-1 to rotate clockwise
        self.rect = self.image.get_rect(center=center)           

class trimmer(activeElement):
    def __init__(self,x,y,angle):
        activeElement.__init__(self,x,y,trimmerSize,trimmerSize,ORANGE)
        self.angle=angle
        self.arrow=Arrow()
        self.sprite = pygame.sprite.RenderPlain((self.arrow))
        
    def draw(self):
        # draw the trimmer with arrow at correct angle
        cx= self.x 
        cy= self.y 
        cr=trimmerSize/2
        pygame.draw.circle(DISPLAYSURF,self.colour,[cx,cy],cr)   
        # add arrow next
        self.arrow.rotate(self.angle,(self.x,self.y),trimsector)
        self.sprite.update()
        self.sprite.draw(DISPLAYSURF)            

class led(activeElement):
    def __init__(self,x,y):
        activeElement.__init__(self,x,y,ledSize,ledSize,BLACK)
        
    def draw(self):
        # draw the appropraite led with its current colour
        ledBox = pygame.Rect(self.x, self.y, ledSize, ledSize)
        pygame.draw.rect(DISPLAYSURF, WHITE, ledBox)
        cx=self.x+ledSize/2
        cy=self.y+ledSize/2
        cr=ledSize/2
        pygame.draw.circle(DISPLAYSURF,self.colour,[cx,cy],cr)

class button(activeElement):
    def __init__(self,x,y):
        activeElement.__init__(self,x,y,buttonSize,buttonSize,BLACK)
        self.pressed=False
    
    def draw(self):
        # draw the button with appropriate status colour
        if self.pressed == True :
           colour= RED
        else:
           colour = BLACK
        buttonBox = pygame.Rect(self.x,self.y,self.w,self.h)
        pygame.draw.rect(DISPLAYSURF, LIGHTGRAY, buttonBox)
        cx=self.x+ buttonSize/2
        cy=self.y+buttonSize/2
        cr=buttonSize/3
        pygame.draw.circle(DISPLAYSURF,colour,[cx,cy],cr)   

    def buttonPressed(self,mouse):
        # check to see if a particular button has been pressed  
        if mouse[0] > self.x: # topleft x
                if mouse[1] > self.y:  # topleft y
                    if mouse[0] < self.x + buttonSize: # bottomright x
                        if mouse[1] < self.y + buttonSize: # bottomright y
                            return True
                        else: return False
                    else: return False
                else: return False
        else: return False

def initialisegraphics():
    global ledBlock1,ledBlock2,button1, button2, FPSCLOCK, DISPLAYSURF, allsprites ,\
           Tarrow1 , Tarrow2, angle1, angle2, trimmer1, trimmer2  # so can change global vaiables
  
    #using pygame for graphics so start it off
    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((windowWidth, windowHeight))
    pygame.display.set_caption('RPi Cream Interface')
   
    #Create the Backgound
    background = pygame.Surface(DISPLAYSURF.get_size())
    background = background.convert()
    background.fill(OFFWHITE) 
    #Display The Background
    DISPLAYSURF.blit(background, (0, 0))

    # build up pcb on scrfeen
    drawbaseboard()
    pygame.display.flip()

    # Create buttons
    button1=button(button1x,button1y)
    button2=button(button2x,button2y)
    
    # Create trimmers    
    trimmer1=trimmer(trimmer1x,trimmer1y,angle1)
    trimmer2=trimmer(trimmer2x,trimmer2y,angle2)

    # Show connection status
    drawBillBoardAttached(bbpresent)
    
    # create led blocks
    ledBlock1=[led(ledBlock1x,ledBlock1y),led(ledBlock1x,ledBlock1y+ledSize),\
               led(ledBlock1x,ledBlock1y+ledSize+ledSize)]
    ledBlock2=[led(ledBlock2x,ledBlock2y),led(ledBlock2x,ledBlock2y+ledSize),\
               led(ledBlock2x,ledBlock2y+ledSize+ledSize)]

def updatescreen():
    trimmer1.draw()
    trimmer2.draw()
    for ind in range((len(ledBlock1))):
        ledBlock1[ind].draw()
    for ind in range((len(ledBlock2))):
        ledBlock2[ind].draw()
    button1.draw()
    button2.draw()
    TempDisplay(temperature)          
    drawBillBoardAttached(bbpresent)# Show connection status
    pygame.display.update()
          
def main():
    #set up pcb simulation on screen
    initialisegraphics()
    #draw screen 
    updatescreen()  
           
    while True: # main  loop
       # check for keypress
       for event in pygame.event.get():
           if event.type == QUIT:
               pygame.quit()
               sys.exit()
                                
if __name__ == '__main__':
    main()
