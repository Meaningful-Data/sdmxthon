from model import abstract
from datetime import datetime

ls_en = abstract.LocalisedString(locale="en", label="test string")
ls_es = abstract.LocalisedString(locale="es", label="String de prueba")

i_string = abstract.InternationalString([ls_en])
i_string.addLocalisedString(ls_es)

annotation = abstract.Annotation(id_ = "Annotation ID test", 
                                    title = "Test title", 
                                    type_ = "Test type",
                                    url = "Test url", 
                                    text = i_string)




date = datetime(year=2020, month=4, day=29)

versionable = abstract.VersionableArtefact(id_ = "id1",
                                                    uri = "uri",
                                                    annotations = [annotation],
                                                    name = i_string,
                                                    description = i_string,
                                                    version = "1",
                                                    validFrom=datetime(year=2020, month=4, day=29),
                                                    validTo=datetime(year=2020, month=4, day=29))
versionable = abstract.VersionableArtefact()


