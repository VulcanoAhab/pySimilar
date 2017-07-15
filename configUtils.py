import json
import copy


# ======================== Confs Objects ==========================
class BaseConf:
    """
    """
    @staticmethod
    def _monthYear(stringMonthYear):
        """
        """
        year, month=[int(d.strip())
                     for d in stringMonthYear.split("-")]
        return {"month":month, "year":year}

    @staticmethod
    def _monthYearRange(stringMonthYearStart, stringMonthYearEnd):
        """
        """
        start=Api._monthYear(stringMonthYearStart)
        end=Api._monthYear(stringMonthYearEnd)
        yearDiff=end["year"]-start["year"]
        max_month=13
        if not yearDiff:
            callRange=["{}-{:02d}".format(end["year"],month)
                      for month in range(start["month"], end["month"]+1)]
            return callRange

        callRange=["{}-{:02d}".format(start["year"],month)
                  for month in range(start["month"], max_month)]
        year=start["year"]
        for _ in range(yearDiff):
            year+=1
            if year == end["year"]:
                max_month=end["month"]+1
            for month in range(1,max_month):
                callRange.append("{}-{:02d}".format(year,month))
        return callRange

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
    def start_date(self):
        """
        """
        return self.getValue("START_DATE", True)

    @property
    def end_date(self):
        """
        """
        return self.getValue("END_DATE", True)

    @property
    def granularity(self):
        """
        """
        return self.getValue("GRANULARITY", True)

    @property
    def commonsDict(self):
        """
        """
        newDict=copy.deepcopy(self._data)
        newDict.pop("SITES")
        return newDict

    @property
    def projectPath(self):
        """
        """
        return self.getValue("PROJECT_PATH", True)

    @property
    def projectName(self):
        """
        """
        return self.getValue("PROJECT_PATH", True).split("/")[-1]


class TaskConf(BaseConf):
    """
    """
    def __init__(self, data):
        """
        """
        super().__init__(data)

    @property
    def site(self):
        """
        """
        return self.getValue("SITE", True)


class JobConf(BaseConf):
    """
    """
    def __init__(self, data):
        """
        """
        super().__init__(data)

    @property
    def sites(self):
        """
        """
        return self.getValue("SITES", True)

    @property
    def tasksGenerator(self):
        """
        """
        #task by site
        for siteDict in self.sites:
            data=self.commonsDict
            data["SITE"]=siteDict
            #gen task
            yield TaskConf(data)

    @property
    def tasksGeneratorByMonth(self):
        """
        """
        dateRange=JobConf._monthYearRange(self.start_date, self.end_date)
        for siteDict in self.sites:
            for date in dateRange:
                data=self.commonsDict
                data["SITE"]=siteDict
                data["START_DATE"]=date
                data["END_DATE"]=date
                #gen task
                yield TaskConf(data)


# ======================== Confs Workers ==========================
class FromFile(JobConf):
    """
    """

    @staticmethod
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
