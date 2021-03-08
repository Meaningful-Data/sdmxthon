import logging

from .message_parsers import MetadataType
from .read import readXML

logger = logging.getLogger('logger')


def getMetadata(pathToMetadata):
    metadata = readXML(pathToMetadata)
    if isinstance(metadata, MetadataType):
        setReferences(metadata)
    return metadata


def setOnComponent(comp, obj, missing_rep):
    control_errors = False
    if comp.concept_identity is not None:
        if comp.concept_identity['CS'] in obj.structures.concepts.keys():
            if comp.concept_identity['CON'] in obj.structures.concepts[comp.concept_identity['CS']]. \
                    items.keys():
                comp.concept_identity = obj.structures.concepts[comp.concept_identity['CS']]. \
                    items[comp.concept_identity['CON']]
            else:
                if comp.concept_identity['CON'] not in missing_rep['CON']:
                    missing_rep['CON'].append(comp.concept_identity['CON'])
                control_errors = True

        else:
            if comp.concept_identity['CS'] not in missing_rep['CS']:
                missing_rep['CS'].append(comp.concept_identity['CS'])
            control_errors = True

    if comp.local_representation is not None:
        if comp.local_representation.codelist is not None:
            if comp.local_representation.codelist in obj.structures.codelists.keys():
                comp.local_representation.codelist = obj.structures.codelists[comp.local_representation.codelist]
            else:
                if comp.local_representation.codelist not in missing_rep['CL']:
                    missing_rep['CL'].append(comp.local_representation.codelist)
                control_errors = True

        elif comp.local_representation.conceptScheme is not None:
            if comp.local_representation.conceptScheme in obj.structures.concepts.keys():
                comp.local_representation.conceptScheme = obj.structures.concepts[
                    comp.local_representation.conceptScheme]
            else:
                if comp.concept_identity['CS'] not in missing_rep['CS']:
                    missing_rep['CS'].append(comp.concept_identity['CS'])
                control_errors = True

    return control_errors


def checkRelationship(att, dsd, obj):
    if isinstance(att.relatedTo['id'], list) and att.relatedTo['type'] == 'Dimension':
        relations = att.relatedTo['id'].copy()
        att.relatedTo = {}
        for i in relations:
            if i in dsd.dimensionCodes:
                att.relatedTo[i] = dsd.dimensionDescriptor.components[i]
            else:
                obj.structures.add_error({'Code': 'MS04', 'ErrorLevel': 'CRITICAL',
                                          'ObjectID': f'{dsd.unique_id}-{dsd.attributeDescriptor.id}',
                                          'ObjectType': f'Attribute',
                                          'Message': f'Missing Dimension {i} related to Attribute '
                                                     f'{att.id}'})
    else:
        if att.relatedTo['type'] == 'Dimension':
            if att.relatedTo['id'] in dsd.dimensionCodes:
                att.relatedTo = dsd.dimensionDescriptor.components[att.relatedTo['id']]
            else:
                obj.structures.add_error({'Code': 'MS04', 'ErrorLevel': 'CRITICAL',
                                          'ObjectID': f'{dsd.unique_id}-{dsd.attributeDescriptor.id}',
                                          'ObjectType': f'Attribute',
                                          'Message': f'Missing Dimension {att.relatedTo["id"]} related to Attribute '
                                                     f'{att.id}'})
        elif att.relatedTo['type'] == 'PrimaryMeasure':
            if att.relatedTo['id'] in dsd.measureCode:
                att.relatedTo = dsd.measureDescriptor.components[att.relatedTo['id']]
            else:
                obj.structures.add_error({'Code': 'MS05', 'ErrorLevel': 'CRITICAL',
                                          'ObjectID': f'{dsd.unique_id}-{dsd.attributeDescriptor.id}',
                                          'ObjectType': f'Attribute',
                                          'Message': f'Missing Primary Measure {att.relatedTo["id"]} '
                                                     f'related to Attribute {att.id}'})


def setReferences(obj):
    agencies = {}
    if obj.structures.organisations is not None and obj.structures.organisations.agencySchemes is not None and len(
            obj.structures.organisations.agencySchemes.items) > 0:
        agencies = obj.structures.organisations.agencySchemes.items
        if obj.structures.organisations.agencySchemes.maintainer in agencies.keys():
            obj.structures.organisations.agencySchemes.maintainer = agencies[
                obj.structures.organisations.agencySchemes.maintainer]

    if len(obj.structures.codelists) > 0:
        for cl in obj.structures.codelists.values():
            if cl.maintainer in agencies.keys():
                cl.maintainer = agencies[cl.maintainer]

    if len(obj.structures.codelists) > 0 and len(obj.structures.concepts) > 0:
        for sch in obj.structures.concepts.values():
            if sch.maintainer in agencies.keys():
                sch.maintainer = agencies[sch.maintainer]
            for con in sch.items.values():
                if con.id in sch.cl_references.keys():
                    cl = sch.cl_references[con.id]
                    if cl in obj.structures.codelists.keys():
                        sch.items[con.id].coreRepresentation.codelist = obj.structures.codelists[cl]
                    else:
                        obj.structures.add_error({'Code': 'MX04', 'ErrorLevel': 'CRITICAL',
                                                  'ObjectID': f'{sch.unique_id}-{con.id}', 'ObjectType': f'Concept',
                                                  'Message': f'Codelist {cl} not found for '
                                                             f'Concept {sch.unique_id}-{con.id}'})

        if len(obj.structures.dsds) > 0:
            missing_rep = {'CS': [], 'CL': [], 'CON': []}
            keys_errors = []
            for key, dsd in obj.structures.dsds.items():
                if dsd.maintainer in agencies.keys():
                    dsd.maintainer = agencies[dsd.maintainer]
                if dsd.dimensionDescriptor is not None:
                    for dim in dsd.dimensionDescriptor.components.values():
                        control_errors = setOnComponent(comp=dim, obj=obj, missing_rep=missing_rep)
                        if control_errors and key not in keys_errors:
                            keys_errors.append(key)

                else:
                    if key not in keys_errors:
                        keys_errors.append(key)
                    obj.structures.add_error({'Code': 'MX01', 'ErrorLevel': 'CRITICAL',
                                              'ObjectID': f'{dsd.unique_id}', 'ObjectType': f'DSD',
                                              'Message': f'DSD {dsd.unique_id} does not have a DimensionList'})

                if dsd.attributeDescriptor is not None:
                    for att in dsd.attributeDescriptor.components.values():
                        control_errors = setOnComponent(comp=att, obj=obj, missing_rep=missing_rep)
                        if control_errors and key not in keys_errors:
                            keys_errors.append(key)
                        if att.relatedTo is not None and att.relatedTo != 'NoSpecifiedRelationship':
                            checkRelationship(att, dsd, obj)

                if dsd.measureDescriptor is not None:
                    if len(dsd.measureDescriptor.components) == 1:
                        for meas in dsd.measureDescriptor.components.values():
                            control_errors = setOnComponent(comp=meas, obj=obj, missing_rep=missing_rep)

                            if control_errors and key not in keys_errors:
                                keys_errors.append(key)

                    else:
                        if key not in keys_errors:
                            keys_errors.append(key)
                        obj.structures.add_error({'Code': 'MX02', 'ErrorLevel': 'CRITICAL',
                                                  'ObjectID': f'{dsd.unique_id}', 'ObjectType': f'DSD',
                                                  'Message': f'DSD {dsd.unique_id} does not have a Primary Measure'})

            grouping_errors(missing_rep, obj, keys_errors)
        else:
            obj.structures.add_error({'Code': 'MS01', 'ErrorLevel': 'CRITICAL', 'ObjectID': None,
                                      'ObjectType': f'DSD',
                                      'Message': f'Not found any DSD in this file'})

    elif len(obj.structures.dsds) == 0:
        obj.structures.add_error({'Code': 'MS01', 'ErrorLevel': 'CRITICAL', 'ObjectID': None,
                                  'ObjectType': f'DSD',
                                  'Message': f'Not found any DSD in this file'})

    if len(obj.structures.dsds) > 0 and len(obj.structures.dataflows) > 0:
        for key, flow in obj.structures.dataflows.items():
            if flow.structure in obj.structures.dsds.keys():
                flow.structure = obj.structures.dsds[flow.structure]


def grouping_errors(missing_rep, obj, keys_errors):
    for k in keys_errors:
        del obj.structures.dsds[k]

    if len(missing_rep['CL']) > 0:
        for e in missing_rep['CL']:
            obj.structures.add_error({'Code': 'MS02', 'ErrorLevel': 'CRITICAL',
                                      'ObjectID': f'{e}', 'ObjectType': f'Codelist',
                                      'Message': f'Missing Codelist {e}'})

    if len(missing_rep['CS']) > 0:
        for e in missing_rep['CS']:
            obj.structures.add_error({'Code': 'MS07', 'ErrorLevel': 'CRITICAL',
                                      'ObjectID': f'{e}', 'ObjectType': f'Concept',
                                      'Message': f'Missing Concept Scheme {e}'})

    if len(missing_rep['CON']) > 0:
        for e in missing_rep['CON']:
            obj.structures.add_error({'Code': 'MS03', 'ErrorLevel': 'CRITICAL',
                                      'ObjectID': f'{e}', 'ObjectType': f'Concept',
                                      'Message': f'Missing Concept {e}'})
