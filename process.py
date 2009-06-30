from PIL import Image, ImageColor, ImageDraw
import itertools

im = Image.open("2009-06-27-160922.jpg")
#im = im.transform(im.size, Image.QUAD, (32-15,23-10,44-15,192-10,208-15,186-10,208-15,20-10))
pix = im.load()
draw = ImageDraw.Draw(im)

box = 10

def colorTargetMatch(c):
  if c[0] < 130 and c[0] > 70: #red
    if c[1] < 140 and c[1] > 100: #green
      if c[2] < 170 and c[2] > 100: #blue
        return True
  return False

def colorBandMatch(c):
  if c[0] < 215 and c[0] > 110: #red
    if c[1] < 215 and c[1] > 125: #green
      if c[2] < 215 and c[2] > 140: #blue
        return True
  return False
  
start = -1
xlist = []
for x in range(0, im.size[0]):
  color = pix[x, 0]
  if colorBandMatch(color) == False:
    pix[x, 0] = (255, 0, 0, 255)
    if start == -1:
      start = x
  elif start != -1:
    if x - start < 10:
      print "X Axis Center Discarded; Start: ",start," End: ",x
    else:
      print "X Axis Center Found; Start: ",start," End: ",x
      xlist.append((start+x)/2)
      pix[(start+x)/2, 0] = (0,255,0,255)
    start = -1
start = -1
ylist = []
for y in range(0, im.size[1]):
  color = pix[0, y]
  if colorBandMatch(color) == False:
    pix[0, y] = (255, 0, 0, 255)
    if start == -1:
      start = y
  elif start != -1:
    if y - start < 10:
      print "Y Axis Center Discarded; Start: ",start," End: ",y
    else:
      print "Y Axis Center Found; Start: ",start," End: ",y
      ylist.append((start+y)/2)
      pix[0,(start+y)/2] = (0,255,0,255)
    start = -1

xm = 210.0
ym = 130.0
l = 525.0

for point in itertools.product(xlist, ylist):
  x = point[0] #- 5# - (point[1]*0.05) - 5
  y = point[1] #+ (x*0.1) - 15
  
  print "Iterating: x: ",x," y: ", y
  
  x = (y + (l/float(x-xm))*x)/((l/float(x-xm))-(float(y-ym)/l))

  y = (float(y-ym)/l)*x + y
  
  x = int(x)
  y = int(y)
  
  print "Adjusted: x: ",x," y: ",y
  
  if x-box < 0 or x+box > im.size[0] or y-box < 0 or y+box > im.size[1]:
    print "Out of Range"
    continue
  
  color = pix[x, y]
  print color
  
  pix[x, y] = (255, 255, 255, 255)
  if colorTargetMatch(color) == True:
    pix[x, y] = (255, 255, 0, 255)
    count = 0.0
    for x1 in range(x-box, x+box):
      color = pix[x1, y-box]
      if colorTargetMatch(color) == True:
        count += 1
        pix[x1, y-box] = (50, 50, 255, 255)
    for x2 in range(x-box, x+box):
      color = pix[x2, y+box]
      if colorTargetMatch(color) == True:
        count += 1
        pix[x2, y+box] = (50, 50, 255, 255)
    for y1 in range(y-box, y+box):
      color = pix[x-box,y1]
      if colorTargetMatch(color) == True:
        count += 1
        pix[x-box,y1] = (50, 50, 255, 255)
    for y2 in range(y-box, y+box):
      color = pix[x+box,y2]
      if colorTargetMatch(color) == True:
        count += 1
        color = pix[x+box,y2] = (50, 50, 255, 255)
    ratio = count / (box*2*4)

    #draw.rectangle(((x-box, y-box),(x+box, y+box)), outline=(255,255,0))
    
    draw.text((x+1, y+1), str(ratio), fill=(0,0,0))
    #draw.rectangle(((x-box, y-box),(x+box, y+box)), outline=(0,0,0))
    if ratio > 0.09 and ratio < 0.8:
      pix[x, y] = (255, 0, 255, 255)
      draw.rectangle(((x-10, y-10),(x+10, y+10)), outline=(100,255,100))
      print ratio
      print point
    #yay, the point is actually on the blah
  

#im.show()
im.save("ScanOut.png", "PNG")
