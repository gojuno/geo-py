cimport cython
cimport cpython
from libc.math cimport fabs, sqrt, cos, sin, tan, atan, asin, atan2, log, exp, M_PI
from _helpers cimport unpack_point, to_degrees

from geo.constants import WGS84

cdef double CONVERGENCE_THRESHOLD = 1e-12
cdef int MAX_ITERATIONS = 10
cdef double HALF_PI = M_PI / 2.0
cdef double QUARTER_PI = M_PI / 4.0


def _distance(point1, point2, ellipsoid=WGS84):
    cdef double lon1, lat1, lon2, lat2
    cdef ellipsoid_a = ellipsoid.a
    cdef ellipsoid_b = ellipsoid.b
    cdef ellipsoid_f = ellipsoid.f

    unpack_point(point1, &lon1, &lat1)
    unpack_point(point2, &lon2, &lat2)

    cdef double U1 = atan((1 - ellipsoid_f) * tan(lat1))
    cdef double U2 = atan((1 - ellipsoid_f) * tan(lat2))
    cdef double L = lon2 - lon1

    cdef double sinU1 = sin(U1)
    cdef double cosU1 = cos(U1)
    cdef double sinU2 = sin(U2)
    cdef double cosU2 = cos(U2)

    cdef double sinLambda, sinSigma, sigma, sinAlpha, cosSqAlpha
    cdef double C, Lambda, LambdaPrev

    Lambda = L

    for _ in range(MAX_ITERATIONS):
        sinLambda = sin(Lambda)
        cosLambda = cos(Lambda)
        sinSigma = sqrt(
            (cosU2 * sinLambda) ** 2 +
            (cosU1 * sinU2 - sinU1 * cosU2 * cosLambda) ** 2)
        # coincident points
        if sinSigma == 0:
            return 0.0

        cosSigma = sinU1 * sinU2 + cosU1 * cosU2 * cosLambda
        sigma = atan2(sinSigma, cosSigma)
        sinAlpha = cosU1 * cosU2 * sinLambda / sinSigma
        cosSqAlpha = 1 - sinAlpha ** 2
        try:
            cos2SigmaM = cosSigma - 2 * sinU1 * sinU2 / cosSqAlpha
        except ZeroDivisionError:
            cos2SigmaM = 0

        C = (ellipsoid_f / 16) * cosSqAlpha * (
            4 + ellipsoid_f * (4 - 3 * cosSqAlpha)
        )
        LambdaPrev = Lambda
        Lambda = (
            L + (1 - C) * ellipsoid.f * sinAlpha * (
                sigma + C * sinSigma * (
                    cos2SigmaM + C * cosSigma * (
                        -1 + 2 * cos2SigmaM ** 2
                    )
                )
            )
        )

        if abs(Lambda - LambdaPrev) < CONVERGENCE_THRESHOLD:
            break
    else:
        # failure to converge
        return None

    cdef double uSq, A, B, deltaSigma, s

    uSq = cosSqAlpha * (ellipsoid_a ** 2 - ellipsoid_b ** 2) / (ellipsoid_b ** 2)
    A = 1 + uSq / 16384 * (4096 + uSq * (-768 + uSq * (320 - 175 * uSq)))
    B = uSq / 1024 * (256 + uSq * (-128 + uSq * (74 - 47 * uSq)))
    deltaSigma = B * sinSigma * (cos2SigmaM + B / 4 * (cosSigma *
                 (-1 + 2 * cos2SigmaM ** 2) - B / 6 * cos2SigmaM *
                 (-3 + 4 * sinSigma ** 2) * (-3 + 4 * cos2SigmaM ** 2)))
    s = ellipsoid_b * A * (sigma - deltaSigma)
    return s


def _from4326_to3395(point, ellipsoid=WGS84):
    cdef double lon, lat
    cdef double ellipsoid_a = ellipsoid.a
    cdef double ellipsoid_e = ellipsoid.e

    unpack_point(point, &lon, &lat)

    cdef double e_sin_lat = ellipsoid_e*sin(lat)
    cdef double multiplier1 = tan(QUARTER_PI + lat / 2.0)
    cdef double multiplier2 = pow((1-e_sin_lat)/(1+e_sin_lat), ellipsoid_e/2)
    cdef double E = ellipsoid_a * lon
    cdef double N = ellipsoid_a * log(multiplier1*multiplier2)
    return (E, N)


def _from3395_to4326(point, ellipsoid=WGS84):
    cdef double E, N
    E, N = point
    cdef double a = ellipsoid.a
    cdef double e = ellipsoid.e
    cdef double half_e = e * 0.5

    cdef double m1 = exp(-N / a)
    cdef double m2
    cdef double new_phi
    cdef double phi = HALF_PI - 2.0 * atan(m1)
    cdef double e_sin_phi

    for _ in range(MAX_ITERATIONS):
        e_sin_phi = e*sin(phi)
        m2 = ((1 - e_sin_phi) / (1 + e_sin_phi))**half_e
        new_phi = HALF_PI  - 2.0 * atan(m1 * m2)
        if abs(new_phi - phi) <= CONVERGENCE_THRESHOLD:
            phi = new_phi
            break
        phi = new_phi

    lon = to_degrees(E / a)
    lat = to_degrees(phi)
    return (lon, lat)
