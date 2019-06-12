from xml.etree import ElementTree as ET
from datetime import datetime as DT

tree = ET.parse('squires-castle-willoughby-hills-oh-usa.gpx')
root = tree.getroot()

prefix = '{http://www.topografix.com/GPX/1/1}'

lat = list()  # in decimal degrees
lon = list()  # in decimal degrees
ele = list()  # in meters
time = list()

for trkpt in root.iter(prefix + 'trkpt'):
    lat.append(float(trkpt.attrib['lat']))
    lon.append(float(trkpt.attrib['lon']))
    ele.append(float(trkpt.find(prefix + 'ele').text))
    time.append(DT.strptime(trkpt.find(
        prefix + 'time').text, '%Y-%m-%dT%H:%M:%SZ'))

for la, lo, el, ti in zip(lat, lon, ele, time):
    print(la, lo, el, ti)
