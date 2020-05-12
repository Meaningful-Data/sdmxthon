from ECU import api
from pathlib import Path

dataFl  = Path().absolute() / "ECU" / "IRIS" / "R017_ALE.csv"
metadataFl  = Path().absolute() / "tests" /"resources_structureMessage" /  "RBI_ALE.xml"
saveTo = Path().absolute() / "ECU" / "IRIS" / "output.xml"

api.convertFile(dataFl, metadataFl, saveTo, id_ = "test")

