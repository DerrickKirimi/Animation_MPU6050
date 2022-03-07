#from turtle import title
from vpython import *
import math 
import serial

def rotationInfo(ringPos, arrowOffset, angleName):
    """
    Returns Yaw, pitch and roll direction indication  arrows with rings, labled with angle name

    arrowOffset: arrow offset from ring centre
    angleName: one of yaw, pitch and roll

    """
    
    #ring
    rotRing = ring(pos = ringPos, axis = ringPos, radius = arrowOffset.mag,
                    thickness = 0.04)
    #arrow
    ringArrow = arrow (pos = ringPos+arrowOffset, axis = cross(ringPos, arrowOffset),
                    radius = 0.2, thickness = 0.06, length = 0.3, shaftwidth = 0.05)
    #angleName  
    ringText = text(pos = ringPos*(1+(0.4/ringPos.mag)), text = angleName,
                    color = color.white, height = 0.2, depth = 0.05,
                        align = 'center', up = vector(0,0,-1))

    




def setScene() :
    scene.range = 5
    scene.forward=vector(-0.8, -1.2, -0.8)
    scene.background = color.cyan
    scene.width=1200
    scene.height=1080
    title = text(pos=vec(0,3,0),text = 'MPU-6050', align = 'centre', color = color.blue,
    height = 0.4, depth = 0.2)

    return title

def make3DRotatingObj():
    #The MPU-6050 module
    mpu=box(length=4, width = 2, height = .2, opacity = .3, pos = vector(0,0,0),
    color = color.blue )
    
    #The markings on MPU6050 module
    Yaxis = arrow(length=2, shaftwidth = 0.1, axis = mpu.axis, color = color.white)
    Xaxis = arrow(length=0.7, shaftwidth = 0.1, axis = vector(0,0,1), color = color.white)

    XaxisLabel = text(pos=vec(-0.6,0.1,0.7),text = 'Xaxis', align = 'centre', color = color.white,
    height = 0.2, depth = 0.05, up = vector(0,0,-1))
    
    YaxisLabel = text(pos=vec(1, 0.1, -0.1),text = 'Yaxis', align = 'centre', color = color.white,
    height = 0.2, depth = 0.05, up = vector(0,0,-1))

    TopsdLabel = text(pos=vec(-1.2,0.1,-0.2),text = 'Top Side', align = 'centre', color = color.white,
    height = 0.2, depth = 0.05, up = vector(0,0,-1))

    #Yaw, pitch and roll direction indication  arrows with rings
    rotInfoY = rotationInfo(vector(2.4, 0, 0),vector(0, 0, 0.02), 'roll')
    rotInfoX = rotationInfo(vector(0, 0.1, 0.3),vector(0.2,0,0), 'pitch')
    rotInfoZ = rotationInfo(vector(0,-1,0),vector(-0.2,0,0), 'yaw')

    return compound([mpu, Xaxis,Yaxis, XaxisLabel, YaxisLabel, TopsdLabel,
    rotInfoY,rotInfoX, rotInfoZ])

def rodriguesRotation(v,k, angle):
    return v*cos(angle)+cross(k,v)*sin(angle)

title = setScene()
angles = label(pos=vec(-2.5, 2, 1),text = "yaw: 0\npitch: 0\nroll: 0" ,
         align = 'centre', color = color.black,
    height = 30, depth = 0)
rotatingObjects = make3DRotatingObj()
  
ESPSerial = serial.Serial('dev/ttyUSB0',115200)  

while (True):
    try:
        while (ESPSerial.inWaiting()==0):
            pass
        dataPacket = ESPSerial.readline()
        dataPacket = str(dataPacket, 'utf_8')
        splitPacket = dataPacket.split("\t")
        yaw = float(splitPacket[0])
        pitch = float(splitPacket[1])
        roll = float(splitPacket[2])

        #update display based on rotation
        rate(50) #Display update rate

        #display angles in degrees
        angles.text = f'yaw: {round(yaw)}\npitch: {round(pitch)}\nroll: {round(roll)}'

        #Convert to radians for python usage
        yaw = math.radians(yaw)
        pitch = math.radians(pitch)
        roll = math.radians(roll)

        #stipulating at zero yaw, pitch and roll x and y are:
        x = vector(0,0,1)
        y = vector(1,0,0)
 
        #x In pitch rotation X doesn't vary. Rotate Y
        y = rodriguesRotation(y,x, pitch)

        #y is invariant under roll. Rotate X
        x = rodriguesRotation(x, y , roll)

        #getting up vector from x and y vector
        rotatingObjects.axis = y
        rotatingObjects.up = cross(x,y)

    except:
            pass
