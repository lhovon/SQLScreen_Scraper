"""Handler class for PostgreSQL database access.

Default DB Config file is ./config/db.ini
"""

import psycopg2
import psycopg2.extras

from configparser import SafeConfigParser

# Config file to use
configfile = "./config/db.ini"


class DbHandler:
    def __init__(self):
        super()

    def config(self, filename=configfile):
        """Load the PostgreSQL configuration file."""

        section = "postgresql"
        parser = SafeConfigParser()
        parser.read(filename)

        db = {}
        if parser.has_section(section):
            params = parser.items(section)
            for param in params:
                db[param[0]] = param[1]
        else:
            raise Exception(f"Section {section} not found in the {filename} file")

        return db

    def create_connection(self):
        """Create a database connection to a PostgreSQL database."""
        conn = None

        try:
            params = self.config()
            conn = psycopg2.connect(**params)

            cur = conn.cursor()
            cur.execute("SELECT version()")
            db_version = cur.fetchone()[0].split(",")[0]
            print(f"Connected to {db_version}")
            cur.close()

        except (Exception, psycopg2.DatabaseError) as error:
            raise Exception(error)

        return conn

    def execute(self, conn, sql_statement):
        """Execute a given SQL statement using the given connection."""
        result = None
        try:
            c = conn.cursor()
            c.execute(sql_statement)
            result = c.fetchall()
            c.close()
        except Exception as e:
            print(e)
        finally:
            return result

    def execute_self_contained(self, sql_statement):
        """Create a single-use connection to execute the given SQL statement."""
        conn = self.create_connection()

        result = None
        try:
            cursor = conn.cursor()
            cursor.execute(sql_statement)
            result = cursor.fetchall()
        except Exception as e:
            print(e)
        finally:
            cursor.close()
            conn.commit()
            return result

    def delete_quote(self, conn, symbol):
        result = None
        try:
            c = conn.cursor()
            sql = """DELETE FROM quote WHERE symbol=%s;"""
            c.execute(sql, (symbol,))
            result = c.fetchone()
            c.close()

        except (Exception, psycopg2.Error) as e:
            print(e)
        finally:
            conn.commit()
            return result

    def insert_quote(self, conn, quote_info, timestamp):
        """Insert a TMX quote object in the db with all financial information."""
        result = None

        try:
            c = conn.cursor()

            sql = """INSERT INTO quote (symbol, name, price, priceChange, percentChange, exchangeName, exShortName, exchangeCode, marketPlace, 
                    sector, industry, volume, openPrice, dayHigh, dayLow, MarketCap, MarketCapAllClasses, peRatio, prevClose, dividendFrequency, 
                    dividendYield, dividendAmount, dividendCurrency, beta, eps, exDividendDate, shortDescription, longDescription, website, email,
                    phoneNumber, fullAddress, employees, shareOutStanding, totalDebtToEquity, totalSharesOutStanding, sharesESCROW, vwap, 
                    dividendPayDate, weeks52high, weeks52low, alpha, averageVolume10D, averageVolume30D, averageVolume50D, priceToBook, 
                    priceToCashFlow, returnOnEquity, returnOnAssets, day21MovingAvg, day50MovingAvg, day200MovingAvg, dividend3Years, 
                    dividend5Years, datatype, typename, suspended, lastupdate)  
                    VALUES 
                    (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
                    ON CONFLICT (symbol) DO UPDATE SET 
                    (name, price, priceChange, percentChange, exchangeName, exShortName, exchangeCode, marketPlace, 
                    sector, industry, volume, openPrice, dayHigh, dayLow, MarketCap, MarketCapAllClasses, peRatio, prevClose, dividendFrequency, 
                    dividendYield, dividendAmount, dividendCurrency, beta, eps, exDividendDate, shortDescription, longDescription, website, email,
                    phoneNumber, fullAddress, employees, shareOutStanding, totalDebtToEquity, totalSharesOutStanding, sharesESCROW, vwap, 
                    dividendPayDate, weeks52high, weeks52low, alpha, averageVolume10D, averageVolume30D, averageVolume50D, priceToBook, 
                    priceToCashFlow, returnOnEquity, returnOnAssets, day21MovingAvg, day50MovingAvg, day200MovingAvg, dividend3Years, 
                    dividend5Years, datatype, typename, suspended, lastupdate)  
                    = 
                    (EXCLUDED.name, EXCLUDED.price, EXCLUDED.priceChange, EXCLUDED.percentChange, EXCLUDED.exchangeName, EXCLUDED.exShortName, 
                    EXCLUDED.exchangeCode, EXCLUDED.marketPlace, EXCLUDED.sector, EXCLUDED.industry, EXCLUDED.volume, EXCLUDED.openPrice, 
                    EXCLUDED.dayHigh, EXCLUDED.dayLow, EXCLUDED.MarketCap, EXCLUDED.MarketCapAllClasses, EXCLUDED.peRatio, EXCLUDED.prevClose, 
                    EXCLUDED.dividendFrequency, EXCLUDED.dividendYield, EXCLUDED.dividendAmount, EXCLUDED.dividendCurrency, EXCLUDED.beta, 
                    EXCLUDED.eps, EXCLUDED.exDividendDate, EXCLUDED.shortDescription, EXCLUDED.longDescription, EXCLUDED.website, EXCLUDED.email, 
                    EXCLUDED.phoneNumber, EXCLUDED.fullAddress, EXCLUDED.employees, EXCLUDED.shareOutStanding, EXCLUDED.totalDebtToEquity, 
                    EXCLUDED.totalSharesOutStanding, EXCLUDED.sharesESCROW, EXCLUDED.vwap, EXCLUDED.dividendPayDate, EXCLUDED.weeks52high, 
                    EXCLUDED.weeks52low, EXCLUDED.alpha, EXCLUDED.averageVolume10D, EXCLUDED.averageVolume30D, EXCLUDED.averageVolume50D, 
                    EXCLUDED.priceToBook, EXCLUDED.priceToCashFlow, EXCLUDED.returnOnEquity, EXCLUDED.returnOnAssets, EXCLUDED.day21MovingAvg, 
                    EXCLUDED.day50MovingAvg, EXCLUDED.day200MovingAvg, EXCLUDED.dividend3Years, EXCLUDED.dividend5Years, EXCLUDED.datatype, 
                    EXCLUDED.typename, EXCLUDED.suspended, EXCLUDED.lastupdate)
                    
                    RETURNING symbol;"""

            c.execute(sql, quote_info + (timestamp,))
            result = c.fetchone()
            c.close()

        except (Exception, psycopg2.Error) as e:
            print(e)
        finally:
            conn.commit()
            return result
