import numpy as np
from decimal import Decimal
import datetime
import dateutil.parser
from app.models import symbols,prices as prc,clients,BuySell
import pandas as pd
from .prepareSymbol import prepareSymbol

class supports(object):
    supports=None
    ressists = None
    prepare=None
    BUYPoint = None 
    SELLPoint = None
    def __init__(self,prepare:prepareSymbol):
        self.prepare = prepare
        self.supports = []
        self.ressists = []
        self.BUYPoint=[]
        self.SELLPoint=[]
        self.calculate()
        self.BuySignal()
        self.SellSignal()
    def supportRessists(self):
        
        for index in  range(len(self.prepare.indexes)):
            if index<3:
                continue
            if self.supportFinder(index):
                try:
                    self.supports.append(self.prepare.df.loc[self.prepare.indexes[index]]['close'])
                except:
                    a=''
            if self.ressistFinder(index):
                try:
                    self.ressists.append(self.prepare.df.loc[self.prepare.indexes[index]]['close'])
                except:
                    a=''
    def supportFinder(self,index):
        try:
            if (#self.prepare.df.loc[self.prepare.indexes[index-3]]['close']>self.prepare.df.loc[self.prepare.indexes[index-2]]['close'] and 
                #self.prepare.df.loc[self.prepare.indexes[index-2]]['close']>self.prepare.df.loc[self.prepare.indexes[index-1]]['close'] and 
                self.prepare.df.loc[self.prepare.indexes[index-1]]['close']>self.prepare.df.loc[self.prepare.indexes[index]]['close'] and
                self.prepare.df.loc[self.prepare.indexes[index]]['close']<self.prepare.df.loc[self.prepare.indexes[index+1]]['close'] #and
                #self.prepare.df.loc[self.prepare.indexes[index+1]]['close']>self.prepare.df.loc[self.prepare.indexes[index+2]]['close'] and
                #self.prepare.df.loc[self.prepare.indexes[index+1]]['close']>self.prepare.df.loc[self.prepare.indexes[index+2]]['close']
            ):
                return True
        except:
            return False
    def ressistFinder(self,index):
        try:
            if (#self.prepare.df.loc[self.prepare.indexes[index-3]]['close']>self.prepare.df.loc[self.prepare.indexes[index-2]]['close'] and 
                #self.prepare.df.loc[self.prepare.indexes[index-2]]['close']>self.prepare.df.loc[self.prepare.indexes[index-1]]['close'] and 
                self.prepare.df.loc[self.prepare.indexes[index-1]]['close']<self.prepare.df.loc[self.prepare.indexes[index]]['close'] and
                self.prepare.df.loc[self.prepare.indexes[index]]['close']>self.prepare.df.loc[self.prepare.indexes[index+1]]['close'] #and
                #self.prepare.df.loc[self.prepare.indexes[index+1]]['close']>self.prepare.df.loc[self.prepare.indexes[index+2]]['close'] and
                #self.prepare.df.loc[self.prepare.indexes[index+1]]['close']>self.prepare.df.loc[self.prepare.indexes[index+2]]['close']
            ):
                return True
        except:
            return False
    def calculate(self):
        self.supportRessists()
        SupportsArr = np.array(self.supports)
        RessistsArr = np.array(self.ressists)

        SupportsArr = np.sort(SupportsArr)
        RessistsArr = np.sort(RessistsArr)

        self.supports = []
        for index1 in range(len(SupportsArr)):
            countIterate=1
            myindex1 = index1
            for index2 in range(myindex1+1,len(SupportsArr),1):
                if abs(SupportsArr[index2]-SupportsArr[myindex1])< self.getPercent(SupportsArr[myindex1],3):
                    break
                else:
                    index1=index2+1
                    countIterate+=1
            self.supports.append([SupportsArr[myindex1],countIterate])
        self.ressists = []
        for index1 in range(len(RessistsArr)):
            countIterate=1
            myindex1 = index1
            for index2 in range(myindex1+1,len(RessistsArr),1):
                if abs(RessistsArr[index2]-RessistsArr[myindex1])< self.getPercent(RessistsArr[myindex1],3):
                    break
                else:
                    index1=index2+1
                    countIterate+=1
            self.ressists.append([RessistsArr[myindex1],countIterate])
        self.BuyCurrPrice()
    def BuyCurrPrice(self):
        lastSupports = self.supports
        lastRessists = self.ressists
        self.supports = []
        self.ressists = []
        
        for sup,res in zip(lastSupports,lastRessists): #CALC REAL SUPPORT RESSISTANCE
            
            if self.prepare.df.loc[self.prepare.indexes[len(self.prepare.indexes)-1]]['close']>=sup[0]:
                self.supports.append(sup)
            elif self.prepare.df.loc[self.prepare.indexes[len(self.prepare.indexes)-1]]['close']<sup[0]:
                self.ressists.append(sup)
        
            if self.prepare.df.loc[self.prepare.indexes[len(self.prepare.indexes)-1]]['close']>=res[0]:
                self.supports.append(res)
            elif self.prepare.df.loc[self.prepare.indexes[len(self.prepare.indexes)-1]]['close']<res[0]:
                self.ressists.append(res)
        self.supports = sorted(self.supports,key=lambda x: x[0])
        self.ressists = sorted(self.ressists,key=lambda x: x[0])
    def BuySignal(self):
        try:
            lastPrice = self.prepare.df.loc[self.prepare.indexes[len(self.prepare.indexes)-1]]['close']
            firstSupport = self.supports[0]
            lastResistance = self.ressists[len(self.ressists)-1]
            if (abs(lastPrice-firstSupport[0])<self.getPercent(lastPrice,5) and 
                firstSupport[1]>1 and
                abs(lastPrice-lastResistance[0])>self.getPercent(lastPrice,10)):
                return self.BUYPoint.append({"currPrice":lastPrice,"Resistance":lastResistance[0],"Support":firstSupport})
            return ''
        except:
            return 'Error'
    def SellSignal(self):
        try:
            lastPrice = self.prepare.df.loc[self.prepare.indexes[len(self.prepare.indexes)-1]]['close']
            firstSupport = self.supports[0]
            lastResistance = self.ressists[len(self.ressists)-1]
            if (abs(lastPrice-lastResistance[0])<self.getPercent(lastPrice,3)):
                return self.SELLPoint.append({"currPrice":lastPrice,"Resistance":lastResistance[0],"Support":firstSupport})
            return ''
        except:
            return 'Error'
    def getPercent(self,value:Decimal,percent)-> Decimal:
        return value*percent/100
    

    