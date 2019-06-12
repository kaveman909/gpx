from xml.etree import ElementTree as ET
from datetime import datetime as DT
from math import sin, cos, asin, sqrt, radians, atan2, degrees
import matplotlib.pyplot as plt


def haversine(lon1, lat1, lon2, lat2):
    """
    Calculate the great circle distance between two points 
    on the earth (specified in decimal degrees)
    """
    # convert decimal degrees to radians
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    # haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    r = 6371  # Radius of earth in km
    return c * r


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

for i in range(1, len(lat)):
    ddist = haversine(lon[i - 1], lat[i - 1], lon[i], lat[i])
    dtime = (time[i] - time[i - 1]).seconds
    dele = ele[i] - ele[i - 1]

    speed_kmh = ddist/dtime * 3600
    slope_deg = degrees(atan2(dele, ddist*1000))

    print(ddist*1000, dtime, dele, speed_kmh, slope_deg)
