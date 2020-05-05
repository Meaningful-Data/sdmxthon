from model import message
from pathlib import Path


testsFolder  = Path().absolute() / "tests" / "resources_structureMessage"

mes = message.Message().fromXml(str(testsFolder / "IMF_ECOFIN_DSD.xml"))

print(mes.header)