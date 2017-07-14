class Generic:
    """
    """

    _traffic="https://api.similarweb.com/v1/website/{site}/" \
            "total-traffic-and-engagement/{endpoint}?api_key={token}"

    _traffic_fields={
        "granularity",
        "main_domain_only",
        "start_date",
        "end_date"
    }

    _traffic_geo="https://api.similarweb.com/v1/website/{site}/"\
                 "Geo/traffic-by-country?api_key={token}"

    def __init__(self, token, **kwargs):
        """
        """
        self._token=token
        self.site=None
        self.start_date=None
        self.end_date=None
        self.granularity=None
        # default
        self.main_domain_only=False

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

    def _traffic_url(self, endpoint):
        """
        """
        return self._traffic.format(endpoint=endpoint,
                                    site=self.site,
                                    token=self._token)

    def _traffic_args(self, fields=None):
        """
        @fields: field1[+ or -],field2[+ or -]...
        """
        if not fields:return {arg:getattr(self, arg)
                             for arg in  self._traffic_fields}
        addis=set()
        subis=set()
        new_args=copy.deepcopy(self._traffic_fields)
        for arg in fields.split(","):
            if arg[-1]=="+":
                addis.add(arg[:-1])
            elif arg[-1]=="-":
                subis.add(arg[:-1])
            else:
                raise TypeError("[-] Unkown ARGS SET operation")
        if addis:
            new_args=new_args.union(addis)
        if subis:
            new_args=new_args.difference(subis)
        return {arg:getattr(self, arg) for arg in new_args}

    def _traffic_get(self, url, params):
        """
        """
        r=requests.get(url, params=params)
        if r.status_code != 200:
            msg="[-] Request fail. Status:{} "\
                "Msg:{} | URL: {}".format(r.status_code,r.content, url)
            print(msg)
            return None
        return r.json()

    def countVisits(self):
        """
        """
        url=self._traffic_url("visits")
        params=self._traffic_args()
        return self._traffic_get(url, params)

    def durationVisits(self):
        """
        """
        url=self._traffic_url("average-visit-duration")
        params=self._traffic_args()
        return self._traffic_get(url, params)

    def bounceRateVisits(self):
        """
        """
        url=self._traffic_url("bounce-rate")
        params=self._traffic_args()
        return self._traffic_get(url, params)

    def pageViewVisits(self):
        """
        """
        url=self._traffic_url("pages-per-visit")
        params=self._traffic_args()
        return self._traffic_get(url, params)

    def splitVisits(self):
        """
        """
        url=self._traffic_url("visits-split")
        params=self._traffic_args("granularity-")
        return self._traffic_get(url, params)

    def byGeoVisits(self):
        """
        """
        url=self._traffic_geo.format(site=self.site,token=self._token)
        params=self._traffic_args("granularity-")
        return self._traffic_get(url, params)
