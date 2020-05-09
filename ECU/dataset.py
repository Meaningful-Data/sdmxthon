from datetime import datetime
import utils
import pandas as pd

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