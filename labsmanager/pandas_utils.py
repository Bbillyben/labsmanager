from decimal import Decimal
import math


class PDUtils():
    
    @classmethod
    def applyColumnFormat(self, df, formatFc):
        for c in df.columns:
            df[c]=df[c].apply(formatFc)


    

    @classmethod
    def getBootstrapTable(self, df):
        return df.to_html(classes=["table table-bordered table-striped table-hover"])



















    """ Formatters Utils """
    @classmethod
    def moneyFormat(self, dynvarname):
        """ Returns the value of dynvarname into the context """
        if dynvarname != None and (type(dynvarname) == int or type(dynvarname)==float or type(dynvarname)==Decimal) and math.isnan(dynvarname)==False :
            val =  "{:0,.0f}€".format(dynvarname).replace(',', ' ') 
        else:
            val="-" 
        return val