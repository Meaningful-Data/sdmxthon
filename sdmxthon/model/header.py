"""
    header file contains the parsers for the Header
"""

import datetime as datetime_

from SDMXThon.parsers.data_parser import DataParser, Validate_simpletypes_
from SDMXThon.parsers.payload_parser import GenericDataStructureType
from SDMXThon.parsers.references import ReferenceType
from SDMXThon.utils.handlers import add_indent
from SDMXThon.utils.mappings import *
from SDMXThon.utils.xml_base import cast, find_attr_value_, encode_str_2_3, BaseStrType_
from .base import InternationalString, LocalisedString


class Contact(DataParser):
    """Contact provides defines the contact information about a party."""

    def __init__(self, Name=None, Department=None, Role=None, Telephone=None, Fax=None, X400=None, URI=None, Email=None,
                 gds_collector_=None):
        super(Contact, self).__init__(gds_collector_)
        self.gds_collector_ = gds_collector_

        self._name = Name

        self._department = Department

        self._role = Role

        self._telephone = Telephone

        self._fax = Fax

        self._x400 = X400

        self._uri = URI

        self._email = Email

    def __eq__(self, other):
        if isinstance(other, Contact):
            return (self._name == other._name and self._uri == other._uri
                    and self._email == other._email and self._fax == other._fax
                    and self._role == other._role and self._telephone == other._telephone
                    and self._department == other._department)

    @staticmethod
    def _factory(*args_, **kwargs_):
        """Factory Method of Contact"""
        return Contact(*args_, **kwargs_)

    @property
    def name(self):
        """Name of the Contact"""
        if self._name is None:
            return None
        elif isinstance(self._name, InternationalString):
            if len(self._name.items) == 0:
                return None
            elif len(self._name.items) == 1:
                values_view = self._name.items.values()
                value_iterator = iter(values_view)
                first_value = next(value_iterator)
                return first_value['content']
            else:
                return self._name.items
        return self._name

    @name.setter
    def name(self, value):
        if value is None:
            self._name = []
        elif isinstance(value, list):
            self._name = value
        else:
            raise TypeError('Name must be a list')

    @property
    def department(self):
        """Department of the Contact"""
        if self._department is None:
            return None
        elif isinstance(self._department, InternationalString):
            if len(self._department.items) == 0:
                return None
            elif len(self._department.items) == 1:
                values_view = self._department.items.values()
                value_iterator = iter(values_view)
                first_value = next(value_iterator)
                return first_value['content']
            else:
                return self._department.items
        return self._department

    @department.setter
    def department(self, value):
        self._department = value

    @property
    def role(self):
        """Role of the Contact"""
        if self._role is None:
            return None
        elif isinstance(self._role, InternationalString):
            if len(self._role.items) == 0:
                return None
            elif len(self._role.items) == 1:
                values_view = self._role.items.values()
                value_iterator = iter(values_view)
                first_value = next(value_iterator)
                return first_value['content']
            else:
                return self._role.items
        return self._role

    @role.setter
    def role(self, value):
        self._role = value

    @property
    def telephone(self):
        """Telephone of the Contact"""
        if self._telephone is None:
            return None
        elif len(self._telephone) == 1:
            return self._telephone[0]
        else:
            return self._telephone

    @telephone.setter
    def telephone(self, value):
        if value is None:
            self._telephone = []
        elif isinstance(value, list):
            self._telephone = value
        else:
            raise TypeError('Telephone must be a list')

    @property
    def fax(self):
        """Fax of the Contact"""
        if self._fax is None:
            return None
        elif len(self._fax) == 1:
            return self._fax[0]
        else:
            return self._fax

    @fax.setter
    def fax(self, value):
        if value is None:
            self._fax = []
        elif isinstance(value, list):
            self._fax = value
        else:
            raise TypeError('Fax must be a list')

    @property
    def X400(self):
        """IPM of the Contact"""
        if self._x400 is None:
            return None
        elif len(self._x400) == 1:
            return self._x400[0]
        else:
            return self._x400

    @X400.setter
    def X400(self, value):
        if value is None:
            self._x400 = []
        elif isinstance(value, list):
            self._x400 = value
        else:
            raise TypeError('X400 must be a list')

    @property
    def URI(self):
        """URI of the Contact"""
        if self._uri is None:
            return None
        elif len(self._uri) == 1:
            return self._uri[0]
        else:
            return self._uri

    @URI.setter
    def URI(self, value):
        if value is None:
            self._uri = []
        elif isinstance(value, list):
            self._uri = value
        else:
            raise TypeError('URI must be a list')

    @property
    def email(self):
        """Email of the Contact"""
        if self._email is None:
            return None
        elif len(self._email) == 1:
            return self._email[0]
        else:
            return self._email

    @email.setter
    def email(self, value):
        if value is None:
            self._email = []
        elif isinstance(value, list):
            self._email = value
        else:
            raise TypeError('Email must be a list')

    def _has_content_(self):
        """Check if it has any content"""
        if (
                self._name or
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

    def _build_children(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        """Builds the childs of the XML element"""
        if nodeName_ == 'Name':
            obj_ = LocalisedString._factory()
            obj_._build(child_, gds_collector_=gds_collector_)
            if self._name is None:
                self._name = InternationalString()
            self._name.addLocalisedString(obj_)

        elif nodeName_ == 'Department':
            obj_ = LocalisedString._factory()
            obj_._build(child_, gds_collector_=gds_collector_)
            if self._department is None:
                self._department = InternationalString()
            self._department.addLocalisedString(obj_)

        elif nodeName_ == 'Role':
            obj_ = LocalisedString._factory()
            obj_._build(child_, gds_collector_=gds_collector_)
            if self._role is None:
                self._role = InternationalString()
            self._role.addLocalisedString(obj_)

        elif nodeName_ == 'Telephone':
            value_ = child_.text
            value_ = self._gds_parse_string(value_)
            value_ = self._gds_validate_string(value_)

            if self._telephone is None:
                self._telephone = []

            self._telephone.append(value_)

        elif nodeName_ == 'Fax':
            value_ = child_.text
            value_ = self._gds_parse_string(value_)
            value_ = self._gds_validate_string(value_)

            if self._fax is None:
                self._fax = []

            self._fax.append(value_)

        elif nodeName_ == 'X400':
            value_ = child_.text
            value_ = self._gds_parse_string(value_)
            value_ = self._gds_validate_string(value_)

            if self._x400 is None:
                self._x400 = []

            self._x400.append(value_)

        elif nodeName_ == 'URI':
            value_ = child_.text
            value_ = self._gds_parse_string(value_)
            value_ = self._gds_validate_string(value_)

            if self._uri is None:
                self._uri = []

            self._uri.append(value_)

        elif nodeName_ == 'Email':
            value_ = child_.text
            value_ = self._gds_parse_string(value_)
            value_ = self._gds_validate_string(value_)

            if self._email is None:
                self._email = []

            self._email.append(value_)

    def to_XML(self, indent):
        outfile = ''

        prettyprint = indent != ''

        if self.name is not None:
            data = self._name._to_XML(f'{commonAbbr}:Name', prettyprint)
            for e in data:
                outfile += f'{indent}{e}'
        if self._department is not None:
            data = self._department._to_XML(f'{structureAbbr}:Department', prettyprint)
            for e in data:
                outfile += f'{indent}{e}'
        if self._role is not None:
            data = self._role._to_XML(f'{structureAbbr}:Role', prettyprint)
            for e in data:
                outfile += f'{indent}{e}'
        indent = add_indent(indent)
        if self._telephone is not None:
            for e in self._telephone:
                outfile += f'{indent}<{structureAbbr}:Telephone>{e}</{structureAbbr}:Telephone>'
        if self._uri is not None:
            for e in self._uri:
                outfile += f'{indent}<{structureAbbr}:URI>{e}</{structureAbbr}:URI>'
        if self._x400 is not None:
            for e in self._x400:
                outfile += f'{indent}<{structureAbbr}:X400>{e}</{structureAbbr}:X400>'
        if self._fax is not None:
            for e in self._fax:
                outfile += f'{indent}<{structureAbbr}:Fax>{e}</{structureAbbr}:Fax>'
        if self._email is not None:
            for e in self._email:
                outfile += f'{indent}<{structureAbbr}:Email>{e}</{structureAbbr}:Email>'
        return outfile


class Party(DataParser):
    """Party defines the information which is sent about various parties
    such as senders and receivers of messages.The id attribute holds the
    identification of the party."""

    def __init__(self, id_=None, Name=None, contact=None, extensiontype_=None, gds_collector_=None, **kwargs_):
        super(Party, self).__init__(gds_collector_, **kwargs_)
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self._id = cast(None, id_)

        if Name is None:
            self._Name = []
        else:
            self._Name = Name

        if contact is None:
            self._contact = []
        else:
            self._contact = contact

        self._extensiontype_ = extensiontype_

    @staticmethod
    def _factory(*args_, **kwargs_):
        """Factory Method of Party"""
        return Party(*args_, **kwargs_)

    @property
    def name(self):
        """Name of the Party"""
        return self._Name

    @name.setter
    def name(self, value):
        if value is None:
            self._Name = []
        elif isinstance(value, list):
            self._Name = value
        else:
            raise TypeError('Name must be a list')

    @property
    def contact(self):
        """Contact of the Party"""
        return self._contact

    @contact.setter
    def contact(self, value):
        if value is None:
            self._contact = []
        elif isinstance(value, list):
            self._contact = value
        else:
            raise TypeError('Contact must be a list')

    @property
    def id_(self):
        """ID of the Sender/Receiver"""
        return self._id

    @id_.setter
    def id_(self, value):
        self._id = value

    @property
    def extensiontype(self):
        """Dim_type attribute"""
        return self._extensiontype_

    @extensiontype.setter
    def extensiontype(self, value):
        self._extensiontype_ = value

    def _has_content_(self):
        """Check if it has any content"""
        if (
                self._Name or
                self._contact
        ):
            return True
        else:
            return False

    def _build_attributes(self, node, attrs, already_processed):
        """Builds the attributes present in the XML element"""
        value = find_attr_value_('id', node)
        if value is not None and 'id' not in already_processed:
            already_processed.add('id')
            self._id = value
            self._validate_id_type(self._id)
        # validate dim_type IDType
        value = find_attr_value_('xsi:dim_type', node)
        if value is not None and 'xsi:dim_type' not in already_processed:
            already_processed.add('xsi:dim_type')
            self._extensiontype_ = value

    def _build_children(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        """Builds the childs of the XML element"""
        if nodeName_ == 'Name':
            class_obj_ = self._get_class_obj_(child_, LocalisedString)
            obj_ = class_obj_._factory()
            obj_._build(child_, gds_collector_=gds_collector_)
            self._Name.append(obj_)
        elif nodeName_ == 'Contact':
            obj_ = Contact._factory()
            obj_._build(child_, gds_collector_=gds_collector_)
            self._contact.append(obj_)


class Sender(Party):
    """Sender extends the basic party structure to add an optional time
    zone declaration."""

    def __init__(self, id_=None, name=None, contact=None, timezone=None, gds_collector_=None, **kwargs_):
        super(Sender, self).__init__(id_, name, contact, gds_collector_, **kwargs_)
        self._timezone = timezone
        self.validate_TimezoneType(self._timezone)

    @staticmethod
    def _factory(*args_, **kwargs_):
        """Factory Method of Sender"""
        return Sender(*args_, **kwargs_)

    @property
    def timezone(self):
        """Timezone of the Sender"""
        return self._timezone

    @timezone.setter
    def timezone(self, value):
        self._timezone = value

    def validate_TimezoneType(self, value):
        """Validate dim_type TimezoneType, a restriction on xs:string."""
        result = True
        validate_timezone_type_patterns_ = [['^(Z)$', '^((\\+|\\-)(14:00|((0[0-9]|1[0-3]):[0-5][0-9])))$']]

        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self._gds_get_node_line_number_()
                self.gds_collector_.add_message(
                    f'Value "{value}": {lineno} is not of the correct base simple dim_type (str)')
                return False

            if not self._gds_validate_simple_patterns(validate_timezone_type_patterns_, value):
                self.gds_collector_.add_message(f'Value "{encode_str_2_3(value)}" '
                                                f'does not match xsd pattern restrictions: '
                                                f'{self.__validate_IDType_patterns}')
                result = False
        return result

    def _has_content_(self):
        """Check if it has any content"""
        if (
                self._timezone is not None or
                super(Sender, self)._has_content_()
        ):
            return True
        else:
            return False

    def _build_attributes(self, node, attrs, already_processed):
        """Builds the attributes present in the XML element"""
        super(Sender, self)._build_attributes(node, attrs, already_processed)

    def _build_children(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        """Builds the childs of the XML element"""
        if nodeName_ == 'Timezone':
            value_ = child_.text
            value_ = self._gds_parse_string(value_)
            value_ = self._gds_validate_string(value_)
            self._timezone = value_
            self.validate_TimezoneType(self._timezone)
        super(Sender, self)._build_children(child_, node, nodeName_, True)


class Header(DataParser):
    """Header defines the basis for all message headers."""

    def __init__(self, ID=None, Test=False, Prepared=None, sender=None, Receiver=None, Name=None, Structure=None,
                 DataProvider=None, DataSetAction=None, DataSetID=None, Extracted=None, ReportingBegin=None,
                 ReportingEnd=None, EmbargoDate=None, Source=None, gds_collector_=None, **kwargs_):
        super(Header, self).__init__(gds_collector_, **kwargs_)
        self.gds_collector_ = gds_collector_
        self._ID = ID
        self._validate_id_type(self._ID)
        self._Test = Test
        self._Prepared = Prepared
        self._Sender = sender

        if Receiver is None:
            self._Receiver = []
        else:
            self._Receiver = Receiver

        if Name is None:
            self._Name = []
        else:
            self._Name = Name

        if Structure is None:
            self._structure = {}
        else:
            self._structure = Structure

        self._dataProvider = DataProvider
        self._DataSetAction = DataSetAction
        self._validate_action_type(self._DataSetAction)

        if DataSetID is None:
            self._DataSetID = []
        else:
            self._DataSetID = DataSetID

        if isinstance(Extracted, BaseStrType_):
            initvalue_ = datetime_.datetime.strptime(Extracted, '%Y-%m-%dT%H:%M:%S')
        else:
            initvalue_ = Extracted

        self._Extracted = initvalue_
        self._ReportingBegin = ReportingBegin
        self._ReportingEnd = ReportingEnd

        if isinstance(EmbargoDate, BaseStrType_):
            initvalue_ = datetime_.datetime.strptime(EmbargoDate, '%Y-%m-%dT%H:%M:%S')
        else:
            initvalue_ = EmbargoDate

        self._EmbargoDate = initvalue_

        if Source is None:
            self._Source = []
        else:
            self._Source = Source

    @staticmethod
    def _factory(*args_, **kwargs_):
        """Factory Method of Header"""
        return Header(*args_, **kwargs_)

    @property
    def id_(self):
        """Identifier of the Message"""
        return self._ID

    @id_.setter
    def id_(self, value):
        self._ID = value

    @property
    def test(self):
        """Sets if the Message is for testing purposes"""
        return self._Test

    @test.setter
    def test(self, value):
        self._Test = value

    @property
    def prepared(self):
        """Datetime of the preparation of the Message"""
        return self._Prepared

    @prepared.setter
    def prepared(self, value):
        self._Prepared = value

    @property
    def sender(self):
        """Sender of the Message"""
        return self._Sender

    @sender.setter
    def sender(self, value):
        self._Sender = value

    @property
    def receiver(self):
        """Receiver of the Message"""
        return self._Receiver

    @receiver.setter
    def receiver(self, value):
        if value is None:
            self._Receiver = []
        elif isinstance(value, list):
            self._Receiver = value
        else:
            raise TypeError('Receiver must be a list')

    @property
    def name(self):
        """Name of the Message"""
        return self._Name

    @name.setter
    def name(self, value):
        if value is None:
            self._Name = []
        elif isinstance(value, list):
            self._Name = value
        else:
            raise TypeError('Name must be a list')

    @property
    def structure(self):
        """Structures of the data in the Message"""
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
        """Data provider of the Message"""
        return self._dataProvider

    @dataProvider.setter
    def dataProvider(self, value):
        self._dataProvider = value

    @property
    def datasetAction(self):
        """Action of the Dataset"""
        return self._DataSetAction

    @datasetAction.setter
    def datasetAction(self, value):
        self._DataSetAction = value

    @property
    def datasetID(self):
        """ID of the Dataset"""
        return self._DataSetID

    @datasetID.setter
    def datasetID(self, value):
        if value is None:
            self._DataSetID = []
        elif isinstance(value, list):
            self._DataSetID = value
        else:
            raise TypeError('DatasetID must be a list')

    @property
    def extracted(self):
        """Datetime of the information extracted"""
        return self._Extracted

    @extracted.setter
    def extracted(self, value):
        self._Extracted = value

    @property
    def reportingBegin(self):
        """Start of the reporting"""
        return self._ReportingBegin

    @reportingBegin.setter
    def reportingBegin(self, value):
        self._ReportingBegin = value

    @property
    def reportingEnd(self):
        """End of the reporting"""
        return self._ReportingEnd

    @reportingEnd.setter
    def reportingEnd(self, value):
        self._ReportingEnd = value

    @property
    def embargoDate(self):
        """Datetime of the Embargo (only in Data Messages)"""
        return self._EmbargoDate

    @embargoDate.setter
    def embargoDate(self, value):
        self._EmbargoDate = value

    @property
    def source(self):
        """Source of the Message"""
        return self._Source

    @source.setter
    def source(self, value):
        if value is None:
            self._Source = []
        elif isinstance(value, list):
            self._Source = value
        else:
            raise TypeError('Source must be a list')

    def _has_content_(self):
        """Check if it has any content"""
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

    def _build_children(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        """Builds the childs of the XML element"""
        if nodeName_ == 'ID':
            value_ = child_.text
            value_ = self._gds_parse_string(value_)
            value_ = self._gds_validate_string(value_)
            self._ID = value_
            self._validate_id_type(self._ID)
        elif nodeName_ == 'Test':
            sval_ = child_.text
            ival_ = self._gds_parse_boolean(sval_)
            ival_ = self._gds_validate_boolean(ival_)
            self._Test = ival_
        elif nodeName_ == 'Prepared':
            value_ = child_.text
            value_ = self._gds_parse_string(value_)
            value_ = self._gds_validate_string(value_)
            self._Prepared = value_
        elif nodeName_ == 'Sender':
            obj_ = Sender._factory()
            obj_._build(child_, gds_collector_=gds_collector_)
            self._Sender = obj_
        elif nodeName_ == 'Receiver':
            class_obj_ = self._get_class_obj_(child_, Party)
            obj_ = class_obj_._factory()
            obj_._build(child_, gds_collector_=gds_collector_)
            self._Receiver.append(obj_)
        elif nodeName_ == 'Name':
            class_obj_ = self._get_class_obj_(child_, LocalisedString)
            obj_ = class_obj_._factory()
            obj_._build(child_, gds_collector_=gds_collector_)
            self._Name.append(obj_)
        elif nodeName_ == 'Structure':
            obj_ = GenericDataStructureType._factory()
            obj_._build(child_, gds_collector_=gds_collector_)

            if obj_.structure is not None:
                self._structure[obj_.structureID] = {'dimAtObs': obj_.dimensionAtObservation,
                                                     'ID': obj_.structure, 'type': 'DataStructure'}
            elif obj_.structureUsage is not None:
                self._structure[obj_.structureID] = {'dimAtObs': obj_.dimensionAtObservation,
                                                     'ID': obj_.structureUsage, 'type': 'DataFlow'}

            elif obj_.provisionAgreement is not None:
                self._structure[obj_.structureID] = {'dimAtObs': obj_.dimensionAtObservation,
                                                     'ID': obj_.provisionAgreement, 'type': 'ProvisionAgreement'}
            else:
                pass

        elif nodeName_ == 'DataProvider':
            obj_ = ReferenceType._factory()
            obj_._build(child_, gds_collector_=gds_collector_)
            self._dataProvider = obj_
        elif nodeName_ == 'DataSetAction':
            value_ = child_.text
            value_ = self._gds_parse_string(value_)
            value_ = self._gds_validate_string(value_)
            self._DataSetAction = value_
            self._validate_action_type(self._DataSetAction)
        elif nodeName_ == 'DataSetID':
            value_ = child_.text
            value_ = self._gds_parse_string(value_)
            value_ = self._gds_validate_string(value_)
            self._DataSetID.append(value_)
            self._validate_id_type(self._DataSetID[-1])
        elif nodeName_ == 'Extracted':
            sval_ = child_.text
            dval_ = self._gds_parse_datetime(sval_)
            self._Extracted = dval_
        elif nodeName_ == 'ReportingBegin':
            value_ = child_.text
            value_ = self._gds_parse_string(value_)
            value_ = self._gds_validate_string(value_)
            self._ReportingBegin = value_
        elif nodeName_ == 'ReportingEnd':
            value_ = child_.text
            value_ = self._gds_parse_string(value_)
            value_ = self._gds_validate_string(value_)
            self._ReportingEnd = value_
        elif nodeName_ == 'EmbargoDate':
            sval_ = child_.text
            dval_ = self._gds_parse_datetime(sval_)
            self._EmbargoDate = dval_
        elif nodeName_ == 'Source':
            class_obj_ = self._get_class_obj_(child_, LocalisedString)
            obj_ = class_obj_._factory()
            obj_._build(child_, gds_collector_=gds_collector_)
            self._Source.append(obj_)