from sdmxthon.model.base import InternationalString, LocalisedString, \
    Annotation
from sdmxthon.model.component import Component, Dimension, TimeDimension, \
    Attribute, PrimaryMeasure
from sdmxthon.model.component_list import DataStructureDefinition, \
    DimensionDescriptor, AttributeDescriptor, MeasureDescriptor, \
    GroupDimensionDescriptor
from sdmxthon.model.header import Contact
from sdmxthon.model.itemScheme import Agency, AgencyScheme, Codelist, Code, \
    Item, ConceptScheme, Concept
from sdmxthon.model.representation import Representation, Facet
from sdmxthon.model.utils import FacetType
from sdmxthon.utils.handlers import add_list, unique_id
from sdmxthon.utils.mappings import Locale_Codes
from sdmxthon.utils.parsing_words import ORGS, AGENCIES, AGENCY, ID, \
    AGENCY_ID, VERSION, NAME, DESC, LANG, XML_TEXT, URI, EMAIL, ROLE, \
    DEPARTMENT, TELEPHONE, FAX, CONTACT, MAINTAINER, CODELISTS, CL, \
    CODE, CONCEPTS, CS, CON, ANNOTATIONS, ANNOTATION, ANNOTATION_TITLE, \
    TITLE, ANNOTATION_TYPE, TYPE, ANNOTATION_TEXT, TEXT, CORE_REP, \
    CORE_REP_LOW, ENUM, REF, XMLNS, ENUM_FORMAT, TEXT_FORMAT, \
    TEXT_TYPE, TEXT_TYPE_LOW, FACETS, DSDS, DSD, DSD_COMPS, DIM_LIST, \
    ATT_LIST, ME_LIST, GROUP, DIM_LIST_LOW, ATT_LIST_LOW, ME_LIST_LOW, DIM, \
    TIME_DIM, ATT, COMPS, CON_ID, PAR_ID, PAR_VER, CS_LOW, LOCAL_REP, \
    LOCAL_REP_LOW, ATT_REL, REL_TO, PRIM_MEASURE, DATAFLOWS

schemes_classes = {CL: Codelist, AGENCIES: AgencyScheme, CS: ConceptScheme}
items_classes = {AGENCY: Agency, CODE: Code, CON: Concept}
comp_lists_classes = {DIM_LIST: DimensionDescriptor,
                      ATT_LIST: AttributeDescriptor,
                      ME_LIST: MeasureDescriptor,
                      GROUP: GroupDimensionDescriptor}

comp_classes = {DIM: Dimension,
                TIME_DIM: TimeDimension,
                ATT: Attribute,
                PRIM_MEASURE: PrimaryMeasure}

comp_lists_names = {DIM_LIST: DIM_LIST_LOW,
                    ATT_LIST: ATT_LIST_LOW,
                    ME_LIST: ME_LIST_LOW}

comp_lists_items = {DIM_LIST: [DIM, TIME_DIM],
                    ATT_LIST: [ATT],
                    ME_LIST: [PRIM_MEASURE]}

# Global dict to be used in all elements
metadata = {}
agencies = {}
codelists = {}
concepts = {}


def create_int_str(json_int) -> InternationalString:
    json_int = add_list(json_int)
    locals = []
    for e in json_int:
        locals.append(LocalisedString(locale=Locale_Codes[e[LANG]],
                                      label=e[LANG],
                                      content=e[XML_TEXT]))
    return InternationalString(localisedStrings=locals)


def create_contact(json_contact) -> Contact:
    node_int = [NAME, DEPARTMENT, ROLE]
    node_str = [URI, EMAIL, TELEPHONE, FAX]

    for e in node_int:
        if e in json_contact:
            json_contact[e.lower()] = create_int_str(json_contact[e])
            del json_contact[e]
    for e in node_str:
        if e in json_contact:
            json_contact[e.lower()] = json_contact.pop(e)

    return Contact(**json_contact)


def format_name_description(element: any):
    node = [NAME, DESC]
    for e in node:
        if e in element:
            element[e.lower()] = create_int_str(element[e])
            del element[e]
    return element


def format_id(element: any):
    element[ID + '_'] = element.pop(ID)
    return element


def format_maintainer(element: any):
    agency = Agency(element[AGENCY_ID])
    element[MAINTAINER] = agency
    del element[AGENCY_ID]
    return element


def format_annotations(item_elem: any):
    annotations = []
    if ANNOTATIONS in item_elem:
        ann = item_elem[ANNOTATIONS]
        if ANNOTATION in ann:
            ann[ANNOTATION] = add_list(ann[ANNOTATION])
            for e in ann[ANNOTATION]:
                if ANNOTATION_TITLE in e:
                    e[TITLE] = e.pop(ANNOTATION_TITLE)
                if ANNOTATION_TYPE in e:
                    e[TYPE] = e.pop(ANNOTATION_TYPE)
                if ANNOTATION_TEXT in e:
                    e[TEXT] = create_int_str(e[ANNOTATION_TEXT])
                    del e[ANNOTATION_TEXT]

                annotations.append(Annotation(**e))

        item_elem[ANNOTATIONS.lower()] = annotations
        del item_elem[ANNOTATIONS]

    return item_elem


def format_facets(json_fac) -> dict:
    fac = {FACETS: []}
    if TEXT_TYPE in json_fac:
        fac[TEXT_TYPE_LOW] = json_fac.pop(TEXT_TYPE)
    for e in json_fac:
        if e in FacetType:
            fac[FACETS].append(Facet(facetType=e, facetValue=json_fac[e]))

    return fac


def format_representation(json_rep) -> Representation:
    rep = {}
    node = [ENUM_FORMAT, TEXT_FORMAT]
    if ENUM in json_rep:
        data = json_rep[ENUM][REF]
        full_id = unique_id(data[AGENCY_ID], data[ID], data[VERSION])
        if full_id in codelists:
            rep[CL.lower()] = codelists[full_id]

    for e in node:
        if e in json_rep:
            rep = {**rep, **format_facets(json_rep[e])}

    return Representation(**rep)


def create_item(item_elem, item) -> Item:
    if XMLNS in item_elem:
        del item_elem[XMLNS]
    item_elem = format_annotations(item_elem)
    item_elem = format_name_description(item_elem)
    item_elem = format_id(item_elem)
    if CONTACT in item_elem and item == AGENCY:
        item_elem[CONTACT] = add_list(item_elem[CONTACT])
        contacts = []
        for e in item_elem[CONTACT]:
            contacts.append(create_contact(e))
        item_elem[CONTACT.lower() + 's'] = contacts
        del item_elem[CONTACT]
    if CORE_REP in item_elem and item == CON:
        item_elem[CORE_REP_LOW] = format_representation(item_elem[CORE_REP])
        del item_elem[CORE_REP]
    return items_classes[item](**item_elem)


def create_scheme(json_elem, scheme, item):
    elements = {}

    if scheme in json_elem:
        json_elem[scheme] = add_list(json_elem[scheme])
        for element in json_elem[scheme]:

            if XMLNS in element:
                del element[XMLNS]

            element = format_annotations(element)
            element = format_name_description(element)
            if item in element:
                element[item] = add_list(element[item])
                items = []
                for item_elem in element[item]:
                    # Dynamic
                    items.append(create_item(item_elem, item))
                del element[item]
                element['items'] = items
            else:
                element['items'] = []
            full_id = unique_id(element[AGENCY_ID],
                                element[ID],
                                element[VERSION])

            element = format_maintainer(element)
            element = format_id(element)
            # Dynamic creation with specific class
            elements[full_id] = schemes_classes[scheme](**element)

    return elements


def create_organisations(json_orgs):
    orgs = {}
    if AGENCIES in json_orgs:
        if len(json_orgs) == 1 and isinstance(json_orgs[AGENCIES], dict):
            ag_sch = create_scheme(json_orgs, AGENCIES, AGENCY)
            agencies.update(ag_sch.items())
            return ag_sch
        else:
            for e in json_orgs[AGENCIES]:
                ag_sch = create_scheme(e, AGENCIES, AGENCY)
                orgs = {**orgs, **ag_sch}
    return orgs


def format_con_id(json_ref):
    rep = {}
    full_cs_id = unique_id(json_ref[AGENCY_ID],
                           json_ref[PAR_ID],
                           json_ref[PAR_VER])

    if full_cs_id in concepts:
        if json_ref[ID] in concepts[full_cs_id].items:
            rep[CS_LOW] = concepts[full_cs_id]
            core_rep = concepts[full_cs_id].items[json_ref[ID]]. \
                core_representation
            if core_rep is not None:
                cl = core_rep.codelist
                if cl is not None:
                    rep[CODELISTS.lower()] = cl
        else:
            raise Exception
    else:
        raise Exception

    return rep


def format_component(json_comp, comp) -> Component:
    json_comp = format_id(json_comp)
    json_comp = format_annotations(json_comp)
    rep = {}
    rep_class = None
    if LOCAL_REP in json_comp:
        rep_class = format_representation(json_comp[LOCAL_REP])
        del json_comp[LOCAL_REP]
    if CON_ID in json_comp:
        rep = format_con_id(json_comp[CON_ID][REF])
        del json_comp[CON_ID]
    if rep_class is None:
        rep_class = Representation(**rep)
    elif CS_LOW in rep:
        rep_class.concept_scheme = rep[CS_LOW]

    json_comp[LOCAL_REP_LOW] = rep_class

    # Attribute Handling
    if ATT_REL in json_comp:
        json_comp[REL_TO] = json_comp.pop(ATT_REL)

    return comp(**json_comp)


def format_component_lists(json_comp_lists, comp_list, comp):
    components = {}
    json_comp_lists = format_annotations(json_comp_lists)
    json_comp_lists = format_id(json_comp_lists)
    for e in comp:
        if e in json_comp_lists:
            json_comp_lists[e] = add_list(json_comp_lists[e])
            for i in json_comp_lists[e]:
                new_element = format_component(i, comp_classes[e])
                components[new_element.id] = new_element
            del json_comp_lists[e]

    json_comp_lists[COMPS] = components

    return comp_list(**json_comp_lists)


def format_dsd_comps(json_comps):
    node = [DIM_LIST, ATT_LIST, ME_LIST]
    comps = json_comps[DSD_COMPS]
    for e in node:
        name = comp_lists_names[e]
        json_comps[name] = format_component_lists(comps[e],
                                                  comp_lists_classes[e],
                                                  comp_lists_items[e])

    del json_comps[DSD_COMPS]

    return json_comps


def create_datastructures(json_dsds):
    elements = {}

    if DSD in json_dsds:
        json_dsds[DSD] = add_list(json_dsds[DSD])
        for element in json_dsds[DSD]:

            if XMLNS in element:
                del element[XMLNS]

            element = format_annotations(element)
            element = format_name_description(element)
            if DSD_COMPS in element:
                element = format_dsd_comps(element)

            full_id = unique_id(element[AGENCY_ID],
                                element[ID],
                                element[VERSION])

            element = format_maintainer(element)
            element = format_id(element)
            # Creation of DSD
            if full_id not in elements:
                elements[full_id] = DataStructureDefinition(**element)
            else:
                raise Exception

    return elements


def create_dataflows(json_dfs):
    print(json_dfs)


def create_metadata(json_meta):
    if ORGS in json_meta:
        metadata[ORGS] = create_organisations(json_meta[ORGS])
    if CODELISTS in json_meta:
        metadata[CODELISTS] = create_scheme(json_meta[CODELISTS], CL, CODE)
        codelists.update(metadata[CODELISTS])
    if CONCEPTS in json_meta:
        metadata[CONCEPTS] = create_scheme(json_meta[CONCEPTS], CS, CON)
        concepts.update(metadata[CONCEPTS])
    if DSDS in json_meta:
        metadata[DSDS] = create_datastructures(json_meta[DSDS])
    if DATAFLOWS in json_meta:
        metadata[DATAFLOWS] = create_dataflows(json_meta[DATAFLOWS])
    return metadata
