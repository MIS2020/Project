from math import sin, cos, sqrt, atan2, radians

vlat= 40.0370601
vlong= -75.3457687
danlat= 40.0452466
danlong= -75.4089339

lat1= radians(vlat)
long1= radians(vlong)
lat2= radians(danlat)
long2= radians(danlong)

# Provide a relatively accurate center lat, lon returned as a list pair, given
# a list of list pairs.
# ex: in: geolocations = ((lat1,lon1), (lat2,lon2),)
#     out: (center_lat, center_lon)


lst=[(lat1,long1),(lat2,long2)]


def center_geolocation(lst):
    x = 0
    y = 0
    z = 0

    for lat, lon in lst:
        lat = float(lat)
        lon = float(lon)
        x += cos(lat) * cos(lon)
        y += cos(lat) * sin(lon)
        z += sin(lat)

    x = float(x / len(lst))
    y = float(y / len(lst))
    z = float(z / len(lst))

    return (atan2(z, sqrt(x * x + y * y)), atan2(y, x))

