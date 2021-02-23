from urllib.request import urlopen

from lxml import etree

from .metadata_parsers import get_codelist_model, get_concept_schemes, get_DSDs


def getMetadata(pathToMetadata):
    if isinstance(pathToMetadata, str) and 'http' in pathToMetadata:
        res = urlopen(pathToMetadata)
        root = etree.parse(res)
    else:
        root = etree.parse(pathToMetadata)
    codelists = get_codelist_model(root)
    concepts, errors_con = get_concept_schemes(root, codelists)

    if errors_con is not None:
        dsds, errors_dsd = get_DSDs(root, concepts, codelists)
        if errors_dsd is not None:
            errors_con += errors_dsd
        return dsds, errors_con
    else:
        return get_DSDs(root, concepts, codelists)


def setReferences(obj):
    if len(obj.structures.codelists) > 0:
        for k, v in obj.structures.concepts.items():
            for l, m in v.cl_references.items():
                if m in obj.structures.codelists.keys():
                    v.items[l].coreRepresentation.codelist = obj.structures.codelists[m]
                else:
                    # TODO Error MX04
                    print(m)