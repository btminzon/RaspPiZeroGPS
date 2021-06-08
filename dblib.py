import pymysql
from geopy import distance


########################
# DB: routeDb
#
# Tables:
#
#   Table: routes
#   Columns:
#    *  RouteID
#    *  Date
#       Latitude
#       Longitude
#       Altitude
#       Speed
#       Segment
#       DistanceFromPreviousSegment
#       Satellites
#
#   Table: segmentDetailed
#   Columns:
#    *  Segment
#    *  RouteID
#       DistanceRun
#
#   Table: routeId
#   Columns
#    *  route
#########################


class Dblib:

    def __init__(self):
        self.connectToSql()

    def connectToSql(self):
        try:
            self.con = pymysql.connect(host="localhost", user='gpsuser', passwd='##gps123', db="routeDb")
            self.cur = self.con.cursor()
            self.connected = True
            return True
        except Exception as e:
            self.connected = False
            print("Failed to connect to DB: ".format(e))
            return False

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

    def getRoute(self, routeID):
        if self.connected:
            query = "SELECT * FROM routes WHERE RouteID = \'" + str(routeID) + "\'"
            self.cur.execute(query)
            return self.cur.fetchall()
        else:
            print("getRoute: Not connected to DB")

    def getlatlngalt(self, routeID):
        if self.connected:  # Return in the format Lon, Lat, Alt
            query = "SELECT Longitude, Latitude, Altitude FROM routes WHERE RouteID = \'" + str(routeID) + "\'"
            self.cur.execute(query)
            return self.cur.fetchall()
        else:
            print("getRoute: Not connected to DB")

    def getdistancefromprevioussegment(self, routeId):
        if self.connected:
            query = "SELECT DistanceFromPreviousSegment FROM routes WHERE RouteID = \'" + str(routeId) + "\'"
            self.cur.execute(query)
            return self.cur.fetchall()
        else:
            print("getdistancefromprevioussegment: Not connected to DB")

    def getLastCoordinate(self, routeId, segment):
        if self.connected:
            query = "SELECT Longitude, Latitude FROM routes WHERE RouteID = \'" + str(
                routeId) + "\' AND Segment = \'" + str(segment) + "\'"
            self.cur.execute(query)
            return self.cur.fetchall()
        else:
            print("getLastCoordinate: Not connected to DB")

    def getDistance(self, routeId):
        if self.connected:
            query = "SELECT distanceRun from segmentDetailed where RouteID = \'" + str(routeId) + "\'"
            self.cur.execute(query)
            return self.cur.fetchone()[0]
        else:
            print("getDistance: Not connected to DB")

    def setSegmentId(self, segmentId, routeId):
        if self.connected:
            query = "INSERT INTO segmentDetailed (Segment,RouteID) VALUES (\'" + str(segmentId) + "\',\'" + str(
                routeId) + "\')"
            self.cur.execute(query)
            self.con.commit()
        else:
            print("setSegmentId: Not connected to DB")

    def setNewRoute(self, newRouteId, lastRouteId):
        if self.connected:
            query = "UPDATE routeId SET route = \'" + str(newRouteId) + "\' WHERE route = \'" + str(
                lastRouteId) + "\'"
            self.cur.execute(query)
            self.con.commit()
        else:
            print("setNewRouteId: Not connected to DB")

    def updateSegmentId(self, routeId, newSegment):
        if self.connected:
            query = "UPDATE segmentDetailed SET Segment = \'" + str(newSegment) + "\' WHERE RouteID = \'" + str(
                routeId) + "\'"
            self.cur.execute(query)
            self.con.commit()
        else:
            print("updateSegmentId: Not connected to DB")

    def updateDistance(self, routeId, dist):
        if self.connected:
            query = "UPDATE segmentDetailed SET DistanceRun = \'" + "{:.4f}".format(dist) + "\' WHERE RouteID = \'" + str(
                routeId) + "\'"
            self.cur.execute(query)
            self.con.commit()
        else:
            print("updateDistance: Not connected to DB")

    def findRouteId(self, date):
        if self.connected:
            query = "SELECT distinct(RouteID) from routes WHERE Date like \'%%" + str(date) + "%%\'"
            self.cur.execute(query)
            routeId = self.cur.fetchall()[0][0]
            return routeId
        else:
            print("findRouteId: Not connected to DB")

    def insertCoordinate(self, routeId, date, latitude, longitude, speed, segment, dist):
        if self.connected:
            query = "SELECT RouteID,Date FROM routes WHERE RouteID = \'" + str(routeId) + "\' AND Date = \'" + str(
                date) + "\'"
            self.cur.execute(query)
            if self.cur.rowcount == 0:
                query = "INSERT INTO routes (RouteID, Date, Latitude, Longitude, Speed, Segment, \
                DistanceFromPreviousSegment) VALUES (\'" + str(routeId) + "\',\'" + str(date) + \
                        "\',\'" + str(latitude) + "\',\'" + str(longitude) + "\',\'" + str(speed) + \
                        "\',\'" + str(segment) + "\',\'" + str(dist) + "\')"
                self.cur.execute(query)
                self.con.commit()
            else:
                print("RouteID " + str(routeId) + " already inserted with Date = " + str(date))
        else:
            print("insertCoordinate: Not connected to DB")

    def insertAltitude(self, routeId, date, altitude):
        if self.connected:
            query = "SELECT * FROM routes WHERE RouteID = \'" + str(routeId) + "\' AND Date like \'%%" + str(
                date) + "%%\'"
            self.cur.execute(query)
            if self.cur.rowcount == 1:
                query = "UPDATE routes SET Altitude = \'" + str(altitude) + "\' WHERE RouteID = \'" + str(
                    routeId) + "\' AND Date like \'%%" + \
                        str(date) + "%%\'"
                self.cur.execute(query)
                self.con.commit()
            else:
                print("insertAltitude: there is no Coordinate inserted to update altitude")
        else:
            print("insertAltitude: Not connected to DB")

    def insertSatellites(self, routeId, date, satellites):
        if self.connected:
            query = "SELECT * FROM routes WHERE RouteID = \'" + str(routeId) + "\' AND Date like \'%%" + str(
                date) + "%%\'"
            self.cur.execute(query)
            if self.cur.rowcount == 1:
                query = "UPDATE routes SET Satellites = \'" + str(satellites) + "\' WHERE RouteID = \'" + str(
                    routeId) + "\' AND Date like \'%%" + \
                        str(date) + "%%\'"
                self.cur.execute(query)
                self.con.commit()
            else:
                print("insertSatellites: there is no Coordinate inserted to update satellites")
        else:
            print("insertSatellites: Not connected to DB")


def startNewRoute():
    lib = Dblib()
    lastUsedRouteId = lib.getLastRouteId()
    newRouteId = int(lastUsedRouteId) + 1
    print("New routeId: ", newRouteId)
    lib.setNewRoute(newRouteId, lastUsedRouteId)
    lib.setSegmentId(0, newRouteId)
    lib.updateDistance(newRouteId, float("{:.4f}".format(0)))


def saveCoordinate(date, latitude, longitude, speed):
    lib = Dblib()
    routeId = lib.getLastRouteId()
    lastSegment = lib.getLastSegmentId(routeId)
    newSegment = int(lastSegment) + 1
    lib.updateSegmentId(routeId, newSegment)
    if newSegment > 1:
        dist = getdistanceFromPrevious(routeId, latitude, longitude)
    else:
        dist = 0.0000
    lib.insertCoordinate(routeId, date, latitude, longitude, speed, newSegment, dist)


def saveAltitude(date, altitude, satellites):
    lib = Dblib()
    routeID = lib.getLastRouteId()
    lib.insertAltitude(routeID, date, altitude)
    lib.insertSatellites(routeID, date, satellites)


def saveDistance(latitude, longitude):
    lib = Dblib()
    routeId = lib.getLastRouteId()
    currentDist = float(lib.getDistance(routeId))
    newDist = getdistanceFromPrevious(routeId, latitude, longitude)
    dist = newDist + currentDist
    lib.updateDistance(routeId, dist)


def updateDistance(routeId, dist):
    lib = Dblib()
    lib.updateDistance(routeId, dist)


def getCoordinates(date):
    lib = Dblib()
    routeId = lib.findRouteId(date)
    return lib.getlatlngalt(routeId)


def getdistancebetweensegments(routeId):
    lib = Dblib()
    return lib.getdistancefromprevioussegment(routeId)


def getdistanceFromPrevious(routeId, latitude, longitude):
    lib = Dblib()
    segment = lib.getLastSegmentId(routeId)
    last = lib.getLastCoordinate(routeId, segment-1)
    actual = (longitude, latitude)
    newDistance = round(distance.distance(last, actual).km, 4)
    return newDistance


def getsegments(routeId):
    lib = Dblib()
    return lib.getLastSegmentId(routeId)
