import pandas as pd
from decimal import Decimal
import datetime
import dateutil.parser
from app.models import symbols,prices as prc,clients,BuySell
import pandas_ta as ta
import numpy as np
from .prepareSymbol import prepareSymbol
class technical(object):
    
    count=None
    BUYPoint = None 
    SELLPoint = None
    prepare=None
    
    def __init__(self, prepare:prepareSymbol):
        self.columns= ['open','high','low','adjclose','value','volume','count','close']
        self.count=0
        self.BUYPoint=[]
        self.SELLPoint=[]
        self.prepare= prepare
        self.smaSignal()
        self.macdSignal()
        self.rsiSignal()
        
    def smaSignal(self):
        # try:
        if(len(self.prepare.indexes)>=5):
            Diffrnces = []
            Diffrnces.append( self.prepare.indexes[len(self.prepare.indexes)-1]) #TODAY
            Diffrnces.append( self.prepare.indexes[len(self.prepare.indexes)-2]) 
            Diffrnces.append( self.prepare.indexes[len(self.prepare.indexes)-3]) 
            Diffrnces.append( self.prepare.indexes[len(self.prepare.indexes)-4]) 
            Diffrnces.append( self.prepare.indexes[len(self.prepare.indexes)-5]) 
            
        
            #[indicator_bb.size-2] 
            samShort = ta.sma(self.prepare.df["close"], length=10)
            samLong = ta.sma(self.prepare.df["close"], length=20)
            
            if (samShort.loc[Diffrnces[0]] - samLong.loc[Diffrnces[0]] >0 and samShort.loc[Diffrnces[1]] - samLong.loc[Diffrnces[1]] >=0 and samShort.loc[Diffrnces[2]] - samLong.loc[Diffrnces[2]] <0 and samShort.loc[Diffrnces[3]] - samLong.loc[Diffrnces[3]]<0 and samShort.loc[Diffrnces[4]] - samLong.loc[Diffrnces[4]]<0 ) :
                self.BUYPoint.append('SMA')
            elif (samShort.loc[Diffrnces[0]] - samLong.loc[Diffrnces[0]] <=0 and samShort.loc[Diffrnces[1]] - samLong.loc[Diffrnces[1]] >0 ) : 
                self.SELLPoint.append('SMA')
            return True
        # except:
        #     return False
    def macdSignal(self):
        # try:
        if(len(self.prepare.indexes)>=5):
            Diffrnces = []
            Diffrnces.append( self.prepare.indexes[len(self.prepare.indexes)-1]) #TODAY
            Diffrnces.append( self.prepare.indexes[len(self.prepare.indexes)-2]) 
            Diffrnces.append( self.prepare.indexes[len(self.prepare.indexes)-3]) 
            Diffrnces.append( self.prepare.indexes[len(self.prepare.indexes)-4]) 
            Diffrnces.append( self.prepare.indexes[len(self.prepare.indexes)-5]) 
            
            #[indicator_bb.size-2] 
            macdObj = ta.macd(self.prepare.df["close"], fast=12,slow=26,length=9)
            if (macdObj.loc[Diffrnces[0]].MACD_12_26_9 - macdObj.loc[Diffrnces[0]].MACDs_12_26_9 >0 and macdObj.loc[Diffrnces[1]].MACD_12_26_9 - macdObj.loc[Diffrnces[1]].MACDs_12_26_9 >=0 and macdObj.loc[Diffrnces[2]].MACD_12_26_9 - macdObj.loc[Diffrnces[2]].MACDs_12_26_9 <0 and macdObj.loc[Diffrnces[3]].MACD_12_26_9 - macdObj.loc[Diffrnces[3]].MACDs_12_26_9<0 and macdObj.loc[Diffrnces[4]].MACD_12_26_9 - macdObj.loc[Diffrnces[4]].MACDs_12_26_9<0 ) :
                self.BUYPoint.append('MACD')
            elif (macdObj.loc[Diffrnces[0]].MACD_12_26_9 - macdObj.loc[Diffrnces[0]].MACDs_12_26_9 <=0 and macdObj.loc[Diffrnces[1]].MACD_12_26_9 - macdObj.loc[Diffrnces[1]].MACDs_12_26_9 >0 ) : 
                self.SELLPoint.append('MACD')
            return True
        # except:
        #     return False    
    def rsiSignal(self):
        indicator_rsi = ta.rsi(close=self.prepare.df["close"],length=14)
        # try:
        if(len(self.prepare.indexes)>=5):
            Diffrnces = []
            Diffrnces.append( self.prepare.indexes[len(self.prepare.indexes)-1]) #TODAY
            Diffrnces.append( self.prepare.indexes[len(self.prepare.indexes)-2]) 
            if (indicator_rsi.loc[Diffrnces[0]]>=30 and indicator_rsi.loc[Diffrnces[1]]<=30):
                self.BUYPoint.append('RSI')
            elif (indicator_rsi.loc[Diffrnces[1]]>=70 and indicator_rsi.loc[Diffrnces[0]]<=70 ):
                self.SELLPoint.append('RSI')
            return True
        # except :
        #     return False
    def cciSignal(self):
        indicator_cci = ta.cci(high=self.prepare.df["high"],low=self.prepare.df["low"],close=self.prepare.df["close"])
        # try:
        if(len(self.prepare.indexes)>=5):
            Diffrnces = []
            Diffrnces.append( self.prepare.indexes[len(self.prepare.indexes)-1]) #TODAY
            Diffrnces.append( self.prepare.indexes[len(self.prepare.indexes)-2]) 
            if (indicator_cci.loc[Diffrnces[0]]>=30 and indicator_cci.loc[Diffrnces[1]]<=30):
                self.BUYPoint.append('CCI')
            elif (indicator_cci.loc[Diffrnces[1]]>=70 and indicator_cci.loc[Diffrnces[0]]<=70 ):
                self.SELLPoint.append('CCI')
            return True
        # except :
        #     return False
    def check(self):
        self.smaSignal()
        self.macdSignal()
        self.rsiSignal()
        #self.cciSignal()
    def findInIndexes(self,obj):
        for index in self.prepare.indexes:
            if index==obj:
                return True
        return False
    
    
    
        

    
