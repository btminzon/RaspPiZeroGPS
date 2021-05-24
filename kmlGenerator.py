import sys
import dblib
import simplekml


def createKml(date):
    kml = simplekml.Kml()
    coordinates = dblib.getCoordinates(date)
    kml.newlinestring(name='Route', description=date, coords=coordinates)
    filename = 'Route_' + date + '.kml'
    kml.save(filename)
    print("File " + filename + " created successfully!")


if __name__ == '__main__':
    date = sys.argv[1]
    createKml(date)
