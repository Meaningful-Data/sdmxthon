"""
def id_creator(agencyID, id_, version):
    return f"{agencyID}:{id_}({version})"

def get_codelist_model(root):
    expression = "/mes:Structure/mes:Structures/str:Codelists/str:Codelist"
    result = root.xpath(expression,
                        namespaces={'str': 'http://www.sdmx.org/resources/sdmxml/schemas/v2_1/structure',
                                    'mes': 'http://www.sdmx.org/resources/sdmxml/schemas/v2_1/message'})

    if result is not None:
        codelists: Dict = {}
        for element in result:
            cl = Codelist(id_=element.attrib['id'],
                          uri=element.attrib['urn'],
                          isExternalReference=element.attrib['isExternalReference'],
                          maintainer=Agency(id_=element.attrib['agencyID']),
                          isFinal=element.attrib['isFinal'],
                          version=element.attrib['version']
                          )
            expression = "./com:Name/text()"
            name = element.xpath(expression,
                                 namespaces={'com': 'http://www.sdmx.org/resources/sdmxml/schemas/v2_1/common'})
            if len(name) > 0:
                cl.name = name[0]

            expression = "./str:Code"
            codes = element.xpath(expression,
                                  namespaces={'str': 'http://www.sdmx.org/resources/sdmxml/schemas/v2_1/structure'})
            for code in codes:
                cd = Code(id_=code.attrib['id'], uri=code.attrib['urn'])
                expression = "./com:Name/text()"
                name = code.xpath(expression,
                                  namespaces={'com': 'http://www.sdmx.org/resources/sdmxml/schemas/v2_1/common'})
                if len(name) > 0:
                    cd.name = name[0]

                expression = "./com:Description/text()"
                desc = code.xpath(expression,
                                  namespaces={'com': 'http://www.sdmx.org/resources/sdmxml/schemas/v2_1/common'})
                if len(desc) > 0:
                    cd.description = desc[0]
                cl.append(cd)

            codelists[cl.unique_id] = cl
        return codelists
    else:
        return None


def get_concept_schemes(root, codelists=None):
    errors = []

    expression = "/mes:Structure/mes:Structures/str:Concepts/str:ConceptScheme"
    result = root.xpath(expression,
                        namespaces={'str': 'http://www.sdmx.org/resources/sdmxml/schemas/v2_1/structure',
                                    'mes': 'http://www.sdmx.org/resources/sdmxml/schemas/v2_1/message'})

    if result is not None:
        schemes: Dict = {}
        for element in result:
            sch = ConceptScheme(id_=element.attrib['id'],
                                uri=element.attrib['urn'],
                                isExternalReference=element.attrib['isExternalReference'],
                                maintainer=Agency(id_=element.attrib['agencyID']),
                                isFinal=element.attrib['isFinal'],
                                version=element.attrib['version']
                                )
            expression = "./com:Name/text()"
            name = element.xpath(expression,
                                 namespaces={'com': 'http://www.sdmx.org/resources/sdmxml/schemas/v2_1/common'})
            if len(name) > 0:
                sch.name = name[0]

            expression = "./str:Concept"
            concepts = element.xpath(expression,
                                     namespaces={'str': 'http://www.sdmx.org/resources/sdmxml/schemas/v2_1/structure'})
            for concept in concepts:
                cd = Concept(id_=concept.attrib['id'], uri=concept.attrib['urn'])
                expression = "./com:Name/text()"
                name = concept.xpath(expression,
                                     namespaces={'com': 'http://www.sdmx.org/resources/sdmxml/schemas/v2_1/common'})
                if len(name) > 0:
                    cd.name = name[0]

                facets = []

                expression = "./str:CoreRepresentation/child::*"
                representation = concept. \
                    xpath(expression,
                          namespaces={'str': 'http://www.sdmx.org/resources/sdmxml/schemas/v2_1/structure'})
                if len(representation) > 0:
                    cl = None
                    for e in representation:
                        if e.tag == '{http://www.sdmx.org/resources/sdmxml/schemas/v2_1/structure}Enumeration':
                            expression = "./str:CoreRepresentation/str:Enumeration/Ref"
                            rep_data = concept. \
                                xpath(expression,
                                      namespaces={'str': 'http://www.sdmx.org/resources/sdmxml/schemas/v2_1/structure'})
                            if len(rep_data) == 1:
                                attrib = rep_data[0].attrib
                                if attrib['package'] == 'codelist' and attrib['class'] == 'Codelist':
                                    id_ = id_creator(attrib['agencyID'], attrib['id'], attrib['version'])
                                    if codelists is not None and id_ in codelists.keys():
                                        cl = codelists[id_]
                                    else:
                                        errors.append({'Code': 'MX04', 'ErrorLevel': 'CRITICAL',
                                                       'ObjectID': f'{sch.unique_id}-{cd.id}', 'ObjectType': f'Concept',
                                                       'Message': f'Codelist {id_} not found for '
                                                                  f'Concept {sch.unique_id}-{cd.id}'})

                        elif e.tag == '{http://www.sdmx.org/resources/sdmxml/schemas/v2_1/structure}TextFormat':
                            for k, v in dict(e.attrib).items():
                                if k in FacetType:
                                    facets.append(Facet(facetType=k, facetValue=v))
                                elif k in FacetValueType:
                                    facets.append(Facet(facetValueType=k, facetValue=v))
                        elif e.tag == '{http://www.sdmx.org/resources/sdmxml/schemas/v2_1/structure}EnumerationFormat':
                            for k, v in dict(e.attrib).items():
                                if k in FacetType:
                                    facets.append(Facet(facetType=k, facetValue=v))
                                elif k in FacetValueType:
                                    facets.append(Facet(facetValueType=k, facetValue=v))
                        else:
                            # TODO Error in Local Representation
                            print(
                                f'CoreRepresentation for Concept {sch.unique_id}-{cd.id} '
                                f'has not been parsed. Implemented elements are '
                                f'Enumeration, Text Format and EnumerationFormat')
                    cd.coreRepresentation = Representation(codelist=cl, facets=facets)
                sch.append(cd)
            identifier = id_creator(sch.maintainer.id, sch.id, sch.version)
            schemes[identifier] = sch

        if len(errors) > 0:
            return schemes, errors
        return schemes, None
    else:
        return None


def extract_ref_data(ref, concepts, missing_rep):
    attrib_cs = ref[0].attrib
    cs_id = id_creator(attrib_cs['agencyID'], attrib_cs['maintainableParentID'],
                       attrib_cs['maintainableParentVersion'])

    if cs_id in concepts.keys():
        cs = concepts[cs_id]
        if attrib_cs['id'] in cs.items.keys():
            con = cs.items[attrib_cs['id']]
            if con.coreRepresentation is not None:
                cl = con.coreRepresentation.codelist
            else:
                cl = None
        else:
            cs = None
            con = None
            cl = None
    else:
        if cs_id not in missing_rep['CS']:
            missing_rep['CS'].append(cs_id)
        id_con = f"{cs_id}-{attrib_cs['id']}"
        if id_con not in missing_rep['CON']:
            missing_rep['CON'].append(id_con)

        cs = None
        con = None
        cl = None

    return cs, con, cl


def override_core_rep(record, codelist_list, obj, dsd_id, missing_rep):
    facets = []
    codelist = None
    expression = "./str:LocalRepresentation/child::*"
    representation = record.xpath(expression,
                                  namespaces={
                                      'str': 'http://www.sdmx.org/resources/sdmxml/schemas/v2_1/structure'})

    if len(representation) > 0:
        for e in representation:
            if e.tag == '{http://www.sdmx.org/resources/sdmxml/schemas/v2_1/structure}Enumeration':
                expression = "./str:LocalRepresentation/str:Enumeration/Ref"
                rep_data = record.xpath(expression,
                                        namespaces={
                                            'str': 'http://www.sdmx.org/resources/sdmxml/schemas/v2_1/structure'})
                if len(rep_data) == 1:
                    attrib = rep_data[0].attrib
                    if attrib['package'] == 'codelist' and attrib['class'] == 'Codelist':
                        id_ = id_creator(attrib['agencyID'], attrib['id'], attrib['version'])
                        if codelist_list is not None and id_ in codelist_list.keys():
                            codelist = codelist_list[id_]
                        else:
                            if id_ not in missing_rep['CL']:
                                missing_rep['CL'].append(id_)

            elif e.tag == '{http://www.sdmx.org/resources/sdmxml/schemas/v2_1/structure}TextFormat':
                for k, v in dict(e.attrib).items():
                    if k in FacetType:
                        facets.append(Facet(facetType=k, facetValue=v))
                    elif k in FacetValueType:
                        facets.append(Facet(facetValueType=k, facetValue=v))
                codelist = None
            elif e.tag == '{http://www.sdmx.org/resources/sdmxml/schemas/v2_1/structure}EnumerationFormat':
                for k, v in dict(e.attrib).items():
                    if k in FacetType:
                        facets.append(Facet(facetType=k, facetValue=v))
                    elif k in FacetValueType:
                        facets.append(Facet(facetValueType=k, facetValue=v))
            else:
                # TODO Error in Local Representation
                print(f'Local Representation for attribute {dsd_id}-{obj.id} has not been parsed. Implemented elements '
                      f'are Enumeration, Text Format and EnumerationFormat')

    return codelist, facets


def gen_representation(record, concepts, codelists, obj, dsd_id, missing_rep):
    expression = "./str:ConceptIdentity/Ref"
    ref = record.xpath(expression,
                       namespaces={
                           'str': 'http://www.sdmx.org/resources/sdmxml/schemas/v2_1/structure'})
    if len(ref) == 1 and concepts is not None:
        cs, con, cl = extract_ref_data(ref=ref, concepts=concepts, missing_rep=missing_rep)
    else:
        # TODO Error no concept scheme found in DataStructureDefinition (validate_metadata)
        cs = None
        con = None
        cl = None

    expression = "./str:LocalRepresentation"
    local = record.xpath(expression,
                         namespaces={
                             'str': 'http://www.sdmx.org/resources/sdmxml/schemas/v2_1/structure'})
    facets = []
    if len(local) == 1:

        cl, facets = override_core_rep(record=record, codelist_list=codelists,
                                       obj=obj, dsd_id=dsd_id, missing_rep=missing_rep)
    else:
        if con is not None and con.coreRepresentation is not None and len(con.coreRepresentation.facets) > 0:
            facets = con.coreRepresentation.facets

    return Representation(codelist=cl, conceptScheme=cs, facets=facets)


def get_attribute_relationship(record, measure_descriptor, attribute_descriptor, dimension_descriptor, dsd_id, errors):
    expression = "./str:AttributeRelationship/child::*"
    obj = record.xpath(expression,
                       namespaces={
                           'str': 'http://www.sdmx.org/resources/sdmxml/schemas/v2_1/structure'})
    related = []
    if len(obj) > 0:
        expression = "./str:AttributeRelationship/str:PrimaryMeasure/Ref"
        meas_data = record.xpath(expression,
                                 namespaces={
                                     'str': 'http://www.sdmx.org/resources/sdmxml/schemas/v2_1/structure'})
        if len(meas_data) > 0 and measure_descriptor is not None:
            for e in meas_data:
                if e.attrib['id'] in measure_descriptor.components.keys():
                    related.append(measure_descriptor.components.get(e.attrib['id']))
                else:
                    # TODO Measure not found in Measure Descriptor
                    errors.append({'Code': 'MS05', 'ErrorLevel': 'CRITICAL',
                                   'ObjectID': f'{dsd_id}-{attribute_descriptor.id}', 'ObjectType': f'Attribute',
                                   'Message': f'Missing Primary Measure {e.attrib["id"]} related to Attribute '
                                              f'{record.attrib["id"]}'})
                    related = None

        elif len(meas_data) == 0 and dimension_descriptor is not None:
            expression = "./str:AttributeRelationship/str:Dimension/Ref"
            dim_data = record.xpath(expression,
                                    namespaces={
                                        'str': 'http://www.sdmx.org/resources/sdmxml/schemas/v2_1/structure'})
            if len(dim_data) > 0:
                for e in dim_data:
                    if e.attrib['id'] in dimension_descriptor.components.keys():
                        related.append(dimension_descriptor.components.get(e.attrib['id']))
                    else:
                        errors.append({'Code': 'MS04', 'ErrorLevel': 'CRITICAL',
                                       'ObjectID': f'{dsd_id}-{attribute_descriptor.id}',
                                       'ObjectType': f'Attribute',
                                       'Message': f'Missing Dimension {e.attrib["id"]} related to Attribute '
                                                  f'{record.attrib["id"]}'})
                        related = None

        else:
            # TODO Not found Ref in Attribute Relationship (validate_metadata)
            related = None

    return related


def create_dimension_data(dsd, dimension_descriptor, dsd_id, concepts, codelists, missing_rep,
                          dim_type='Dimension'):
    if dim_type not in ['Dimension', 'TimeDimension']:
        return None

    # Add Dimensions or TimeDimensions
    expression = "./str:DataStructureComponents/str:DimensionList/str:" + dim_type
    dimensions = dsd.xpath(expression,
                           namespaces={
                               'str': 'http://www.sdmx.org/resources/sdmxml/schemas/v2_1/structure'})

    # Add Dimensions to Dimension Descriptor
    for record in dimensions:
        if dim_type == 'TimeDimension':
            dim = TimeDimension(id_=record.attrib['id'], uri=record.attrib['urn'],
                                position=record.attrib['position'])
        else:
            dim = Dimension(id_=record.attrib['id'], uri=record.attrib['urn'],
                            position=record.attrib['position'])

        rep = gen_representation(record, concepts, codelists, dim, dsd_id, missing_rep=missing_rep)
        dim.local_representation = rep
        dimension_descriptor.addComponent(dim)

    return dimension_descriptor


def create_attribute_data(errors, dsd, attribute_descriptor,
                          dsd_id, concepts, missing_rep,
                          codelists, measure_descriptor: MeasureDescriptor = None,
                          dimension_descriptor: DimensionDescriptor = None):
    expression = "./str:DataStructureComponents/str:AttributeList/str:Attribute"
    attributes = dsd.xpath(expression,
                           namespaces={
                               'str': 'http://www.sdmx.org/resources/sdmxml/schemas/v2_1/structure'})
    # Add Attributes to Attribute Descriptor
    for record in attributes:
        att = Attribute(id_=record.attrib['id'], uri=record.attrib['urn'],
                        usageStatus=record.attrib['assignmentStatus'])

        # Attribute Relationship
        list_related = get_attribute_relationship(record, measure_descriptor, attribute_descriptor,
                                                  dimension_descriptor, dsd_id,
                                                  errors)
        if list_related is None or len(list_related) == 0:
            att.relatedTo = None
        elif len(list_related) == 1:
            att.relatedTo = list_related[0]
        else:
            att.relatedTo = list_related

        rep = gen_representation(record, concepts, codelists, att, dsd_id, missing_rep=missing_rep)
        att.local_representation = rep
        attribute_descriptor.addComponent(att)

    return attribute_descriptor


def create_measures_data(dsd_xml, measure_descriptor, dsd_id, concepts, codelists, missing_rep, errors):
    expression = "./str:DataStructureComponents/str:MeasureList/str:PrimaryMeasure"
    measures = dsd_xml.xpath(expression,
                             namespaces={
                                 'str': 'http://www.sdmx.org/resources/sdmxml/schemas/v2_1/structure'})

    if measures is None or len(measures) == 0:
        errors.append({'Code': 'MX02', 'ErrorLevel': 'CRITICAL',
                       'ObjectID': f'{dsd_id}', 'ObjectType': f'DSD',
                       'Message': f'DSD {dsd_id} does not have a Primary Measure'})
    else:

        # Add Measure to Measure Descriptor
        for record in measures:
            meas = PrimaryMeasure(id_=record.attrib['id'], uri=record.attrib['urn'])

            rep = gen_representation(record, concepts, codelists, meas, dsd_id, missing_rep=missing_rep)
            meas.local_representation = rep
            measure_descriptor.addComponent(meas)

    return measure_descriptor


def grouping_errors(missing_rep):
    errors = []

    if len(missing_rep['CL']) > 0:
        for e in missing_rep['CL']:
            errors.append({'Code': 'MS02', 'ErrorLevel': 'CRITICAL',
                           'ObjectID': f'{e}', 'ObjectType': f'Codelist',
                           'Message': f'Missing Codelist {e}'})

    if len(missing_rep['CS']) > 0:
        for e in missing_rep['CS']:
            errors.append({'Code': 'MS07', 'ErrorLevel': 'CRITICAL',
                           'ObjectID': f'{e}', 'ObjectType': f'Concept',
                           'Message': f'Missing Concept Scheme {e}'})

    if len(missing_rep['CON']) > 0:
        for e in missing_rep['CON']:
            errors.append({'Code': 'MS03', 'ErrorLevel': 'CRITICAL',
                           'ObjectID': f'{e}', 'ObjectType': f'Concept',
                           'Message': f'Missing Concept {e}'})

    return errors


def get_DSDs(root, concepts=None, codelists=None):
    errors = []
    duplicated_dsds = []
    missing_rep = {'CS': [], 'CL': [], 'CON': []}

    expression = "/mes:Structure/mes:Structures/str:DataStructures/str:DataStructure"
    result = root.xpath(expression,
                        namespaces={'str': 'http://www.sdmx.org/resources/sdmxml/schemas/v2_1/structure',
                                    'mes': 'http://www.sdmx.org/resources/sdmxml/schemas/v2_1/message'})
    if result is None or len(result) == 0:
        errors = [{'Code': 'MS01', 'ErrorLevel': 'CRITICAL', 'ObjectID': None,
                   'ObjectType': f'DSD',
                   'Message': f'Not found any DSD in this file'}]
        return {}, errors

    dsds: Dict = {}
    for element in result:
        errors_dsd = []
        dsd = DataStructureDefinition(id_=element.attrib['id'],
                                      uri=element.attrib['urn'],
                                      isExternalReference=element.attrib['isExternalReference'],
                                      maintainer=Agency(id_=element.attrib['agencyID']),
                                      isFinal=element.attrib['isFinal'],
                                      version=element.attrib['version']
                                      )

        expression = "./com:Name/text()"
        name = element.xpath(expression,
                             namespaces={'com': 'http://www.sdmx.org/resources/sdmxml/schemas/v2_1/common'})
        if len(name) > 0:
            dsd.name = str(name[0])

        expression = "./com:Description/text()"
        desc = element.xpath(expression,
                             namespaces={'com': 'http://www.sdmx.org/resources/sdmxml/schemas/v2_1/common'})
        if len(desc) > 0:
            dsd.description = str(desc[0])

        expression = "./str:DataStructureComponents/str:DimensionList"
        dimension_element = element.xpath(expression,
                                          namespaces={
                                              'str': 'http://www.sdmx.org/resources/sdmxml/schemas/v2_1/structure'})

        dd = None

        if len(dimension_element) == 1:
            dd = DimensionDescriptor(id_=dimension_element[0].attrib['id'],
                                     uri=dimension_element[0].attrib['urn'])

            dd = create_dimension_data(dsd=element, dimension_descriptor=dd, dsd_id=dsd.unique_id,
                                       concepts=concepts, codelists=codelists, missing_rep=missing_rep)
            dd = create_dimension_data(dsd=element, dimension_descriptor=dd, dsd_id=dsd.unique_id,
                                       concepts=concepts, codelists=codelists, missing_rep=missing_rep,
                                       dim_type='TimeDimension')

            if 'TIME_PERIOD' not in dd.components.keys() and dsd.agencyID == 'RBI':
                errors_dsd.append({'Code': 'MX03', 'ErrorLevel': 'WARNING',
                                   'ObjectID': f'{dsd.unique_id}', 'ObjectType': f'DSD',
                                   'Message': f'Missing TIME_PERIOD as TimeDimension'})

            dsd.dimensionDescriptor = dd
        else:
            errors_dsd.append({'Code': 'MX01', 'ErrorLevel': 'CRITICAL',
                               'ObjectID': f'{dsd.unique_id}', 'ObjectType': f'DSD',
                               'Message': f'DSD {dsd.unique_id} does not have a DimensionList'})

        # Add Measures
        expression = "./str:DataStructureComponents/str:MeasureList"
        measure_element = element.xpath(expression,
                                        namespaces={
                                            'str': 'http://www.sdmx.org/resources/sdmxml/schemas/v2_1/structure'})

        md = None
        if len(measure_element) == 1:
            md = MeasureDescriptor(id_=measure_element[0].attrib['id'], uri=measure_element[0].attrib['urn'])

            create_measures_data(errors=errors_dsd, dsd_xml=element, dsd_id=dsd.unique_id, measure_descriptor=md,
                                 concepts=concepts, codelists=codelists, missing_rep=missing_rep)

            if 'OBS_VALUE' not in md.components.keys() and dsd.agencyID == 'RBI':
                errors_dsd.append({'Code': 'MX03', 'ErrorLevel': 'WARNING',
                                   'ObjectID': f'{dsd.unique_id}', 'ObjectType': f'DSD',
                                   'Message': f'Missing OBS_VALUE as PrimaryMeasure'})

            dsd.measureDescriptor = md
        else:
            # TODO Missing measure list on DSD (validate_metadata)
            errors_dsd.append({'Code': 'MX01', 'ErrorLevel': 'CRITICAL',
                               'ObjectID': f'{dsd.unique_id}', 'ObjectType': f'DSD',
                               'Message': f'DSD {dsd.unique_id} does not have a MeasureList'})

        # Add Attributes
        expression = "./str:DataStructureComponents/str:AttributeList"
        attribute_element = element.xpath(expression,
                                          namespaces={
                                              'str': 'http://www.sdmx.org/resources/sdmxml/schemas/v2_1/structure'})
        if len(attribute_element) == 1:
            ad = AttributeDescriptor(id_=attribute_element[0].attrib['id'], uri=attribute_element[0].attrib['urn'])

            if concepts is not None:
                create_attribute_data(errors=errors_dsd, dsd=element, dsd_id=dsd.unique_id,
                                      attribute_descriptor=ad, measure_descriptor=md, missing_rep=missing_rep,
                                      concepts=concepts, codelists=codelists, dimension_descriptor=dd)

            dsd.attributeDescriptor = ad

        if dsd.unique_id in dsds.keys():
            duplicated_dsds.append(dsd.unique_id)
        else:
            if len(errors_dsd) > 0:
                errors += errors_dsd.copy()
            else:
                dsds[dsd.unique_id] = dsd

    if len(duplicated_dsds) > 0:
        for e in duplicated_dsds:
            errors.append({'Code': 'MS06', 'ErrorLevel': 'CRITICAL',
                           'ObjectID': f'{e}', 'ObjectType': f'DSD',
                           'Message': f'DSD {e} is not unique'})
            del dsds[e]

    errors_rep = grouping_errors(missing_rep=missing_rep)

    if len(errors_rep) > 0:
        errors += errors_rep
        dsds = {}

    if len(errors) > 0:
        return dsds, errors
    return dsds, None



def validate_dataset_attributes_from_dsd(dsd, dataset):
    dataset_keys = dsd.datasetAttributeCodes
    attached_keys = dataset.attached_attributes.keys()
    wrong_attributes = {"missing_attributes": [], "spared_attributes": []}

    for key in dataset_keys:
        if key not in attached_keys:
            wrong_attributes.get("missing_attributes").append(key)

    for key in attached_keys:
        if key not in dataset_keys:
            wrong_attributes.get("spared_attributes").append(key)

    return wrong_attributes


def add_elements_to_dict(dict1: dict, dict2: dict, updateElementsFromDict2=True):
    if updateElementsFromDict2:
        dict1.update(dict2)
    else:
        for e in dict2.keys():
            if e not in dict1.keys():
                dict1[e] = dict2[e]

    return dict1
    

def delete_unused_codelists(codelists: dict, concepts: dict, dsds: dict):
    used_codelists = []
    used_concepts = []

    for e in dsds.values():
        for i in e.attributeDescriptor.components.values():
            if i.localRepresentation.codeList is not None:
                a = i.localRepresentation.codeList
                used_codelists.append(id_creator(a.agencyID, a.id_, a.version))
            if i.localRepresentation.concept is not None:
                b = i.localRepresentation.concept.scheme
                used_concepts.append(id_creator(b.agencyID, b.id_, b.version))

        for j in e.dimensionDescriptor.components.values():
            if j.localRepresentation.codeList is not None:
                a = j.localRepresentation.codeList
                used_codelists.append(id_creator(a.agencyID, a.id_, a.version))
            if j.localRepresentation.concept is not None:
                b = j.localRepresentation.concept.scheme
                used_concepts.append(id_creator(b.agencyID, b.id_, b.version))

        for k in e.measureDescriptor.components.values():
            if k.localRepresentation.codeList is not None:
                a = k.localRepresentation.codeList
                used_codelists.append(id_creator(a.agencyID, a.id_, a.version))
            if k.localRepresentation.concept is not None:
                b = k.localRepresentation.concept.scheme
                used_concepts.append(id_creator(b.agencyID, b.id_, b.version))

    for m in concepts.values():
        for n in m.items.values():
            if n.coreRepresentation is not None:
                if n.coreRepresentation.codeList is not None:
                    a = n.coreRepresentation.codeList
                    used_codelists.append(id_creator(a.agencyID, a.id_, a.version))
    updated_cl = codelists.copy()
    updated_cs = concepts.copy()
    for o in codelists.keys():
        if o not in used_codelists:
            updated_cl.pop(o)
            print('Deleted CL key %s' % o)
    for o in concepts.keys():
        if o not in used_concepts:
            updated_cs.pop(o)
            print('Deleted CS key %s' % o)
    return updated_cl, updated_cs


def set_dsds_checked_to_false(dsds: dict):
    for e in dsds.values():
        if e.attributeDescriptor is not None:
            for i in e.attributeDescriptor.components.values():
                if i.localRepresentation.codeList is not None:
                    i.localRepresentation.codeList._checked = False
                if i.localRepresentation.concept is not None:
                    i.localRepresentation.concept.scheme._checked = False
        if e.dimensionDescriptor is not None:
            for j in e.dimensionDescriptor.components.values():
                if j.localRepresentation.codeList is not None:
                    j.localRepresentation.codeList._checked = False
                if j.localRepresentation.concept is not None:
                    j.localRepresentation.concept.scheme._checked = False
        if e.measureDescriptor is not None:
            for k in e.measureDescriptor.components.values():
                if k.localRepresentation.codeList is not None:
                    k.localRepresentation.codeList._checked = False
                if k.localRepresentation.concept is not None:
                    k.localRepresentation.concept.scheme._checked = False


def set_codelists_checked_to_false(codelists: dict):
    for e in codelists.values():
        e._checked = False


def set_concepts_checked_to_false(concepts: dict):
    for e in concepts.values():
        e._checked = False
"""
