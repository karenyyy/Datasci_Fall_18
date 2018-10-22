import sqlite3
import pandas as pd

conn = sqlite3.connect('airline.db')
c = conn.cursor()

try:
    c.execute('''
    CREATE TABLE `airline data`
    (
      City1                                     CHAR(3) NOT NULL,
      City2                                     CHAR(3) NOT NULL,
      `Average Fare (AvgFare)`                  DOUBLE  NOT NULL,
      Distance                                  INT     NOT NULL,
      `Average weekly passengers (AvgWklyPsgr)` DOUBLE  NOT NULL,
      `market leading airline (LdAirline)`      CHAR(2) NOT NULL,
      `market share (LdShare)`                  DOUBLE  NOT NULL,
      `Average fare (LdAvgFare)`                DOUBLE  NOT NULL,
      `Low price airline (LowAirline)`          CHAR(2) NOT NULL,
      `market share (LowShare)`                 DOUBLE  NOT NULL,
      `price (LowFare)`                         DOUBLE  NOT NULL
    );
    ''')
except Exception as e:
    print(str(e))


df = pd.read_sql("SELECT * FROM `airline data` WHERE City1 LIKE 'C%'", conn)
print(df.head())
