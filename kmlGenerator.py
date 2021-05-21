import sys
import dblib
import simplekml


def createKml(date):
    kml = simplekml.Kml()
    coordinates = dblib.getCoordinates(date)
    kml.newlinestring(name='Route', description=date, coords=coordinates)
    filename = 'Route_' + date + '.kml'
    kml.save(filename)
    print("File " + filename + " created succesfully!")


if __name__ == '__main__':
   print("Arg size: "+ str(len(sys.argv)))
   print("0: " + str(sys.argv[0]) + " 1: " + str(sys.argv[1]))
   date = sys.argv[1]
   createKml(date)


