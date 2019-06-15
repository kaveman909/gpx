from xml.etree import ElementTree as ET
from datetime import datetime as DT
from math import sin, cos, asin, sqrt, radians, atan2, degrees, exp, tan
import matplotlib.pyplot as plt
import scipy.optimize as op
import numpy as np
import random

speed_filter = 100  # km/h max
slope_filter = 100  # deg max


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


def tobler(thetas, a, b, c):
    y = list()
    for theta in thetas:
        y.append(a * exp(-b * abs(tan(radians(theta)) + c)))
    return np.array(y)


tree = ET.parse('Tracks.gpx')
root = tree.getroot()

prefix = '{http://www.topografix.com/GPX/1/1}'

lat = list()  # in decimal degrees
lon = list()  # in decimal degrees
ele = list()  # in meters
time = list()
speed_kmh = list()
slope_deg = list()
speed_kmh_ind = list()
slope_deg_ind = list()
name_colors = dict()
i = 0
for trk in root.iter(prefix + 'trk'):
    speed_kmh_ind.clear()
    slope_deg_ind.clear()
    lat.clear()
    lon.clear()
    ele.clear()
    time.clear()
    name = trk.find(prefix + 'name').text
    try:
        color = name_colors[name]
    except KeyError:
        name_colors[name] = 'C{}'.format(i)
        i += 1
        color = name_colors[name]
    for trkpt in trk.iter(prefix + 'trkpt'):
        lat.append(float(trkpt.attrib['lat']))
        lon.append(float(trkpt.attrib['lon']))
        ele.append(float(trkpt.find(prefix + 'ele').text))
        time.append(DT.strptime(trkpt.find(
            prefix + 'time').text, '%Y-%m-%dT%H:%M:%SZ'))

    for i in range(1, len(lat)):
        ddist = haversine(lon[i - 1], lat[i - 1], lon[i], lat[i])
        dtime = (time[i] - time[i - 1]).seconds
        dele = ele[i] - ele[i - 1]

        speed_kmh_temp = ddist/dtime * 3600
        slope_deg_temp = degrees(atan2(dele, ddist*1000))
        if (speed_kmh_temp < speed_filter) and (abs(slope_deg_temp) < slope_filter):
            speed_kmh.append(speed_kmh_temp)
            speed_kmh_ind.append(speed_kmh_temp)
            slope_deg.append(slope_deg_temp)
            slope_deg_ind.append(slope_deg_temp)

    plt.plot(slope_deg_ind, speed_kmh_ind, c=color,
             marker='o', label=name, ms=1, ls="")

slope_deg_x = np.array(slope_deg)
speed_kmh_y = np.array(speed_kmh)
initial_guess = np.array([6, 3.5, 0.05])  # default params of tobler function

popt, pcov = op.curve_fit(tobler, slope_deg_x,
                          speed_kmh_y, p0=initial_guess)

print('Number of data points: {}'.format(len(slope_deg)))

perr = np.sqrt(np.diag(pcov))
print('Error: {}'.format(perr))
tobler_kmh = list(tobler(slope_deg_x, *popt))

plt.plot(slope_deg, tobler_kmh, 'bo',
         label='fit : a=%5.3f, b=%5.3f, c=%5.3f' % tuple(popt), ms=1)
plt.xlabel('slope (deg)')
plt.ylabel('speed (km/h)')
plt.legend()
plt.show()
