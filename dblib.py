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
            return self.cur.fetchone()
        else:
            print("getLastRouteId: Not connected to DB")


    def setNewRouteId(self):
        if self.connected:
            lastUsedRouteId = getLastRouteId()
            newRouteId = lastUsedRouteId + 1
            query = "UPDATE routeId SET route = " + newRouteId + " WHERE route = " + lastUsedRouteId
            self.cur.execute(query)
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
            return False


    def getRoute(self, routeID):
        if self.connected:
            query = "SELECT * FROM routes WHERE RouteID ='" + routeID
            self.cur.execute(query)
            return self.cur.fetchone() # TODO: return the whole query
        else:
            print("getRoute: Not connected to DB")


    def insertCoordinate(self, date, latitude, longitude):
        if self.connected:
            query = "SELECT RouteID,Date FROM routes WHERE RouteID = " + routeID " AND Date = " + date 
            self.cur.execute(query)
            if self.cur.rowcount == 0:
                routeID = self.getLastRouteId()
                if isNewRoute:
                    routeID = self.setNewRouteId(routeID)
                query = "INSERT INTO routes" + " (`RouteID`, `Date`, `Latitude`, `Longitude`) VALUES ('" + routeID + "','" + date + "','" + latitude + "','" + longitude + "')"
                self.cur.execute(query)
                self.con.commit()
            else:
                print("Primary Key Violation: RouteID " + routeId + " already inserted with Date = " + date)


def saveCoordinate(date, latitude, longitude):
    lib = DBlib()
    lib.insertCoordinate(date, latitude, longitude)


def startNewRoute():
    lib = DBlib()
    lib.setNewRouteId()


