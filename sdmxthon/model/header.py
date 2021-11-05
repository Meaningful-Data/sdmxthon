"""
    header file contains the parsers for the Header
"""
from datetime import datetime

from sdmxthon.model.base import InternationalString
from sdmxthon.model.utils import generic_setter, string_setter, bool_setter
from sdmxthon.utils.handlers import add_indent
from sdmxthon.utils.mappings import commonAbbr, structureAbbr


class Contact(object):
    """Contact provides defines the contact information about a party."""

    def __init__(self, name=None, department=None, role=None, telephone=None,
                 fax=None, X400=None, uri=None, email=None):
        self._name = name
        self._department = department
        self._role = role
        self._telephone = telephone
        self._fax = fax
        self._x400 = X400
        self._uri = uri
        self._email = email

    def __eq__(self, other):
        if isinstance(other, Contact):
            return (self._name == other._name and
                    self._uri == other._uri and
                    self._email == other._email and
                    self._fax == other._fax and
                    self._role == other._role and
                    self._telephone == other._telephone and
                    self._department == other._department)

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
        self.name = generic_setter(value, InternationalString)

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
        self._department = generic_setter(value, InternationalString)

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
        self._role = generic_setter(value, InternationalString)

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
    def uri(self):
        """URI of the Contact"""
        if self._uri is None:
            return None
        elif len(self._uri) == 1:
            return self._uri[0]
        else:
            return self._uri

    @uri.setter
    def uri(self, value):
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

    def to_xml(self, indent):
        outfile = ''

        prettyprint = indent != ''

        if self.name is not None:
            data = self._name._to_XML(f'{commonAbbr}:Name', prettyprint)
            for e in data:
                outfile += f'{indent}{e}'
        if self._department is not None:
            data = self._department._to_XML(f'{structureAbbr}:Department',
                                            prettyprint)
            for e in data:
                outfile += f'{indent}{e}'
        if self._role is not None:
            data = self._role._to_XML(f'{structureAbbr}:Role', prettyprint)
            for e in data:
                outfile += f'{indent}{e}'
        indent = add_indent(indent)
        if self._telephone is not None:
            for e in self._telephone:
                outfile += f'{indent}<{structureAbbr}:Telephone>{e}' \
                           f'</{structureAbbr}:Telephone>'
        if self._uri is not None:
            for e in self._uri:
                outfile += f'{indent}<{structureAbbr}:URI>{e}' \
                           f'</{structureAbbr}:URI>'
        if self._x400 is not None:
            for e in self._x400:
                outfile += f'{indent}<{structureAbbr}:X400>{e}' \
                           f'</{structureAbbr}:X400>'
        if self._fax is not None:
            for e in self._fax:
                outfile += f'{indent}<{structureAbbr}:Fax>{e}' \
                           f'</{structureAbbr}:Fax>'
        if self._email is not None:
            for e in self._email:
                outfile += f'{indent}<{structureAbbr}:Email>{e}' \
                           f'</{structureAbbr}:Email>'
        return outfile


class Party(object):
    """Party defines the information which is sent about various parties
    such as senders and receivers of messages.The id attribute holds the
    identification of the party."""

    def __init__(self, id_=None, Name=None, contact=None, extensiontype_=None):
        self.id = id_

        if Name is None:
            self.name = []
        else:
            self.name = Name

        if contact is None:
            self.contact = []
        else:
            self.contact = contact

        self.extensiontype_ = extensiontype_

    def __eq__(self, other):
        if isinstance(other, Party):
            return (self.name == other.name and
                    self.contact == other.contact and
                    self.id_ == other.id_ and
                    self.extensiontype == other.extensiontype)

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


class Sender(Party):
    """Sender extends the basic party structure to add an optional time
    zone declaration."""

    def __init__(self, id_=None, name=None, contact=None, timezone=None):
        super(Sender, self).__init__(id_, name, contact)
        self._timezone = timezone

    def __eq__(self, other):
        if isinstance(other, Sender):
            return self.timezone == other.timezone

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


class Header(object):
    """Header defines the basis for all message headers."""

    def __init__(self, ID=None, Test=False, Prepared=None, sender=None,
                 Receiver=None, Name=None, Structure=None,
                 DataProvider=None, DataSetAction=None, DataSetID=None,
                 Extracted=None, ReportingBegin=None,
                 ReportingEnd=None, EmbargoDate=None, Source=None):
        self._ID = ID
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

        if DataSetID is None:
            self._DataSetID = []
        else:
            self._DataSetID = DataSetID

        if isinstance(Extracted, str):
            initvalue_ = datetime.strptime(Extracted, '%Y-%m-%dT%H:%M:%S')
        else:
            initvalue_ = Extracted

        self._Extracted = initvalue_
        self._ReportingBegin = ReportingBegin
        self._ReportingEnd = ReportingEnd

        if isinstance(EmbargoDate, str):
            initvalue_ = datetime.strptime(EmbargoDate, '%Y-%m-%dT%H:%M:%S')
        else:
            initvalue_ = EmbargoDate

        self._EmbargoDate = initvalue_

        self._Source = Source

    def __eq__(self, other):
        if isinstance(other, Header):
            return (self.name == other.name and self.id_ == other.id_ and
                    self.test == other.test and self.sender == other.sender and
                    self.receiver == other.receiver and
                    self.structure == other.structure and
                    self.data_provider == other.data_provider and
                    self.dataset_action == other.dataset_action and
                    self.datasetID == other.datasetID and
                    self.extracted == other.extracted and
                    self.reporting_begin == other.reporting_begin and
                    self.reporting_end == other.reporting_end and
                    self.embargo_date == other.embargo_date and
                    self.source == other.source)

    @property
    def id_(self):
        """Identifier of the Message"""
        return self._ID

    @id_.setter
    def id_(self, value):
        self._ID = string_setter(value)

    @property
    def test(self):
        """Sets if the Message is for testing purposes"""
        return self._Test

    @test.setter
    def test(self, value):
        self._Test = bool_setter(value)

    @property
    def prepared(self):
        """Datetime of the preparation of the Message"""
        return self._Prepared

    @prepared.setter
    def prepared(self, value):
        self._Prepared = generic_setter(value, datetime)

    @property
    def sender(self):
        """Sender of the Message"""
        return self._Sender

    @sender.setter
    def sender(self, value):
        self._Sender = generic_setter(value, Sender)

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
        elif isinstance(value, Party):
            self._Receiver = [value]
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
    def data_provider(self):
        """Data provider of the Message"""
        return self._dataProvider

    @data_provider.setter
    def data_provider(self, value):
        self._dataProvider = value

    @property
    def dataset_action(self):
        """Action of the Dataset"""
        return self._DataSetAction

    @dataset_action.setter
    def dataset_action(self, value):
        self._DataSetAction = string_setter(value)

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
        self._Extracted = generic_setter(value, datetime)

    @property
    def reporting_begin(self):
        """Start of the reporting"""
        return self._ReportingBegin

    @reporting_begin.setter
    def reporting_begin(self, value):
        self._ReportingBegin = string_setter(value)

    @property
    def reporting_end(self):
        """End of the reporting"""
        return self._ReportingEnd

    @reporting_end.setter
    def reporting_end(self, value):
        self._ReportingEnd = string_setter(value)

    @property
    def embargo_date(self):
        """Datetime of the Embargo (only in Data Messages)"""
        return self._EmbargoDate

    @embargo_date.setter
    def embargo_date(self, value):
        self._EmbargoDate = generic_setter(value, datetime)

    @property
    def source(self):
        """Source of the Message"""
        return self._Source

    @source.setter
    def source(self, value):
        self._Source = generic_setter(value, InternationalString)
