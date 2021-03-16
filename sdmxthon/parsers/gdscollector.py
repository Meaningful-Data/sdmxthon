import base64
import datetime as datetime_
import decimal as decimal_
import re as re_
import sys

from lxml import etree as etree_

from ..utils.xml_base import raise_parse_error, GDSParseError

ExternalEncoding = ''


def gds_str_lower(in_string):
    return in_string.lower()


class FixedOffsetTZ(datetime_.tzinfo):
    def __init__(self, offset, name):
        self.__offset = datetime_.timedelta(minutes=offset)
        self._name = name

    def utcoffset(self, dt):
        return self.__offset

    def tzname(self, dt):
        return self._name

    def dst(self, dt):
        return None


class GenerateSuper(object):

    def __init__(self, gds_collector):
        self.gds_element_tree_node_ = None
        if gds_collector is not None:
            self.gds_collector_ = gds_collector
        else:
            self.gds_collector_ = GdsCollector()

    @staticmethod
    def gds_format_string(input_data):
        return input_data

    @staticmethod
    def gds_parse_string(input_data):
        return input_data

    @staticmethod
    def gds_validate_string(input_data):
        if not input_data:
            return ''
        else:
            return input_data

    @staticmethod
    def gds_format_base64(input_data):
        return base64.b64encode(input_data)

    @staticmethod
    def gds_validate_base64(input_data):
        return input_data

    @staticmethod
    def gds_format_integer(input_data):
        return '%d' % input_data

    @staticmethod
    def gds_parse_integer(input_data, node=None):
        i_val = None
        try:
            i_val = int(input_data)
        except (TypeError, ValueError):
            raise_parse_error(node, f'Requires integer value')

        return i_val

    @staticmethod
    def gds_validate_integer(input_data, node=None):
        value = None
        try:
            value = int(input_data)
        except (TypeError, ValueError):
            raise_parse_error(node, 'Requires integer value')

        return value

    @staticmethod
    def gds_format_integer_list(input_data):
        return '%s' % ' '.join(input_data)

    @staticmethod
    def gds_validate_integer_list(input_data, node=None):
        values = input_data.split()

        for value in values:
            try:
                int(value)
            except (TypeError, ValueError):
                raise_parse_error(node, 'Requires sequence of integer values')

        return values

    @staticmethod
    def gds_format_float(input_data):
        return f'{input_data}'.rstrip('0')

    @staticmethod
    def gds_parse_float(input_data, node=None):
        float_val_ = None
        try:
            float_val_ = float(input_data)
        except (TypeError, ValueError):
            raise_parse_error(node, 'Requires float or double value')

        return float_val_

    @staticmethod
    def gds_validate_float(input_data, node=None):
        value = None
        try:
            value = float(input_data)
        except (TypeError, ValueError):
            raise_parse_error(node, 'Requires float value')

        return value

    @staticmethod
    def gds_format_float_list(input_data):
        return '%s' % ' '.join(input_data)

    @staticmethod
    def gds_validate_float_list(input_data, node=None):
        values = input_data.split()

        for value in values:
            try:
                float(value)
            except (TypeError, ValueError):
                raise_parse_error(node, 'Requires sequence of float values')

        return values

    @staticmethod
    def gds_format_decimal(input_data):
        return_value = f'{input_data}'

        if '.' in return_value:
            return_value = return_value.rstrip('0')

            if return_value.endswith('.'):
                return_value = return_value.rstrip('.')

        return return_value

    @staticmethod
    def gds_parse_decimal(input_data, node=None):
        decimal_value = None
        try:
            decimal_value = decimal_.Decimal(input_data)
        except (TypeError, ValueError):
            raise_parse_error(node, 'Requires decimal value')

        return decimal_value

    @staticmethod
    def gds_validate_decimal(input_data, node=None):
        value = None
        try:
            value = decimal_.Decimal(input_data)
        except (TypeError, ValueError):
            raise_parse_error(node, 'Requires decimal value')

        return value

    def gds_format_decimal_list(self, input_data):
        return ' '.join([self.gds_format_decimal(item) for item in input_data])

    @staticmethod
    def gds_validate_decimal_list(input_data, node=None):
        values = input_data.split()

        for value in values:
            try:
                decimal_.Decimal(value)
            except (TypeError, ValueError):
                raise_parse_error(node, 'Requires sequence of decimal values')

        return values

    @staticmethod
    def gds_format_double(input_data):
        return float(input_data)

    @staticmethod
    def gds_parse_double(input_data, node=None):
        value = None
        try:
            value = float(input_data)
        except (TypeError, ValueError):
            raise_parse_error(node, 'Requires double or float value')

        return value

    @staticmethod
    def gds_validate_double(input_data, node=None):
        value = None
        try:
            value = float(input_data)
        except (TypeError, ValueError):
            raise_parse_error(node, 'Requires double or float value')

        return value

    @staticmethod
    def gds_format_double_list(input_data):
        return ' '.join(str(input_data))

    @staticmethod
    def gds_validate_double_list(input_data, node=None):
        values = input_data.split()

        for value in values:
            try:
                float(value)
            except (TypeError, ValueError):
                raise_parse_error(node, 'Requires sequence of double or float values')

        return values

    @staticmethod
    def gds_format_boolean(input_data):
        return f'{input_data}'.lower()

    @staticmethod
    def gds_parse_boolean(input_data, node=None):
        value = None
        if input_data in ('true', '1'):
            value = True
        elif input_data in ('false', '0'):
            value = False
        else:
            raise_parse_error(node, 'Requires boolean value')

        return value

    @staticmethod
    def gds_validate_boolean(input_data, node=None):
        if input_data not in (True, 1, False, 0, 'false', 'true'):
            raise_parse_error(node, 'Requires boolean value (one of True, 1, False, 0)')

        return input_data

    @staticmethod
    def gds_format_boolean_list(input_data):
        return ' '.join(str(input_data))

    @staticmethod
    def gds_validate_boolean_list(input_data, node=None):
        values = input_data.split()

        for value in values:
            if value not in (True, 1, False, 0,):
                raise_parse_error(node, 'Requires sequence of boolean values (one of True, 1, False, 0)')

        return values

    @staticmethod
    def gds_validate_datetime(input_data):
        return input_data

    @staticmethod
    def gds_validate_duration(input_data):
        return input_data

    @staticmethod
    def gds_format_datetime(input_data):
        if input_data.microsecond == 0:
            _svalue = '%04d-%02d-%02dT%02d:%02d:%02d' % (
                input_data.year, input_data.month, input_data.day, input_data.hour, input_data.minute,
                input_data.second,)
        else:
            _svalue = '%04d-%02d-%02dT%02d:%02d:%02d.%s' % (
                input_data.year, input_data.month, input_data.day, input_data.hour, input_data.minute,
                input_data.second,
                ('%f' % (float(input_data.microsecond) / 1000000))[2:],)
        if input_data.tzinfo is not None:
            tzoff = input_data.tzinfo.utcoffset(input_data)

            if tzoff is not None:
                total_seconds = tzoff.seconds + (86400 * tzoff.days)
                if total_seconds == 0:
                    _svalue += 'Z'
                else:
                    if total_seconds < 0:
                        _svalue += '-'
                        total_seconds *= -1
                    else:
                        _svalue += '+'
                    hours = total_seconds // 3600
                    minutes = (total_seconds - (hours * 3600)) // 60
                    _svalue += '{0:02d}:{1:02d}'.format(hours, minutes)

        return _svalue

    @classmethod
    def gds_parse_datetime(cls, input_data):
        tz = None
        tz_off_pattern = re_.compile(r'([+\-])((0\d|1[0-3]):[0-5]\d|14:00)$')
        if input_data[-1] == 'Z':
            tz = FixedOffsetTZ(0, 'UTC')
            input_data = input_data[:-1]
        else:
            results = tz_off_pattern.search(input_data)

            if results is not None:
                tzoff_parts = results.group(2).split(':')
                tzoff = int(tzoff_parts[0]) * 60 + int(tzoff_parts[1])

                if results.group(1) == '-':
                    tzoff *= -1

                tz = FixedOffsetTZ(tzoff, results.group(0))
                input_data = input_data[:-6]

        time_parts = input_data.split('.')

        if len(time_parts) > 1:
            micro_seconds = int(float('0.' + time_parts[1]) * 1000000)
            input_data = '%s.%s' % (time_parts[0], "{}".format(micro_seconds).rjust(6, "0"),)
            dt = datetime_.datetime.strptime(input_data, '%Y-%m-%dT%H:%M:%S.%f')
        else:
            dt = datetime_.datetime.strptime(input_data, '%Y-%m-%dT%H:%M:%S')

        dt = dt.replace(tzinfo=tz)
        return dt

    @staticmethod
    def gds_validate_date(input_data):
        return input_data

    @staticmethod
    def gds_format_date(input_data):
        _svalue = '%04d-%02d-%02d' % (input_data.year, input_data.month, input_data.day)
        try:
            if input_data.tzinfo is not None:
                tzoff = input_data.tzinfo.utcoffset(input_data)

                if tzoff is not None:
                    total_seconds = tzoff.seconds + (86400 * tzoff.days)

                    if total_seconds == 0:
                        _svalue += 'Z'
                    else:
                        if total_seconds < 0:
                            _svalue += '-'
                            total_seconds *= -1
                        else:
                            _svalue += '+'

                        hours = total_seconds // 3600
                        minutes = (total_seconds - (hours * 3600)) // 60
                        _svalue += '{0:02d}:{1:02d}'.format(hours, minutes)

        except AttributeError:
            pass
        return _svalue

    @classmethod
    def gds_parse_date(cls, input_data):
        tz = None
        tz_off_pattern = re_.compile(r'([+\-])((0\d|1[0-3]):[0-5]\d|14:00)$')
        if input_data[-1] == 'Z':
            tz = FixedOffsetTZ(0, 'UTC')
            input_data = input_data[:-1]
        else:
            results = tz_off_pattern.search(input_data)

            if results is not None:
                tzoff_parts = results.group(2).split(':')
                tzoff = int(tzoff_parts[0]) * 60 + int(tzoff_parts[1])

                if results.group(1) == '-':
                    tzoff *= -1
                tz = FixedOffsetTZ(tzoff, results.group(0))
                input_data = input_data[:-6]

        dt = datetime_.datetime.strptime(input_data, '%Y-%m-%d')
        dt = dt.replace(tzinfo=tz)
        return dt.date()

    @staticmethod
    def gds_validate_time(input_data):
        return input_data

    @staticmethod
    def gds_format_time(input_data):
        if input_data.microsecond == 0:
            _svalue = '%02d:%02d:%02d' % (input_data.hour, input_data.minute, input_data.second)
        else:
            _svalue = '%02d:%02d:%02d.%s' % (input_data.hour, input_data.minute, input_data.second,
                                             ('%f' % (float(input_data.microsecond) / 1000000))[2:])

        if input_data.tzinfo is not None:
            tzoff = input_data.tzinfo.utcoffset(input_data)

            if tzoff is not None:
                total_seconds = tzoff.seconds + (86400 * tzoff.days)

                if total_seconds == 0:
                    _svalue += 'Z'
                else:
                    if total_seconds < 0:
                        _svalue += '-'
                        total_seconds *= -1
                    else:
                        _svalue += '+'
                    hours = total_seconds // 3600
                    minutes = (total_seconds - (hours * 3600)) // 60
                    _svalue += '{0:02d}:{1:02d}'.format(hours, minutes)

        return _svalue

    @staticmethod
    def gds_validate_simple_patterns(patterns, target):
        # pat is a list of lists of strings/patterns.
        # The target value must match at least one of the patterns
        # in order for the test to succeed.
        found1 = True

        for patterns1 in patterns:
            found2 = False

            for patterns2 in patterns1:
                mo = re_.search(patterns2, target)
                if mo is not None and len(mo.group(0)) == len(target):
                    found2 = True
                    break

            if not found2:
                found1 = False
                break

        return found1

    @classmethod
    def gds_parse_time(cls, input_data):
        tz = None
        tz_off_pattern = re_.compile(r'([+\-])((0\d|1[0-3]):[0-5]\d|14:00)$')
        if input_data[-1] == 'Z':
            tz = FixedOffsetTZ(0, 'UTC')
            input_data = input_data[:-1]
        else:
            results = tz_off_pattern.search(input_data)
            if results is not None:
                tzoff_parts = results.group(2).split(':')
                tzoff = int(tzoff_parts[0]) * 60 + int(tzoff_parts[1])

                if results.group(1) == '-':
                    tzoff *= -1

                tz = FixedOffsetTZ(tzoff, results.group(0))
                input_data = input_data[:-6]

        if len(input_data.split('.')) > 1:
            dt = datetime_.datetime.strptime(input_data, '%H:%M:%S.%f')
        else:
            dt = datetime_.datetime.strptime(input_data, '%H:%M:%S')

        dt = dt.replace(tzinfo=tz)
        return dt.time()

    def gds_check_cardinality_(self, value, input_name, min_occurs=0, max_occurs=1, required=None):
        if value is None:
            length = 0
        elif isinstance(value, list):
            length = len(value)
        else:
            length = 1

        if required is not None:
            if required and length < 1:
                self.gds_collector_.add_message(
                    "Required value {}{} is missing".format(input_name, self.gds_get_node_line_number_()))

        if length < min_occurs:
            self.gds_collector_.add_message(
                "Number of values for {}{} is below the minimum allowed, expected at least {}, found {}".format(
                    input_name, self.gds_get_node_line_number_(), min_occurs, length))
        elif length > max_occurs:
            self.gds_collector_.add_message(
                "Number of values for {}{} is above the maximum allowed, expected at most {}, found {}".format(
                    input_name, self.gds_get_node_line_number_(), max_occurs, length))

    def gds_validate_builtin_st_(self, validator, value, input_name):
        if value is not None:
            try:
                validator(value, input_name=input_name)
            except GDSParseError as parse_error:
                self.gds_collector_.add_message(str(parse_error))

    def gds_validate_defined_st_(self, validator, value):

        if value is not None:
            try:
                validator(value)
            except GDSParseError as parse_error:
                self.gds_collector_.add_message(str(parse_error))

    def get_path_(self, node):
        path_list = []
        self.get_path_list_(node, path_list)
        path_list.reverse()
        path = '/'.join(path_list)
        return path

    def get_path_list_(self, node, path_list):
        if node is None:
            return
        tag_strip_pattern_ = re_.compile(r'{.*}')

        tag = tag_strip_pattern_.sub('', node.tag)

        if tag:
            path_list.append(tag)

        self.get_path_list_(node.getparent(), path_list)

    @staticmethod
    def get_class_obj_(node, default_class=None):
        class_obj1 = default_class

        if 'xsi' in node.nsmap:
            class_name = node.get('{%s}dim_type' % node.nsmap['xsi'])
            if class_name is not None:
                names = class_name.split(':')
                if len(names) == 2:
                    class_name = names[1]
                class_obj2 = globals().get(class_name)
                if class_obj2 is not None:
                    class_obj1 = class_obj2

        return class_obj1

    @staticmethod
    def gds_build_any(node):
        # provide default value in case option --disable-xml is used.
        content = etree_.tostring(node, encoding="unicode")
        return content

    @classmethod
    def gds_reverse_node_mapping(cls, mapping):
        return dict(((v, k) for k, v in mapping.items()))

    @staticmethod
    def gds_encode(in_string):
        if sys.version_info.major == 2:
            if ExternalEncoding:
                encoding = ExternalEncoding
            else:
                encoding = 'utf-8'
            return in_string.encode(encoding)
        else:
            return in_string

    """
    def __eq__(self, other):
        def excl_select_objs_(obj):
            return obj[0] != 'parent_object_' and obj[0] != 'gds_collector_'

        if type(self) != type(other):
            return False

        return all(x == y for x, y in zip(filter(excl_select_objs_, self.__dict__.items()),
                                          filter(excl_select_objs_, other.__dict__.items())))
    """

    def __ne__(self, other):
        return not self.__eq__(other)

    # Django ETL transform hooks.

    def gds_djo_etl_transform(self):
        pass

    def gds_djo_etl_transform_db_obj(self, dbobj):
        pass

    # SQLAlchemy ETL transform hooks.

    @staticmethod
    def gds_sqa_etl_transform():
        return 0, None

    def gds_sqa_etl_transform_db_obj(self, dbobj):
        pass

    def gds_get_node_line_number_(self):
        if hasattr(self, "gds_element_tree_node_") and self.gds_element_tree_node_ is not None:
            return ' near line {}'.format(self.gds_element_tree_node_.sourceline)
        else:
            return ""


class GdsCollector(object):
    def __init__(self, messages=None):
        if messages is None:
            self.messages = []
        else:
            self.messages = messages

    def add_message(self, msg):
        self.messages.append(msg)

    def get_messages(self):
        return self.messages

    def clear_messages(self):
        self.messages = []

    def print_messages(self):
        for msg in self.messages:
            print(f"Warning: {msg}")
