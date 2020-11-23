from SDMXThon.utils.data_parser import DataParser


class EmptyType(DataParser):
    """EmptyType is an empty complex type for elements where the presence of
    the tag indicates all that is necessary."""
    __hash__ = DataParser.__hash__
    subclass = None
    superclass = None

    def __init__(self, gds_collector_=None, **kwargs_):
        super(EmptyType, self).__init__(gds_collector_, **kwargs_)
        self.gds_collector_ = gds_collector_
        self._namespace_def = 'xmlns:message="http://www.sdmx.org/resources/sdmxml/schemas/v2_1/message"'
        self._name = 'EmptyType'
        self.gds_element_tree_node_ = None
        self.original_tag_name_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None

    def factory(*args_, **kwargs_):
        return EmptyType(*args_, **kwargs_)

    factory = staticmethod(factory)


# end class EmptyType

class Any(EmptyType):
    __hash__ = EmptyType.__hash__
    subclass = None
    superclass = EmptyType

    def __init__(self, gds_collector_=None, **kwargs_):
        super(Any, self).__init__(gds_collector_, **kwargs_)
        self._name = 'Any'


class Agency(EmptyType):
    __hash__ = EmptyType.__hash__
    subclass = None
    superclass = EmptyType

    def __init__(self, gds_collector_=None, **kwargs_):
        super(Agency, self).__init__(gds_collector_, **kwargs_)
        self._name = 'Agency'


class AgencyScheme(EmptyType):
    __hash__ = EmptyType.__hash__
    subclass = None
    superclass = EmptyType

    def __init__(self, gds_collector_=None, **kwargs_):
        super().__init__(gds_collector_, **kwargs_)
        self._name = 'AgencyScheme'


class AttachmentConstraint(EmptyType):
    __hash__ = EmptyType.__hash__
    subclass = None
    superclass = EmptyType

    def __init__(self, gds_collector_=None, **kwargs_):
        super().__init__(gds_collector_, **kwargs_)
        self._name = 'AttachmentConstraint'


class Attribute(EmptyType):
    __hash__ = EmptyType.__hash__
    subclass = None
    superclass = EmptyType

    def __init__(self, gds_collector_=None, **kwargs_):
        super().__init__(gds_collector_, **kwargs_)
        self._name = 'Attribute'


class AttributeDescriptor(EmptyType):
    __hash__ = EmptyType.__hash__
    subclass = None
    superclass = EmptyType

    def __init__(self, gds_collector_=None, **kwargs_):
        super().__init__(gds_collector_, **kwargs_)
        self._name = 'AttributeDescriptor'


class Categorisation(EmptyType):
    __hash__ = EmptyType.__hash__
    subclass = None
    superclass = EmptyType

    def __init__(self, gds_collector_=None, **kwargs_):
        super().__init__(gds_collector_, **kwargs_)
        self._name = 'Categorisation'


class Category(EmptyType):
    __hash__ = EmptyType.__hash__
    subclass = None
    superclass = EmptyType

    def __init__(self, gds_collector_=None, **kwargs_):
        super(Category, self).__init__(gds_collector_, **kwargs_)
        self._name = 'Category'


class CategorySchemeMap(EmptyType):
    __hash__ = EmptyType.__hash__
    subclass = None
    superclass = EmptyType

    def __init__(self, gds_collector_=None, **kwargs_):
        super(CategorySchemeMap, self).__init__(gds_collector_, **kwargs_)
        self._name = 'CategorySchemeMap'


class CategoryScheme(EmptyType):
    __hash__ = EmptyType.__hash__
    subclass = None
    superclass = EmptyType

    def __init__(self, gds_collector_=None, **kwargs_):
        super(CategoryScheme, self).__init__(gds_collector_, **kwargs_)
        self._name = 'CategoryScheme'


class Code(EmptyType):
    __hash__ = EmptyType.__hash__
    subclass = None
    superclass = EmptyType

    def __init__(self, gds_collector_=None, **kwargs_):
        super(Code, self).__init__(gds_collector_, **kwargs_)
        self._name = 'Code'


class CodeMap(EmptyType):
    __hash__ = EmptyType.__hash__
    subclass = None
    superclass = EmptyType

    def __init__(self, gds_collector_=None, **kwargs_):
        super(CodeMap, self).__init__(gds_collector_, **kwargs_)
        self._name = 'CodeMap'


class Codelist(EmptyType):
    __hash__ = EmptyType.__hash__
    subclass = None
    superclass = EmptyType

    def __init__(self, gds_collector_=None, **kwargs_):
        super(Codelist, self).__init__(gds_collector_, **kwargs_)
        self._name = 'Codelist'


class CodelistMap(EmptyType):
    __hash__ = EmptyType.__hash__
    subclass = None
    superclass = EmptyType

    def __init__(self, gds_collector_=None, **kwargs_):
        super(CodelistMap, self).__init__(gds_collector_, **kwargs_)
        self._name = 'CodelistMap'


class ComponentMap(EmptyType):
    __hash__ = EmptyType.__hash__
    subclass = None
    superclass = EmptyType

    def __init__(self, gds_collector_=None, **kwargs_):
        super(ComponentMap, self).__init__(gds_collector_, **kwargs_)
        self._name = 'ComponentMap'


class Concept(EmptyType):
    __hash__ = EmptyType.__hash__
    subclass = None
    superclass = EmptyType

    def __init__(self, gds_collector_=None, **kwargs_):
        super(Concept, self).__init__(gds_collector_, **kwargs_)
        self._name = 'Concept'


class ConceptMap(EmptyType):
    __hash__ = EmptyType.__hash__
    subclass = None
    superclass = EmptyType

    def __init__(self, gds_collector_=None, **kwargs_):
        super(ConceptMap, self).__init__(gds_collector_, **kwargs_)
        self._name = 'ConceptMap'


class ConceptScheme(EmptyType):
    __hash__ = EmptyType.__hash__
    subclass = None
    superclass = EmptyType

    def __init__(self, gds_collector_=None, **kwargs_):
        super(ConceptScheme, self).__init__(gds_collector_, **kwargs_)
        self._name = 'ConceptScheme'


class ConceptSchemeMap(EmptyType):
    __hash__ = EmptyType.__hash__
    subclass = None
    superclass = EmptyType

    def __init__(self, gds_collector_=None, **kwargs_):
        super(ConceptSchemeMap, self).__init__(gds_collector_, **kwargs_)
        self._name = 'ConceptSchemeMap'


class ConstraintTarget(EmptyType):
    __hash__ = EmptyType.__hash__
    subclass = None
    superclass = EmptyType

    def __init__(self, gds_collector_=None, **kwargs_):
        super(ConstraintTarget, self).__init__(gds_collector_, **kwargs_)
        self._name = 'ConstraintTarget'


class ContentConstraint(EmptyType):
    __hash__ = EmptyType.__hash__
    subclass = None
    superclass = EmptyType

    def __init__(self, gds_collector_=None, **kwargs_):
        super(ContentConstraint, self).__init__(gds_collector_, **kwargs_)
        self._name = 'ContentConstraint'


class Dataflow(EmptyType):
    __hash__ = EmptyType.__hash__
    subclass = None
    superclass = EmptyType

    def __init__(self, gds_collector_=None, **kwargs_):
        super(Dataflow, self).__init__(gds_collector_, **kwargs_)
        self._name = 'Dataflow'


class DataConsumer(EmptyType):
    __hash__ = EmptyType.__hash__
    subclass = None
    superclass = EmptyType

    def __init__(self, gds_collector_=None, **kwargs_):
        super(DataConsumer, self).__init__(gds_collector_, **kwargs_)
        self._name = 'DataConsumer'


class DataConsumerScheme(EmptyType):
    __hash__ = EmptyType.__hash__
    subclass = None
    superclass = EmptyType

    def __init__(self, gds_collector_=None, **kwargs_):
        super(DataConsumerScheme, self).__init__(gds_collector_, **kwargs_)
        self._name = 'DataConsumerScheme'


class DataProvider(EmptyType):
    __hash__ = EmptyType.__hash__
    subclass = None
    superclass = EmptyType

    def __init__(self, gds_collector_=None, **kwargs_):
        super(DataProvider, self).__init__(gds_collector_, **kwargs_)
        self._name = 'DataProvider'


class DataProviderScheme(EmptyType):
    __hash__ = EmptyType.__hash__
    subclass = None
    superclass = EmptyType

    def __init__(self, gds_collector_=None, **kwargs_):
        super(DataProviderScheme, self).__init__(gds_collector_, **kwargs_)
        self._name = 'DataProviderScheme'


class DataSetTarget(EmptyType):
    __hash__ = EmptyType.__hash__
    subclass = None
    superclass = EmptyType

    def __init__(self, gds_collector_=None, **kwargs_):
        super().__init__(gds_collector_, **kwargs_)
        self._name = 'DataSetTarget'


class DataStructure(EmptyType):
    __hash__ = EmptyType.__hash__
    subclass = None
    superclass = EmptyType

    def __init__(self, gds_collector_=None, **kwargs_):
        super().__init__(gds_collector_, **kwargs_)
        self._name = 'DataSetTarget'


class Dimension(EmptyType):
    __hash__ = EmptyType.__hash__
    subclass = None
    superclass = EmptyType

    def __init__(self, gds_collector_=None, **kwargs_):
        super(EmptyType, self).__init__(gds_collector_, **kwargs_)
        self._name = 'EmptyType'


class DimensionDescriptor(EmptyType):
    __hash__ = EmptyType.__hash__
    subclass = None
    superclass = EmptyType

    def __init__(self, gds_collector_=None, **kwargs_):
        super(DimensionDescriptor, self).__init__(gds_collector_, **kwargs_)
        self._name = 'DimensionDescriptor'


class DimensionDescriptorValuesTarget(EmptyType):
    __hash__ = EmptyType.__hash__
    subclass = None
    superclass = EmptyType

    def __init__(self, gds_collector_=None, **kwargs_):
        super(DimensionDescriptorValuesTarget, self).__init__(gds_collector_, **kwargs_)
        self._name = 'DimensionDescriptorValuesTarget'


class GroupDimensionDescriptor(EmptyType):
    __hash__ = EmptyType.__hash__
    subclass = None
    superclass = EmptyType

    def __init__(self, gds_collector_=None, **kwargs_):
        super(GroupDimensionDescriptor, self).__init__(gds_collector_, **kwargs_)
        self._name = 'GroupDimensionDescriptor'


class HierarchicalCode(EmptyType):
    __hash__ = EmptyType.__hash__
    subclass = None
    superclass = EmptyType

    def __init__(self, gds_collector_=None, **kwargs_):
        super(HierarchicalCode, self).__init__(gds_collector_, **kwargs_)
        self._name = 'HierarchicalCode'


class HierarchicalCodelist(EmptyType):
    __hash__ = EmptyType.__hash__
    subclass = None
    superclass = EmptyType

    def __init__(self, gds_collector_=None, **kwargs_):
        super(HierarchicalCodelist, self).__init__(gds_collector_, **kwargs_)
        self._name = 'HierarchicalCodelist'


class Hierarchy(EmptyType):
    __hash__ = EmptyType.__hash__
    subclass = None
    superclass = EmptyType

    def __init__(self, gds_collector_=None, **kwargs_):
        super(Hierarchy, self).__init__(gds_collector_, **kwargs_)
        self._name = 'Hierarchy'


class HybridCodelistMap(EmptyType):
    __hash__ = EmptyType.__hash__
    subclass = None
    superclass = EmptyType

    def __init__(self, gds_collector_=None, **kwargs_):
        super(HybridCodelistMap, self).__init__(gds_collector_, **kwargs_)
        self._name = 'HybridCodelistMap'


class HybridCodeMap(EmptyType):
    __hash__ = EmptyType.__hash__
    subclass = None
    superclass = EmptyType

    def __init__(self, gds_collector_=None, **kwargs_):
        super(HybridCodeMap, self).__init__(gds_collector_, **kwargs_)
        self._name = 'HybridCodeMap'


class IdentifiableObjectTarget(EmptyType):
    __hash__ = EmptyType.__hash__
    subclass = None
    superclass = EmptyType

    def __init__(self, gds_collector_=None, **kwargs_):
        super(IdentifiableObjectTarget, self).__init__(gds_collector_, **kwargs_)
        self._name = 'IdentifiableObjectTarget'


class Level(EmptyType):
    __hash__ = EmptyType.__hash__
    subclass = None
    superclass = EmptyType

    def __init__(self, gds_collector_=None, **kwargs_):
        super(Level, self).__init__(gds_collector_, **kwargs_)
        self._name = 'Level'


class MeasureDescriptor(EmptyType):
    __hash__ = EmptyType.__hash__
    subclass = None
    superclass = EmptyType

    def __init__(self, gds_collector_=None, **kwargs_):
        super(MeasureDescriptor, self).__init__(gds_collector_, **kwargs_)
        self._name = 'MeasureDescriptor'


class MeasureDimension(EmptyType):
    __hash__ = EmptyType.__hash__
    subclass = None
    superclass = EmptyType

    def __init__(self, gds_collector_=None, **kwargs_):
        super(MeasureDimension, self).__init__(gds_collector_, **kwargs_)
        self._name = 'MeasureDimension'


class Metadataflow(EmptyType):
    __hash__ = EmptyType.__hash__
    subclass = None
    superclass = EmptyType

    def __init__(self, gds_collector_=None, **kwargs_):
        super(Metadataflow, self).__init__(gds_collector_, **kwargs_)
        self._name = 'Metadataflow'


class MetadataAttribute(EmptyType):
    __hash__ = EmptyType.__hash__
    subclass = None
    superclass = EmptyType

    def __init__(self, gds_collector_=None, **kwargs_):
        super(MetadataAttribute, self).__init__(gds_collector_, **kwargs_)
        self._name = 'MetadataAttribute'


class MetadataSet(EmptyType):
    __hash__ = EmptyType.__hash__
    subclass = None
    superclass = EmptyType

    def __init__(self, gds_collector_=None, **kwargs_):
        super(MetadataSet, self).__init__(gds_collector_, **kwargs_)
        self._name = 'MetadataSet'


class MetadataStructure(EmptyType):
    __hash__ = EmptyType.__hash__
    subclass = None
    superclass = EmptyType

    def __init__(self, gds_collector_=None, **kwargs_):
        super(MetadataStructure, self).__init__(gds_collector_, **kwargs_)
        self._name = 'MetadataStructure'


class MetadataTarget(EmptyType):
    __hash__ = EmptyType.__hash__
    subclass = None
    superclass = EmptyType

    def __init__(self, gds_collector_=None, **kwargs_):
        super(MetadataTarget, self).__init__(gds_collector_, **kwargs_)
        self._name = 'MetadataTarget'


class OrganisationMap(EmptyType):
    __hash__ = EmptyType.__hash__
    subclass = None
    superclass = EmptyType

    def __init__(self, gds_collector_=None, **kwargs_):
        super(OrganisationMap, self).__init__(gds_collector_, **kwargs_)
        self._name = 'OrganisationMap'


class OrganisationSchemeMap(EmptyType):
    __hash__ = EmptyType.__hash__
    subclass = None
    superclass = EmptyType

    def __init__(self, gds_collector_=None, **kwargs_):
        super(OrganisationSchemeMap, self).__init__(gds_collector_, **kwargs_)
        self._name = 'OrganisationSchemeMap'


class OrganisationUnit(EmptyType):
    __hash__ = EmptyType.__hash__
    subclass = None
    superclass = EmptyType

    def __init__(self, gds_collector_=None, **kwargs_):
        super(OrganisationUnit, self).__init__(gds_collector_, **kwargs_)
        self._name = 'OrganisationUnit'


class OrganisationUnitScheme(EmptyType):
    __hash__ = EmptyType.__hash__
    subclass = None
    superclass = EmptyType

    def __init__(self, gds_collector_=None, **kwargs_):
        super(OrganisationUnitScheme, self).__init__(gds_collector_, **kwargs_)
        self._name = 'OrganisationUnitScheme'


class PrimaryMeasure(EmptyType):
    __hash__ = EmptyType.__hash__
    subclass = None
    superclass = EmptyType

    def __init__(self, gds_collector_=None, **kwargs_):
        super(PrimaryMeasure, self).__init__(gds_collector_, **kwargs_)
        self._name = 'PrimaryMeasure'


class Process(EmptyType):
    __hash__ = EmptyType.__hash__
    subclass = None
    superclass = EmptyType

    def __init__(self, gds_collector_=None, **kwargs_):
        super(Process, self).__init__(gds_collector_, **kwargs_)
        self._name = 'Process'


class ProcessStep(EmptyType):
    __hash__ = EmptyType.__hash__
    subclass = None
    superclass = EmptyType

    def __init__(self, gds_collector_=None, **kwargs_):
        super(ProcessStep, self).__init__(gds_collector_, **kwargs_)
        self._name = 'ProcessStep'


class ProvisionAgreement(EmptyType):
    __hash__ = EmptyType.__hash__
    subclass = None
    superclass = EmptyType

    def __init__(self, gds_collector_=None, **kwargs_):
        super(ProvisionAgreement, self).__init__(gds_collector_, **kwargs_)
        self._name = 'ProvisionAgreement'


class ReportingCategory(EmptyType):
    __hash__ = EmptyType.__hash__
    subclass = None
    superclass = EmptyType

    def __init__(self, gds_collector_=None, **kwargs_):
        super(ReportingCategory, self).__init__(gds_collector_, **kwargs_)
        self._name = 'ReportingCategory'


class ReportingCategoryMap(EmptyType):
    __hash__ = EmptyType.__hash__
    subclass = None
    superclass = EmptyType

    def __init__(self, gds_collector_=None, **kwargs_):
        super(ReportingCategoryMap, self).__init__(gds_collector_, **kwargs_)
        self._name = 'ReportingCategoryMap'


class ReportingTaxonomy(EmptyType):
    __hash__ = EmptyType.__hash__
    subclass = None
    superclass = EmptyType

    def __init__(self, gds_collector_=None, **kwargs_):
        super(ReportingTaxonomy, self).__init__(gds_collector_, **kwargs_)
        self._name = 'ReportingTaxonomy'


class ReportingTaxonomyMap(EmptyType):
    __hash__ = EmptyType.__hash__
    subclass = None
    superclass = EmptyType

    def __init__(self, gds_collector_=None, **kwargs_):
        super(ReportingTaxonomyMap, self).__init__(gds_collector_, **kwargs_)
        self._name = 'ReportingTaxonomyMap'


class ReportPeriodTarget(EmptyType):
    __hash__ = EmptyType.__hash__
    subclass = None
    superclass = EmptyType

    def __init__(self, gds_collector_=None, **kwargs_):
        super(ReportPeriodTarget, self).__init__(gds_collector_, **kwargs_)
        self._name = 'ReportPeriodTarget'


class ReportStructure(EmptyType):
    __hash__ = EmptyType.__hash__
    subclass = None
    superclass = EmptyType

    def __init__(self, gds_collector_=None, **kwargs_):
        super(ReportStructure, self).__init__(gds_collector_, **kwargs_)
        self._name = 'ReportStructure'


class StructureMap(EmptyType):
    __hash__ = EmptyType.__hash__
    subclass = None
    superclass = EmptyType

    def __init__(self, gds_collector_=None, **kwargs_):
        super(StructureMap, self).__init__(gds_collector_, **kwargs_)
        self._name = 'StructureMap'


class StructureSet(EmptyType):
    __hash__ = EmptyType.__hash__
    subclass = None
    superclass = EmptyType

    def __init__(self, gds_collector_=None, **kwargs_):
        super(StructureSet, self).__init__(gds_collector_, **kwargs_)
        self._name = 'StructureSet'


class TimeDimension(EmptyType):
    __hash__ = EmptyType.__hash__
    subclass = None
    superclass = EmptyType

    def __init__(self, gds_collector_=None, **kwargs_):
        super(TimeDimension, self).__init__(gds_collector_, **kwargs_)
        self._name = 'TimeDimension'


class Transition(EmptyType):
    __hash__ = EmptyType.__hash__
    subclass = None
    superclass = EmptyType

    def __init__(self, gds_collector_=None, **kwargs_):
        super(Transition, self).__init__(gds_collector_, **kwargs_)
        self._name = 'Transition'
