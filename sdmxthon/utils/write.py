from io import StringIO

from .xml_base import makeWarnings


def save_file(message, path='', print_warnings=True):
    if path != '':
        gds_collector = message.gds_collector_
        makeWarnings(print_warnings, gds_collector)
        with open(path, "w") as f:
            message.export(f, 0, pretty_print=True, has_parent=False)
    else:
        f = StringIO()
        message.export(f, 0, pretty_print=True, has_parent=False)
        return f
