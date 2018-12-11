from abc import ABCMeta, abstractmethod
from collections import namedtuple
import simplekml
from devgps import DevGPSL, DevGPS

IconItem = namedtuple('IconItem', ('scale', 'url', 'color'))

class KmlStyle(metaclass=ABCMeta):
    ICONS = []
    @abstractmethod
    def setGroup(self, devgpsl: DevGPSL):
        pass

    @abstractmethod
    def getName(self, devgps: DevGPS):
        pass

    @abstractmethod
    def getDescription(self, devgps: DevGPS):
        pass

    @abstractmethod
    def setKmlOptions(self, kmlpoint, devgps: DevGPS):
        pass

def generate(devgpsl: DevGPSL, filename, kmlstyle: KmlStyle, setGroupValid=True, deltaele=0, description='', option=False):
    if setGroupValid:
        kmlstyle.setGroup(devgpsl)

    kml = simplekml.Kml()
    if description:
        kml.document = simplekml.Document(description=description)
    for d in devgpsl.datalist:
        p = kml.newpoint(name=kmlstyle.getName(d))

        p.coords = [(d.lon, d.lat, d.ele+deltaele)]
        p.description = kmlstyle.getDescription(d)

        p.style.iconstyle.scale = kmlstyle.ICONS[d.group].scale
        p.style.iconstyle.icon.href = kmlstyle.ICONS[d.group].url
        if kmlstyle.ICONS[d.group].color:
            p.style.iconstyle.color = kmlstyle.ICONS[d.group].color

        if option:
            kmlstyle.setKmlOptions(p, d)

    kml.save(filename)

if __name__ == '__main__':
    icons = [
        IconItem(1, 'http://maps.google.com/mapfiles/kml/pushpin/blue-pushpin.png', ''),
        IconItem(.6, 'http://maps.google.com/mapfiles/kml/pal3/icon33.png', '')
    ]

    gpxfile = 'sample.gpx'
    samplejsonfile = 'sample.json'

    # GPXデータを取得
    import gpxpy
    import gpxpy.gpx
    with open(gpxfile, 'r') as f:
        gpx = gpxpy.parse(f)

    # input
    from dataset_sample import DevDataL_Sample
    devdatal = DevDataL_Sample(samplejsonfile)

    # make
    from devgps import DevGPS, DevGPSL
    devgpsl = DevGPSL(gpx, devdatal)

    # generate
    for d in devgpsl.datalist:
        d.setGroupNumber(0 if d.status < DevGPS.STATUS_NG else 1)
 
    generate(devgpsl, 'sample.kml', icons)
