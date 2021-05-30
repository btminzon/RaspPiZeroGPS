import dblib
import sys

def calculatedistance(routeId):
    dist = dblib.getdistancebetweensegments(routeId)
    sum = 0.0
    for i in dist:
        sum = sum + float(i[0])
    print("Total Distance is: " + str("{:.3f}".format(sum)) + " Km")


if __name__ == '__main__':
    calculatedistance(sys.argv[1])