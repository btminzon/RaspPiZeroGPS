import dblib

if __name__ == '__main__':
    dblib.startNewRoute()
    dblib.saveCoordinate('2021-06-07 00:14:28', '45.27147', '-75.88351', 1.23)
    dblib.saveCoordinate('2021-06-07 00:14:29', '45.27145', '-75.88350', 1.24)
    dblib.saveDistance('45.27145', '-75.88350')
