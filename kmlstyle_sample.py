import sys
from DefDev import DevData
from devgps import DevGPS
from dataset_sample import DevDataL_Sample, DevGPSL_Sample
import genkml
from genkml import IconItem, KmlStyle
import simplekml

# samplegpslistを通信できたかを元にした色付けで，KMLファイルで出力
# samplegpslist: DevGPS list
# filename: output file name
class KmlStyle_normal(KmlStyle):
    ICONS = [
        IconItem(1, 'http://maps.google.com/mapfiles/kml/pushpin/blue-pushpin.png', ''),
        IconItem(.6, 'http://maps.google.com/mapfiles/kml/pal3/icon33.png', '')
    ]

    def setGroup(self, samplegpsl: DevDataL_Sample):
        samplegpsl.setGroupNormal()

    def getName(self, devgpssample: DevGPS):
        res = ''
        sampledata = devgpssample.data
        if sampledata.status < DevData.STATUS_NG:
            res = str(sampledata.id)
        else:
            res = 'NG-{0}'.format(str(devgpssample.id))
            
        return res

    def getDescription(self, devgpssample: DevGPS):
        data = devgpssample.data
        txt = '<table><tbody>'
        txt += '<tr><td><nobr>ID: {0}</nobr></td></tr>'.format(data.id) if data.id else ''
        txt += '<tr><td><nobr>Time: {0}</nobr></td></tr>'.format(data.time.isoformat())
        txt += '<tr><td><nobr>data1: {0}</nobr></td></tr>'.format(data.mydata[0]) if data.mydata else ''
        txt += '<tr><td><nobr>data2: {0}</nobr></td></tr>'.format(data.mydata[1]) if data.mydata else ''
        txt += '</tbody></table>'
        return txt

    def setKmlOptions(self, kml, devgpssample: DevGPS):
        kml.altitudemode = simplekml.AltitudeMode.absolute
        kml.extrude = 1

