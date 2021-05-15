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
    def __init__(self, dbFolder = None):
        self.connectToSql()

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
        return None

    def insertCoordinate(self, routeID, date, latitude, longitude):
        if self.connected:
            query = "SELECT RouteID,Date FROM routes WHERE RouteID = " + routeID " AND Date = " + date 
            self.cur.execute(query)
            if self.cur.rowcount == 0:
                query = "INSERT INTO routes" + " (`RouteID`, `Date`, `Latitude`, `Longitude`) VALUES ('" + routeID + "','" + date + "','" + latitude + "','" + longitude + "')"
				self.cur.execute(query)
				self.con.commit()
			else:
				print("Primary Key Violation: RouteID " + routeId + " already inserted with Date = " + date)


def saveCoordinate(routeID, date, latitude, longitude):
    lib = DBlib()
    lib.insertCoordinate(routeID, date, latitude, longitude)
