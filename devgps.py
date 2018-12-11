from typing import List
import gpxpy
import gpxpy.gpx
from datetime import datetime, timezone, timedelta
from DefDev import DevData, DevDataL

class DevGPS:
    def __init__(self, id, lat, lon, ele, data):
        self.id = id
        self.lat = lat
        self.lon = lon
        self.ele = ele
        self.data = data
        self.group = 0

    def __str__(self):
        res = self.__class__.__name__
        res = '('
        res += str(self.id) + ','
        res += str(self.lat) + ','
        res += str(self.lon) + ','
        res += str(self.ele) + ','
        res += str(self.data) + ','
        res += str(self.group)
        res += ')'
        return res

    def setGroupNumber(self, gno):
        self.group = gno

class DevGPSL:
    # 取得データにGPSのデータを付加
    # gpx: gpx data
    # devdatal: DevDataL
    def __init__(self, gpx, devdatal: DevDataL, deltaele=0):
        datalist = []

        tr_idx, seg_idx = self.__getSegment(gpx, devdatal.datalist)

        id = 0
        for d in devdatal.datalist:
            id += 1

            devgpsdata = ()
            point_s = []
            adjtime = d.time + d.leap
            for point in gpx.tracks[tr_idx].segments[seg_idx].points:
                if adjtime <= point.time:
                    # 座標の決定
                    if adjtime == point.time:
                        lat, lon, ele = point.latitude, point.longitude, point.elevation
                    else:
                        lat, lon, ele = self.__estimatePos(point_s, point, adjtime)
    
                    ele += deltaele
                    devgpsdata = DevGPS(id, lat, lon, ele, d)
                    break
                else:
                    point_s = point
                    continue
    
            if devgpsdata:
                datalist.append(devgpsdata)

        self.datalist = datalist

    def __str__(self):
        res = self.__class__.__name__
        res += '('
        for d in self.datalist:
            res += str(d) + ','
        res += ')'
        return res

    def __getSegment(self, gpx, datalist: List[DevData]):
        for t in range(0, len(gpx.tracks)):
            for s in range(0, len(gpx.tracks[t].segments)):
                p = gpx.tracks[t].segments[s].points
                for d in datalist:
                    if p[0].time <= d.time <= p[-1].time:
                        return t, s

        return 0, 0
        
    # 時刻から座標を推定
    # point_s: latest gpx data
    # point_e: next gpx data
    # time_c: current time
    def __estimatePos(self, point_s, point_e, time_c: datetime):
        if not point_s:
            lat = point_e.latitude
            lon = point_e.longitude
            ele = point_e.elevation
        else:        
            td_es = point_e.time - point_s.time
            td_cs = time_c - point_s.time
            
            ratio = td_cs.seconds / td_es.seconds
            
            lat = point_e.latitude * ratio + point_s.latitude * (1 - ratio)
            lon = point_e.longitude * ratio + point_s.longitude * (1 - ratio)
            ele = point_e.elevation * ratio + point_s.elevation * (1 - ratio)
        
        return lat, lon, ele

