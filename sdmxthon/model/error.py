class SDMXError:
    """
    Base class for SDMX Error messages
    """

    def __init__(self, code, text):
        self._code = code
        self._text = text

    @property
    def code(self):
        """
        SDMX Error code.
        :return: SDMX Error code
        """
        return self._code

    @property
    def text(self):
        """
        SDMX Error text.
        :return: SDMX Error text
        """
        return self._text

    def __str__(self):
        return f"<SDMX Error - Code: {self.code} - Text: {self.text}>"

    def __repr__(self):
        return self.__str__()

    def __dict__(self):
        return {'code': self.code, 'text': self.text}
