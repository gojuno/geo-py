cimport cython
cimport cpython
from libc.math cimport M_PI


@cython.cdivision(True)
cdef inline double to_degrees(double radians):
    return radians * (180.0 / M_PI)


@cython.cdivision(True)
cdef inline double to_radians(double degrees):
    return (degrees * M_PI) / 180.0


cdef inline unpack_point(point, double *lon, double *lat):
    if (not cpython.PySequence_Check(point)):
        raise TypeError("point must be an iterable of double")
    lon[0] = to_radians(point[0])
    lat[0] = to_radians(point[1])
