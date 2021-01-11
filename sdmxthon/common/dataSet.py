import json
from datetime import date, datetime

import pandas as pd
from pandas import DataFrame

from ..model.structure import DataStructureDefinition
from ..utils.enums import DatasetType
from ..utils.validations import validate_obs
from ..utils.write import writer


class DataSet:
    subclass = None
    superclass = None

    def __init__(self, structure: DataStructureDefinition, dataset_attributes: dict = None,
                 attached_attributes: dict = None, data=None):

        self._structure = structure

        if dataset_attributes is None:
            self.check_DA_keys({}, structure.id)
        else:
            self.check_DA_keys(dataset_attributes, structure.id)

        if attached_attributes is None:
            self._attached_attributes = {}
        else:
            self._attached_attributes = attached_attributes.copy()

        if data is None:
            self._data = pd.DataFrame()
        else:
            if isinstance(data, pd.DataFrame):
                self.data = data.copy()
            else:
                self.data = pd.DataFrame(data)

    def __str__(self):
        return '<DataSet  - %s>' % self.structure.id

    def __unicode__(self):
        return '<DataSet  - %s>' % self.structure.id

    def __repr__(self):
        return '<DataSet  - %s>' % self.structure.id

    @property
    def structure(self):
        return self._structure

    @structure.setter
    def structure(self, value):
        self._structure = value

    @property
    def datasetAttributes(self):
        return self._dataset_attributes

    @datasetAttributes.setter
    def datasetAttributes(self, value):
        self._dataset_attributes = value

    @property
    def attachedAttributes(self):
        return self._attached_attributes

    @attachedAttributes.setter
    def attachedAttributes(self, value):
        self._attached_attributes = value

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, value):
        self._data = value

    @property
    def dimAtObs(self):
        return self.datasetAttributes.get('dimensionAtObservation')

    def readCSV(self, pathToCSV: str):
        self._data = pd.read_csv(pathToCSV)

    def readJSON(self, pathToJSON: str):
        self._data = pd.read_json(pathToJSON, orient='records')

    def readExcel(self, pathToExcel: str):
        self._data = pd.read_excel(pathToExcel)

    def toCSV(self, pathToCSV: str = None):
        return self.data.to_csv(pathToCSV, sep=',', encoding='utf-8', index=False, header=True)

    def toJSON(self, pathToJSON: str = None):
        element = {}

        element['structureRef'] = {"code": self.structure.id, "version": self.structure.version,
                                   "agencyID": self.structure.agencyId}
        element['dataset_attributes'] = self.datasetAttributes
        element['attached_attributes'] = self.attachedAttributes

        result = self.data.to_json(orient="records")
        element['data'] = json.loads(result).copy()
        if pathToJSON is None:
            return element
        else:
            with open(pathToJSON, 'w') as f:
                f.write(json.dumps(element, ensure_ascii=False, indent=2))

    def toFeather(self, pathToFeather):
        self.data.to_feather(pathToFeather)

    def semanticValidation(self):
        if isinstance(self.data, DataFrame):
            return validate_obs(self.data, self.structure)
        else:
            raise ValueError('Data for dataset %s is not well formed' % self.structure.id)

    def setDimensionAtObservation(self, dimAtObs):
        if dimAtObs in self.structure.dimensionCodes:
            self.datasetAttributes['dimensionAtObservation'] = dimAtObs
        elif dimAtObs == 'AllDimensions':
            self.datasetAttributes['dimensionAtObservation'] = dimAtObs
        else:
            raise ValueError('%s is not a dimension of dataset %s' % (dimAtObs, self.structure.id))

    def check_DA_keys(self, attributes, code):
        keys = ["reportingBegin", "reportingEnd", "dataExtractionDate", "validFrom", "validTo", "publicationYear",
                "publicationPeriod", "action", "setId", "dimensionAtObservation"]

        for spared_key in attributes.keys():
            if spared_key not in keys:
                attributes.pop(spared_key)

        for k in keys:
            if k not in attributes.keys():
                if k == "dataExtractionDate":
                    attributes[k] = date.today()
                elif k == "action":
                    attributes[k] = "Replace"
                elif k == "setId":
                    attributes[k] = code
                elif k == "dimensionAtObservation":
                    attributes[k] = "AllDimensions"
                else:
                    attributes[k] = None

        self.datasetAttributes = attributes.copy()

    def toXML(self, dataset_type: DatasetType = DatasetType.GenericDataSet, outputPath='', id_='test',
              test='true',
              prepared=datetime.now(),
              sender='Unknown',
              receiver='Not_supplied'):
        if outputPath == '':
            return writer(path=outputPath, dType=dataset_type, dataset=self, id_=id_, test=test,
                          prepared=prepared, sender=sender, receiver=receiver)
        else:
            writer(path=outputPath, dType=dataset_type, dataset=self, id_=id_, test=test,
                   prepared=prepared, sender=sender, receiver=receiver)
