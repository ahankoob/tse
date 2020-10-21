from app.models import symbols,prices,clients,BuySell
import pandas as pd
from decimal import Decimal
import datetime
import dateutil.parser
import pandas_ta as ta
import numpy as np
import pytse_client as tse
from multiprocessing.pool import ThreadPool as Pool
import time
class symbolPack(object):
    symbol:symbols = None
    symbolData = None
    def __init__(self,symbol:symbols):
        self.symbol = symbol
        self.symbolData = None
        
                
    def get_history_from_pytse(self):
        import csv
        pool_size = 4  # your "parallelness"
        
        self.symbolData = tse.Ticker(self.symbol.symbolName)
        symbol_client_types = self.symbolData.client_types

        pool = Pool(pool_size)
        for index,row in self.symbolData.history.iterrows() :
            pool.apply_async(self.get_history_from_tse_worker, (index,row))
        pool.close()
        pool.join()
        
        pool1 = Pool(pool_size)
        for index,row in symbol_client_types.iterrows() :
            pool1.apply_async(self.get_history_from_tse_worker_clients, (index,row))
        pool1.close()
        pool1.join()
        return True
    def get_from_csv(self):
        returnStr=""
        try:
            try:
                self.get_history_from_csv()
                returnStr+="History OK "
            except:
                time.sleep(1) 
                self.get_history_from_csv()
                returnStr+="History OK "
        except:
            returnStr+="History Erro "
        try:
            try:
                self.get_clients_from_csv()
                returnStr+="Clients OK "
            except:
                time.sleep(1) 
                self.get_clients_from_csv()
                returnStr+="Clients OK "
        except:
            returnStr+="Clients Error "
        return returnStr            

    def get_history_from_csv(self):
        import csv
        import os
        BASE_DIR = os.path.abspath(
            os.path.join(os.path.dirname(__file__), "../..")
        )
        #try:
        df=None

        try:    
            df = pd.read_csv(BASE_DIR+"\\tickers_data\\"+self.to_arabic(self.symbol.symbolName)+".csv") 
        except:
            df = pd.read_csv(BASE_DIR+"\\tickers_data\\"+self.symbol.symbolName+".csv")     
        for index,row in df.iterrows() :
            symbol_price = prices(symbol_id=self.symbol,priceDate=dateutil.parser.parse(row['date']+' 12:30:00 +0430'), open=Decimal( row['open']),hight=Decimal(row['high']),low=Decimal(row['low']),adjClose=Decimal(row['adjClose']),value=Decimal(row['value']), volume=Decimal(row['volume']), count=Decimal(row['count']), close=Decimal(row['close']))
            symbol_price.pk= None
            symbol_price.save()
        return True
        #eturn False
    def get_clients_from_csv(self):
        import os
        BASE_DIR = os.path.abspath(
            os.path.join(os.path.dirname(__file__), "../..")
        )
        #try:
        df=None
        try:    
            df = pd.read_csv(BASE_DIR+"\\client_types_data\\"+self.to_arabic(self.symbol.symbolName)+".csv") 
        except:
            df = pd.read_csv(BASE_DIR+"\\client_types_data\\"+self.symbol.symbolName+".csv") 
        for index,row in df.iterrows() :
            symbol_clients = clients(symbol_id=self.symbol,date=dateutil.parser.parse(row['date']+' 12:30:00 +0430'), haghighiBuyVolume=Decimal( row["individual_buy_vol"]),hoghooghiBuyVolume=Decimal(row['corporate_buy_vol']),haghighiSellVolume=Decimal(row['individual_sell_vol']),hoghooghiSellVolume=Decimal(row['corporate_sell_value']),haghighiBuyCount=Decimal(row['individual_buy_count']), hoghooghiBuyCount=Decimal(row['corporate_buy_count']), haghighiSellCount=Decimal(row['individual_sell_count']), hoghooghiSellCount=Decimal(row['corporate_sell_count']))
            symbol_clients.pk= None
            symbol_clients.save()
        
        return True
        #eturn False
    def checkActive(self):
        import os

        try:
            BASE_DIR = os.path.abspath(
                os.path.join(os.path.dirname(__file__), "../..")
            )
            df = pd.read_csv(BASE_DIR+"\\tickers_data\\"+self.symbol.symbolName+".csv") 
        except:
            self.symbol.symbolActive - False
            self.symbol.save()

    def to_arabic(self,string: str):
        return string.replace('ک', 'ك').replace('ی', 'ي').replace('ی','ي').strip()  
       