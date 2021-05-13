#!/usr/bin/env python

import serial
import time
import os
import sys
from string import Template

if os.geteuid() != 0: # Source: https://gist.github.com/davejamesmiller/1965559
    os.execvp("sudo", ["sudo"] + sys.argv)

ser = serial.Serial('/dev/ttyACM0',9600,timeout=1) # Open Serial port

counter = 0 # Used to generate a html page every 10s

in_file = open("maps_template.html", "rt") # Read html template
template = in_file.read()
in_file.close()

def generateHtml(latlng):
    global template
    output = Template(template).substitute(lat=latlng[0], lng=latlng[1], timefix=latlng[2])
    out_file = open("/var/www/html/gps/index.html", "wt")
    out_file.write(output)
    out_file.close()

def readString():
    while 1:
        while ser.read().decode("utf-8") != '$': # Wait for the begging of the string
            pass # Do nothing
        line = ser.readline().decode("utf-8") # Read the entire string
        return line

def getTime(string,format,returnFormat):
    return time.strftime(returnFormat, time.strptime(string, format)) # Convert date and time to a nice printable format

def getLatLng(latString,latDir,lngString,lngDir,fixTimeString):
    lat = latString[:2].lstrip('0') + "." + "%.4s" % str(float(latString[2:])*1.0/60.0).lstrip("0.")
    lng = lngString[:3].lstrip('0') + "." + "%.4s" % str(float(lngString[3:])*1.0/60.0).lstrip("0.")

    if latDir == 'S':
       lat = '-' + lat

    if lngDir == 'W':
       lng = '-' + lng

    return lat,lng,fixTimeString

def printRMC(lines):
    global counter
    print("========================================RMC========================================")
    fixTime = ''
    fixTime = ''.join(getTime(lines[1]+lines[9], "%H%M%S.%W%d%m%y", "%a %b %d %H:%M:%S %Y")) # added a %W to ignore 00  str
    print("Fix taken at:" + fixTime, "UTC")
    print("Status (A=OK,V=KO):", lines[2])
    latlng = getLatLng(lines[3],lines[4],lines[5],lines[6],fixTime)
    print("Lat,Long: ", latlng[0].replace('-',''), lines[4], ", ", latlng[1].replace('-',''),lines[6], sep='')
    print("Speed (knots):", lines[7])
    print("Track angle (deg):", lines[8])
    print("Magnetic variation: ", lines[10], end='')
    if len(lines) == 13: # The returned string will be either 12 or 13 - it will return 13 if NMEA standard used is above 2.3
        print(lines[11])
        print("Mode (A=Autonomous, D=Differential, E=Estimated, N=Data not valid):", lines[12].partition("*")[0])
    else:
        print(lines[11].partition("*")[0])

    counter += 1
    if counter == 10: # Generate HTML every 10s
        counter = 0
        generateHtml(latlng)

def printGGA(lines):
    print("========================================GGA========================================")

    fixTime = ''
    fixTime = ''.join(getTime(lines[1], "%H%M%S.%f", "%H:%M:%S"))
    print("Fix taken at:", fixTime, "UTC")
    latlng = getLatLng(lines[2],lines[3],lines[4],lines[5],fixTime)
    print("Lat,Long: ", latlng[0].replace('-',''), lines[3], ", ", latlng[1].replace('-',''), lines[5], sep='')
    print("Fix quality (0 = invalid, 1 = fix, 2..8):", lines[6])
    print("Satellites:", lines[7].lstrip("0"))
    print("Horizontal dilution:", lines[8])
    print("Altitude: ", lines[9], lines[10],sep="")
    print("Height of geoid: ", lines[11],lines[12],sep="")
    print("Time in seconds since last DGPS update:", lines[13])
    print("DGPS station ID number:", lines[14].partition("*")[0])

def printGSA(lines):
    print("========================================GSA========================================")

    print("Selection of 2D or 3D fix (A=Auto,M=Manual):", lines[1])
    print("3D fix (1=No fix,2=2D fix, 3=3D fix):", lines[2])
    print("PRNs of satellites used for fix:", end='')
    for i in range(0, 12):
        prn = lines[3+i].lstrip("0")
        if prn:
            print(" ", prn, end='')
    print("\nPDOP", lines[15])
    print("HDOP", lines[16])
    print("VDOP", lines[17].partition("*")[0])

def printGSV(lines):
    if lines[2] == '1': # First sentence
        print("========================================GSV========================================")
    else:
        print("===================================================================================")

    print("Number of sentences:", lines[1])
    print("Sentence:", lines[2])
    print("Satellites in view:", lines[3].lstrip("0"))
    for i in range(0, int(len(lines)/4)-1):
        print("Satellite PRN:", lines[4+i*4].lstrip("0"))
        print("Elevation (deg):", lines[5+i*4].lstrip("0"))
        print("Azimuth (deg):", lines[6+i*4].lstrip("0"))
        print("SNR (higher is better):", lines[7+i*4].partition("*")[0])

def printGLL(lines):
    print("========================================GLL========================================")

    fixTime = ''

    fixTime = ''.join(getTime(lines[5], "%H%M%S.%f", "%H:%M:%S"))
    latlng = getLatLng(lines[1],lines[2],lines[3],lines[4],fixTime)
    print("Lat,Long: ", latlng[0].replace('-',''), lines[2], ", ", latlng[1].replace('-',''), lines[4], sep='')
    print("Fix taken at:", fixTime, "UTC")
    print("Status (A=OK,V=KO):", lines[6])
    if lines[7].partition("*")[0]: # Extra field since NMEA standard 2.3
        print("Mode (A=Autonomous, D=Differential, E=Estimated, N=Data not valid):", lines[7].partition("*")[0])

def printVTG(lines):
    print("========================================VTG========================================")

    print("True Track made good (deg):", lines[1], lines[2])
    print("Magnetic track made good (deg):", lines[3], lines[4])
    print("Ground speed (knots):", lines[5], lines[6])
    print("Ground speed (km/h):", lines[7], lines[8].partition("*")[0])
    if lines[9].partition("*")[0]: # Extra field since NMEA standard 2.3
        print("Mode (A=Autonomous, D=Differential, E=Estimated, N=Data not valid):", lines[9].partition("*")[0])

def checksum(line):
    checkString = line.partition("*")
    checksum = 0
    for c in checkString[0]:
        checksum ^= ord(c)

    try: # Just to make sure
        inputChecksum = int(checkString[2].rstrip(), 16);
    except:
        print("Error in string")
        return False

    if checksum == inputChecksum:
        return True
    else:
        print("=====================================================================================")
        print("===================================Checksum error!===================================")
        print("=====================================================================================")
        print(hex(checksum), "!=", hex(inputChecksum))
        return False

if __name__ == '__main__':
    while 1:
        line = readString()
        lines = line.split(",")
        if checksum(line):
            if lines[0][2:] == "RMC":
                printRMC(lines)
                pass
            elif lines[0][2:] == "GGA":
                printGGA(lines)
                pass
            elif lines[0][2:] == "GSA":
                pass
            elif lines[0][2:] == "GSV":
                pass
            elif lines[0][2:] == "GLL":
                printGLL(lines)
                pass
            elif lines[0][2:] == "VTG":
                printVTG(lines)
                pass
            else:
                print("\n\nUnknown type:", lines[0], "\n\n")
