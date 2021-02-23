from ..utils.data_parser import DataParser
from ..utils.xml_base import find_attr_value_, cast


class TextType(DataParser):
    """TextType provides for a set of language-specific alternates to be
    provided for any human-readable constructs in the instance.The xml:lang
    attribute specifies a language code for the text. If not supplied, the

    default language is assumed to be English."""
    __hash__ = DataParser.__hash__
    subclass = None
    superclass = None

    def __init__(self, lang='en', value_of=None, extension_type=None, gds_collector_=None):
        super(TextType, self).__init__(gds_collector_)
        self._namespace_prefix = ''
        self._lang = cast(None, lang)
        self._lang_nsprefix_ = None
        self._value = value_of
        self._extension_type_ = extension_type
        self._namespace_def = 'xmlns:common="http://www.sdmx.org/resources/sdmxml/schemas/v2_1/common"'
        self._namespace_prefix = "common"
        self._name = 'TextType'

    @staticmethod
    def factory(*args_, **kwargs_):
        return TextType(*args_, **kwargs_)

    @property
    def lang(self):
        return self._lang

    @lang.setter
    def lang(self, value):
        self._lang = value

    @property
    def extensiontype(self):
        return self._extension_type_

    @extensiontype.setter
    def extensiontype(self, value):
        self._extension_type_ = value

    def has_content_(self):
        if type(self._value) in [int, float]:
            return True
        else:
            return False

    def build_attributes(self, node, attrs, already_processed):
        value = find_attr_value_('_lang', node)

        if value is not None and '_lang' not in already_processed:
            already_processed.add('_lang')
            self._lang = value

        value = find_attr_value_('xsi:dim_type', node)

        if value is not None and 'xsi:dim_type' not in already_processed:
            already_processed.add('xsi:dim_type')
            self._extension_type_ = value


# end class TextType

class AnnotationType(DataParser):
    """_annotationType provides for non-documentation notes and annotations to
    be embedded in data and structure messages. It provides optional fields
    for providing a title, a dim_type description, a URI, and the text of the
    annotation.The id_ attribute provides a non-standard identification of
    an annotation. It can be used to disambiguate annotations."""
    __hash__ = DataParser.__hash__
    subclass = None
    superclass = None

    def __init__(self, idx=None, annotation_title=None, annotation_type_member=None, annotation_URL=None,
                 AnnotationText=None, gds_collector_=None, **kwargs_):
        super(AnnotationType, self).__init__(gds_collector_)
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self._id = cast(None, idx)
        self._id_nsprefix_ = None
        self._annotationTitle = annotation_title
        self._annotationTitle_nsprefix_ = None
        self._annotationType = annotation_type_member
        self._annotationType_nsprefix_ = None
        self._annotationURL = annotation_URL
        self._annotationURL_nsprefix_ = None

        if AnnotationText is None:
            self._annotationText = []
        else:
            self._annotationText = AnnotationText

        self.AnnotationText_nsprefix_ = None
        self._namespace_def = 'xmlns:common="http://www.sdmx.org/resources/sdmxml/schemas/v2_1/common"'
        self._namespace_prefix = "common"
        self._name = 'AnnotationType'

    @staticmethod
    def factory(*args_, **kwargs_):
        return AnnotationType(*args_, **kwargs_)

    @property
    def annotation_title(self):
        return self._annotationTitle

    @annotation_title.setter
    def annotation_title(self, value):
        self._annotationTitle = value

    @property
    def annotation_type(self):
        return self._annotationType

    @annotation_type.setter
    def annotation_type(self, value):
        self._annotationType = value

    @property
    def annotation_url(self):
        return self._annotationURL

    @annotation_url.setter
    def annotation_url(self, value):
        self._annotationURL = value

    @property
    def annotation_text(self):
        return self._annotationText

    @annotation_text.setter
    def annotation_text(self, value):
        if value is None:
            self._annotationText = []
        elif isinstance(value, list):
            self._annotationText = value
        else:
            raise TypeError('Annotation Text must be a list')

    def add_AnnotationText(self, value):
        self._annotationText.append(value)

    def insert_AnnotationText_at(self, index, value):
        self._annotationText.insert(index, value)

    def replace_AnnotationText_at(self, index, value):
        self._annotationText[index] = value

    @property
    def id_(self):
        return self._id

    def has_content_(self):
        if (
                self._annotationTitle is not None or
                self._annotationType is not None or
                self._annotationURL is not None or
                self._annotationText
        ):
            return True
        else:
            return False

    def build_attributes(self, node, attrs, already_processed):
        value = find_attr_value_('id', node)

        if value is not None and 'id' not in already_processed:
            already_processed.add('id')
            self._id = value

    def build_children(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'AnnotationTitle':
            value_ = child_.text
            value_ = self.gds_parse_string(value_)
            value_ = self.gds_validate_string(value_)
            self._annotationTitle = value_
            self._annotationTitle_nsprefix_ = child_.prefix
        elif nodeName_ == 'AnnotationType':
            value_ = child_.text
            value_ = self.gds_parse_string(value_)
            value_ = self.gds_validate_string(value_)
            self._annotationType = value_
            self._annotationType_nsprefix_ = child_.prefix
        elif nodeName_ == 'AnnotationURL':
            value_ = child_.text
            value_ = self.gds_parse_string(value_)
            value_ = self.gds_validate_string(value_)
            self._annotationURL = value_
            self._annotationURL_nsprefix_ = child_.prefix
        elif nodeName_ == 'AnnotationText':
            class_obj_ = self.get_class_obj_(child_, TextType)
            obj_ = class_obj_.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self._annotationText.append(obj_)
            obj_.original_tag_name_ = 'AnnotationText'


# end class _annotationType

class AnnotationsType(DataParser):
    """AnnotationsType provides for a list of annotations to be attached to
    data and structure messages."""
    __hash__ = DataParser.__hash__
    subclass = None
    superclass = None

    def __init__(self, Annotation=None, gds_collector_=None, **kwargs_):
        super(AnnotationsType, self).__init__(gds_collector_)
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None

        if Annotation is None:
            self._annotation = []
        else:
            self._annotation = Annotation

        self.Annotation_nsprefix_ = None
        self._name = 'AnnotationsType'
        self._namespacedef = 'xmlns:common="http://www.sdmx.org/resources/sdmxml/schemas/v2_1/common"'
        self._namespaceprefix = "common"

    @staticmethod
    def factory(*args_, **kwargs_):
        return AnnotationsType(*args_, **kwargs_)

    @property
    def annotation(self):
        return self._annotation

    @annotation.setter
    def annotation(self, value):
        if value is None:
            self._annotation = []
        elif isinstance(value, list):
            self._annotation = value
        else:
            raise TypeError('Annotation must be a list')

    def add_Annotation(self, value):
        self._annotation.append(value)

    def insert_Annotation_at(self, index, value):
        self._annotation.insert(index, value)

    def replace_Annotation_at(self, index, value):
        self._annotation[index] = value

    def has_content_(self):
        if (
                self._annotation
        ):
            return True
        else:
            return False

    def build_children(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'Annotation':
            obj_ = AnnotationType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self._annotation.append(obj_)
            obj_.original_tagname_ = 'Annotation'


# end class AnnotationsType

class AnnotableType(DataParser):
    """AnnotableType is an abstract base dim_type used for all annotable artefacts.
    Any dim_type that provides for annotations should extend this dim_type."""
    __hash__ = DataParser.__hash__
    subclass = None
    superclass = None

    def __init__(self, Annotations=None, extensiontype_=None, gds_collector_=None, **kwargs_):
        super(AnnotableType, self).__init__(gds_collector_, **kwargs_)
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self._annotations = Annotations
        self._annotations_nsprefix_ = None
        self._extension_type_ = extensiontype_
        self._namespacedef = 'xmlns:common="http://www.sdmx.org/resources/sdmxml/schemas/v2_1/common"'
        self._namespaceprefix = "common"
        self._name = 'AnnotableType'
        self._childs = None

    @staticmethod
    def factory(*args_, **kwargs_):
        return AnnotableType(*args_, **kwargs_)

    @property
    def annotations(self):
        return self._annotations

    @annotations.setter
    def annotations(self, value):
        self._annotations = value

    @property
    def extensiontype(self):
        return self._extension_type_

    @extensiontype.setter
    def extensiontype(self, value):
        self._extension_type_ = value

    def build_children(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'Annotations':
            obj_ = AnnotationsType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            obj_.original_tagname_ = 'Annotations'
            self._childs = obj_
# end class AnnotableType
