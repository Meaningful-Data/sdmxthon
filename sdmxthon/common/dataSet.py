import json

import pandas as pd
from pandas import DataFrame

from ..model.structure import DataStructureDefinition
from ..utils.validations import validate_obs


class DataSet:
    subclass = None
    superclass = None

    def __init__(self, structure: DataStructureDefinition, dataset_attributes: dict = None,
                 attached_attributes: dict = None, data=None):

        self._structure = structure

        if dataset_attributes is None:
            self._dataset_attributes = {}
        else:
            self._dataset_attributes = dataset_attributes.copy()

        if attached_attributes is None:
            self._attached_attributes = {}
        else:
            self._attached_attributes = attached_attributes.copy()

        if data is None:
            self._data = pd.DataFrame()
        else:
            self._data = data.copy()

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
        validation_list = []
        if isinstance(self.data, DataFrame):
            validate_obs(self.data, self.structure, validation_list)
        else:
            raise ValueError('Obs for dataset %s is not well formed' % self.structure.id)
        return validation_list

    def setDimensionAtObservation(self, dimAtObs):
        if dimAtObs in self.structure.dimensionCodes:
            self.datasetAttributes['dimensionAtObservation'] = dimAtObs
        else:
            raise ValueError('%s is not a dimension of dataset %s' % (dimAtObs, self.structure.id))
