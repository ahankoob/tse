from app.models import symbols,prices,clients,BuySell
import pandas as pd
from decimal import Decimal
import datetime
import dateutil.parser
import pandas_ta as ta
import numpy as np
import pytse_client as tse
class symbolPack(object):
    symbol:symbols = None
    symbolData = None
    def __init__(self,symbol:symbols):
        self.symbol = symbol
        self.symbolData = None
    def get_history_from_tse(self):
        self.symbolData = tse.Ticker(self.symbol.symbolName)
        prices.objects.filter(symbol_id=self.symbol.pk).delete()
        for index,row in self.symbolData.history.iterrows() :
            symbol_price = prices(symbol_id=self.symbol.pk,priceDate=dateutil.parser.parse(str(index)+' +0430'), open=Decimal( row[0]),hight=Decimal(row[1]),low=Decimal(row[2]),adjClose=Decimal(row[3]),value=Decimal(row[4]), volume=Decimal(row[5]), count=Decimal(row[6]), close=Decimal(row[7]))
            symbol_price.pk= None;
            symbol_price.save()
        return True