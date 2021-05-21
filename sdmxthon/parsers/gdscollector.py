"""
    GDS collector file contains all structural classes
"""

import datetime as datetime_
import decimal as decimal_
import re as re_

from SDMXThon.utils.xml_base import raise_parse_error

ExternalEncoding = ''


def _gds_str_lower(in_string):
    return in_string.lower()


class FixedOffsetTZ(datetime_.tzinfo):
    """Offset of a Timezone"""

    def __init__(self, offset, name):
        self.__offset = datetime_.timedelta(minutes=offset)
        self._name = name

    def utcoffset(self, dt):
        """Offset for UTC"""
        return self.__offset

    def tzname(self, dt):
        """Timezone name"""
        return self._name

    def dst(self, dt):
        """Override of method tz.dst"""
        return None


class GenerateSuper(object):
    """Class above all that has the GDS collector to get all messages"""

    def __init__(self, gds_collector):
        self.gds_element_tree_node_ = None
        if gds_collector is not None:
            self.gds_collector_ = gds_collector
        else:
            self.gds_collector_ = GdsCollector()

    @staticmethod
    def _gds_validate_string(input_data):
        if not input_data:
            return ''
        else:
            return input_data

    @staticmethod
    def _gds_validate_integer(input_data, node=None):
        value = None
        try:
            value = int(input_data)
        except (TypeError, ValueError):
            raise_parse_error(node, 'Requires integer value')

        return value

    @staticmethod
    def _gds_validate_decimal(input_data, node=None):
        try:
            decimal_.Decimal(input_data)
        except (TypeError, ValueError):
            raise_parse_error(node, 'Requires decimal value')

        return input_data

    @staticmethod
    def _gds_validate_double(input_data, node=None):

        try:
            float(input_data)
        except (TypeError, ValueError):
            raise_parse_error(node, 'Requires double or float value')

        return input_data

    def _gds_get_node_line_number_(self):
        if hasattr(self, "gds_element_tree_node_") and \
                self.gds_element_tree_node_ is not None:
            return f' near line {self.gds_element_tree_node_.sourceline}'
        else:
            return ""

    @staticmethod
    def _gds_format_boolean(input_data):
        return f'{input_data}'.lower()

    @staticmethod
    def _gds_parse_boolean(input_data, node=None):
        value = None
        if input_data in ('true', '1'):
            value = True
        elif input_data in ('false', '0'):
            value = False
        else:
            raise_parse_error(node, 'Requires boolean value')

        return value

    @staticmethod
    def _gds_validate_boolean(input_data, node=None):
        if input_data not in (True, 1, False, 0, 'false', 'true'):
            raise_parse_error(node, 'Requires boolean value '
                                    '(one of True, 1, False, 0)')

        return input_data

    @classmethod
    def _gds_parse_datetime(cls, input_data):
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
            input_data = '%s.%s' % (
                time_parts[0], "{}".format(micro_seconds).rjust(6, "0"),)
            dt = datetime_.datetime.strptime(input_data,
                                             '%Y-%m-%dT%H:%M:%S.%f')
        else:
            dt = datetime_.datetime.strptime(input_data, '%Y-%m-%dT%H:%M:%S')

        dt = dt.replace(tzinfo=tz)
        return dt

    @staticmethod
    def _gds_validate_simple_patterns(patterns, target):
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


class GdsCollector(object):
    """Collector of error messages"""

    def __init__(self, messages=None):
        if messages is None:
            self.messages = []
        else:
            self.messages = messages

    def add_message(self, msg):
        """Add messages to the list"""
        self.messages.append(msg)

    def get_messages(self):
        """Get all messages"""
        return self.messages

    def clear_messages(self):
        """Clear list of messages"""
        self.messages = []

    def print_messages(self):
        """Print all messages"""
        for msg in self.messages:
            print(f"Warning: {msg}")
