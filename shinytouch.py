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
buildrange = False

canvas = Image.new("RGB", (640,480))
canvaspix = canvas.load()
draw2 = ImageDraw.Draw(canvas)
touchconf = False
camera = highgui.cvCreateCameraCapture(0)

f = open('shinyconf.py', 'r')
exec(f.read())
f.close()

f = open('shinyautoconf.py', 'r')
exec(f.read())
f.close()


w = xe-xs
ytr = float(tl-tr)/float(w);
ybr = float(bl-br)/float(w);


def get_image(dolog = False, getpix = False):
    global im, pix, draw
    im = highgui.cvQueryFrame(camera)
    # Add the line below if you need it (Ubuntu 8.04+)
    im = opencv.cvGetMat(im)
    #convert Ipl image to PIL image
    im = opencv.adaptors.Ipl2PIL(im)

    pix = im.load()
    draw = ImageDraw.Draw(im)

    if getpix != False:
      global rmin, rmax, gmin, gmax, bmin, bmax
      cr = pix[getpix[0],getpix[1]]
      if cr[0] < rmin:
        rmin = cr[0]
      if cr[0] > rmax:
        rmax = cr[0]
      if cr[1] < gmin:
        gmin = cr[1]
      if cr[1] > gmax:
        gmax = cr[1]
      if cr[2] < bmin:
        bmin = cr[2]
      if cr[2] > bmax:
        bmax = cr[2]
      print "Pixel Color:",cr
      saveconfig()

      
    pix[xs, tl] = (100,100,255,255)
    pix[xs, bl] = (100,100,255,255)
    pix[xe, tr] = (100,100,255,255)
    pix[xe, br] = (100,100,255,255)
    
    xp = 0
    yp = 0
    wp = 0
    oy = 0

    for x in range(0, w):
      count = 0
      if x % 3 > 0:
        continue
      for y in range(tr + int(ytr*x), br + int(ybr * x)):
        if y % 4 > 0:
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
            oy = y-count
            wp = count
            
            count = -1
            break
      if count == -1:
        break

    if xp > 0 and yp - 10> 0 and xp + 10 < im.size[0]:
      touchcolor = pix[xp-5,yp]
      pix[xp,yp] = (255,255,255,255)
      #if colorShadowTest(draw, pix[xp+5, yp-10], pix[xp+5,yp-10], xp, yp):
      if colorTest(xp, yp, dolog):
        #if colorTest(pix[xp+5,yp],pix[xp+5,yp-10], touchcolor, xp, yp, dolog):
        #print "reflectoin: x:",(xe-x),"y:",(y-(count/2))
        draw.rectangle(((xp-10, yp-10),(xp+10, oy+10)), outline=(100,255,100))
        xd = ((xp - xs)/float(w))*640
        disttop = (((tr-tl)/w) * (xp-xs)) + tl
        vwid = (bl-tl) + (((br-tr)-(bl-tl)) * ((xp - xs)/float(w)))
        yd = ((yp - disttop)/vwid) * 480
        draw2.rectangle(((xd-5, yd-5),(xd+5, yd+5)), outline=(100,255,100), fill=(100,255,100))
      else:
        #print "fayle"
        pix[xp+5,oy-10] = (255,255,255,255)
        pix[xp+5,yp] = (255,0,255,255)
        pix[xp-5,yp] = (0,0,255,255)
    if mode == "draw":
      return canvas
    elif mode == "transform":
      return im.transform((640,480), Image.QUAD, (xs,tl,xs,bl,xe,br,xe,tr))
    else:
      return im


def saveconfig():
  conf = """#this is the perspective distortion configuration section
xs = """+str(xs)+"""
xe = """+str(xe)+"""

tl = """+str(tl)+"""
bl = """+str(bl)+"""

tr = """+str(tr)+"""
br = """+str(br)+"""

#this is the color detection configuration section
rmin = """+str(rmin)+"""
rmax = """+str(rmax)+"""

gmin = """+str(gmin)+"""
gmax = """+str(gmax)+"""

bmin = """+str(bmin)+"""
bmax = """+str(bmax)
  print conf
  f = open('shinyautoconf.py', 'w')
  f.write(conf)
  f.close()
  print "Wrote configuration to file shinyautoconf.py"

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
print "Middle click to clear drawing canvas/Reload configuration."
print "Right click to enable debug mode."

while True:
    dolog = False
    getpix = False
    events = pygame.event.get()
    for event in events:
        if event.type == QUIT:
            sys.exit(0)
        if event.type == KEYDOWN:
          if event.unicode == "g":
            touchconf = True
            print "Move your finger around the visible area, click to stop"
          else:
            touchconf = False  
          if event.unicode == "d":
            mode = "draw"
          elif event.unicode == "i":
            mode = "image"
          elif event.unicode == "b":
            if buildrange == True:
              buildrange = False
              print "Disabled Color Range Building"
            else:
              buildrange = True
              print "Enabled Color Range Building"
          elif event.unicode == "t":
            if mode == "transform":
              mode = ""
              print "Disabled Auto Transform"
            else:
              mode = "transform"
              print "Enabled Auto Transform"
          elif event.unicode == "s":
            import datetime
            canvas.save("imgs/purty"+str(datetime.datetime.now().isoformat())+".png","PNG")
            print "Saved Image"
          elif event.unicode == "c":
            calibrate = True
            print "Click Top Left Corner"
        if event.type == MOUSEBUTTONDOWN:
            touchconf = False
            if event.button == 3:
              dolog = True
            elif event.button == 2:
              canvas = Image.new("RGB", (640,480))
              canvaspix = canvas.load()
              draw2 = ImageDraw.Draw(canvas)
              print "Reset Canvas"
              f = open('shinyconf.py', 'r')
              exec(f.read())
              f.close()
              print "Loaded Manual Configuration and Detection Runtime"
              f = open('shinyautoconf.py', 'r')
              exec(f.read())
              f.close()
              print "Loaded Automatic Generated Configuration"
            elif event.button == 1 and calibrate == False and buildrange == True:
              #yes, i did something very stupid and ugly just to not edit the calibration code
              getpix = event.pos
              #buildrange = False
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
                saveconfig()
                clicks = 0
            
    im = get_image(dolog, getpix)
    pg_img = pygame.image.frombuffer(im.tostring(), im.size, im.mode)
    screen.blit(pg_img, (0,0))
    pygame.display.flip()
    pygame.time.delay(int(1000 * 1.0/fps))

