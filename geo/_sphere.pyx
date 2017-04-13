cimport cython
cimport cpython
from libc.math cimport log, exp, fabs, sqrt, cos, sin, tan, asin, atan, atan2, M_PI

from _helpers cimport unpack_point, to_radians, to_degrees

from geo.constants import (
    EARTH_MEAN_RADIUS as py_EARTH_MEAN_RADIUS,
    EARTH_MEAN_DIAMETER as py_EARTH_MEAN_DIAMETER,
    EARTH_EQUATORIAL_RADIUS as py_EARTH_EQUATORIAL_RADIUS,
    EARTH_EQUATORIAL_METERS_PER_DEGREE as py_EARTH_EQUATORIAL_METERS_PER_DEGREE,
    I_EARTH_EQUATORIAL_METERS_PER_DEGREE as py_I_EARTH_EQUATORIAL_METERS_PER_DEGREE
)

cdef double EARTH_MEAN_RADIUS = py_EARTH_MEAN_RADIUS
cdef double EARTH_MEAN_DIAMETER = py_EARTH_MEAN_DIAMETER
cdef double EARTH_EQUATORIAL_RADIUS = py_EARTH_EQUATORIAL_RADIUS
cdef double EARTH_EQUATORIAL_METERS_PER_DEGREE = py_EARTH_EQUATORIAL_METERS_PER_DEGREE
cdef double I_EARTH_EQUATORIAL_METERS_PER_DEGREE = py_I_EARTH_EQUATORIAL_METERS_PER_DEGREE
cdef HALF_PI = M_PI / 2.0

def _approximate_distance(point1, point2):
    cdef double lon1, lat1, lon2, lat2

    unpack_point(point1, &lon1, &lat1)
    unpack_point(point2, &lon2, &lat2)

    cdef double cos_lat
    cos_lat = cos((lat1+lat2)/2.0)

    cdef double dx = (lat2 - lat1)
    cdef double dy = (cos_lat*(lon2 - lon1))

    return EARTH_MEAN_RADIUS*sqrt(dx**2 + dy**2)


def _haversine_distance(point1, point2):
    cdef double lon1, lat1, lon2, lat2

    unpack_point(point1, &lon1, &lat1)
    unpack_point(point2, &lon2, &lat2)

    cdef double dlat = (lat2 - lat1)
    cdef double dlon = (lon2 - lon1)
    cdef double a = (
        sin(dlat * 0.5)**2 +
        cos(lat1) * cos(lat2) * sin(dlon * 0.5)**2
    )

    return EARTH_MEAN_DIAMETER * asin(sqrt(a))


def _distance(point1, point2):
    cdef double lon1, lat1, lon2, lat2

    unpack_point(point1, &lon1, &lat1)
    unpack_point(point2, &lon2, &lat2)

    cdef double dlon = fabs(lon1 - lon2)
    cdef double dlat = fabs(lat1 - lat2)

    cdef double numerator = sqrt(
        (cos(lat2)*sin(dlon))**2 +
        ((cos(lat1)*sin(lat2)) - (sin(lat1)*cos(lat2)*cos(dlon)))**2)

    cdef double denominator = (
        (sin(lat1)*sin(lat2)) +
        (cos(lat1)*cos(lat2)*cos(dlon)))

    cdef double c = atan2(numerator, denominator)
    return EARTH_MEAN_RADIUS*c

def _from4326_to3857(point):
    cdef double lon = point[0]
    cdef double lat = point[1]

    cdef double xtile = lon * EARTH_EQUATORIAL_METERS_PER_DEGREE
    cdef double ytile = log(tan(to_radians(45 + lat / 2.0))) * EARTH_EQUATORIAL_RADIUS
    return (xtile, ytile)


def _from3857_to4326(point):
    cdef double x = point[0]
    cdef double y = point[1]
    cdef double lon = x / EARTH_EQUATORIAL_METERS_PER_DEGREE
    cdef double lat = to_degrees(
        2.0 * atan(exp(y/EARTH_EQUATORIAL_RADIUS)) - HALF_PI)
    return (lon, lat)
