#!/usr/bin/env python

import Adafruit_MCP3008
import socket
import math
import time

VCC = 3.3
RDIV = 10000

CH_X = 0
CH_Y = 1
CH_K = 2

X_MIN = 0.0
X_MID = 1.62
X_MAX = 3.3
Y_MIN = 0.0
Y_MID = 1.59
Y_MAX = 3.3
K_OFF = 1.65
K_ON  = 0.0

SCALE = 6

CLK  = 22
MISO = 23
MOSI = 24
CS   = 25

mcp = Adafruit_MCP3008.MCP3008(clk=CLK, cs=CS, miso=MISO, mosi=MOSI)

try:
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
except socket.error, msg:
    print 'Failed to create socket. Error code: ' + str(msg[0]) + ' , Error message : ' + msg[1]
    sys.exit();
    

while True:
    xADC = mcp.read_adc(CH_X)
    x = round((xADC * VCC) / 1023, 2)
    if x < X_MID:
        xp = (X_MID - x) / -X_MID
    elif x == X_MID:
        xp = 0
    else:
        xp = min((x - X_MID) / X_MID, 1)
    print("x: " + str(xp))
    
    yADC = mcp.read_adc(CH_Y)
    y = round((yADC * VCC) / 1023, 2)
    if y < Y_MID:
        yp = (Y_MID - y) / -Y_MID
    elif y == Y_MID:
        yp = 0
    else:
        yp = min((y - Y_MID) / Y_MID, 1)
    print("y: " + str(yp))
    
    kADC = mcp.read_adc(CH_K)
    k = (kADC * VCC) / 1023
    if k == K_ON:
        kp = 1
    else:
        kp = 0
    print("k: " + str(kp))
    
    try:
        s.sendto("b:" + 
                 str(xp) + "," + 
                 str(yp) + "," + 
                 str(kp),
                 ("192.168.1.7", 8080))
    except socket.error:
        print 'Send failed'
        # sys.exit()
    
    time.sleep(0.1)
