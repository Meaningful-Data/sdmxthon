"""
    Data parser file contains only the DataParser class
"""

from sdmxthon.utils.xml_base import encode_str_2_3, Tag_pattern_
from .gdscollector import GenerateSuper

Validate_simpletypes_ = True
UseCapturedNS_ = True
save_element_tree_node = False


class DataParser(GenerateSuper):
    """
    Data Parser contains all abstract methods to parse the information of a
    SDMX-ML file, as well as the validations methods.
    """

    def __init__(self, gds_collector_=None, **kwargs_):
        super().__init__(gds_collector_)
        self._value = ''
        self.gds_collector_ = gds_collector_
        if save_element_tree_node:
            self.gds_element_tree_node_ = None
        self.__validate_NestedNCNameIDType_patterns = [
            ['^([A-Za-z][A-Za-z0-9_\\-]*(\\.[A-Za-z][A-Za-z0-9_\\-]*)*)$'],
            ['^([A-Za-z0-9_@$\\-]+(\\.[A-Za-z0-9_@$\\-]+)*)$']]
        self.__validate_IDType_patterns = [['^([A-Za-z0-9_@$\\-]+)$'],
                                           ['^([A-Za-z0-9_@$\\-]+(\\.['
                                            'A-Za-z0-9_@$\\-]+)*)$']]
        self.__validate_VersionType_patterns = [['^([0-9]+(\\.[0-9]+)*)$']]
        self.__validate_NestedIDType_patterns = [
            ['^([A-Za-z0-9_@$\\-]+(\\.[A-Za-z0-9_@$\\-]+)*)$']]
        self.__validate_NCNameIDType_patterns = [
            ['^([A-Za-z][A-Za-z0-9_\\-]*)$'], ['^([A-Za-z0-9_@$\\-]+)$'],
            ['^([A-Za-z0-9_@$\\-]+(\\.[A-Za-z0-9_@$\\-]+)*)$']]

    @staticmethod
    def _factory(*args_, **kwargs_):
        """Factory methods are provided to generate the desired class in
        order to parse any XML Element that is currently supported by the
        library """
        pass

    def _build(self, node, gds_collector_=None):
        """Build method is used to parse a XML element, its attributes and
        its children """

        self.gds_collector_ = gds_collector_

        if save_element_tree_node:
            self.gds_element_tree_node_ = node

        already_processed = set()

        self._build_attributes(node, node.attrib, already_processed)

        for child in node:
            node_name_ = Tag_pattern_.match(child.tag).groups()[-1]
            self._build_children(child, node, node_name_,
                                 gds_collector_=gds_collector_)

        return self

    def _build_attributes(self, node, attributes_, already_processed):
        """Builds the attributes present in the XML element"""
        pass

    def _validate_nested_NC_name_id_type(self, value):
        """Validate dim_type NestedNCNameIDType, a restriction on
        NestedIDType. """
        result = True

        if (value is not None and Validate_simpletypes_ and
                self.gds_collector_ is not None):
            if not isinstance(value, str):
                lineno = self._gds_get_node_line_number_()
                self.gds_collector_.add_message(f'Value "{value}": {lineno} '
                                                f'is not of the correct base '
                                                f'simple dim_type (str)')
                return False

            if not self._gds_validate_simple_patterns(
                    self.__validate_NestedNCNameIDType_patterns, value):
                self.gds_collector_.add_message(
                    f'Value "{encode_str_2_3(value)}" '
                    f'does not match xsd pattern restrictions: '
                    f'{self.__validate_NestedNCNameIDType_patterns}')
                result = False

        return result

    def _validate_id_type(self, value):
        """Validate dim_type IDType, a restriction on NestedIDType."""
        result = True

        if (value is not None and Validate_simpletypes_ and
                self.gds_collector_ is not None):
            if not isinstance(value, str):
                lineno = self._gds_get_node_line_number_()
                self.gds_collector_.add_message(f'Value "{value}": {lineno} is'
                                                f' not of the correct base '
                                                f'simple dim_type (str)')
                return False

            if not self._gds_validate_simple_patterns(
                    self.__validate_IDType_patterns, value):
                self.gds_collector_.add_message(
                    f'Value "{encode_str_2_3(value)}" '
                    f'does not match xsd pattern restrictions: '
                    f'{self.__validate_IDType_patterns}')
                result = False

        return result

    def _validate_version_type(self, value):
        """Validate dim_type VersionType, a restriction on xs:string."""
        result = True

        if (value is not None and Validate_simpletypes_ and
                self.gds_collector_ is not None):
            if not isinstance(value, str):
                lineno = self._gds_get_node_line_number_()
                self.gds_collector_.add_message(f'Value "{value}": {lineno} is'
                                                f' not of the correct base '
                                                f'simple dim_type (str)')
                return False

            if not self._gds_validate_simple_patterns(
                    self.__validate_VersionType_patterns, value):
                self.gds_collector_.add_message(
                    f'Value "{encode_str_2_3(value)}" '
                    f'does not match xsd pattern restrictions: '
                    f'{self.__validate_IDType_patterns}')
                result = False

        return result

    def _validate_action_type(self, value):
        """Validate dim_type ActionType, a restriction on xs:NMTOKEN."""
        result = True
        if (value is not None and Validate_simpletypes_ and
                self.gds_collector_ is not None):
            if not isinstance(value, str):
                lineno = self._gds_get_node_line_number_()
                self.gds_collector_.add_message(
                    f'Value "{value}" : {lineno} is not of '
                    f'the correct base simple dim_type (str)')
                return False
            value = value
            enumerations = ['Append', 'Replace', 'Delete', 'Information']
            if value not in enumerations:
                lineno = self._gds_get_node_line_number_()
                self.gds_collector_.add_message(
                    f'Value "{encode_str_2_3(value)}":{lineno} '
                    f'does not match xsd enumeration '
                    f'restriction on ActionType')
                result = False
        return result

    def _build_children(self, child, node, node_name_, gds_collector_):
        """Builds the childs of the XML element"""
        pass
