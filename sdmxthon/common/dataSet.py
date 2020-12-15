import json

import pandas as pd
from pandas import DataFrame

from ..model.structure import DataStructureDefinition
from ..utils.validations import validate_obs, validate_series


class DataSet:
    subclass = None
    superclass = None

    def __init__(self, structure: DataStructureDefinition, dataset_attributes: dict = None,
                 attached_attributes: dict = None, obs=None):

        self._structure = structure

        if dataset_attributes is None:
            self._dataset_attributes = {}
        else:
            self._dataset_attributes = dataset_attributes.copy()

        if attached_attributes is None:
            self._attached_attributes = {}
        else:
            self._attached_attributes = attached_attributes.copy()

        if obs is None:
            self._obs = pd.DataFrame()
        else:
            self._obs = obs.copy()

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
    def obs(self):
        return self._obs

    @obs.setter
    def obs(self, value):
        self._obs = value

    def readCSV(self, pathToCSV: str):
        self._obs = pd.read_csv(pathToCSV)

    def readJSON(self, pathToJSON: str):
        self._obs = pd.read_json(pathToJSON, orient='records')

    def readExcel(self, pathToExcel: str):
        self._obs = pd.read_excel(pathToExcel)

    def toCSV(self, pathToCSV: str = None):
        return self.obs.to_csv(pathToCSV, sep=',', encoding='utf-8', index=False, header=True)

    def toJSON(self, pathToJSON: str = None):
        element = {}

        element['structureRef'] = {"code": self.structure.id, "version": self.structure.version,
                                   "agencyID": self.structure.agencyId}
        element['dataset_attributes'] = self.datasetAttributes
        element['attached_attributes'] = self.attachedAttributes

        result = self.obs.to_json(orient="records")
        element['obs'] = json.loads(result).copy()
        if pathToJSON is None:
            return element
        else:
            with open(pathToJSON, 'w') as f:
                f.write(json.dumps(element, ensure_ascii=False, indent=2))

    def toFeather(self, pathToFeather):
        self.obs.to_feather(pathToFeather)

    def semanticValidation(self):
        validation_list = []
        if isinstance(self.obs, DataFrame):
            validate_obs(self.obs, self.structure, validation_list)
        elif isinstance(self.obs, dict):
            validate_series(self.obs, self.structure, validation_list)
        else:
            raise ValueError('Obs for dataset %s is not well formed' % self.structure.id)
        return validation_list
