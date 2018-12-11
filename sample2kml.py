import sys
import gpxpy
import gpxpy.gpx
from dataset_sample import DevDataL_Sample, DevGPSL_Sample
import genkml
import kmlstyle_sample

if __name__ == '__main__':
    gpxfile = 'sample.gpx'
    samplejsonfile = 'sample.json'
    savefile = 'sample.kml'
    options = []

    if len(sys.argv) < 4:
        print('gpx_file json_file save_file')
        print('sample data exec.')
        options = sys.argv[1:]
    else:
        gpxfile = sys.argv[1]
        samplejsonfile = sys.argv[2]
        savefile = sys.argv[3]
        options = sys.argv[4:]

    # input(gpx file)
    with open(gpxfile, 'r') as f:
        gpx = gpxpy.parse(f)

    # input(data file)
    devdatal = DevDataL_Sample(samplejsonfile)
    devdatal.setOptions(options)

    # gpx + sample
    samplegpsl = DevGPSL_Sample(gpx, devdatal)

    # output
    genkml.generate(samplegpsl, savefile, kmlstyle_sample.KmlStyle_normal())
