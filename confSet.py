import json

class ConfObj:
    """
    """
    def __init__(self, data):
        """
        """
        self._data=data

    def getValue(self, key, fail=False):
        """
        """
        if key not in self._data and fail:
            raise KeyError("[-] Unkown: {}".format(key))
        return self._data[key]

    @property
    def token(self):
        """
        """
        return self.getValue("TOKEN", True)

    @property
    def sites(self):
        """
        """
        return self.getValue("SITES", True)

    @property
    def start_date(self):
        """
        """
        return self.getValue("START_DATE", True)

    @property
    def end_date(self):
        """
        """
        return self.getValue("END_DATE", True)


class FromFile(ConfObj):
    """
    """

    @classmethod
    def load_file(filePath):
        """
        """
        fd=open(filePath, "r")
        _fileData=json.load(fd)
        fd.close()
        return _fileData

    def __init__(self, filePath=None):
        """
        """
        self.filePath=filePath
        super().__init__(FromFile.load_file(filePath))
