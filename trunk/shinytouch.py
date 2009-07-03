import pygame
import Image
from pygame.locals import *
import sys
from PIL import Image, ImageColor, ImageDraw
import itertools
import opencv
#this is important for capturing/displaying images
from opencv import highgui 
mode = "image"
calibrate = False
box = 10

canvas = Image.new("RGB", (640,480))
canvaspix = canvas.load()
draw2 = ImageDraw.Draw(canvas)

camera = highgui.cvCreateCameraCapture(0)


def colorTargetMatch(c):
  if c[0] < 245 and c[0] > 170: #red
    if c[1] < 220 and c[1] > 85: #green
      if c[2] < 205 and c[2] > 70: #blue
        return True
  return False

def colorReflectionDiff(c,d, dolog = False):
  if dolog == True:
    print "Red",c[0]-d[0]
    print "Green",c[1]-d[1]
    print "Blue",c[2]-d[2]
  if c[0]-d[0] < 50 and c[0]-d[0] > 15: #red
    if c[1]-d[1] < 13 and c[1]-d[1] > -60: #green
      if c[2]-d[2] < 13 and c[2]-d[2] > -60: #blue
        return True
  return False





xs = 146
xe = 277

tl = 152
bl = 395

tr = 9
br = 468



w = xe-xs
ytr = float(tl-tr)/float(w);
ybr = float(bl-br)/float(w);

def get_image(dolog = False):
    im = highgui.cvQueryFrame(camera)
    # Add the line below if you need it (Ubuntu 8.04+)
    im = opencv.cvGetMat(im)
    #convert Ipl image to PIL image
    im = opencv.adaptors.Ipl2PIL(im)

    pix = im.load()
    draw = ImageDraw.Draw(im)

    pix[xs, tl] = (100,100,255,255)
    pix[xs, bl] = (100,100,255,255)
    pix[xe, tr] = (100,100,255,255)
    pix[xe, br] = (100,100,255,255)
    
    xp = 0
    yp = 0
    wp = 0

    for x in range(0, w):
      count = 0
      if x % 3 > 0:
        continue
      for y in range(tr + int(ytr*x), br + int(ybr * x)):
        if y % 3 > 0:
          continue
        if colorTargetMatch(pix[xe-x,y]):
          pix[xe-x,y] = (0,255,0,255)
          count += 1
        else:
          #pix[xe-x,y] = (0,0,0,255)
          if count >= 1:
            #print "x:",(xe-x),"y:",(y-(count/2))
            xp = xe-x
            yp = y-(count/2)
            wp = count
            count = -1
            break
      if count == -1:
        break

    if xp > 0 and yp - 20> 0 and xp + 10 < im.size[0]:
      pix[xp,yp] = (255,255,255,255)
      if colorReflectionDiff(pix[xp+10,yp],pix[xp+10,yp-20], dolog):
        #print "reflectoin: x:",(xe-x),"y:",(y-(count/2))
        draw.rectangle(((xp-10, yp-10),(xp+10, yp+10)), outline=(100,255,100))
        xd = ((xp - xs)/float(w))*640
        disttop = (((tr-tl)/w) * (xp-xs)) + tl
       
        vwid = (bl-tl) + (((br-tr)-(bl-tl)) * ((xp - xs)/float(w)))
        
        yd = ((yp - disttop)/vwid) * 480
        
        draw2.rectangle(((xd-5, yd-5),(xd+5, yd+5)), outline=(100,255,100))
      else:
        #print "fayle"
        pix[xp+10,yp-20] = (255,255,255,255)
        pix[xp+10,yp] = (255,0,255,255)
    if mode == "draw":
      return canvas
    else:
      return im

fps = 60.0
pygame.init()
window = pygame.display.set_mode((640,480))
pygame.display.set_caption("ShinyTouch")
screen = pygame.display.get_surface()
clicks = 0
subavg = 0

print "Press d to switch to draw mode."
print "Press i to switch to image mode."
print "Press c to calibrate image."

while True:
    dolog = False
    events = pygame.event.get()
    for event in events:
        if event.type == QUIT:
            sys.exit(0)
        if event.type == KEYDOWN:
    
          if event.unicode == "d":
            mode = "draw"
          elif event.unicode == "i":
            mode = "image"
          elif event.unicode == "c":
            calibrate = True
            print "Click Top Left Corner"
        if event.type == MOUSEBUTTONDOWN:
            if event.button == 3:
              dolog = True
              import datetime
              canvas.save("purty"+str(datetime.datetime.now().isoformat())+".png","PNG")
            elif event.button == 2:
              canvas = Image.new("RGB", (640,480))
              canvaspix = canvas.load()
              draw2 = ImageDraw.Draw(canvas)
              print "Reset Canvas"
            elif event.button == 1 and calibrate == True:
              clicks += 1
              if clicks == 1:
                tl = event.pos[1]
                subavg = event.pos[0]
                xs = subavg
                print "Click Bottom Left Corner"
              elif clicks == 2:
                bl = event.pos[1]
                xs = (subavg + event.pos[0])/2
                print "Click Bottom Right Corner"
              elif clicks == 3:
                br = event.pos[1]
                subavg = event.pos[0]
                xe = subavg
                print "Click Top Right Corner"
              elif clicks == 4:
                tr = event.pos[1]
                xe = (subavg + event.pos[0])/2
                print "Done. To recalibrate, press c and then click Top Left corner again."
                calibrate = False
                print """xs = """+str(xs)+"""
xe = """+str(xe)+"""

tl = """+str(tl)+"""
bl = """+str(bl)+"""

tr = """+str(tr)+"""
br = """+str(br)
                clicks = 0
            
    im = get_image(dolog)
    pg_img = pygame.image.frombuffer(im.tostring(), im.size, im.mode)
    screen.blit(pg_img, (0,0))
    pygame.display.flip()
    pygame.time.delay(int(1000 * 1.0/fps))

