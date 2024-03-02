class RowResult:
    """
    Represents a result obtained from sending a row from Excel to an HTTP server asynchronously.

    Attributes:
        is_page_found: (bool): Indicates whether the page associated with the row was found.
        table_info: (list of dict): Information about the table associated with the row, where each dictionary represents a row in the table.
        word (str): The word associated with the row.
        idioms: (list of str): List of idioms associated with the row.
    """

    def __init__(self, is_page_found=None, table_info=None, word=None, idioms=None):
        self._is_page_found = is_page_found
        self._table_info = table_info
        self._word = word
        self._idioms = idioms

    @property
    def is_page_found(self):
        """
        bool: Indicates whether the page associated with the row was found.
        """
        return self._is_page_found

    @is_page_found.setter
    def is_page_found(self, value):
        self._is_page_found = value

    @property
    def table_info(self):
        """
        list of dict: Information about the table associated with the row, where each dictionary represents a row in the table.
        """
        return self._table_info

    @table_info.setter
    def table_info(self, value):
        self._table_info = value

    @property
    def word(self):
        """
        str: The word associated with the row.
        """
        return self._word

    @word.setter
    def word(self, value):
        self._word = value

    @property
    def idioms(self):
        """
        list of str: List of idioms associated with the row.
        """
        return self._idioms

    @idioms.setter
    def idioms(self, value):
        self._idioms = value
