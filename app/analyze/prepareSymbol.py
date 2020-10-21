import pandas as pd
from decimal import Decimal
import datetime
import dateutil.parser
from app.models import symbols,prices,clients,BuySell
import pandas_ta as ta
import numpy as np
class prepareSymbol(object):
    symbol=None
    prices=None
    df = None
    columns= None
    indexes=None
    prices=None
    def __init__(self, symbol):
        self.symbol = symbol
        self.columns= ['open','high','low','adjclose','value','volume','count','close']
        self.indexes=[]
        self.df=[]
        self.prices = []
        self.dataRead()
        
    def dataRead(self):
        date_min = datetime.datetime.combine(datetime.datetime.now() - datetime.timedelta(days=90), datetime.time.min)
        date_max = datetime.datetime.combine(datetime.date.today(), datetime.time.max)
        self.prices = prices.objects.filter(symbol_id=self.symbol,priceDate__range=(date_min, date_max))
        for item in self.prices:
            if self.findInIndexes(self.dateFormat(item.priceDate))==False:
                self.indexes.append(self.dateFormat(item.priceDate))
        
        self.df = pd.DataFrame(columns=self.columns, index=self.indexes)
        for dateIndex in self.indexes:  
            today_min = self.dateToObjMin(dateIndex)
            today_max = self.dateToObjMax(dateIndex)
            self.prices = prices.objects.filter(symbol_id=self.symbol,priceDate__range=(today_min, today_max)).last()
            self.df.loc[dateIndex] = pd.Series({'open':self.prices.open, 'high':self.prices.hight, 'low':self.prices.low, 'adjclose':self.prices.adjClose,'value':self.prices.value, 'volume':self.prices.volume, 'count':self.prices.count, 'close':self.prices.close})  
    def dateFormat(self,myDate:datetime):
        return "{:04}-{:02}-{:02}".format(myDate.year,myDate.month,myDate.day)
    def dateToObjMin(self,myDate:str):
        return dateutil.parser.parse(myDate+" 00:00:00")
    def dateToObjMax(self,myDate:str):
        return dateutil.parser.parse(myDate+" 23:59:00")
    def findInIndexes(self,obj):
        for index in self.indexes:
            if index==obj:
                return True
        return False