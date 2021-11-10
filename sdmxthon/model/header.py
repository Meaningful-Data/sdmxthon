"""
    header file contains the parsers for the Header
"""
from datetime import datetime

from sdmxthon.model.base import InternationalString
from sdmxthon.model.utils import generic_setter, string_setter, bool_setter
from sdmxthon.utils.handlers import add_indent
from sdmxthon.utils.mappings import commonAbbr, structureAbbr


def _int_str_getter(attr):
    if attr is None:
        return None
    if isinstance(attr, InternationalString):
        if len(attr.items) == 0:
            return None
        if len(attr.items) == 1:
            values_view = attr.items.values()
            value_iterator = iter(values_view)
            first_value = next(value_iterator)
            return first_value['content']

        return attr.items

    return attr


def _writer_int_str(attr, word, abbr, indent, prettyprint):
    outfile = ""
    if attr is not None:
        data = attr._to_XML(f'{abbr}:{word}', prettyprint)
        for e in data:
            outfile += f'{indent}{e}'
    return outfile


def _writer_attr(attr, word, indent):
    outfile = ""
    if attr is not None:
        for e in attr:
            outfile += f'{indent}<{structureAbbr}:{word}>{e}' \
                       f'</{structureAbbr}:{word}>'

    return outfile


class Contact(object):
    """Contact provides defines the contact information about a party."""

    def __init__(self, name=None, department=None, role=None, telephone=None,
                 fax=None, X400=None, uri=None, email=None):
        self.name = name
        self.department = department
        self.role = role
        self.telephone = telephone
        self.fax = fax
        self.X400 = X400
        self.uri = uri
        self.email = email

    def __eq__(self, other):
        if isinstance(other, Contact):
            return (self.name == other.name and
                    self.uri == other.uri and
                    self.email == other.email and
                    self.fax == other.fax and
                    self.role == other.role and
                    self.telephone == other.telephone and
                    self.department == other.department)

    @property
    def name(self):
        """Name of the Contact"""
        return _int_str_getter(self._name)

    @name.setter
    def name(self, value):
        self._name = generic_setter(value, InternationalString)

    @property
    def department(self):
        """Department of the Contact"""
        return _int_str_getter(self._department)

    @department.setter
    def department(self, value):
        self._department = generic_setter(value, InternationalString)

    @property
    def role(self):
        """Role of the Contact"""
        return _int_str_getter(self._role)

    @role.setter
    def role(self, value):
        self._role = generic_setter(value, InternationalString)

    @property
    def telephone(self):
        """Telephone of the Contact"""
        if self._telephone is None:
            return None
        if len(self._telephone) == 1:
            return self._telephone[0]
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
        if len(self._fax) == 1:
            return self._fax[0]
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
        if len(self._x400) == 1:
            return self._x400[0]

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
        if len(self._uri) == 1:
            return self._uri[0]

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
        if len(self._email) == 1:
            return self._email[0]

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

        outfile += _writer_int_str(self._name, 'Name', commonAbbr, indent,
                                   prettyprint)
        outfile += _writer_int_str(self._department, 'Department',
                                   structureAbbr, indent,
                                   prettyprint)
        outfile += _writer_int_str(self._role, 'Role', structureAbbr, indent,
                                   prettyprint)

        indent = add_indent(indent)
        outfile += _writer_attr(self._telephone, 'Telephone', indent)
        outfile += _writer_attr(self._uri, 'URI', indent)
        outfile += _writer_attr(self._x400, 'X400', indent)
        outfile += _writer_attr(self._fax, 'Fax', indent)
        outfile += _writer_attr(self._email, 'Email', indent)
        return outfile


class Party(object):
    """Party defines the information which is sent about various parties
    such as senders and receivers of messages.The id attribute holds the
    identification of the party."""

    def __init__(self, id_=None, Name=None, contact=None, extensiontype_=None):
        self.id_ = id_

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

        return False

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
