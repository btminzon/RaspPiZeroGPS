import sys
import dblib
import simplekml
from string import Template


in_file = open("/home/pi/gpsProject/RaspPiZeroGPS/maps_template.html", "rt")  # Read html template
template = in_file.read()
in_file.close()


def createKml(date):
    kml = simplekml.Kml()
    coordinates = dblib.getCoordinates(date)
    kml.newlinestring(name='Route', description=date, coords=coordinates)
    filename = 'Route_' + date + '.kml'
    kml.save(filename)
    print("File " + filename + " created successfully!")


def generateHtml(date):
    global template
    lnglat = dblib.getCoordinates(date)
    output = Template(template).substitute(lnglat=lnglat)
    out_file = open("/var/www/html/gps/index.html", "wt")
    out_file.write(output)
    out_file.close()
    print("Map created successfully!")


if __name__ == '__main__':
    date = sys.argv[1]
    if sys.argv[2] == 'kml':
        createKml(date)
    elif sys.argv[2] == 'map':
        generateHtml(date)
    else:
        print("Option " + sys.argv[2] + " invalid")
