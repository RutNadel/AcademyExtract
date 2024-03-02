class RowResult:
    """
    Represents a result obtained from sending a row from Excel to an HTTP server asynchronously.

    Attributes:
        is_page_found (bool): Indicates whether the page associated with the row was found.
        table_info (list of dict): Information about the table associated with the row, where each dictionary represents a row in the table.
        word (str): The word associated with the row.
        idioms (list of str): List of idioms associated with the row.
    """

    def __init__(self):
        self._is_page_found = None
        self._table_info = None
        self._word = None
        self._idioms = None

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


# Example usage:
result = RowResult()
result.is_page_found = True
result.table_info = [{"key1": "value1"}, {"key2": "value2"}]
result.word = "Some word"
result.idioms = ["idiom1", "idiom2"]

print(result.is_page_found)
print(result.table_info)
print(result.word)
print(result.idioms)
