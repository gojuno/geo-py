import unittest
import time
import logging
import math

import geo.sphere as sphere
import geo._sphere as _sphere
import geo.ellipsoid as ellipsoid
import geo._ellipsoid as _ellipsoid
import geo._sphere as csphere

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger()

p_minsk = (27.561831, 53.902257)
p_moscow = (37.620393, 55.75396)


def isclose(a, b, rel_tol=1e-09, abs_tol=0):
    """
    Python 2 implementation of Python 3.5 math.isclose()
    https://hg.python.org/cpython/file/v3.5.2/Modules/mathmodule.c#l1993
    """
    # sanity check on the inputs
    if rel_tol < 0 or abs_tol < 0:
        raise ValueError("tolerances must be non-negative")
    # short circuit exact equality -- needed to catch two infinities of
    # the same sign. And perhaps speeds things up a bit sometimes.
    if a == b:
        return True
    # This catches the case of two infinities of opposite sign, or
    # one infinity and one finite number. Two infinities of opposite
    # sign would otherwise have an infinite relative tolerance.
    # Two infinities of the same sign are caught by the equality check
    # above.
    if math.isinf(a) or math.isinf(b):
        return False
    # Cast to float to allow decimal.Decimal arguments
    if not isinstance(a, float):
        a = float(a)
    if not isinstance(b, float):
        b = float(b)
    # now do the regular computation
    # this is essentially the "weak" test from the Boost library
    diff = math.fabs(b - a)
    result = ((diff <= math.fabs(rel_tol * a)) or
              (diff <= math.fabs(rel_tol * b)) or
              (diff <= abs_tol))
    return result


if not hasattr(math, 'isclose'):
    math.isclose = isclose


class TestSphere(unittest.TestCase):

    def test_distance(self):
        assert math.isclose(
            sphere._py_approximate_distance(p_minsk, p_moscow),
            676371.322420,
            rel_tol=1e-06)
        assert math.isclose(
            _sphere._approximate_distance(p_minsk, p_moscow),
            676371.322420,
            rel_tol=1e-06)

        assert math.isclose(
            sphere._py_haversine_distance(p_minsk, p_moscow),
            675656.299481,
            rel_tol=1e-06)
        assert math.isclose(
            _sphere._haversine_distance(p_minsk, p_moscow),
            675656.299481,
            rel_tol=1e-06)

        assert math.isclose(
            sphere._py_distance(p_minsk, p_moscow),
            675656.299481,
            rel_tol=1e-06)
        assert math.isclose(
            _sphere._distance(p_minsk, p_moscow),
            675656.299481,
            rel_tol=1e-06)

    def test_projection(self):
        x, y = sphere._py_from4326_to3857(p_minsk)
        assert math.isclose(x, 3068168.9922502628, rel_tol=1e-06)
        assert math.isclose(y, 7151666.629430503, rel_tol=1e-06)
        x, y = _sphere._from4326_to3857(p_minsk)
        assert math.isclose(x, 3068168.9922502628, rel_tol=1e-06)
        assert math.isclose(y, 7151666.629430503, rel_tol=1e-06)

        lon, lat = sphere._py_from3857_to4326(
            sphere._py_from4326_to3857(p_minsk))
        assert math.isclose(lon, p_minsk[0], rel_tol=1e-06)
        assert math.isclose(lat, p_minsk[1], rel_tol=1e-06)

        lon, lat = _sphere._from3857_to4326(
            _sphere._from4326_to3857(p_minsk))
        assert math.isclose(lon, p_minsk[0], rel_tol=1e-06)
        assert math.isclose(lat, p_minsk[1], rel_tol=1e-06)


class TestEllipsoid(unittest.TestCase):

    def test_distance(self):
        assert math.isclose(
            ellipsoid._py_distance(p_minsk, p_moscow),
            677789.531233,
            rel_tol=1e-06)
        assert math.isclose(
            _ellipsoid._distance(p_minsk, p_moscow),
            677789.531233,
            rel_tol=1e-06)

    def test_projection(self):
        assert (
            ellipsoid._py_from4326_to3395(p_minsk) ==
            (3068168.9922502623, 7117115.955611216)
        )
        rp_minsk = ellipsoid._py_from3395_to4326(
                ellipsoid._py_from4326_to3395(p_minsk))

        assert math.isclose(rp_minsk[0], p_minsk[0], rel_tol=1e-06)
        assert math.isclose(rp_minsk[1], p_minsk[1], rel_tol=1e-06)

        assert (
            _ellipsoid._from4326_to3395(p_minsk) ==
            (3068168.9922502623, 7117115.955611216)
        )

        rp_minsk = _ellipsoid._from3395_to4326(
                _ellipsoid._from4326_to3395(p_minsk))

        assert math.isclose(rp_minsk[0], p_minsk[0], rel_tol=1e-06)
        assert math.isclose(rp_minsk[1], p_minsk[1], rel_tol=1e-06)
