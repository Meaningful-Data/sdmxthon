from datetime import datetime
import utils
import pandas as pd
import numpy as np
import csv

class FilingInformation():
    def __init__(self, returnCode:str = None, bankCode:str = None, filingFrequency:str = None,
                    endDate:datetime = None, auditStatus:str = None):
        

        self.returnCode = returnCode
        self.bankCode = bankCode
        self.filingFrequency = filingFrequency
        self.endDate = endDate
        self.auditStatus = auditStatus

    
    @property
    def returnCode(self):
        return self._returnCode

    @property
    def bankCode(self):
        return self._bankCode
    
    @property
    def filingFrequency(self):
        return self._filingFrequency

    @property
    def endDate(self):
        return self._endDate

    @property
    def auditStatus(self):
        return self._auditStatus

    @returnCode.setter 
    def returnCode(self, value):
        self._returnCode = utils.stringSetter(value)

    @bankCode.setter 
    def bankCode(self, value):
        self._bankCode = utils.stringSetter(value)

    @filingFrequency.setter 
    def filingFrequency(self, value):
        self._filingFrequency = utils.stringSetter(value)

    @endDate.setter 
    def endDate(self, value):
        self._endDate = utils.dateSetter(value)

    @auditStatus.setter 
    def auditStatus(self, value):
        self._auditStatus = utils.stringSetter(value)

    @classmethod
    def fromDict(cls, dct: dict):
        filInf = cls()

        dateAttributes = ["Filing period end date"]

        filInFMap = {
            "Return Codes": "returnCode",
            "Bank Code": "bankCode",
            "Filing Frequency": "filingFrequency",
            "Filing period end date": "endDate",
            "Audit Status": "auditStatus"
        }

        for k in dct:
            if k not in dct:
                raise ValueError(f"The filing information {k} is not supported")
            
            if k in dateAttributes:
                dct[k] = datetime.strptime(dct[k], "%d-%m-%Y")
            
            setattr(filInf,  filInFMap[k],  dct[k])

        return filInf

class Dataset():
    def __init__(self, filingInfomration:FilingInformation = None, data:pd.DataFrame =None):
       self.filingInfomration = filingInfomration
       self.data = data

    @property
    def filingInformation(self):
        return self._filingInformation

    @property
    def data(self):
        return self._data

    @filingInformation.setter
    def filingInformation(self, value):
        if isinstance(value, FilingInformation) or value is None:
            self._filingInformation = value
        else:
            raise TypeError(f"FilingInformation object expected, {type(value)} received")
    
    @data.setter
    def data(self, value):
        if isinstance(value, pd.DataFrame) or value is None:
            self._data = value
        else:
            raise TypeError(f"DataFrame object expected, {type(value)} received")

    @property
    def dsds(self):
        return self.data.DSDID.unique()

   
    @classmethod
    def fromCsv(cls, csvPath:str):
        ds = cls()

        #1. look for the row that delimits the header and the data, get the filing information as dict
        with open(csvPath, newline='') as f:
            reader = csv.reader(f)
            
            filInformation = {}
            
            lineCount = 1
            for row in reader:
                if row[0] == "Filing Data":
                    delimiterLine = lineCount
                    break
                elif lineCount > 1:
                    filInformation[row[0]] = row[1]
                    
                lineCount += 1

        #2. Get the data
        ds.data = pd.read_csv(csvPath,
                                skiprows = delimiterLine)

        #3. Get the filing Infomration
        ds.filingInfomration = FilingInformation.fromDict(filInformation)
        return ds