from typing import List
from datetime import datetime, timezone, timedelta
import json
from DefDev import DevData, DevDataL
from devgps import DevGPS, DevGPSL

class DevData_Sample(DevData):
    def __init__(self, id, time: datetime, mydata, status=DevData.STATUS_OK):
        super().__init__(time, status)
        self.id = id
        self.mydata = mydata

    def __str__(self):
        res = self.__class__.__name__
        res += '('
        res += str(self.id) + ','
        res += str(self.time) + ','
        res += str(self.mydata) + ','
        res += str(self.status)
        res += ')'
        return res

    def setInterpolationPointData(self, time: datetime):
        self.entry_id = ''
        self.time = time
        self.mydata = ()
        self.status = DevData.STATUS_NG

class DevDataL_Sample(DevDataL):
    # Sampleデータを取得
    # filename: Sample json file
    def __init__(self, filename):
        super().__init__()
        jsondata = self.__getJsonData(filename)
        sampledata = self.__transSampleData(jsondata)
        self.datalist = sampledata

    # SampleのJSONデータを取得
    # filename: Sample json file
    # return: Sample json data
    def __getJsonData(self, filename):
        with open(filename, 'r') as f:
            jsondata = json.load(f)
        return jsondata

    # SampleのJSONデータをSampleDataSetに変換
    # jsondata: Sample json data
    # return: SampleDataSet list
    def __transSampleData(self, jsondata):
        sampledata = []
        for d in jsondata['feeds']:
            time = datetime.strptime(d['time'], '%Y-%m-%dT%H:%M:%SZ')
            ds = DevData_Sample(id=d['id'], time=time, mydata=(d['data1'], d['data2']))
            sampledata.append(ds)

        return sampledata

class DevGPSL_Sample(DevGPSL):
    def __init__(self, gpx, devdatal: List[DevData_Sample], deltaele=0):
        super().__init__(gpx, devdatal, deltaele)

    def setGroupNormal(self):
        for d in self.datalist:
            d.setGroupNumber(0 if d.data.status < DevData.STATUS_NG else 1)

if __name__ == '__main__':
    print(DevDataL_Sample('sample.json'))

