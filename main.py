from model import message, base, itemScheme
from pathlib import Path


# testsFolder  = Path().absolute() / "tests" / "resources_structureMessage"

# mes = message.Message().fromXml(str(testsFolder / "IMF_ECOFIN_DSD.xml"))

# print(mes.header)


ls_en = base.LocalisedString(locale="en", label="test string")
ls_es = base.LocalisedString(locale="es", label="String de prueba")
i_string = base.InternationalString([ls_en, ls_es])
annotation = base.Annotation(id_ = "AnnotationIDtest", 
                                title = "Test title", 
                                type_ = "Test type",
                                url = "Test url", 
                                text = i_string)

agencyList = itemScheme.AgencyList()
agency = itemScheme.Agency()
concept = itemScheme.Concept()

agencyList.append(agency)
assert(agencyList.items == [agency], "Error appending an agency to an agency list")

        # self.assertEqual(agency.scheme, agencyList, "Error appending an agency to an agency list. The property scheme of the agency has not changed")
