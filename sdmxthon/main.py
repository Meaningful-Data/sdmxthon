from model import message, base, itemScheme
from ECU import dataset
from pathlib import Path





fl  = Path().absolute() / "tests" /"resources_structureMessage" /  "RBI_ALE.xml"
fl  = Path().absolute() / "tests" /"resources_structureMessage" /  "BSI_amounts.xml"

mes = message.Message().fromXml(str(fl))

print(mes.dsds["urn:sdmx:org.sdmx.infomodel.datastructure.DataStructure=BIS.XTD:AMOUNTS(1.0)"].dimensionCodes)
