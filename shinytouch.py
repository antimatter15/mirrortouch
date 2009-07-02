import pygame
import Image
from pygame.locals import *
import sys
from PIL import Image, ImageColor, ImageDraw
import itertools
import opencv
#this is important for capturing/displaying images
from opencv import highgui 

camera = highgui.cvCreateCameraCapture(0)


def colorTargetMatch(c):
  if c[0] < 245 and c[0] > 190: #red
    if c[1] < 220 and c[1] > 120: #green
      if c[2] < 205 and c[2] > 95: #blue
        return True
  return False

def colorReflectionDiff(c,d):
  #print "Red",c[0]-d[0]
  if c[0]-d[0] < 40 and c[0]-d[0] > -60: #red
    #print "Green",c[1]-d[1]
    if c[1]-d[1] < 0 and c[1]-d[1] > -60: #green
      #print "Blue",c[2]-d[2]
      if c[2]-d[2] < -20 and c[2]-d[2] > -60: #blue
        return True
  return False



box = 10

xs = 132
xe = 247

tr = 43
br = 463

tl = 165
bl = 402


w = xe-xs
ytr = float(tl-tr)/float(w);
ybr = float(bl-br)/float(w);

def get_image():
    im = highgui.cvQueryFrame(camera)
    # Add the line below if you need it (Ubuntu 8.04+)
    im = opencv.cvGetMat(im)
    #convert Ipl image to PIL image
    im = opencv.adaptors.Ipl2PIL(im)

    pix = im.load()
    draw = ImageDraw.Draw(im)

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

    if xp > 0 and yp > 0:
      pix[xp,yp] = (255,255,255,255)
      if colorReflectionDiff(pix[xp+10,yp],pix[xp+20,yp-30]):
        #print "reflectoin: x:",(xe-x),"y:",(y-(count/2))
        draw.rectangle(((xp-10, yp-10),(xp+10, yp+10)), outline=(100,255,100))
      else:
        #print "fayle"
        pix[xp+20,yp-30] = (255,255,255,255)
        pix[xp+10,yp] = (255,0,255,255)
    return im

fps = 60.0
pygame.init()
window = pygame.display.set_mode((640,480))
pygame.display.set_caption("ShinyTouch")
screen = pygame.display.get_surface()

while True:
    events = pygame.event.get()
    for event in events:
        if event.type == QUIT or event.type == KEYDOWN:
            sys.exit(0)
    im = get_image()
    pg_img = pygame.image.frombuffer(im.tostring(), im.size, im.mode)
    screen.blit(pg_img, (0,0))
    pygame.display.flip()
    pygame.time.delay(int(1000 * 1.0/fps))

