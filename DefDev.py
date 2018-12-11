from abc import ABCMeta, abstractmethod
from datetime import datetime, timezone, timedelta
import copy

class DevData:
    STATUS_OK = 0
    STATUS_NG = 100

    def __init__(self, time: datetime, status=0, leap=0):
        self.time = time
        self.status = status
        self.leap = timedelta(seconds=leap)

    def setLeap(self, leap):
        self.leap = timedelta(seconds=leap)

    @abstractmethod
    def setInterpolationPointData(self, time: datetime):
        pass

class DevDataL:
    def __init__(self):
        self.datalist = []

    def __str__(self):
        res = self.__class__.__name__
        res += '('
        for d in self.datalist:
            res += str(d) + ','
        res += ')'
        return res

    def setOptions(self, options=[]):
        for option in options:
            opt = option.split('=')
            if opt[0] == '-i':
                self.interpolation(int(opt[1]))
            elif opt[0] == '-l':
                self.setLeap(int(opt[1]))
 
    # 通信できなかった地点を補間
    # cycle: device commuication cycle[sec]
    def interpolation(self, cycle):
        adjdata = []
        nexttime = self.datalist[0].time
        for d in self.datalist:
            nexttime += timedelta(seconds=cycle)
            while nexttime < d.time:
                ds = copy.copy(d)
                ds.setInterpolationPointData(nexttime)
                adjdata.append(ds)
                nexttime += timedelta(seconds=cycle)
            adjdata.append(d)
            nexttime = d.time
        self.datalist = adjdata

    # UTCをGPS時刻に補正する
    # leap: leap seconds[sec]
    # というのを作ったけど，多分，GPSデータの時刻はUTCに補正されてるっぽいので使わない．
    def setLeap(self, leap=0):
        for d in self.datalist:
            d.setLeap(leap)

