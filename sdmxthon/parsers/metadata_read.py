import copy

from sdmxthon.model.base import Annotation, InternationalString, LocalisedString
from sdmxthon.model.component import Attribute, Component, Dimension, \
    GroupDimensionDescriptor, PrimaryMeasure, TimeDimension
from sdmxthon.model.definitions import ContentConstraint, CubeRegion, \
    DataFlowDefinition, DataKeySet, DataStructureDefinition, MemberSelection
from sdmxthon.model.descriptors import (AttributeDescriptor,
                                        DimensionDescriptor,
                                        MeasureDescriptor)
from sdmxthon.model.header import Contact
from sdmxthon.model.itemScheme import Agency, AgencyScheme, Code, Codelist, \
    Concept, ConceptScheme, Item
from sdmxthon.model.representation import Facet, Representation
from sdmxthon.model.utils import FacetType
from sdmxthon.utils.handlers import add_list, unique_id
from sdmxthon.utils.mappings import Locale_Codes
from sdmxthon.utils.parsing_words import (AGENCIES, AGENCY, AGENCY_ID,
                                          ANNOTATION, ANNOTATION_TEXT,
                                          ANNOTATION_TITLE, ANNOTATION_TYPE,
                                          ANNOTATION_URL, ANNOTATIONS, ATT,
                                          ATT_LIST, ATT_LIST_LOW, ATT_REL, CL,
                                          CODE,
                                          CODELISTS, COMPS, CON, CON_CONS,
                                          CON_ID, CON_ID_LOW, CON_ROLE,
                                          CON_ROLE_LOW,
                                          CONCEPTS, CONS_ATT, CONSTRAINTS,
                                          CONTACT, CONTENT_REGION, CORE_REP,
                                          CORE_REP_LOW, CS, CS_LOW, CUBE_REGION,
                                          DATA_KEY_SET, DATA_KEY_SET_LOW,
                                          DATAFLOWS, DEPARTMENT, DESC, DF, DIM,
                                          DIM_LIST, DIM_LIST_LOW, DIM_REF, DSD,
                                          DSD_COMPS, DSDS, EMAIL, ENUM,
                                          ENUM_FORMAT, FACETS, FAX, GROUP,
                                          GROUP_DIM,
                                          GROUP_DIM_LOW, ID, INCLUDE, INCLUDED,
                                          KEY, KEY_VALUE, LANG, LOCAL_REP,
                                          LOCAL_REP_LOW, MAINTAINER, ME_LIST,
                                          ME_LIST_LOW, NAME, ORGS, PAR_ID,
                                          PAR_VER, PARENT, PRIM_MEASURE, REF,
                                          REL_TO, ROLE, SER_URL, SER_URL_LOW,
                                          STR_URL, STR_URL_LOW, STRUCTURE,
                                          TELEPHONE, TEXT, TEXT_FORMAT,
                                          TEXT_TYPE,
                                          TEXT_TYPE_LOW, TIME_DIM, TITLE, TYPE,
                                          TYPE_, URI, URL, VALUE, VERSION,
                                          XML_TEXT, XMLNS)

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

dimensions = {}
measures = {}
groups = {}

# Global dict to be used in all elements
agencies = {}
codelists = {}
concepts = {}
datastructures = {}
dataflows = {}

# Errors
errors = []
missing_rep = {"CON": [], "CS": [], "CL": []}
dsd_id = ""


def create_int_str(json_int) -> InternationalString:
    json_int = add_list(json_int)
    locals_list = []
    for e in json_int:
        if e[XML_TEXT].strip() not in ['', '\n']:
            e[XML_TEXT] = " ".join(e[XML_TEXT].split())
        locals_list.append(LocalisedString(locale=Locale_Codes[e[LANG]],
                                           label=e[LANG],
                                           content=e[XML_TEXT]))
    return InternationalString(localisedStrings=locals_list)


def create_contact(json_contact) -> Contact:
    node_int = [NAME, DEPARTMENT, ROLE]
    node_str = [URI, EMAIL, TELEPHONE, FAX]

    for e in node_int:
        if e in json_contact:
            json_contact[e.lower()] = create_int_str(json_contact[e])
            del json_contact[e]
    for e in node_str:
        if e in json_contact:
            json_contact[e.lower()] = add_list(json_contact.pop(e))

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
    if element[AGENCY_ID] in agencies:
        element[MAINTAINER] = agencies[element[AGENCY_ID]]
    else:
        element[MAINTAINER] = Agency(element[AGENCY_ID])
    del element[AGENCY_ID]
    return element


def format_annotations(item_elem: any):
    annotations = []
    if ANNOTATIONS in item_elem:
        ann = item_elem[ANNOTATIONS]
        if ANNOTATION in ann:
            ann[ANNOTATION] = add_list(ann[ANNOTATION])
            for e in ann[ANNOTATION]:
                if ID in e:
                    e = format_id(e)
                if ANNOTATION_TITLE in e:
                    e[TITLE] = e.pop(ANNOTATION_TITLE)
                if ANNOTATION_TYPE in e:
                    e[TYPE_] = e.pop(ANNOTATION_TYPE)
                if ANNOTATION_TEXT in e:
                    e[TEXT] = create_int_str(e[ANNOTATION_TEXT])
                    del e[ANNOTATION_TEXT]
                if ANNOTATION_URL in e:
                    e[URL] = e.pop(ANNOTATION_URL)

                annotations.append(Annotation(**e))

        item_elem[ANNOTATIONS.lower()] = annotations
        del item_elem[ANNOTATIONS]

    return item_elem


def format_facets(json_fac) -> dict:
    fac = {FACETS: []}
    if json_fac is None:
        return fac
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
        elif full_id not in missing_rep["CL"]:
            missing_rep["CL"].append(full_id)
            rep[CL.lower()] = full_id

    for e in node:
        if e in json_rep:
            rep = {**rep, **format_facets(json_rep[e])}

    return Representation(**rep)


def format_urls(json_elem):
    if STR_URL in json_elem:
        json_elem[STR_URL_LOW] = json_elem.pop(STR_URL)
    if SER_URL in json_elem:
        json_elem[SER_URL_LOW] = json_elem.pop(SER_URL)
    return json_elem


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

    if PARENT in item_elem:
        item_elem[PARENT.lower()] = item_elem.pop(PARENT)[REF][ID]

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
            full_id = unique_id(element[AGENCY_ID],
                                element[ID],
                                element[VERSION])
            element = format_urls(element)
            element = format_maintainer(element)
            element = format_id(element)
            if item in element:
                element[item] = add_list(element[item])
                items = []
                for item_elem in element[item]:
                    # Dynamic
                    items.append(create_item(item_elem, item))
                del element[item]
                element['items'] = items
                if scheme == AGENCIES:
                    agencies.update({e.id: e for e in items})
            else:
                element['items'] = []
            # Dynamic creation with specific class
            elements[full_id] = schemes_classes[scheme](**element)

    return elements


def create_organisations(json_orgs):
    orgs = {}
    if AGENCIES in json_orgs:
        if len(json_orgs) == 1 and isinstance(json_orgs[AGENCIES], dict):
            ag_sch = create_scheme(json_orgs, AGENCIES, AGENCY)
            return ag_sch
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
            # rep[CS_LOW] = concepts[full_cs_id]
            rep[CON] = concepts[full_cs_id].items[json_ref[ID]]
            core_rep = concepts[full_cs_id].items[json_ref[ID]]. \
                core_representation
            if core_rep is not None:
                cl = core_rep.codelist
                if cl is not None:
                    rep[CL.lower()] = cl
        elif json_ref[ID] not in missing_rep["CON"]:
            missing_rep["CON"].append(json_ref[ID])

    elif full_cs_id not in missing_rep["CS"]:
        missing_rep["CS"].append(full_cs_id)

    return rep


def format_relationship(json_rel, node=DIM, att_name=None):
    rels = {}
    if node in json_rel:
        json_rel[node] = add_list(json_rel[node])
        for e in json_rel[node]:
            if DIM_REF in e:
                element = e[DIM_REF][REF][ID]
            else:
                element = e[REF][ID]
            if element in dimensions:
                rels[element] = dimensions[element]
            else:
                errors.append(
                    {'Code': 'MS04', 'ErrorLevel': 'CRITICAL',
                     'ObjectID': f'{dsd_id}',
                     'ObjectType': 'Attribute',
                     'Message': f'Missing Dimension {e[REF][ID]} '
                                f'related to Attribute '
                                f'{att_name}'})
    elif PRIM_MEASURE in json_rel:
        if json_rel[PRIM_MEASURE][REF][ID] in measures:
            rels = measures[json_rel[PRIM_MEASURE][REF][ID]]
        else:
            errors.append(
                {'Code': 'MS05', 'ErrorLevel': 'CRITICAL',
                 'ObjectID': f'{dsd_id}',
                 'ObjectType': 'Attribute',
                 'Message': 'Missing Primary Measure '
                            f'{json_rel[PRIM_MEASURE][REF][ID]} '
                            f'related to Attribute {att_name}'})
    elif GROUP in json_rel:
        if json_rel[GROUP][REF][ID] in groups:
            rels = groups[json_rel[GROUP][REF][ID]]
    else:
        rels = 'NoSpecifiedRelationship'
    return rels


def format_component(json_comp, comp) -> Component:
    rep = {}
    rep_class = None
    if LOCAL_REP in json_comp:
        rep_class = format_representation(json_comp[LOCAL_REP])
        del json_comp[LOCAL_REP]
    if CON_ID in json_comp:
        rep = format_con_id(json_comp[CON_ID][REF])
        if CON in rep:
            json_comp[CON_ID_LOW] = rep.pop(CON)
        del json_comp[CON_ID]
    if CS_LOW in rep:
        rep_class.concept_scheme = rep[CS_LOW]

    json_comp[LOCAL_REP_LOW] = rep_class

    # Attribute Handling
    if ATT_REL in json_comp:
        json_comp[REL_TO] = format_relationship(json_comp[ATT_REL],
                                                att_name=json_comp[ID])
        del json_comp[ATT_REL]
    if CON_ROLE in json_comp:
        json_comp[CON_ROLE_LOW] = None
        del json_comp[CON_ROLE]
    json_comp = format_id(json_comp)
    json_comp = format_annotations(json_comp)

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

    if comp == comp_lists_items[DIM_LIST]:
        dimensions.update(components)
    elif comp == comp_lists_items[ME_LIST]:
        measures.update(components)
        if len(components) == 0:
            errors.append({'Code': 'MX02', 'ErrorLevel': 'CRITICAL',
                           'ObjectID': f'{dsd_id}', 'ObjectType': 'DSD',
                           'Message': f'DSD {dsd_id} does not have '
                                      f'a Primary Measure'})

    json_comp_lists[COMPS] = components

    return comp_list(**json_comp_lists)


def format_group_dim(json_group):
    if GROUP_DIM in json_group:
        json_group[COMPS] = format_relationship(json_group, GROUP_DIM)
    else:
        json_group[COMPS] = None

    del json_group[GROUP_DIM]
    json_group = format_id(json_group)

    gd = GroupDimensionDescriptor(**json_group)
    groups.update({json_group[ID + '_']: gd})
    return gd


def format_dsd_comps(json_comps):
    node = [DIM_LIST, ME_LIST, GROUP, ATT_LIST]
    comps = json_comps[DSD_COMPS]
    for e in node:
        if e == GROUP and e in comps:
            json_comps[GROUP_DIM_LOW] = format_group_dim(comps[GROUP])
        elif e in comps:
            name = comp_lists_names[e]
            json_comps[name] = format_component_lists(comps[e],
                                                      comp_lists_classes[e],
                                                      comp_lists_items[e])
        else:
            if e == DIM_LIST:
                errors.append({'Code': 'MX01', 'ErrorLevel': 'CRITICAL',
                               'ObjectID': f'{dsd_id}', 'ObjectType': 'DSD',
                               'Message': f'DSD {dsd_id} does not have '
                                          f'a DimensionList'})
            elif e == ME_LIST:
                errors.append({'Code': 'MX02', 'ErrorLevel': 'CRITICAL',
                               'ObjectID': f'{dsd_id}', 'ObjectType': 'DSD',
                               'Message': f'DSD {dsd_id} does not have '
                                          f'a Primary Measure'})
    del json_comps[DSD_COMPS]

    return json_comps


def create_datastructures(json_dsds):
    elements = {}
    if json_dsds is not None and DSD in json_dsds:
        json_dsds[DSD] = add_list(json_dsds[DSD])
        for element in json_dsds[DSD]:
            dimensions.clear()
            measures.clear()
            groups.clear()
            element = format_annotations(element)
            element = format_name_description(element)
            full_id = unique_id(element[AGENCY_ID],
                                element[ID],
                                element[VERSION])
            global dsd_id
            dsd_id = full_id
            element = format_urls(element)

            element = format_maintainer(element)
            element = format_id(element)
            if XMLNS in element:
                del element[XMLNS]

            if DSD_COMPS in element:
                element = format_dsd_comps(element)
            del dsd_id
            # Creation of DSD
            if full_id not in elements:
                elements[full_id] = DataStructureDefinition(**element)
            else:
                errors.append({'Code': 'MS06', 'ErrorLevel': 'CRITICAL',
                               'ObjectID': f'{full_id}', 'ObjectType': 'DSD',
                               'Message': f'DSD {full_id} is not unique'})

    else:
        errors.append(
            {'Code': 'MS01', 'ErrorLevel': 'CRITICAL',
             'ObjectID': None,
             'ObjectType': 'DSD',
             'Message': 'Not found any DSD in this file'})
    return elements


def create_dataflows(json_dfs):
    elements = {}
    if DF in json_dfs:
        json_dfs[DF] = add_list(json_dfs[DF])
        for element in json_dfs[DF]:
            if XMLNS in element:
                del element[XMLNS]

            element = format_annotations(element)
            element = format_name_description(element)

            if STRUCTURE in element:
                agency_id = element[STRUCTURE][REF][AGENCY_ID]
                id_ = element[STRUCTURE][REF][ID]
                version = element[STRUCTURE][REF][VERSION]

                str_id = unique_id(agency_id, id_, version)

                if str_id in datastructures:
                    element[STRUCTURE.lower()] = datastructures[str_id]

                del element[STRUCTURE]

            full_id = unique_id(element[AGENCY_ID],
                                element[ID],
                                element[VERSION])
            element = format_urls(element)

            element = format_maintainer(element)
            element = format_id(element)
            # Creation of DSD
            if full_id not in elements:
                elements[full_id] = DataFlowDefinition(**element)
            else:
                raise Exception

    return elements


def format_key_set(json_key_set):
    json_key_set[KEY_VALUE] = add_list(json_key_set[KEY_VALUE])
    key_set = {}
    for e in json_key_set[KEY_VALUE]:
        key_set[e[ID]] = e[VALUE]

    return key_set


def format_restrictions(json_cons) -> dict:
    if DATA_KEY_SET in json_cons:
        json_cons[DATA_KEY_SET] = add_list(json_cons[DATA_KEY_SET])
        json_cons[DATA_KEY_SET_LOW] = []
        for element in json_cons[DATA_KEY_SET]:
            list_keys = []
            element[KEY] = add_list(element[KEY])
            for e in element[KEY]:
                list_keys.append(format_key_set(e))

            json_cons[DATA_KEY_SET_LOW].append(DataKeySet(keys=list_keys,
                                                          isIncluded=element[
                                                              INCLUDED]))
        del json_cons[DATA_KEY_SET]
    if CUBE_REGION in json_cons:
        json_cons[CUBE_REGION] = add_list(json_cons[CUBE_REGION])
        cubes = []
        for element in json_cons[CUBE_REGION]:

            is_included = element[INCLUDE]
            keys = format_key_set(element)
            members = []
            for e in keys:
                members.append(MemberSelection(is_included,
                                               values_for=e,
                                               sel_value=keys[e]))

            cubes.append(CubeRegion(is_included=is_included, member=members))

        json_cons[CONTENT_REGION] = cubes
        del json_cons[CUBE_REGION]

    return json_cons


def create_constraints(json_cons):
    elements = {}
    if CON_CONS in json_cons:
        json_cons[CON_CONS] = add_list(json_cons[CON_CONS])
        for element in json_cons[CON_CONS]:
            attachment = None
            references = []
            if XMLNS in element:
                del element[XMLNS]

            element = format_annotations(element)
            element = format_name_description(element)
            full_id = unique_id(element[AGENCY_ID],
                                element[ID],
                                element[VERSION])
            element = format_urls(element)

            element = format_maintainer(element)
            element = format_id(element)

            if CONS_ATT in element:
                if DSD in element[CONS_ATT]:
                    agency_id = element[CONS_ATT][DSD][REF][AGENCY_ID]
                    id_ = element[CONS_ATT][DSD][REF][ID]
                    version = element[CONS_ATT][DSD][REF][VERSION]

                    str_id = unique_id(agency_id, id_, version)

                    references = [str_id, DSD]

                    if str_id in datastructures:
                        attachment = datastructures[str_id]

                elif DF in element[CONS_ATT]:
                    agency_id = element[CONS_ATT][DF][REF][AGENCY_ID]
                    id_ = element[CONS_ATT][DF][REF][ID]
                    version = element[CONS_ATT][DF][REF][VERSION]

                    str_id = unique_id(agency_id, id_, version)

                    references = [str_id, DF]

                    if str_id in dataflows:
                        attachment = dataflows[str_id]
                del element[CONS_ATT]

            if TYPE in element:
                element[ROLE.lower()] = element.pop(TYPE)

            element = format_restrictions(element)

            # Creation of Constraint
            if full_id not in elements:
                elements[full_id] = ContentConstraint(**element)
            else:
                raise Exception

            if attachment is not None:
                attachment.add_constraint(elements[full_id])
                del attachment

            # TODO Delete once we change constraints

            if len(references) > 0:
                elements[full_id]._ref_attach = references[0]
                elements[full_id]._type_attach = references[1]

    return elements


def grouping_errors():
    if len(missing_rep["CS"]) > 0:
        for e in missing_rep["CS"]:
            errors.append({'Code': 'MS07', 'ErrorLevel': 'CRITICAL',
                           'ObjectID': f'{e}',
                           'ObjectType': 'Concept',
                           'Message': f'Missing Concept Scheme {e}'}
                          )
        missing_rep["CS"].clear()
    if len(missing_rep["CL"]) > 0:
        for e in missing_rep["CL"]:
            errors.append({'Code': 'MS02', 'ErrorLevel': 'CRITICAL',
                           'ObjectID': f'{e}',
                           'ObjectType': 'Codelist',
                           'Message': f'Missing Codelist {e}'})
        missing_rep["CL"].clear()
    if len(missing_rep["CON"]) > 0:
        for e in missing_rep["CON"]:
            errors.append({'Code': 'MS03', 'ErrorLevel': 'CRITICAL',
                           'ObjectID': f'{e}',
                           'ObjectType': 'Concept',
                           'Message': f'Missing Concept {e}'})
        missing_rep["CON"].clear()


def create_metadata(json_meta):
    """
        Metadata validations stands for the next schema:

        .. list-table:: Metadata validations
            :widths: 20 80
            :header-rows: 1

            * - Code
              - Description
            * - MS01
              - Check that the metadata file contains at least one DSD
            * - MS02
              - Check that the metadata file contains related codelists
            * - MS03
              - Check if the DSD metadata file contains the concepts needed \
                for each DSD
            * - MS04
              - Check if the dimensions in Attribute Relationship are in \
                DimensionList in DSD file
            * - MS05
              - Check if the primary measure in Attribute Relationship is in
                MeasureList in DSD file
            * - MS06
              - Check if all DSDs present in the metadata file are unique
            * - MS07
              - Check if all Concept Scheme needed are present
            * - MX01
              - Check if minimum structural requirements for DSD xml are \
                satisfied
            * - MX02
              - Check if every DSD has primary measure defined
    """
    # Reset dict to store metadata
    metadata = dict()

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
        datastructures.update(metadata[DSDS])
    if DATAFLOWS in json_meta:
        metadata[DATAFLOWS] = create_dataflows(json_meta[DATAFLOWS])
        dataflows.update(metadata[DATAFLOWS])
    if CONSTRAINTS in json_meta:
        metadata[CONSTRAINTS] = create_constraints(json_meta[CONSTRAINTS])

    grouping_errors()

    metadata['errors'] = copy.copy(errors)

    # Reset global variables
    agencies.clear()
    concepts.clear()
    codelists.clear()
    datastructures.clear()
    dataflows.clear()
    errors.clear()
    return metadata
