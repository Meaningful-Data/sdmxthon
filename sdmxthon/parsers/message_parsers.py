from .data_generic import DataSetType as GenericDataSet, TimeSeriesDataSetType as GenericTimeSeriesDataSet
from .data_parser import DataParser, Validate_simpletypes_
from .data_structure import DataSetType as StructureDataSet, \
    TimeSeriesDataSetType as StructureTimeSeriesDataSet
from .footer_parser import FooterType
from .gdscollector import datetime_, GdsCollector
from ..model.component import DataStructureDefinition, LocalisedString
# from ..common.annotations import LocalisedString
from ..model.data_structure import GenericDataStructureType
from ..model.itemScheme import Codelist, AgencyScheme, ConceptScheme
from ..model.references import DataProviderReferenceType
from ..utils.xml_base import BaseStrType_, encode_str_2_3, find_attr_value_, cast


class ContactType(DataParser):
    """ContactType provides defines the contact information about a party."""
    __hash__ = DataParser.__hash__
    subclass = None
    superclass = None

    def __init__(self, Name=None, Department=None, Role=None, Telephone=None, Fax=None, X400=None, URI=None, Email=None,
                 gds_collector_=None, **kwargs_):
        super(ContactType, self).__init__(gds_collector_)
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.parent_object_ = kwargs_.get('parent_object_')

        if Name is None:
            self._Name = []
        else:
            self._Name = Name

        self._name_nsprefix_ = None

        if Department is None:
            self._department = []
        else:
            self._department = Department

        self._department_nsprefix_ = None

        if Role is None:
            self._role = []
        else:
            self._role = Role

        self._role_nsprefix_ = None

        if Telephone is None:
            self._telephone = []
        else:
            self._telephone = Telephone

        self._telephone_nsprefix_ = None

        if Fax is None:
            self._fax = []
        else:
            self._fax = Fax

        self._fax_nsprefix_ = None

        if X400 is None:
            self._x400 = []
        else:
            self._x400 = X400

        self._x400_nsprefix_ = None

        if URI is None:
            self._uri = []
        else:
            self._uri = URI

        self.URI_nsprefix_ = None

        if Email is None:
            self._email = []
        else:
            self._email = Email

        self._email_nsprefix_ = None
        self._namespacedef = 'xmlns:message="http://www.sdmx.org/resources/sdmxml/schemas/v2_1/message"'
        self._namespaceprefix = 'message'
        self._name = 'ContactType'

    @staticmethod
    def factory(*args_, **kwargs_):
        return ContactType(*args_, **kwargs_)

    @property
    def name(self):
        return self._Name

    @name.setter
    def name(self, value):
        if value is None:
            self._Name = []
        elif isinstance(value, list):
            self._Name = value
        else:
            raise TypeError('Name must be a list')

    def add_Name(self, value):
        self._Name.append(value)

    def insert_Name_at(self, index, value):
        self._Name.insert(index, value)

    def replace_Name_at(self, index, value):
        self._Name[index] = value

    @property
    def department(self):
        return self._department

    @department.setter
    def department(self, value):
        if value is None:
            self._department = []
        elif isinstance(value, list):
            self._department = value
        else:
            raise TypeError('Department must be a list')

    def add_Department(self, value):
        self._department.append(value)

    def insert_Department_at(self, index, value):
        self._department.insert(index, value)

    def replace_Department_at(self, index, value):
        self._department[index] = value

    @property
    def role(self):
        return self._role

    @role.setter
    def role(self, value):
        if value is None:
            self._role = []
        elif isinstance(value, list):
            self._role = value
        else:
            raise TypeError('Role must be a list')

    def add_Role(self, value):
        self._role.append(value)

    def insert_Role_at(self, index, value):
        self._role.insert(index, value)

    def replace_Role_at(self, index, value):
        self._role[index] = value

    @property
    def telephone(self):
        return self._telephone

    @telephone.setter
    def telephone(self, value):
        if value is None:
            self._telephone = []
        elif isinstance(value, list):
            self._telephone = value
        else:
            raise TypeError('Telephone must be a list')

    def add_Telephone(self, value):
        self._telephone.append(value)

    def insert_Telephone_at(self, index, value):
        self._telephone.insert(index, value)

    def replace_Telephone_at(self, index, value):
        self._telephone[index] = value

    @property
    def fax(self):
        return self._fax

    @fax.setter
    def fax(self, value):
        if value is None:
            self._fax = []
        elif isinstance(value, list):
            self._fax = value
        else:
            raise TypeError('Fax must be a list')

    def add_Fax(self, value):
        self._fax.append(value)

    def insert_Fax_at(self, index, value):
        self._fax.insert(index, value)

    def replace_Fax_at(self, index, value):
        self._fax[index] = value

    @property
    def X400(self):
        return self._x400

    @X400.setter
    def X400(self, value):
        if value is None:
            self._x400 = []
        elif isinstance(value, list):
            self._x400 = value
        else:
            raise TypeError('X400 must be a list')

    def add_X400(self, value):
        self._x400.append(value)

    def insert_X400_at(self, index, value):
        self._x400.insert(index, value)

    def replace_X400_at(self, index, value):
        self._x400[index] = value

    @property
    def URI(self):
        return self._uri

    @URI.setter
    def URI(self, value):
        if value is None:
            self._uri = []
        elif isinstance(value, list):
            self._uri = value
        else:
            raise TypeError('URI must be a list')

    def add_URI(self, value):
        self._uri.append(value)

    def insert_URI_at(self, index, value):
        self._uri.insert(index, value)

    def replace_URI_at(self, index, value):
        self._uri[index] = value

    @property
    def email(self):
        return self._email

    @email.setter
    def email(self, value):
        if value is None:
            self._email = []
        elif isinstance(value, list):
            self._email = value
        else:
            raise TypeError('Email must be a list')

    def add_Email(self, value):
        self._email.append(value)

    def insert_Email_at(self, index, value):
        self._email.insert(index, value)

    def replace_Email_at(self, index, value):
        self._email[index] = value

    def has_content_(self):
        if (
                self._Name or
                self._department or
                self._role or
                self._telephone or
                self._fax or
                self._x400 or
                self._uri or
                self._email
        ):
            return True
        else:
            return False

    def build_children(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'Name':
            class_obj_ = self.get_class_obj_(child_, LocalisedString)
            obj_ = class_obj_.factory()
            obj_.build(child_, gds_collector_=gds_collector_)
            self._Name.append(obj_)
            obj_.original_tag_name_ = 'Name'

        elif nodeName_ == 'Department':
            class_obj_ = self.get_class_obj_(child_, LocalisedString)
            obj_ = class_obj_.factory()
            obj_.build(child_, gds_collector_=gds_collector_)
            self._department.append(obj_)
            obj_.original_tag_name_ = 'Department'

        elif nodeName_ == 'Role':
            class_obj_ = self.get_class_obj_(child_, LocalisedString)
            obj_ = class_obj_.factory()
            obj_.build(child_, gds_collector_=gds_collector_)
            self._role.append(obj_)
            obj_.original_tag_name_ = 'Role'

        elif nodeName_ == 'Telephone':
            value_ = child_.text
            value_ = self.gds_parse_string(value_)
            value_ = self.gds_validate_string(value_)
            self._telephone.append(value_)
            self._telephone_nsprefix_ = child_.prefix

        elif nodeName_ == 'Fax':
            value_ = child_.text
            value_ = self.gds_parse_string(value_)
            value_ = self.gds_validate_string(value_)
            self._fax.append(value_)
            self._fax_nsprefix_ = child_.prefix

        elif nodeName_ == 'X400':
            value_ = child_.text
            value_ = self.gds_parse_string(value_)
            value_ = self.gds_validate_string(value_)
            self._x400.append(value_)
            self._x400_nsprefix_ = child_.prefix

        elif nodeName_ == 'URI':
            value_ = child_.text
            value_ = self.gds_parse_string(value_)
            value_ = self.gds_validate_string(value_)
            self._uri.append(value_)
            self.URI_nsprefix_ = child_.prefix

        elif nodeName_ == 'Email':
            value_ = child_.text
            value_ = self.gds_parse_string(value_)
            value_ = self.gds_validate_string(value_)
            self._email.append(value_)
            self._email_nsprefix_ = child_.prefix


# end class ContactType

class PartyType(DataParser):
    """PartyType defines the information which is sent about various parties
    such as senders and receivers of messages.The id_ attribute holds the
    identification of the party."""
    __hash__ = DataParser.__hash__
    subclass = None
    superclass = None

    def __init__(self, id_=None, Name=None, Contact=None, extensiontype_=None, gds_collector_=None, **kwargs_):
        super(PartyType, self).__init__(gds_collector_, **kwargs_)
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self._id = cast(None, id_)
        self._id_nsprefix_ = None

        if Name is None:
            self._Name = []
        else:
            self._Name = Name

        self._name_nsprefix_ = None

        if Contact is None:
            self._contact = []
        else:
            self._contact = Contact

        self.Contact_nsprefix_ = None
        self._extensiontype_ = extensiontype_
        self._namespacedef = 'xmlns:message="http://www.sdmx.org/resources/sdmxml/schemas/v2_1/message"'
        self._namespaceprefix = 'message'

    @staticmethod
    def factory(*args_, **kwargs_):
        return PartyType(*args_, **kwargs_)

    @property
    def name(self):
        return self._Name

    @name.setter
    def name(self, value):
        if value is None:
            self._Name = []
        elif isinstance(value, list):
            self._Name = value
        else:
            raise TypeError('Name must be a list')

    def add_Name(self, value):
        self._Name.append(value)

    def insert_Name_at(self, index, value):
        self._Name.insert(index, value)

    def replace_Name_at(self, index, value):
        self._Name[index] = value

    @property
    def contact(self):
        return self._contact

    @contact.setter
    def contact(self, value):
        if value is None:
            self._contact = []
        elif isinstance(value, list):
            self._contact = value
        else:
            raise TypeError('Contact must be a list')

    def add_Contact(self, value):
        self._contact.append(value)

    def insert_Contact_at(self, index, value):
        self._contact.insert(index, value)

    def replace_Contact_at(self, index, value):
        self._contact[index] = value

    @property
    def id_(self):
        return self._id

    @id_.setter
    def id_(self, value):
        self._id = value

    @property
    def extensiontype(self):
        return self._extensiontype_

    @extensiontype.setter
    def extensiontype(self, value):
        self._extensiontype_ = value

    def has_content_(self):
        if (
                self._Name or
                self._contact
        ):
            return True
        else:
            return False

    def export_attributes_as_dict(self, parent_dict: dict, data: list, valid_fields: list):
        pass

    def build_attributes(self, node, attrs, already_processed):
        value = find_attr_value_('id', node)
        if value is not None and 'id' not in already_processed:
            already_processed.add('id')
            self._id = value
            self.validate_id_type(self._id)
        # validate dim_type IDType
        value = find_attr_value_('xsi:dim_type', node)
        if value is not None and 'xsi:dim_type' not in already_processed:
            already_processed.add('xsi:dim_type')
            self._extensiontype_ = value

    def build_children(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'Name':
            class_obj_ = self.get_class_obj_(child_, LocalisedString)
            obj_ = class_obj_.factory()
            obj_.build(child_, gds_collector_=gds_collector_)
            self._Name.append(obj_)
            obj_.original_tag_name_ = 'Name'
        elif nodeName_ == 'Contact':
            obj_ = ContactType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self._contact.append(obj_)
            obj_.original_tag_name_ = 'Contact'


# end class PartyType

class SenderType(PartyType):
    """SenderType extends the basic party structure to add an optional time
    zone declaration."""
    __hash__ = PartyType.__hash__
    subclass = None
    superclass = PartyType

    def __init__(self, id_=None, Name=None, Contact=None, Timezone=None, gds_collector_=None, **kwargs_):
        super(SenderType, self).__init__(id_, Name, Contact, gds_collector_, **kwargs_)
        self._timezone = Timezone
        self.validate_TimezoneType(self._timezone)
        self.Timezone_nsprefix_ = None
        self._namespacedef = 'xmlns:message="http://www.sdmx.org/resources/sdmxml/schemas/v2_1/message" ' \
                             'xmlns:common="http://www.sdmx.org/resources/sdmxml/schemas/v2_1/common" '
        self._name = 'SenderType'

    @staticmethod
    def factory(*args_, **kwargs_):
        return SenderType(*args_, **kwargs_)

    @property
    def timezone(self):
        return self._timezone

    @timezone.setter
    def timezone(self, value):
        self._timezone = value

    def validate_TimezoneType(self, value):
        result = True
        # Validate dim_type TimezoneType, a restriction on xs:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_line_number_()
                self.gds_collector_.add_message(
                    f'Value "{value}": {lineno} is not of the correct base simple dim_type (str)')
                return False
            if not self.gds_validate_simple_patterns(
                    self.validate_TimezoneType_patterns_, value):
                self.gds_collector_.add_message(f'Value "{encode_str_2_3(value)}" '
                                                f'does not match xsd pattern restrictions: '
                                                f'{self.__validate_IDType_patterns}')
                result = False
        return result

    validate_TimezoneType_patterns_ = [['^(Z)$', '^((\\+|\\-)(14:00|((0[0-9]|1[0-3]):[0-5][0-9])))$']]

    def has_content_(self):
        if (
                self._timezone is not None or
                super(SenderType, self).has_content_()
        ):
            return True
        else:
            return False

    def build_attributes(self, node, attrs, already_processed):
        super(SenderType, self).build_attributes(node, attrs, already_processed)

    def build_children(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'Timezone':
            value_ = child_.text
            value_ = self.gds_parse_string(value_)
            value_ = self.gds_validate_string(value_)
            self._timezone = value_
            self.Timezone_nsprefix_ = child_.prefix
            # validate dim_type TimezoneType
            self.validate_TimezoneType(self._timezone)
        super(SenderType, self).build_children(child_, node, nodeName_, True)


# end class SenderType

class BaseHeaderType(DataParser):
    """BaseHeaderType in an abstract base dim_type that defines the basis for all
    message headers. Specific message formats will refine this"""
    __hash__ = DataParser.__hash__
    subclass = None
    superclass = None

    def __init__(self, ID=None, Test=False, Prepared=None, Sender=None, Receiver=None, Name=None, Structure=None,
                 DataProvider=None, DataSetAction=None, DataSetID=None, Extracted=None, ReportingBegin=None,
                 ReportingEnd=None, EmbargoDate=None, Source=None, gds_collector_=None, **kwargs_):
        super(BaseHeaderType, self).__init__(gds_collector_, **kwargs_)
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self._ID = ID
        self.validate_id_type(self._ID)
        self._ID_nsprefix_ = "message"
        self._Test = Test
        self._Test_nsprefix_ = "message"
        self._Prepared = Prepared
        self.validate_HeaderTimeType(self._Prepared)
        self._Prepared_nsprefix_ = "message"
        self._Sender = Sender
        self._Sender_nsprefix_ = "message"

        if Receiver is None:
            self._Receiver = []
        else:
            self._Receiver = Receiver

        self._Receiver_nsprefix_ = None

        if Name is None:
            self._Name = []
        else:
            self._Name = Name

        self._name_nsprefix_ = None

        if Structure is None:
            self._structure = {}
        else:
            self._structure = Structure

        self._structure_nsprefix_ = None
        self._dataProvider = DataProvider
        self._dataProvider_nsprefix_ = None
        self._DataSetAction = DataSetAction
        self.validate_ActionType(self._DataSetAction)
        self.DataSetAction_nsprefix_ = None

        if DataSetID is None:
            self._DataSetID = []
        else:
            self._DataSetID = DataSetID

        self._DataSetID_nsprefix_ = None

        if isinstance(Extracted, BaseStrType_):
            initvalue_ = datetime_.datetime.strptime(Extracted, '%Y-%m-%dT%H:%M:%S')
        else:
            initvalue_ = Extracted

        self._Extracted = initvalue_
        self._Extracted_nsprefix_ = None
        self._ReportingBegin = ReportingBegin
        self.validate_ObservationalTimePeriodType(self._ReportingBegin)
        self._ReportingBegin_nsprefix_ = None
        self._ReportingEnd = ReportingEnd
        self.validate_ObservationalTimePeriodType(self._ReportingEnd)
        self._ReportingEnd_nsprefix_ = None

        if isinstance(EmbargoDate, BaseStrType_):
            initvalue_ = datetime_.datetime.strptime(EmbargoDate, '%Y-%m-%dT%H:%M:%S')
        else:
            initvalue_ = EmbargoDate

        self._EmbargoDate = initvalue_
        self._EmbargoDate_nsprefix_ = None

        if Source is None:
            self._Source = []
        else:
            self._Source = Source

        self._Source_nsprefix_ = None
        self._namespacedef = 'xmlns:message="http://www.sdmx.org/resources/sdmxml/schemas/v2_1/message"'
        self._namespace_prefix = 'message'
        self._name = 'BaseHeaderType'

    @staticmethod
    def factory(*args_, **kwargs_):
        return BaseHeaderType(*args_, **kwargs_)

    @property
    def id_(self):
        return self._ID

    @id_.setter
    def id_(self, value):
        self._ID = value

    @property
    def test(self):
        return self._Test

    @test.setter
    def test(self, value):
        self._Test = value

    @property
    def prepared(self):
        return self._Prepared

    @prepared.setter
    def prepared(self, value):
        self._Prepared = value

    @property
    def sender(self):
        return self._Sender

    @sender.setter
    def sender(self, value):
        self._Sender = value
        self._Sender._namespace_prefix = 'message'

    @property
    def receiver(self):
        return self._Receiver

    @receiver.setter
    def receiver(self, value):
        if value is None:
            self._Receiver = []
        elif isinstance(value, list):
            self._Receiver = value
        else:
            raise TypeError('Receiver must be a list')

    def add_Receiver(self, value):
        value._namespace_prefix = 'message'
        self._Receiver.append(value)

    def insert_Receiver_at(self, index, value):
        value._namespace_prefix = 'message'
        self._Receiver.insert(index, value)

    def replace_Receiver_at(self, index, value):
        value._namespace_prefix = 'message'
        self._Receiver[index] = value

    @property
    def name(self):
        return self._Name

    @name.setter
    def name(self, value):
        if value is None:
            self._Name = []
        elif isinstance(value, list):
            self._Name = value
        else:
            raise TypeError('Name must be a list')

    def add_Name(self, value):
        self._Name.append(value)

    def insert_Name_at(self, index, value):
        value._namespace_prefix = 'message'
        self._Name.insert(index, value)

    def replace_Name_at(self, index, value):
        value._namespace_prefix = 'message'
        self._Name[index] = value

    @property
    def structure(self):
        return self._structure

    @structure.setter
    def structure(self, value):
        if value is None:
            self._structure = {}
        elif isinstance(value, dict):
            self._structure = value
        else:
            raise TypeError('Structure must be a dict')

    @property
    def dataProvider(self):
        return self._dataProvider

    @dataProvider.setter
    def dataProvider(self, value):
        self._dataProvider = value

    @property
    def datasetAction(self):
        return self._DataSetAction

    @datasetAction.setter
    def datasetAction(self, value):
        self._DataSetAction = value

    @property
    def datasetID(self):
        return self._DataSetID

    @datasetID.setter
    def datasetID(self, value):
        if value is None:
            self._DataSetID = []
        elif isinstance(value, list):
            self._DataSetID = value
        else:
            raise TypeError('DatasetID must be a list')

    def add_DataSetID(self, value):
        self._DataSetID.append(value)

    def insert_DataSetID_at(self, index, value):
        self._DataSetID.insert(index, value)

    def replace_DataSetID_at(self, index, value):
        self._DataSetID[index] = value

    @property
    def extracted(self):
        return self._Extracted

    @extracted.setter
    def extracted(self, value):
        self._Extracted = value

    @property
    def reportingBegin(self):
        return self._ReportingBegin

    @reportingBegin.setter
    def reportingBegin(self, value):
        self._ReportingBegin = value

    @property
    def reportingEnd(self):
        return self._ReportingEnd

    @reportingEnd.setter
    def reportingEnd(self, value):
        self._ReportingEnd = value

    @property
    def embargoDate(self):
        return self._EmbargoDate

    @embargoDate.setter
    def embargoDate(self, value):
        self._EmbargoDate = value

    @property
    def source(self):
        return self._Source

    @source.setter
    def source(self, value):
        if value is None:
            self._Source = []
        elif isinstance(value, list):
            self._Source = value
        else:
            raise TypeError('Source must be a list')

    def add_Source(self, value):
        self._Source.append(value)

    def insert_Source_at(self, index, value):
        self._Source.insert(index, value)

    def replace_Source_at(self, index, value):
        self._Source[index] = value

    def validate_HeaderTimeType(self, value):
        result = True
        # Validate dim_type HeaderTimeType, a restriction on None.
        return result

    def validate_ActionType(self, value):
        result = True
        # Validate dim_type ActionType, a restriction on xs:NMTOKEN.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_line_number_()
                self.gds_collector_.add_message(f'Value "{value}" : {lineno} is not of '
                                                f'the correct base simple dim_type (str)')
                return False
            value = value
            enumerations = ['Append', 'Replace', 'Delete', 'Information']
            if value not in enumerations:
                lineno = self.gds_get_node_line_number_()
                self.gds_collector_.add_message(
                    f'Value "{encode_str_2_3(value)}":{lineno} does not match xsd enumeration '
                    f'restriction on ActionType')
                result = False
        return result

    def validate_ObservationalTimePeriodType(self, value):
        pass

    def has_content_(self):
        if (
                self._ID is not None or
                self._Test or
                self._Prepared is not None or
                self._Sender is not None or
                self._Receiver or
                self._Name or
                self._structure or
                self._dataProvider is not None or
                self._DataSetAction is not None or
                self._DataSetID or
                self._Extracted is not None or
                self._ReportingBegin is not None or
                self._ReportingEnd is not None or
                self._EmbargoDate is not None or
                self._Source
        ):
            return True
        else:
            return False

    def build_children(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'ID':
            value_ = child_.text
            value_ = self.gds_parse_string(value_)
            value_ = self.gds_validate_string(value_)
            self._ID = value_
            self._ID_nsprefix_ = child_.prefix
            # validate dim_type IDType
            self.validate_id_type(self._ID)
        elif nodeName_ == 'Test':
            sval_ = child_.text
            ival_ = self.gds_parse_boolean(sval_)
            ival_ = self.gds_validate_boolean(ival_)
            self._Test = ival_
            self._Test_nsprefix_ = child_.prefix
        elif nodeName_ == 'Prepared':
            value_ = child_.text
            value_ = self.gds_parse_string(value_)
            value_ = self.gds_validate_string(value_)
            self._Prepared = value_
            self._Prepared_nsprefix_ = child_.prefix
            # validate dim_type HeaderTimeType
            self.validate_HeaderTimeType(self._Prepared)
        elif nodeName_ == 'Sender':
            obj_ = SenderType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self._Sender = obj_
            obj_.original_tagname_ = 'Sender'
        elif nodeName_ == 'Receiver':
            class_obj_ = self.get_class_obj_(child_, PartyType)
            obj_ = class_obj_.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self._Receiver.append(obj_)
            obj_.original_tag_name_ = 'Receiver'
        elif nodeName_ == 'Name':
            class_obj_ = self.get_class_obj_(child_, LocalisedString)
            obj_ = class_obj_.factory()
            obj_.build(child_, gds_collector_=gds_collector_)
            self._Name.append(obj_)
            obj_.original_tag_name_ = 'Name'
        elif nodeName_ == 'Structure':
            obj_ = GenericDataStructureType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self._structure[obj_.structureID] = {'dimAtObs': obj_.dimensionAtObservation, 'DSDID': obj_.structure}
        elif nodeName_ == 'DataProvider':
            obj_ = DataProviderReferenceType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self._dataProvider = obj_
            obj_.original_tag_name_ = 'DataProvider'
        elif nodeName_ == 'DataSetAction':
            value_ = child_.text
            value_ = self.gds_parse_string(value_)
            value_ = self.gds_validate_string(value_)
            self._DataSetAction = value_
            self.DataSetAction_nsprefix_ = child_.prefix
            # validate dim_type ActionType
            self.validate_ActionType(self._DataSetAction)
        elif nodeName_ == 'DataSetID':
            value_ = child_.text
            value_ = self.gds_parse_string(value_)
            value_ = self.gds_validate_string(value_)
            self._DataSetID.append(value_)
            self._DataSetID_nsprefix_ = child_.prefix
            # validate dim_type IDType
            self.validate_id_type(self._DataSetID[-1])
        elif nodeName_ == 'Extracted':
            sval_ = child_.text
            dval_ = self.gds_parse_datetime(sval_)
            self._Extracted = dval_
            self._Extracted_nsprefix_ = child_.prefix
        elif nodeName_ == 'ReportingBegin':
            value_ = child_.text
            value_ = self.gds_parse_string(value_)
            value_ = self.gds_validate_string(value_)
            self._ReportingBegin = value_
            self._ReportingBegin_nsprefix_ = child_.prefix
            # validate dim_type ObservationalTimePeriodType
            self.validate_ObservationalTimePeriodType(self._ReportingBegin)
        elif nodeName_ == 'ReportingEnd':
            value_ = child_.text
            value_ = self.gds_parse_string(value_)
            value_ = self.gds_validate_string(value_)
            self._ReportingEnd = value_
            self._ReportingEnd_nsprefix_ = child_.prefix
            # validate dim_type ObservationalTimePeriodType
            self.validate_ObservationalTimePeriodType(self._ReportingEnd)
        elif nodeName_ == 'EmbargoDate':
            sval_ = child_.text
            dval_ = self.gds_parse_datetime(sval_)
            self._EmbargoDate = dval_
            self._EmbargoDate_nsprefix_ = child_.prefix
        elif nodeName_ == 'Source':
            class_obj_ = self.get_class_obj_(child_, LocalisedString)
            obj_ = class_obj_.factory()
            obj_.build(child_, gds_collector_=gds_collector_)
            self._Source.append(obj_)
            obj_.original_tag_name_ = 'Source'


# end class BaseHeaderType

class GenericDataHeaderType(BaseHeaderType):
    """GenericDataHeaderType defines the header structure for a generic data
    message."""
    __hash__ = DataParser.__hash__
    subclass = None
    superclass = BaseHeaderType

    def __init__(self, ID=None, Test=False, Prepared=None, Sender=None, Receiver=None, Name=None, Structure=None,
                 DataProvider=None, DataSetAction=None, DataSetID=None, Extracted=None, ReportingBegin=None,
                 ReportingEnd=None, EmbargoDate=None, Source=None, gds_collector_=None, **kwargs_):
        super(GenericDataHeaderType, self).__init__(ID, Test, Prepared, Sender, Receiver, Name, Structure, DataProvider,
                                                    DataSetAction, DataSetID, Extracted, ReportingBegin, ReportingEnd,
                                                    EmbargoDate, Source, gds_collector_, **kwargs_)
        self._name = 'GenericDataHeaderType'

    @staticmethod
    def factory(*args_, **kwargs_):
        return GenericDataHeaderType(*args_, **kwargs_)

    def validate_ObservationalTimePeriodType(self, value):
        pass


# end class GenericDataHeaderType

class MessageType(DataParser):
    """MessageType is an abstract dim_type which is used by all of the messages, to
    allow inheritance of common features. Every message consists of a
    mandatory header, followed by optional payload (which may occur
    multiple times), and finally an optional footer section for conveying
    error, warning, and informational messages."""
    __hash__ = DataParser.__hash__
    superclass = None

    def __init__(self, Header=None, Footer=None, gds_collector_=None, **kwargs_):
        super(MessageType, self).__init__(gds_collector_, **kwargs_)
        self._gds_collector_ = gds_collector_
        self._header = Header
        self._footer = Footer
        self._footer_nsprefix_ = None
        self._namespace_def = 'xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" ' \
                              'xmlns:message="http://www.sdmx.org/resources/sdmxml/schemas/v2_1/message" ' \
                              'xmlns:data="http://www.sdmx.org/resources/sdmxml/schemas/v2_1/data/structurespecific" ' \
                              'xmlns:common="http://www.sdmx.org/resources/sdmxml/schemas/v2_1/common"'
        self._namespace_prefix = 'message'
        self._name = 'MessageType'

    @staticmethod
    def factory(*args_, **kwargs_):
        return MessageType(**kwargs_)

    @property
    def header(self):
        return self._header

    @header.setter
    def header(self, value):
        self._header = value

    @property
    def footer(self):
        return self._footer

    @footer.setter
    def footer(self, value):
        self._footer = value

    def has_content_(self):
        if (
                self._header is not None or
                self._footer is not None
        ):
            return True
        else:
            return False


# end class MessageType

class GenericDataType(MessageType):
    """GenericDataType defines the contents of a generic data message."""
    __hash__ = DataParser.__hash__
    subclass = None
    superclass = MessageType

    def __init__(self, Header=None, Footer=None, DataSet=None, gds_collector_=None, **kwargs_):
        super(GenericDataType, self).__init__(Header, Footer, gds_collector_, **kwargs_)

        if DataSet is None:
            self._dataSet = []
        else:
            self._dataSet = DataSet

        if gds_collector_ is not None:
            self._gds_collector = gds_collector_
        else:
            self._gds_collector = GdsCollector()

    @staticmethod
    def factory(*args_, **kwargs_):
        return GenericDataType(*args_, **kwargs_)

    @property
    def dataset(self):
        return self._dataSet

    @dataset.setter
    def dataset(self, value):
        if value is None:
            self._dataSet = []
        elif isinstance(value, list):
            self._dataSet = value
        else:
            raise TypeError('Dataset must be a list')

    def add_DataSet(self, value):
        self._dataSet.append(value)

    def insert_DataSet_at(self, index, value):
        self._dataSet.insert(index, value)

    def replace_DataSet_at(self, index, value):
        self._dataSet[index] = value

    def has_content_(self):
        if (self._header is not None or self._dataSet or
                self._footer is not None or super(GenericDataType, self).has_content_()):
            return True
        else:
            return False

    def build_children(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'Header':
            obj_ = GenericDataHeaderType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self._header = obj_
            obj_.original_tagname_ = 'Header'
        elif nodeName_ == 'DataSet':
            obj_ = GenericDataSet.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self._dataSet.append(obj_)
            obj_.original_tag_name_ = 'DataSet'
        elif nodeName_ == 'Footer':
            obj_ = FooterType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self._footer = obj_
            obj_.original_tag_name_ = 'Footer'


# end class GenericDataType

class CodelistsType(DataParser):
    def __init__(self, codelist=None, name=None, gds_collector_=None, **kwargs_):
        super(CodelistsType, self).__init__(gds_collector_, **kwargs_)

        if codelist is None:
            self._codelists = {}
        else:
            self._codelists = codelist

        if name is None:
            self._name = ''
        else:
            self._name = name

        if gds_collector_ is not None:
            self._gds_collector = gds_collector_
        else:
            self._gds_collector = GdsCollector()

    @staticmethod
    def factory(*args_, **kwargs_):
        return CodelistsType(*args_, **kwargs_)

    @property
    def codelists(self):
        return self._codelists

    @codelists.setter
    def codelists(self, value):
        self._codelists = value

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    def has_content_(self):
        if self._codelists is not None or super(CodelistsType, self).has_content_():
            return True
        else:
            return False

    def build_children(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'Codelist':
            obj_ = Codelist.factory()
            obj_.build(child_, gds_collector_=gds_collector_)
            self._codelists[obj_.unique_id] = obj_


class ConceptsType(DataParser):
    def __init__(self, concepts=None, name=None, gds_collector_=None, **kwargs_):
        super(ConceptsType, self).__init__(gds_collector_, **kwargs_)

        self._cl_references = []
        if concepts is None:
            self._concepts = {}
        else:
            self._concepts = concepts

        if name is None:
            self._name = ''
        else:
            self._name = name

        if gds_collector_ is not None:
            self._gds_collector = gds_collector_
        else:
            self._gds_collector = GdsCollector()

    @staticmethod
    def factory(*args_, **kwargs_):
        return ConceptsType(*args_, **kwargs_)

    @property
    def concepts(self):
        return self._concepts

    @concepts.setter
    def concepts(self, value):
        self._concepts = value

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    def has_content_(self):
        if len(self.concepts) > 0 or super(ConceptsType, self).has_content_():
            return True
        else:
            return False

    def build_children(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'ConceptScheme':
            obj_ = ConceptScheme.factory()
            obj_.build(child_, gds_collector_=gds_collector_)
            self.concepts[obj_.unique_id] = obj_


class DataStructuresType(DataParser):
    def __init__(self, dsds=None, gds_collector_=None, **kwargs_):
        super(DataStructuresType, self).__init__(gds_collector_, **kwargs_)

        self._cl_references = []
        if dsds is None:
            self._dsds = {}
        else:
            self._dsds = dsds

        self._non_unique = None

        if gds_collector_ is not None:
            self._gds_collector = gds_collector_
        else:
            self._gds_collector = GdsCollector()

    @staticmethod
    def factory(*args_, **kwargs_):
        return DataStructuresType(*args_, **kwargs_)

    @property
    def dsds(self):
        return self._dsds

    @dsds.setter
    def dsds(self, value):
        self._dsds = value

    @property
    def non_unique(self):
        return self._non_unique

    def add_non_unique(self, id_):
        if self._non_unique is None:
            self._non_unique = []
        self._non_unique.append(id_)

    def build_children(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'DataStructure':
            obj_ = DataStructureDefinition.factory()
            obj_.build(child_, gds_collector_=gds_collector_)
            if obj_.unique_id in self.dsds:
                self.add_non_unique(obj_.unique_id)
            else:
                self.dsds[obj_.unique_id] = obj_


class OrganisationSchemesType(DataParser):
    def __init__(self, agency_scheme=None, gds_collector_=None, **kwargs_):
        super(OrganisationSchemesType, self).__init__(gds_collector_, **kwargs_)

        if agency_scheme is None:
            self._agency_schemes = []
        else:
            self._agency_schemes = agency_scheme

        if gds_collector_ is not None:
            self._gds_collector = gds_collector_
        else:
            self._gds_collector = GdsCollector()

    @staticmethod
    def factory(*args_, **kwargs_):
        return OrganisationSchemesType(*args_, **kwargs_)

    @property
    def agencySchemes(self):
        return self._agency_schemes

    @agencySchemes.setter
    def agencySchemes(self, value):
        self._agency_schemes = value

    def has_content_(self):
        if self.agencySchemes is not None or super(OrganisationSchemesType, self).has_content_():
            return True
        else:
            return False

    def build_children(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'AgencyScheme':
            obj_ = AgencyScheme.factory()
            obj_.build(child_, gds_collector_=gds_collector_)
            self.agencySchemes = obj_


class DataflowsType(DataParser):
    pass


class Structures(DataParser):
    __hash__ = DataParser.__hash__

    def __init__(self, codelists=None, concepts=None, dsds=None, organisations=None, gds_collector_=None, **kwargs_):
        super(Structures, self).__init__(gds_collector_, **kwargs_)

        if dsds is None:
            self._dsds = {}
        else:
            self._dsds = dsds

        if codelists is None:
            self._codelists = {}
        else:
            self._codelists = codelists

        self._organisations = organisations

        if concepts is None:
            self._concepts = {}
        else:
            self._concepts = concepts

        self._errors = None

        if gds_collector_ is not None:
            self._gds_collector = gds_collector_
        else:
            self._gds_collector = GdsCollector()

    @staticmethod
    def factory(*args_, **kwargs_):
        return Structures(*args_, **kwargs_)

    @property
    def organisations(self):
        return self._organisations

    @organisations.setter
    def organisations(self, value):
        self._organisations = value

    @property
    def dsds(self):
        return self._dsds

    @dsds.setter
    def dsds(self, value):
        self._dsds = value

    @property
    def codelists(self):
        return self._codelists

    @codelists.setter
    def codelists(self, value):
        self._codelists = value

    @property
    def concepts(self):
        return self._concepts

    @concepts.setter
    def concepts(self, value):
        self._concepts = value

    @property
    def errors(self):
        return self._errors

    def add_error(self, error):
        if self._errors is None:
            self._errors = []
        self._errors.append(error)

    def has_content_(self):
        if self._concepts is not None or self._codelists or self._dsds is not None \
                or super(Structures, self).has_content_():
            return True
        else:
            return False

    def build_children(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'OrganisationSchemes':
            obj_ = OrganisationSchemesType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self._organisations = obj_
        elif nodeName_ == 'Codelists':
            obj_ = CodelistsType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self._codelists = obj_.codelists
        elif nodeName_ == 'Concepts':
            obj_ = ConceptsType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self._concepts = obj_.concepts
        elif nodeName_ == 'DataStructures':
            obj_ = DataStructuresType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            if obj_.non_unique is not None:
                for e in obj_.non_unique:
                    self.add_error({'Code': 'MS06', 'ErrorLevel': 'CRITICAL',
                                    'ObjectID': f'{e}', 'ObjectType': f'DSD',
                                    'Message': f'DSD {e} is not unique'})
            self._dsds = obj_.dsds
        """
        elif nodeName_ == 'Dataflows':
            obj_ = DataflowsType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self._codelists = obj_
        """


class MetadataType(MessageType):
    __hash__ = DataParser.__hash__
    superclass = MessageType

    def __init__(self, header=None, footer=None, structures=None, gds_collector_=None, **kwargs_):
        super(MetadataType, self).__init__(header, footer, gds_collector_, **kwargs_)

        self._structures = structures

        if gds_collector_ is not None:
            self._gds_collector = gds_collector_
        else:
            self._gds_collector = GdsCollector()

    @staticmethod
    def factory(*args_, **kwargs_):
        return MetadataType(*args_, **kwargs_)

    @property
    def structures(self):
        return self._structures

    @structures.setter
    def structures(self, value):
        self._structures = value

    def has_content_(self):
        if (self._header is not None or self._structures or
                self._footer is not None or super(MetadataType, self).has_content_()):
            return True
        else:
            return False

    def build_children(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'Header':
            obj_ = GenericDataHeaderType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self._header = obj_
        elif nodeName_ == 'Structures':
            obj_ = Structures.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self._structures = obj_
        elif nodeName_ == 'Footer':
            obj_ = FooterType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self._footer = obj_


class StructureSpecificDataHeaderType(BaseHeaderType):
    """StructureSpecificDataHeaderType defines the header structure for a
    structure specific data message."""
    __hash__ = BaseHeaderType.__hash__
    subclass = None
    superclass = BaseHeaderType

    def __init__(self, ID=None, Test=False, Prepared=None, Sender=None, Receiver=None, Name=None, Structure=None,
                 DataProvider=None, DataSetAction=None, DataSetID=None, Extracted=None, ReportingBegin=None,
                 ReportingEnd=None, EmbargoDate=None, Source=None, gds_collector_=None, **kwargs_):
        super(StructureSpecificDataHeaderType, self).__init__(ID, Test, Prepared, Sender, Receiver, Name, Structure,
                                                              DataProvider, DataSetAction, DataSetID, Extracted,
                                                              ReportingBegin, ReportingEnd, EmbargoDate, Source,
                                                              gds_collector_, **kwargs_)
        self._name = 'GenericDataHeaderType'

    @staticmethod
    def factory(*args_, **kwargs_):
        return StructureSpecificDataHeaderType(*args_, **kwargs_)

    def validate_HeaderTimeType(self, value):
        result = True
        return result

    def validate_ObservationalTimePeriodType(self, value):
        result = True
        return result


# end class StructureSpecificDataHeaderType

class StructureSpecificDataType(MessageType):
    """StructureSpecificDataType defines the structure of the structure
    specific data message. Note that the data set payload dim_type is abstract,
    and therefore it will have to be assigned a dim_type in an instance. This
    dim_type must be derived from the base dim_type referenced. This base dim_type
    defines a general structure which can be followed to allow for generic
    processing of the data even if the exact details of the data structure
    specific format are not known."""
    __hash__ = MessageType.__hash__
    subclass = None
    superclass = MessageType

    def __init__(self, Header=None, Footer=None, DataSet=None, gds_collector_=None, **kwargs_):
        super(StructureSpecificDataType, self).__init__(Header, Footer, gds_collector_, **kwargs_)

        if DataSet is None:
            self._dataSet = []
        else:
            self._dataSet = DataSet
        self._name = 'StructureSpecificDataType'

        if gds_collector_ is not None:
            self.gds_collector_ = gds_collector_
        else:
            self.gds_collector_ = GdsCollector()

    @staticmethod
    def factory(*args_, **kwargs_):
        return StructureSpecificDataType(*args_, **kwargs_)

    @property
    def dataset(self):
        return self._dataSet

    @dataset.setter
    def dataset(self, value):
        if value is None:
            self._dataSet = []
        elif isinstance(value, list):
            self._dataSet = value
        else:
            raise TypeError('Dataset must be a list')

    def add_DataSet(self, value):
        self._dataSet.append(value)

    def insert_DataSet_at(self, index, value):
        self._dataSet.insert(index, value)

    def replace_DataSet_at(self, index, value):
        self._dataSet[index] = value

    def has_content_(self):
        if (self._header is not None or self._dataSet or self._footer is not None or super(MessageType,
                                                                                           self).has_content_()):
            return True
        else:
            return False

    def export_attributes_as_dict(self, valid_fields: list, **kwargs) -> list:
        data = []
        for DataSet_ in self._dataSet:
            parent_dict = {}
            DataSet_.export_attributes_as_dict(parent_dict, )

        return data

    def build_children(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'Header':
            obj_ = StructureSpecificDataHeaderType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self._header = obj_
            obj_.original_tagname_ = 'Header'
        elif nodeName_ == 'DataSet':
            obj_ = StructureDataSet.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self._dataSet.append(obj_)
            obj_.original_tag_name_ = 'DataSet'
        elif nodeName_ == 'Footer':
            obj_ = FooterType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self._footer = obj_
            obj_.original_tag_name_ = 'Footer'


# end class StructureSpecificDataType


class GenericTimeSeriesDataType(GenericDataType):
    """GenericDataType defines the contents of a generic data message."""
    __hash__ = GenericDataType.__hash__
    subclass = None
    superclass = GenericDataType

    def __init__(self, Header=None, Footer=None, DataSet=None, gds_collector_=None, **kwargs_):
        super(GenericTimeSeriesDataType, self).__init__(Header, Footer, DataSet, gds_collector_,
                                                        **kwargs_)

    @staticmethod
    def factory(*args_, **kwargs_):
        return GenericTimeSeriesDataType(*args_, **kwargs_)

    @property
    def dataset(self):
        return self._dataSet

    @dataset.setter
    def dataset(self, value):
        if value is None:
            self._dataSet = []
        elif isinstance(value, list):
            self._dataSet = value
        else:
            raise TypeError('Dataset must be a list')

    def add_DataSet(self, value):
        self._dataSet.append(value)

    def insert_DataSet_at(self, index, value):
        self._dataSet.insert(index, value)

    def replace_DataSet_at(self, index, value):
        self._dataSet[index] = value

    def has_content_(self):
        if (self._header is not None or self._dataSet or self._footer is not None
                or super(GenericDataType, self).has_content_()):
            return True
        else:
            return False

    def export_attributes_as_dict(self, valid_fields: list, **kwargs) -> list:
        data = []
        for DataSet_ in self._dataSet:
            parent_dict = {}
            DataSet_.export_attributes_as_dict(parent_dict, )

        return data

    def build_children(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'Header':
            obj_ = GenericTimeSeriesDataHeaderType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self._header = obj_
            obj_.original_tagname_ = 'Header'
        elif nodeName_ == 'DataSet':
            obj_ = GenericTimeSeriesDataSet.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self._dataSet.append(obj_)
            obj_.original_tag_name_ = 'DataSet'
        elif nodeName_ == 'Footer':
            obj_ = FooterType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self._footer = obj_
            obj_.original_tag_name_ = 'Footer'


class GenericTimeSeriesDataHeaderType(GenericDataHeaderType):
    """GenericTimeSeriesDataHeaderType defines the header structure for a time
    series only generic data message."""
    __hash__ = GenericDataHeaderType.__hash__
    subclass = None
    superclass = GenericDataHeaderType

    def __init__(self, ID=None, Test=False, Prepared=None, Sender=None, Receiver=None, Name=None, Structure=None,
                 DataProvider=None, DataSetAction=None, DataSetID=None, Extracted=None, ReportingBegin=None,
                 ReportingEnd=None, EmbargoDate=None, Source=None, gds_collector_=None, **kwargs_):
        super(GenericTimeSeriesDataHeaderType, self).__init__(ID, Test, Prepared, Sender, Receiver, Name, Structure,
                                                              DataProvider, DataSetAction, DataSetID, Extracted,
                                                              ReportingBegin, ReportingEnd, EmbargoDate, Source,
                                                              gds_collector_, **kwargs_)
        self._name = 'GenericTimeSeriesDataHeaderType'

    @staticmethod
    def factory(*args_, **kwargs_):
        return GenericTimeSeriesDataHeaderType(*args_, **kwargs_)

    def validate_HeaderTimeType(self, value):
        pass

    def validate_ObservationalTimePeriodType(self, value):
        pass


class StructureSpecificTimeSeriesDataType(StructureSpecificDataType):
    """StructureSpecificTimeSeriesDataType defines the structure of the
    structure specific time series data message."""

    __hash__ = StructureSpecificDataType.__hash__
    subclass = None
    superclass = StructureSpecificDataType

    def __init__(self, Header=None, Footer=None, DataSet=None, gds_collector_=None, **kwargs_):
        super(StructureSpecificTimeSeriesDataType, self).__init__(Header, Footer, DataSet,
                                                                  gds_collector_, **kwargs_)

        if DataSet is None:
            self._dataSet = []
        else:
            self._dataSet = DataSet

        self._name = 'StructureSpecificTimeSeriesDataType'

        if gds_collector_ is not None:
            self.gds_collector_ = gds_collector_
        else:
            self.gds_collector_ = GdsCollector()

    @staticmethod
    def factory(*args_, **kwargs_):
        return StructureSpecificDataType(*args_, **kwargs_)

    @property
    def dataset(self):
        return self._dataSet

    @dataset.setter
    def dataset(self, value):
        if value is None:
            self._dataSet = []
        elif isinstance(value, list):
            self._dataSet = value
        else:
            raise TypeError('Dataset must be a list')

    def add_DataSet(self, value):
        self._dataSet.append(value)

    def insert_DataSet_at(self, index, value):
        self._dataSet.insert(index, value)

    def replace_DataSet_at(self, index, value):
        self._dataSet[index] = value

    def has_content_(self):
        if (self._header is not None or self._dataSet or self._footer is not None
                or super(StructureSpecificDataType, self).has_content_()):
            return True
        else:
            return False

    def export_attributes_as_dict(self, valid_fields: list, **kwargs) -> list:
        data = []
        for DataSet_ in self._dataSet:
            parent_dict = {}
            DataSet_.export_attributes_as_dict(parent_dict, )

        return data

    def build_children(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'Header':
            obj_ = StructureSpecificTimeSeriesDataHeaderType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self._header = obj_
            obj_.original_tagname_ = 'Header'
        elif nodeName_ == 'DataSet':
            obj_ = StructureTimeSeriesDataSet.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self._dataSet.append(obj_)
            obj_.original_tag_name_ = 'DataSet'
        elif nodeName_ == 'Footer':
            obj_ = FooterType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self._footer = obj_
            obj_.original_tag_name_ = 'Footer'


# end class StructureSpecificDataType


class StructureSpecificTimeSeriesDataHeaderType(StructureSpecificDataHeaderType):
    """StructureSpecificTimeSeriesDataHeaderType defines the header structure
    for a time series only structure specific data message."""
    __hash__ = StructureSpecificDataHeaderType.__hash__
    subclass = None
    superclass = StructureSpecificDataHeaderType

    def __init__(self, ID=None, Test=False, Prepared=None, Sender=None, Receiver=None, Name=None, Structure=None,
                 DataProvider=None, DataSetAction=None, DataSetID=None, Extracted=None, ReportingBegin=None,
                 ReportingEnd=None, EmbargoDate=None, Source=None, gds_collector_=None, **kwargs_):
        super(StructureSpecificTimeSeriesDataHeaderType, self).__init__(ID, Test, Prepared, Sender, Receiver, Name,
                                                                        Structure, DataProvider, DataSetAction,
                                                                        DataSetID,
                                                                        Extracted, ReportingBegin, ReportingEnd,
                                                                        EmbargoDate,
                                                                        Source, gds_collector_, **kwargs_)
        self._name = 'StructureSpecificTimeSeriesDataHeaderType'

    @staticmethod
    def factory(*args_, **kwargs_):
        return StructureSpecificTimeSeriesDataHeaderType(*args_, **kwargs_)

    def validate_HeaderTimeType(self, value):
        result = True
        return result

    def validate_ObservationalTimePeriodType(self, value):
        result = True
        return result
