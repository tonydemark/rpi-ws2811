### Sample python code for NeoPixels on Raspberry Pi
### this code is random suggestion for my christmas tree from my family, friends, and other examples on the web
### orginal code: https://github.com/DanStach/rpi-ws2811
import time
import board
import neopixel
import random
import math
import serial
import ctypes



# Choose an open pin connected to the Data In of the NeoPixel strip, i.e. board.D18
# NeoPixels must be connected to D10, D12, D18 or D21 to work.
pixel_pin = board.D18

# The number of NeoPixels
num_pixels = 400

# The order of the pixel colors - RGB or GRB. Some NeoPixels have red and green reversed!
# For RGBW NeoPixels, simply change the ORDER to RGBW or GRBW.
ORDER = neopixel.RGB

pixels = neopixel.NeoPixel(pixel_pin, num_pixels, brightness=0.2, auto_write=False, pixel_order=ORDER)

wait_time = 1


def colorAll2Color(c1, c2):
    for i in range(num_pixels):
        if(i % 2 == 0): # even
            pixels[i] = c1
        else: # odd   
            pixels[i] = c2
    pixels.show()


def wheel(pos):
    # Input a value 0 to 255 to get a color value.
    # The colours are a transition r - g - b - back to r.
    if pos < 0 or pos > 255:
        r = g = b = 0
    elif pos < 85:
        r = int(pos * 3)
        g = int(255 - pos*3)
        b = 0
    elif pos < 170:
        pos -= 85
        r = int(255 - pos*3)
        g = 0
        b = int(pos*3)
    else:
        pos -= 170
        r = 0
        g = int(pos*3)
        b = int(255 - pos*3)
    return (r, g, b) if ORDER == neopixel.RGB or ORDER == neopixel.GRB else (r, g, b, 0)


def rainbow_cycle(delay, cycles):
    for j in range(255 * cycles):
        for i in range(num_pixels):
            # " // "  this divides and returns the integer value of the quotient. 
            # It dumps the digits after the decimal
            pixel_index = (i * 256 // num_pixels) + j
            pixels[i] = wheel(pixel_index & 255)
        pixels.show()
        time.sleep(delay)


def RGBLoop(delay):
    for j in range(3):
        # Fade IN
        for k in range(256):
            if j == 0:
                pixels.fill((k, 0, 0))
            elif j == 1:
                pixels.fill((0, k, 0))
            elif j == 2:
                pixels.fill((0, 0, k))
            pixels.show()
            time.sleep(delay)

        # Fade OUT
        for k in range(256):
            if j == 2:
                pixels.fill((k, 0, 0))
            elif j == 1:
                pixels.fill((0, k, 0))
            elif j == 0:
                pixels.fill((0, 0, k))
            pixels.show()
            time.sleep(delay)
    
def FadeInOut(red, green, blue, delay):
    r = 0
    g = 0
    b = 0
      
    for k in range(256):
        r = (k/256.0)*red
        g = (k/256.0)*green
        b = (k/256.0)*blue
        pixels.fill((int(r), int(g), int(b)))
        pixels.show()
        time.sleep(delay)
     
    for k in range(256, -1, -1):
        r = (k/256.0)*red
        g = (k/256.0)*green
        b = (k/256.0)*blue
        pixels.fill((int(r), int(g), int(b)))
        pixels.show()
        time.sleep(delay)

def Twinkle(red, green, blue, Count, SpeedDelay, OnlyOne):
    pixels.fill((0,0,0))
  
    for i in range(Count):
        pixels[random.randint(0, num_pixels-1)] = (red, green, blue)
        pixels.show()
        time.sleep(SpeedDelay)
        if OnlyOne:
            pixels.fill((0,0,0))

    time.sleep(SpeedDelay)


def TwinkleRandom(Count, SpeedDelay, OnlyOne):
    pixels.fill((0,0,0))

    for i in range(Count):
        pixels[random.randint(0, num_pixels-1)] = (random.randint(0,255), random.randint(0,255), random.randint(0,255))
        pixels.show()
        time.sleep(SpeedDelay)
        if OnlyOne:
            pixels.fill((0,0,0))

    time.sleep(SpeedDelay)


def Sparkle(red, green, blue, Count, SpeedDelay):

    for i in range(Count):    
        Pixel = random.randint(0,num_pixels-1)
        pixels[Pixel] = (red,green,blue)
        pixels.show()
        time.sleep(SpeedDelay)
        pixels[Pixel] = (0,0,0)

def SnowSparkle(red, green, blue, Count, SparkleDelay, SpeedDelay):
    pixels.fill((red,green,blue))

    for i in range(Count):
        Pixel = random.randint(0,num_pixels-1)
        pixels[Pixel] = (255,255,255)
        pixels.show()
        time.sleep(SparkleDelay)
        pixels[Pixel] = (red,green,blue)
        pixels.show()
        time.sleep(SpeedDelay)


def RunningLights(red, green, blue, WaveDelay):
    Position = 0
    
    for j in range(num_pixels*2):
        Position = Position + 1
        
        for i in range(num_pixels):
            # sine wave, 3 offset waves make a rainbow!
            # float level = sin(i+Position) * 127 + 128;
            # setPixel(i,level,0,0);
            # float level = sin(i+Position) * 127 + 128;
            level = math.sin(i + Position) * 127 + 128
            r = int((level/255)*red)
            g = int((level/255)*green)
            b = int((level/255)*blue)
            pixels[i] = (r,g,b)

        pixels.show()
        time.sleep(WaveDelay)


def colorWipe(red, green, blue, SpeedDelay):
    for i in range(num_pixels):
        pixels[i] = (red, green, blue)
        pixels.show()
        time.sleep(SpeedDelay)



def theaterChase(red, green, blue, cycles, SpeedDelay):
    for j in range(cycles):
        for q in range(3):
            for i in range(0, num_pixels, 3):
                if i+q < num_pixels:
                    # turn every third pixel on
                    pixels[i+q] = (red, green, blue)
            
            pixels.show()
            time.sleep(SpeedDelay)
            
            for i in range(0, num_pixels, 3):
                if i+q < num_pixels:
                    # turn every third pixel off
                    pixels[i+q] = (0,0,0)



def theaterChaseRainbow(SpeedDelay):
    # cycle all 256 colors in the wheel
    for j in range(256):

        for q in range(3):
            for i in range(0, num_pixels, 3):
                # check that pixel index is not greater than number of pixels
                if i+q < num_pixels:
                    # turn every third pixel on
                    pixel_index = (i * 256 // num_pixels) + j
                    pixels[i+q] = wheel(pixel_index & 255)

            
            pixels.show()
            time.sleep(SpeedDelay)
            
            for i in range(0, num_pixels, 3):
                # check that pixel index is not greater than number of pixels
                if i+q < num_pixels:
                    # turn every third pixel off
                    pixels[i+q] = (0,0,0)



### Fix Me - something is broken with the logic. the color doesn't change. and the fire effect seems small
### orginal code; https://www.tweaking4all.com/hardware/arduino/adruino-led-strip-effects/#LEDStripEffectFire
def Fire(Cooling, Sparking, SpeedDelay, LoopCount):
    heat = []
    for i in range(num_pixels):
        heat.append(0)
     
    for l in range(LoopCount):
        cooldown = 0
        
        # Step 1.  Cool down every cell a little
        for i in range(num_pixels):
            #print()
            #print()
            #print("rand interal" + str(((Cooling * 10) / num_pixels) + 2))
            cooldown = random.randint(0, int(((Cooling * 10) / num_pixels) + 2))
            #print("cooldown " + str(cooldown))
            #print("heat " + str(heat[i]))
            if cooldown > heat[i]:
                heat[i]=0
            else: 
                heat[i]=heat[i]-cooldown
        
        # Step 2.  Heat from each cell drifts 'up' and diffuses a little
        for k in range(num_pixels - 1, 2, -1):
            heat[k] = (heat[k - 1] + heat[k - 2] + heat[k - 2]) / 3
            
        # Step 3.  Randomly ignite new 'sparks' near the bottom
        if random.randint(0,255) < Sparking:
            y = random.randint(0,7)
            #heat[y] = heat[y] + random.randint(160,255)
            heat[y] = random.randint(160,255)

        # Step 4.  Convert heat to LED colors
        #print(heat)
        for j in range(num_pixels):
            #print(heat[j] )
            setPixelHeatColor(j, int(heat[j]) )

        pixels.show()
        time.sleep(SpeedDelay)

def setPixelHeatColor (Pixel, temperature):
    # Scale 'heat' down from 0-255 to 0-191
    t192 = round((temperature/255.0)*191)

    # calculate ramp up from
    heatramp = t192 & 63 # 0..63  0x3f=63
    heatramp <<= 2 # scale up to 0..252
    #print("t192=" + str(t192) + "  heatramp=" + str(heatramp))
    # figure out which third of the spectrum we're in:
    if t192 > 0x80: # hottest 128 = 0x80
        pixels[Pixel] = (255, 255, int(heatramp))
    elif t192 > 0x40: # middle 64 = 0x40
        pixels[Pixel] = (255, int(heatramp), 0)
    else: # coolest
        pixels[Pixel] = (int(heatramp), 0, 0)

def FireCustom(CoolingRangeStart, CoolingRangeEnd, Sparking, SparkingRangeStart, SparkingRangeEnd, SpeedDelay, FireColor, FireEffect, LoopCount):
     heat = []
     for i in range(num_pixels):
        heat.append(0)
     for l in range(LoopCount):
        cooldown = 0
        
        # Step 1.  Cool down every cell a little
        for i in range(num_pixels):
            # for 50 leds and cooling 50
            # cooldown = random.randint(0, 12)
            # cooldown = random.randint(0, ((Cooling * 10) / num_pixels) + 2)
            cooldown = random.randint(CoolingRangeStart, CoolingRangeEnd)
            if cooldown > heat[i]:
                heat[i]=0
            else: 
                heat[i]=heat[i]-cooldown
        
        # Step 2.  Heat from each cell drifts 'up' and diffuses a little
        for k in range(num_pixels - 1, 2, -1):
            heat[k] = (heat[k - 1] + heat[k - 2] + heat[k - 2]) / 3
            
        # Step 3.  Randomly ignite new 'sparks' near the bottom
        if random.randint(0,100) < Sparking:
            
            # randomly pick the position of the spark
            y = random.randint(SparkingRangeStart,SparkingRangeEnd)
            # different fire effects 
            if FireEffect == 0:
                heat[y] = random.randint(int(heat[y]),255)
            elif FireEffect == 1:
                heat[y] = heat[y] + random.randint(160,255)
            else:
                heat[y] = random.randint(160,255)

        # Step 4.  Convert heat to LED colors
        for j in range(num_pixels):
            t192 = round((int(heat[j])/255.0)*191)

            # calculate ramp up from
            heatramp = t192 & 63 # 0..63  0x3f=63
            heatramp <<= 2 # scale up to 0..252
            # figure out which third of the spectrum we're in:
            if FireColor == 2: #green flame
                if t192 > 0x80: # hottest 128 = 0x80
                    pixels[j] = (int(heatramp),255, 255)
                elif t192 > 0x40: # middle 64 = 0x40
                    pixels[j] = (0, 255, int(heatramp))
                else: # coolest
                    pixels[j] = (0, int(heatramp), 0)
            elif FireColor == 1: #blue flame
                if t192 > 0x80: # hottest 128 = 0x80
                    pixels[j] = (255, int(heatramp), 255)
                elif t192 > 0x40: # middle 64 = 0x40
                    pixels[j] = (int(heatramp), 0, 255)
                else: # coolest
                    pixels[j] = (0, 0, int(heatramp))
            else: #FireColor == 0: #red flame
                if t192 > 0x80: # hottest 128 = 0x80
                    pixels[j] = (255, 255, int(heatramp))
                elif t192 > 0x40: # middle 64 = 0x40
                    pixels[j] = (255, int(heatramp), 0)
                else: # coolest
                    pixels[j] = (int(heatramp), 0, 0)
                

        pixels.show()
        time.sleep(SpeedDelay)

def meteorRain(red, green, blue, meteorSize, meteorTrailDecay, meteorRandomDecay, LoopCount, SpeedDelay): 
    for loop in range(LoopCount):
        pixels.fill((0,0,0))
        
        for i in range(num_pixels*2):
            # fade brightness all LEDs one step
            for j in range(num_pixels):
                if (not meteorRandomDecay) or (random.randint(0,10) > 5):
                    fadeToBlack(j, meteorTrailDecay )      
            
            # draw meteor
            for j in range(meteorSize):
                if ( i-j < num_pixels) and (i-j >= 0): 
                    pixels[i-j] = (red, green, blue)

            pixels.show()
            time.sleep(SpeedDelay)

def fadeToBlack(ledNo, fadeValue):
    #ctypes.c_uint32 oldColor = 0x00000000UL
    #ctypes.c_uint8 r = 0
    #ctypes.c_uint8 g = 0
    #ctypes.c_uint8 b = 0

    oldColor = pixels[ledNo]
#    r = (oldColor & 0x00ff0000) >> 16
#    g = (oldColor & 0x0000ff00) >> 8
#    b = (oldColor & 0x000000ff)
    #print(oldColor)
#    r = oldColor >> 16
#    g = (oldColor >> 8) & 0xff
#    b = oldColor & 0xff
    r = oldColor[0]
    g = oldColor[1]
    b = oldColor[2]

    if (r<=10):
        r = 0
    else:
        r = r - ( r * fadeValue / 256 )

    if (g<=10):
        g = 0
    else:
        g = g - ( g * fadeValue / 256 )

    if (b<=10):
        b = 0
    else:
        b = b - ( b * fadeValue / 256 )

    pixels[ledNo] = ( int(r), int(g), int(b) )


def BouncingBalls(red, green, blue, BallCount, LoopCount):
    
    ## setup 
    Gravity = -9.81
    StartHeight = 1

    Height = []
    for i in range(BallCount):
        Height.append(0)

    ImpactVelocityStart = math.sqrt( -2 * Gravity * StartHeight )

    ImpactVelocity = []
    for i in range(BallCount):
        ImpactVelocity.append(0)

    TimeSinceLastBounce = []
    for i in range(BallCount):
        TimeSinceLastBounce.append(0)

    Position = []
    for i in range(BallCount):
        Position.append(0)

    ClockTimeSinceLastBounce = []
    for i in range(BallCount):
        ClockTimeSinceLastBounce.append(0)
    
    Dampening = []
    for i in range(BallCount):
        Dampening.append(0)

    for i in range(BallCount):
        ClockTimeSinceLastBounce[i] = int(round(time.time() * 1000))

        Height[i] = StartHeight
        Position[i] = 0
        ImpactVelocity[i] = ImpactVelocityStart
        TimeSinceLastBounce[i] = 0
        Dampening[i] = 0.90 - float(i)/pow(BallCount,2)
    
    ## loop 
    for loop in range(LoopCount):
        for i in range(BallCount):
            TimeSinceLastBounce[i] =  int(round(time.time() * 1000)) - ClockTimeSinceLastBounce[i]
            Height[i] = 0.5 * Gravity * pow( TimeSinceLastBounce[i]/1000 , 2.0 ) + ImpactVelocity[i] * TimeSinceLastBounce[i]/1000
    
            if Height[i] < 0:                 
                Height[i] = 0
                ImpactVelocity[i] = Dampening[i] * ImpactVelocity[i]
                ClockTimeSinceLastBounce[i] = int(round(time.time() * 1000))
        
                if ImpactVelocity[i] < 0.01:
                    ImpactVelocity[i] = ImpactVelocityStart

            Position[i] = round( Height[i] * (num_pixels - 1) / StartHeight)
        
        for i in range(BallCount):
            pixels[Position[i]] = (red,green,blue)
        
        pixels.show()
        pixels.fill((0, 0, 0))
        


def BouncingColoredBalls(BallCount, colors, LoopCount):
    
    ## setup 
    Gravity = -9.81
    StartHeight = 1

    Height = []
    for i in range(BallCount):
        Height.append(0)

    ImpactVelocityStart = math.sqrt( -2 * Gravity * StartHeight )

    ImpactVelocity = []
    for i in range(BallCount):
        ImpactVelocity.append(0)

    TimeSinceLastBounce = []
    for i in range(BallCount):
        TimeSinceLastBounce.append(0)

    Position = []
    for i in range(BallCount):
        Position.append(0)

    ClockTimeSinceLastBounce = []
    for i in range(BallCount):
        ClockTimeSinceLastBounce.append(0)
    
    Dampening = []
    for i in range(BallCount):
        Dampening.append(0)

    for i in range(BallCount):
        ClockTimeSinceLastBounce[i] = int(round(time.time() * 1000))

        Height[i] = StartHeight
        Position[i] = 0
        ImpactVelocity[i] = ImpactVelocityStart
        TimeSinceLastBounce[i] = 0
        Dampening[i] = 0.90 - float(i)/pow(BallCount,2)
    
    ## loop 
    for loop in range(LoopCount):
        for i in range(BallCount):
            TimeSinceLastBounce[i] =  int(round(time.time() * 1000)) - ClockTimeSinceLastBounce[i]
            Height[i] = 0.5 * Gravity * pow( TimeSinceLastBounce[i]/1000 , 2.0 ) + ImpactVelocity[i] * TimeSinceLastBounce[i]/1000
    
            if Height[i] < 0:                 
                Height[i] = 0
                ImpactVelocity[i] = Dampening[i] * ImpactVelocity[i]
                ClockTimeSinceLastBounce[i] = int(round(time.time() * 1000))
        
                if ImpactVelocity[i] < 0.01:
                    ImpactVelocity[i] = ImpactVelocityStart

            Position[i] = round( Height[i] * (num_pixels - 1) / StartHeight)
        
        for i in range(BallCount):
            pixels[Position[i]] = (colors[i][0],colors[i][1],colors[i][2])
        
        pixels.show()
        pixels.fill((0, 0, 0))





def wheelBrightLevel(pos, bright):
    # Input a value 0 to 255 to get a color value.
    # The colours are a transition r - g - b - back to r.
    if pos < 0 or pos > 255:
        r = g = b = 0
    elif pos < 85:
        r = int(pos * 3)
        g = int(255 - pos*3)
        b = 0
    elif pos < 170:
        pos -= 85
        r = int(255 - pos*3)
        g = 0
        b = int(pos*3)
    else:
        pos -= 170
        r = 0
        g = int(pos*3)
        b = int(255 - pos*3)

    # bight level logic
    color = brightnessRGB(r, g, b, bright)
    r = color[0]
    g = color[1]
    b = color[2]

    return color if ORDER == neopixel.RGB or ORDER == neopixel.GRB else (r, g, b, 0)

def brightnessRGB(red, green, blue, bright):
    r = (bright/256.0)*red
    g = (bright/256.0)*green
    b = (bright/256.0)*blue
    return (int(r), int(g), int(b))

def hsv_to_rgb(h, s, v):
    if s == 0.0: 
        v*=255
        return (v, v, v)
    i = int(h*6.) # XXX assume int() truncates!
    f = (h*6.)-i
    p,q,t = int(255*(v*(1.-s))), int(255*(v*(1.-s*f))), int(255*(v*(1.-s*(1.-f))))
    v*=255
    i%=6
    if i == 0: 
        return (v, t, p)
    if i == 1: 
        return (q, v, p)
    if i == 2: 
        return (p, v, t)
    if i == 3: 
        return (p, q, v)
    if i == 4: 
        return (t, p, v)
    if i == 5: 
        return (v, p, q)

def random_burst(delayStart, delayEnd , LoopCount):
    for loop in range(LoopCount):
        randomIndex= random.randint(0, num_pixels-1)
        randomhue = random.randint(0, 255)
        randombright = random.randint(10, thisbright)
        
        # CHSV(rndhue, thissat, rndbright)
        #print(str(randomIndex) + " " + str(rndhue) + " " + str(rndbright))
        pixels[randomIndex] = wheelBrightLevel(randomhue, randombright)
        
        pixels.show()
        delay = random.randint(delayStart*1000, delayEnd*1000)/1000
        time.sleep(delay)

  
def rgb_propeller(LoopCount):
    thishue = 0
    thisbright = 255
    thissat = 255
    index= 0

    for loop in range(LoopCount):
        index = index + 1
        ghue = (thishue + 80) % 255
        bhue = (thishue + 160) % 255
        N3  = int(num_pixels/3)
        N6  = int(num_pixels/6)
        N12 = int(num_pixels/12)

        for i in range(N3):
            j0 = (index + i + num_pixels - N12) % num_pixels
            j1 = (j0+N3) % num_pixels
            j2 = (j1+N3) % num_pixels
            pixels[j0] = wheel(thishue)
            pixels[j1] = wheel(ghue)
            pixels[j2] = wheel(bhue)
            pixels.show()


def rainbow(delay, step, cycles):
    for j in range(255 * cycles):
        for i in range(num_pixels):
            # " // "  this divides and returns the integer value of the quotient. 
            # It dumps the digits after the decimal
            pixel_index = (step *i * 256 // num_pixels) + j
            pixels[i] = wheel(pixel_index & 255)
        pixels.show()
        time.sleep(delay)


def rainbow_loop(delay, step, cycles):
    index = 0
    thishue = 0

    for loop in range(cycles):
        index = index + 1
        thishue = thishue + step
        if index >= num_pixels:
            index = 0
        if thishue > 255:
            thishue = 0
        pixels[index] = wheel(thishue)
        pixels.show()
        time.sleep(delay)

def rainbow_fade(delay, cycles):
    thishue = 0
    for loop in range(cycles):
        thishue = thishue + 1
        if thishue > 255:
             thishue = 0

        # an other option would be to
        pixels.fill(wheel(thishue))
        pixels.show()
        time.sleep(delay)
#        for i in range(num_pixels):
#            print(wheel(thishue))
#            pixels[i] = wheel(thishue)
#            pixels.show()
#            time.sleep(delay)


def matrix(random_percent, delay, cycles):
    for loop in range(cycles):
        rand = random.randint(0, 100)

        # set first pixel
        if rand <= random_percent:
            pixels[0] = wheelBrightLevel(random.randint(0, 255), 255)
        else:
            pixels[0] = (0,0,0)
        
        # show pixels 
        pixels.show()
        time.sleep(delay)

        # rotate pixel positon
        for i in range(num_pixels - 1, 0, -1):
            pixels[i] = pixels[i-1]
        
        # there is an issue with first 2 pixels are same color 
        #pixels[0] = (0,0,0)
        #pixels.show()
        #time.sleep(delay)


 
def random_march(delay, cycles):
    for loop in range(cycles):

        for idex in range(num_pixels-1):
            ### previous logic that was not used...
            #if idex > 0: #if not last pixel
            #    r = idex - 1
            #else: # if last pixel
            #    r = num_pixels - 1

            # shift pixel value to previous pixel (pixel1 = value of pixel2,... and so on)
            pixels[idex] = pixels[idex+1]

        # change color of the last pixel
        pixels[num_pixels-1] = wheelBrightLevel(random.randint(0, 255), 255)

        # show pixel values
        pixels.show()
        time.sleep(delay)

### FixMe: this code does not work
### i think it also has a memory leak
### i have reached out to the author (via youtube comment)
#### next step would be to step though the code on an arduino 

def loop5(delay, cycles):
    for loop in range(cycles):
        #GB = pixels.getBrightness()
        boost = 0
        #  if( GB < 65): boost += 8
        #  if( GB < 33) boost += 8
        
        N = 2
        starttheta = 0
        starttheta = starttheta + ( 100 / N )
        starthue16 = 0
        starthue16 = starthue16 + (20 / N)
    
    
        hue16 = starthue16
        theta = starttheta
        for i in range(num_pixels):
            frac = (math.sin( theta) + 32768) / 256
            frac = frac + 32
            theta = theta + 3700
            hue16 = hue16 + 2000
            hue = hue16 / 256

            ramp = frac + boost
            if( ramp < 128):
                # fade toward black
                brightness = ramp * 2
                saturation = 255
            else:
                # desaturate toward white
                brightness = 255
                saturation = 255 - ((ramp - 128) * 2)
                # saturation = 255 - dim8_video( 255 - saturation);

            pixels[i] = hsv_to_rgb( hue, saturation, brightness)
        
        # show pixel values 
        pixels.show()
        time.sleep(delay)


def twinkle(delay, cycles ):
    for loop in range(cycles):
        huebase = 0
        
        #slowly rotate huebase
        if (random.randint(0, 4) == 0): #randomly, if 0  (0-3)
            huebase = huebase -1
        
        for whichPixel in range(num_pixels):
            hue = random.randint(0, 32) + huebase
            #saturation = 255;    #richest color
            brightness = random.randint(0, 255)
        
            pixels[whichPixel] = wheelBrightLevel(hue, brightness)
            # show pixel values 
            pixels.show()
            time.sleep(delay)

def candycane(delay, cycles):
    index = 0
    thisbright = 255
    for loop in range(cycles):
        index = index + 1
        N3  = int(num_pixels/3)
        N6  = int(num_pixels/6)
        N12 = int(num_pixels/12)
        for i in range(N6):
            j0 = int((index + i + num_pixels - N12) % num_pixels)
            j1 = int((j0+N6) % num_pixels)
            j2 = int((j1+N6) % num_pixels)
            j3 = int((j2+N6) % num_pixels)
            j4 = int((j3+N6) % num_pixels)
            j5 = int((j4+N6) % num_pixels)
            pixels[j0] = brightnessRGB(255, 255, 255, int(thisbright*.75))
            pixels[j1] = brightnessRGB(255, 0, 0, thisbright)
            pixels[j2] = brightnessRGB(255, 255, 255, int(thisbright*.75))
            pixels[j3] = brightnessRGB(255, 0, 0, thisbright)
            pixels[j4] = brightnessRGB(255, 255, 255, int(thisbright*.75))
            pixels[j5] = brightnessRGB(255, 0, 0, thisbright)

            # show pixel values 
            pixels.show()
            time.sleep(delay)


def random_levels( NUM_LEVELS, delay, cycles ):
    for loop in range(cycles):

        level = random.randint(0, NUM_LEVELS)
        if (NUM_LEVELS == level):
            level = 0
        light_level_random(level, 1)
        pixels.show()
        time.sleep(delay)

#fixme: array is hardcoded for 350 lights. needs to be more dynamic.
def light_level_random( level,  clearall ):
    #this only works if you have 350 lights
    #levels = (58, 108, 149, 187, 224, 264, 292, 309, 321, 327, 336, 348)
    
    #this works for 50 lights
    levels = (11, 20, 27, 34, 39, 43, 47, 50)
    #levels = (20, 34, 43, 50)

    if (clearall):
        pixels.fill((0, 0, 0)) # clear all
        pixels.show()
    
    startPxl = 0
    if (level == 0):
        startPxl = 0
    else:
        startPxl = levels[level-1]
    
    for i in range(startPxl, levels[level]):
        pixels[i] = wheelBrightLevel(random.randint(0, 255), random.randint(50, 255))



def drain(level, delay):
    interrupt = False
    for pancakeLevel in range(level):

        # only needed if you ouput to a small display 
        # updateControlVars() 
        
        if (interrupt):
            return
        
        for level in range(pancakeLevel, -1, -1):
            # only needed if you ouput to a small display 
            # updateControlVars()  
            
            if (interrupt) :
                return

            clear_level(level)
            if (level >= 1) :
                light_level_random(level-1, 0)

            # show pixel values 
            pixels.show()
            time.sleep(delay)


def pancake(NUM_LEVELS, delay):
    interrupt = False
    for pancakeLevel in range(NUM_LEVELS):
        # only needed if you ouput to a small display 
        # updateControlVars()  

        if (interrupt):
            return
        
        for level in range(NUM_LEVELS-1, pancakeLevel-1, -1):
            # only needed if you ouput to a small display 
            # updateControlVars()   

            if (interrupt):
                return

            if (level < NUM_LEVELS-1):
                clear_level(level+1)
                
            light_level_random(level, 0)

            # show pixel values 
            pixels.show()
            time.sleep(delay)




def clear_level( level):
    levels = (11, 20, 27, 34, 39, 43, 47, 50)
    startPxl = 0
    if (level == 0):
        startPxl = 0
    else:
        startPxl = levels[level-1]
    for i in range(startPxl, levels[level]):
        pixels[i] = (0,0,0)  #CRGB::Black;










while True:
    random.seed(num_pixels)


    # make all pixels Red
    # fill(red, green, blue)
    pixels.fill((255, 0, 0)) # red
    pixels.show()
    time.sleep(wait_time)

    # make all pixels Green
    # fill(red, green, blue)
    pixels.fill((0, 255, 0))
    pixels.show()
    time.sleep(wait_time)

    # make all pixels Blue
    # fill(red, green, blue)
    pixels.fill((0, 0, 255))
    pixels.show()
    time.sleep(wait_time)

    # shows 2 color every other pixel (red, green)
    # colorAll2Color((red1, green1, blue1), (red2, green2, blue2)) 
    colorAll2Color((255, 0, 0), (0, 255, 0)) 
    time.sleep(wait_time * 5)

    # shows 2 color every other pixel (purple, orange)
    # colorAll2Color((red1, green1, blue1), (red2, green2, blue2)) 
    colorAll2Color((128,0,128), (235,97,35) )
    time.sleep(wait_time * 5)

# makes the strand of pixels show random_levels
    # pancake(level, delay)
    #pixels.fill((0, 0, 0))
    #time.sleep(wait_time)
    #pancake(8, 0.5)
    #time.sleep(wait_time)

    # makes the strand of pixels show drain
    # drain(level, delay)
    #drain(8, 0.5)
    #time.sleep(wait_time)

    # makes the strand of pixels show random_levels
    # random_levels( NUM_LEVELS, delay, cycles )
    #random_levels(12, 0, 500)
    #random_levels(8, 0.1, 500)
    #time.sleep(wait_time)

    # makes the strand of pixels show candycane
    # candycane(delay, cycles)
    candycane(0, 10) 
    time.sleep(wait_time)

    # makes the strand of pixels show twinkle
    # twinkle(delay, cycles)
    twinkle(0.005, 100) 
    time.sleep(wait_time)

    # makes the strand of pixels show loop5
    # loop5( delay, cycles)
    #loop5(0.25, 500) 
    #time.sleep(wait_time)

    ### FixMe: think random_march and matrix are the same
    # makes the strand of pixels show random_march
    # random_march( delay, cycles)
    random_march(0.25, 256) 
    time.sleep(wait_time)

    # makes the strand of pixels show matrix
    # matrix(random_percent, delay, cycles)
    matrix(10, 0.25, 500) 
    time.sleep(wait_time)

    # makes the strand of pixels show rainbow_fade
    # rainbow_fade(delay, cycles):
    rainbow_fade(.02, 256) 
    time.sleep(wait_time)

    # makes the strand of pixels show rainbow_loop
    # rainbow_loop(delay, step, cycles):
    pixels.fill((0, 0, 0))
    pixels.show()
    time.sleep(wait_time*2)
    rainbow_loop(0.01, 10, 1000) 
    time.sleep(wait_time)

    # makes the strand of pixels show rainbow
    # rainbow(delay, step, cycles):
    pixels.fill((255, 255, 0))
    pixels.show()
    time.sleep(wait_time*2)
    rainbow(0.01, 10, 2) 
    time.sleep(wait_time)

    # makes the strand of pixels show random_burst
    # rgb_propeller(LoopCount)
    pixels.fill((0, 0, 0))
    rgb_propeller(1000)
    time.sleep(wait_time)

    # makes the strand of pixels show random_burst
    # random_burst(delayStart, delayEnd , LoopCount)
    pixels.fill((0, 0, 0))
    random_burst(0.005, .2, 100)
    time.sleep(wait_time)




    # makes the strand of pixels show Fire
    # Fire(CoolingRangeStart, CoolingRangeEnd, Sparking, SparkingRangeStart, SparkingRangeEnd, SpeedDelay, FireColor, FireEffect, LoopCount)
    #CoolingRangeStart = 0-255
    #CoolingRangeEnd = 0-255
    #Sparking = 0-100  (0= 0% sparkes randomly added, 100= 100% sparks randomly added)
    #SparkingRangeStart = 0-255 
    #SparkingRangeEnd = 0-255
    #FireColor = 0-2 (0=red, 1=blue , 2=green)
    #FireEffect = 0-2
    # Fire(CoolingRangeStart, CoolingRangeEnd, Sparking, SparkingRangeStart, SparkingRangeEnd, SpeedDelay, FireColor, FireEffect, LoopCount)
    #FireCustom(0, 8, 40, 0, 20, 0.00, 0, 2, 100) # red fire
    #time.sleep(wait_time)


    # makes the strand of pixels show Fire
    # Fire(Cooling, Sparking, SpeedDelay, LoopCount)
    Fire(5, 250,0, 200)
    time.sleep(wait_time)
    
    # makes the strand of pixels show 
    # meteorRain(red, green, blue, meteorSize, meteorTrailDecay, meteorRandomDecay, LoopCount, SpeedDelay)
    meteorRain(255, 255, 255, 10, 64, True, 1, 0)
    time.sleep(wait_time)

    # makes the strand of pixels show theaterChaseRainbow
    # theaterChaseRainbow(SpeedDelay)
    theaterChaseRainbow(0)
    time.sleep(wait_time)

    # makes the strand of pixels show theaterChase
    # theaterChase(red, green, blue, cycles, SpeedDelay)
    theaterChase(255,0,0, 20, 0)
    time.sleep(wait_time)

    # makes the strand of pixels show colorWipe (green)
    # colorWipe(red, green, blue, SpeedDelay)
    colorWipe(0,255,0, 0)

    # makes the strand of pixels show RunningLights (red)
    # RunningLights(red, green, blue, WaveDelay)
    RunningLights(255,0,0, 0)

    # makes the strand of pixels show SnowSparkle (random)
    # SnowSparkle(red, green, blue, Count, SparkleDelay, SpeedDelay)
    # SnowSparkle(16, 16, 16, 100, 0.020, random.randint(100,1000)/1000)
    SnowSparkle(16, 16, 16, 100, 0, 0)

    # makes the strand of pixels show Sparkle (white)
    # Sparkle(red, green, blue, Count, SpeedDelay)
    Sparkle(255, 255, 255, 100, 0)

    # makes the strand of pixels show TwinkleRandom
    # TwinkleRandom( Count, SpeedDelay, OnlyOne) 
    TwinkleRandom(20, 0, False)

    # makes the strand of pixels show Twinkle
    # Twinkle(red, green, blue, Count, SpeedDelay, OnlyOne)
    Twinkle(255, 0, 0, 10, 0, False)

    # fade in/out a single color (red / green / blue / white)
    # FadeInOut(red, green, blue, delay)
    FadeInOut(255, 0, 0, 0)
    FadeInOut(0, 255, 0, 0)
    FadeInOut(0, 0, 255, 0)
    FadeInOut(255, 255, 255, 0)

    # loops red green blue
    # RGBLoop(delay)
    RGBLoop(0.01)
    time.sleep(wait_time)

    # rainbow cycle
    # rainbow cycle with 1ms delay per step, 5 cycles
    # rainbow_cycle(delay, cycles) 
    rainbow_cycle(0.001, 5) 
    time.sleep(wait_time)

