import pymysql
from geopy import distance

########################
# DB: routeDb
#
#Tables:
#
#   Table: routes
#   Colums:
#    *  RouteID
#    *  Date
#       Latitude
#       Longitude
#       Altitude
#       Speed
#       Segment
#       DistanceFromPreviousSegment
#
#   Table: segmentDetailed
#   Columns:
#    *  Segment
#    *  RouteID
#
#   Table: routeId
#   Columns
#    *  route
#########################


class dblib:

    def __init__(self):
        self.connectToSql()


    def getLastRouteId(self):
        if self.connected:
            query = "SELECT route FROM routeId"
            self.cur.execute(query)
            return self.cur.fetchone()[0]
        else:
            print("getLastRouteId: Not connected to DB")


    def getLastSegmentId(self, routeId):
        if self.connected:
            query = "SELECT Segment from segmentDetailed WHERE RouteID = \'" + str(routeId) + "\'"
            self.cur.execute(query)
            return self.cur.fetchone()[0]
        else:
            print("getLastSegmentId: Not connected to DB")


    def setSegmentId(self, segmentId, routeId):
        if self.connected:
            query = "INSERT INTO segmentDetailed (Segment,RouteID) VALUES (\'" + str(segmentId) + "\',\'" + str(routeId) + "\')"
            self.cur.execute(query)
            self.con.commit()
        else:
            print("setSegmentId: Not connected to DB")


    def updateSegmentId(self, routeId):
        if self.connected:
             lastSegment = self.getLastSegmentId(routeId)
             newSegment = int(lastSegment) + 1
             query = "UPDATE segmentDetailed SET Segment = \'" + str(newSegment) + "\' WHERE RouteID = \'" + str(routeId) + "\'"
             self.cur.execute(query)
             self.con.commit()
             return newSegment

        else:
            print("updateSegmentId: Not connected to DB")


    def setNewRoute(self):
        if self.connected:
            lastUsedRouteId = self.getLastRouteId()
            newRouteId = int(lastUsedRouteId) + 1
            print("New routeId: ", newRouteId)
            query = "UPDATE routeId SET route = \'" + str(newRouteId) + "\' WHERE route = \'" + str(lastUsedRouteId) + "\'"
            self.cur.execute(query)
            self.con.commit()
            self.setSegmentId(0, newRouteId)
        else:
            print("setNewRouteId: Not connected to DB")


    def connectToSql(self):
        try:
            self.con = pymysql.connect(host="localhost", user='gpsuser', passwd='##gps123', db="routeDb")
            self.cur = self.con.cursor()
            self.connected = True
            return True
        except:
            self.connected = False
            print("Failed to connect to DB")
            return False


    def getRoute(self, routeID):
        if self.connected:
            query = "SELECT * FROM routes WHERE RouteID = \'" + str(routeID) + "\'"
            self.cur.execute(query)
            return self.cur.fetchall()
        else:
            print("getRoute: Not connected to DB")


    def getlatlngalt(self, routeID):
        if self.connected: # Return in the format Lon, Lat, Alt
            query = "SELECT Longitude, Latitude, Altitude FROM routes WHERE RouteID = \'" + str(routeID) + "\'"
            self.cur.execute(query)
            return self.cur.fetchall()
        else:
            print("getRoute: Not connected to DB")


    def findRouteId(self, date):
        if self.connected:
            query = "SELECT distinct(RouteID) from routes WHERE Date like \'%%" + str(date) + "%%\'"
            self.cur.execute(query)
            routeId = self.cur.fetchall()[0][0]
            print("findRouteId: returned items: " + str(routeId))
            return routeId
        else:
            print("findRouteId: Not connected to DB")


    def getDistanceFromPrevious(self, routeId, lat, lng):
        if self.connected:
            segment = self.getLastSegmentId(routeId)
            if segment == 0:
                return 0
            else:
                query = "SELECT Longitude, Latitude FROM routes WHERE RouteID = \'" + str(routeId) + "\' AND Segment = \'" + str(segment) + "\'"
                self.cur.execute(query)
                previous = self.cur.fetchone()
                actual = (lng, lat)
                return round(distance.distance(previous, actual).km, 3)

    def insertCoordinate(self, date, latitude, longitude, speed):
        if self.connected:
            routeID = self.getLastRouteId()
            query = "SELECT RouteID,Date FROM routes WHERE RouteID = \'" + str(routeID) + "\' AND Date = \'" + str(date) + "\'"
            self.cur.execute(query)
            if self.cur.rowcount == 0:
                distanceFromPreviousSegment  = self.getDistanceFromPrevious(routeID, latitude, longitude)
                segmentID = self.updateSegmentId(routeID)
                query = "INSERT INTO routes (RouteID, Date, Latitude, Longitude, Speed, Segment, DistanceFromPreviousSegment) VALUES (\'" + \
                    str(routeID) +  "\',\'" + str(date) + "\',\'" + str(latitude) + "\',\'" + str(longitude) + "\',\'" + str(speed) + "\',\'" + \
                    str(segmentID) + "\',\'" + str(distanceFromPreviousSegment) + "\')"
                self.cur.execute(query)
                self.con.commit()
            else:
                print("RouteID " + str(routeID) + " already inserted with Date = " + str(date))


    def insertAltitude(self, date, altitude):
        if self.connected:
            routeID = self.getLastRouteId()
            query = "SELECT * FROM routes WHERE RouteID = \'" + str(routeID) + "\' AND Date like \'%%" + str(date) + "%%\'"
            self.cur.execute(query)
            if self.cur.rowcount == 1:
               query = "UPDATE routes SET Altitude = \'" + str(altitude) + "\' WHERE RouteID = \'" + str(routeID) + "\' AND Date like \'%%" + \
                        str(date) + "%%\'"
               self.cur.execute(query)
               self.con.commit()


def saveCoordinate(date, latitude, longitude, speed):
    lib = dblib()
    lib.insertCoordinate(date, latitude, longitude, speed)


def startNewRoute():
    lib = dblib()
    return  lib.setNewRoute()


def saveAltitude(date, altitude):
    lib = dblib()
    lib.insertAltitude(date, altitude)


def getCoordinates(date):
    lib = dblib()
    routeId = lib.findRouteId(date)
    print("RouteID found = " + str(routeId))
    return lib.getlatlngalt(routeId)


