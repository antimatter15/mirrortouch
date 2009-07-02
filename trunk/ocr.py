#!/usr/bin/python

from PIL import Image, ImageColor, ImageDraw
oim = Image.open("captcha.php.png")
im = Image.new("RGB", (oim.size[0],oim.size[1]))
i2 = Image.new("RGB", (oim.size[0],oim.size[1]))
opix = oim.load()
pix = im.load()
p2x = i2.load()

for y in range(0, im.size[1]):
  for x in range(0, im.size[0]):
    if opix[x,y] == 1 or opix[x,y] > 35:
      pix[x,y] = (0,0,0)
      pix[x+1,y] = (0, 0, 0)
      pix[x+1,y+1] = (0, 0, 0)
      pix[x+1,y-1] = (0, 0, 0)
      
      pix[x,y+1] = (0, 0, 0)
      pix[x,y-1] = (0, 0, 0)
      
      pix[x-1,y] = (0, 0, 0)
      pix[x-1,y+1] = (0, 0, 0)
      pix[x-1,y-1] = (0, 0, 0)
    else:
      pix[x,y] = (255,255,255)

last = 0
gtxblck = 0

def copyblock(vx,vy):
  for sx in range(vx - 22, vx):
    for sy in range(vy - 25, vy):
      p2x[sx, sy - vy + 30] = pix[sx,sy] 

for x in range(0, im.size[0]):
  for y in range(0, im.size[1]):
    p2x[x,y] = (255,255,255)

for x in range(0, im.size[0]):
  hasblack = 0
  lastblack = 0
  for y in range(0, im.size[1]):
    if pix[x,y] == (0,0,0):
      hasblack += 1
      lastblack = y
  if hasblack > 2:
    if gtxblck < lastblack:
      gtxblck = lastblack
    #if last == 0:
      #print "Changed"
    last = 1
  else:
    if last == 1:
      print "Ended Letter",gtxblck,"X:",x
      copyblock(x+1, gtxblck)
      pix[x,gtxblck] = (255,0,0)
    last = 0
    gtxblck = 0
      
im.save("captout2.png","PNG")
i2.save("captout.png","PNG")
