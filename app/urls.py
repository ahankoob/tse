from django.conf.urls import url

from . import views

urlpatterns = [
    
    url(r'^$',views.index),
    url(r'^tickersFromJsonFile',views.tickersFromJsonFile,name='tickersFromJsonFile'),
    url(r'^tickersFromTseSite',views.tickersFromTseSite,name='tickersFromTseSite'),
    url(r'^tickersImportFromCsvWithWC',views.tickersImportFromCsvWithWC,name='tickersImportFromCsvWithWC'),
    url(r'^tickersImportFromCsv/(?P<sid>[0-9]+)/',views.tickersImportFromCsv,name='tickersImportFromCsv'),
    url(r'^technical',views.myTechnical,name='myTechnical'),
    url(r'^(?P<sid>[0-9]+)/',views.ticker , name='ticker'),
   
    #url(r'^symbolfastData/(?P<sid>[0-9]+)/',views.importSymbolFastData,name='importSymbolFastData'),
    url(r'^symbolfastData/',views.importFastData,name='importFastData'),

    ]