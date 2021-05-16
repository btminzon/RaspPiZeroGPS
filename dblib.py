import pymysql

########################
#Tables:
#   routes
#   Colums:
#    *  RouteID
#    *  Date
#       Latitude
#       Longitude
#
#   routeId
#   Columns
#    *  route
#########################


class dblib:

    def __init__(self):
        self.connectToSql()


    def getLastRouteId(self):
        if self.connected:
            query = "SELECT * FROM routeId"
            self.cur.execute(query)
            return self.cur.fetchone()[0]
        else:
            print("getLastRouteId: Not connected to DB")


    def setNewRouteId(self):
        if self.connected:
            lastUsedRouteId = self.getLastRouteId()
            newRouteId = int(lastUsedRouteId) + 1
            print("New routeId: ", newRouteId)
            query = "UPDATE routeId SET route = \'" + str(newRouteId) + "\' WHERE route = \'" + str(lastUsedRouteId) + "\'"
            print("setNewRouteId: query: ", query)
            self.cur.execute(query)
            self.con.commit()
        else:
            print("setNewRouteId: Not connected to DB")


    def connectToSql(self):
        try:
            self.con = pymysql.connect(host="localhost", user='gpsuser', passwd='##gps123', db="routeDb")
            self.cur = self.con.cursor()
            self.connected = True
            print("Connected to db")
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


    def insertCoordinate(self, date, latitude, longitude):
        if self.connected:
            routeID = self.getLastRouteId()
            query = "SELECT RouteID,Date FROM routes WHERE RouteID = \'" + str(routeID) + "\' AND Date = \'" + str(date) + "\'"
            self.cur.execute(query)
            if self.cur.rowcount == 0:
                query = "INSERT INTO routes (RouteID, Date, Latitude, Longitude) VALUES (\'" + str(routeID) +  "\',\'" + str(date) +  "\',\'" + str(latitude) + "\',\'" + str(longitude) + "\')"
                self.cur.execute(query)
                self.con.commit()
            else:
                print("RouteID " + str(routeID) + " already inserted with Date = " + str(date))


def saveCoordinate(date, latitude, longitude):
    lib = dblib()
    lib.insertCoordinate(date, latitude, longitude)


def startNewRoute():
    lib = dblib()
    return  lib.setNewRouteId()



