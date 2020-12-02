import pandas as pd


class DataSet:
    subclass = None
    superclass = None

    def __init__(self, code="", version="", agencyID="", dataset_attributes: dict = None,
                 attached_attributes: dict = None, obs=None):

        self.code = code
        self.version = version
        self.agencyID = agencyID

        if dataset_attributes is None:
            self.dataset_attributes = {}
        else:
            self.dataset_attributes = dataset_attributes.copy()

        if attached_attributes is None:
            self.attached_attributes = {}
        else:
            self.attached_attributes = attached_attributes.copy()

        if obs is None:
            self.obs = pd.DataFrame()
        else:
            self.obs = obs.copy()
