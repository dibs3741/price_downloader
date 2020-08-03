import os
import click 
import yfinance as yf
from datetime import date 
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy import Column, String, Date, Integer, Numeric 
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.exc import NoResultFound

load_dotenv()

db_string = "postgres://postgres:postgres@localhost:5755/postgres"
db = create_engine(db_string)
Session = sessionmaker(db)
session = Session()
base = declarative_base()

class cSecurityPrices(base): 
    __tablename__ = 'security_prices'
    id = Column(Integer, primary_key=True) 
    securityid = Column(Integer) 
    asofdate = Column(Date) 
    price = Column(Numeric(20,2)) 

@click.command() 
@click.option('--datefrom',
        type=click.DateTime(formats=["%Y-%m-%d"]),
        default=str(date.today()), 
        help="date from"
        )
@click.option('--dateto',
        type=click.DateTime(formats=["%Y-%m-%d"]),
        default=str(date.today()), 
        help="date to"
        )
def test(datefrom, dateto): 
    #print(datefrom.date()) 
    #print(os.getenv('ABC_KEY')) 
    #print(data) 
    result_set = db.execute("SELECT * FROM securities")
    for r in result_set:
        securityid = r[0] 
        securityname = r[1] 
        df_data = yf.download(securityname, start=datefrom, end=dateto)
        for index, row in df_data.iterrows():
            try: 
                oSecurityPrices = session.query(cSecurityPrices).filter(
                    cSecurityPrices.asofdate == index, 
                    cSecurityPrices.securityid == securityid 
                ).one() 
                session.delete(oSecurityPrices) 
            except NoResultFound: 
                pass 
            oSecurityPrices = cSecurityPrices() 
            oSecurityPrices.securityid = securityid 
            oSecurityPrices.asofdate = index 
            oSecurityPrices.price = row['Close'] 
            session.add(oSecurityPrices) 
            session.commit() 

if __name__ == '__main__':
    test()
