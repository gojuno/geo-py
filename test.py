import unittest
import time
import logging
import math

import geo.sphere as sphere
import geo.ellipsoid as ellipsoid
import geo._sphere as csphere

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger()

p_minsk = (27.561831, 53.902257)
p_moscow = (37.620393, 55.75396)


class TestSphere(unittest.TestCase):

    def test_distance(self):
        assert math.isclose(
            sphere._py_approximate_distance(p_minsk, p_moscow),
            676371.322420,
            rel_tol=1e-06)
        assert math.isclose(
            sphere._approximate_distance(p_minsk, p_moscow),
            676371.322420,
            rel_tol=1e-06)

        assert math.isclose(
            sphere._py_haversine_distance(p_minsk, p_moscow),
            675656.299481,
            rel_tol=1e-06)
        assert math.isclose(
            sphere._haversine_distance(p_minsk, p_moscow),
            675656.299481,
            rel_tol=1e-06)

        assert math.isclose(
            sphere._py_distance(p_minsk, p_moscow),
            675656.299481,
            rel_tol=1e-06)
        assert math.isclose(
            sphere._distance(p_minsk, p_moscow),
            675656.299481,
            rel_tol=1e-06)

    def test_projection(self):
        x, y = sphere._py_from4326_to3857(p_minsk)
        assert math.isclose(x, 3068168.9922502628, rel_tol=1e-06)
        assert math.isclose(y, 7151666.629430503, rel_tol=1e-06)
        x, y = sphere._from4326_to3857(p_minsk)
        assert math.isclose(x, 3068168.9922502628, rel_tol=1e-06)
        assert math.isclose(y, 7151666.629430503, rel_tol=1e-06)

        lon, lat = sphere._py_from3857_to4326(
            sphere._py_from4326_to3857(p_minsk))
        assert math.isclose(lon, p_minsk[0], rel_tol=1e-06)
        assert math.isclose(lat, p_minsk[1], rel_tol=1e-06)

        lon, lat = sphere._from3857_to4326(
            sphere._from4326_to3857(p_minsk))
        assert math.isclose(lon, p_minsk[0], rel_tol=1e-06)
        assert math.isclose(lat, p_minsk[1], rel_tol=1e-06)


class TestEllipsoid(unittest.TestCase):

    def test_distance(self):
        assert math.isclose(
            ellipsoid._py_distance(p_minsk, p_moscow),
            677789.531233,
            rel_tol=1e-06)
        assert math.isclose(
            ellipsoid._distance(p_minsk, p_moscow),
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
            ellipsoid._from4326_to3395(p_minsk) ==
            (3068168.9922502623, 7117115.955611216)
        )

        rp_minsk = ellipsoid._from3395_to4326(
                ellipsoid._from4326_to3395(p_minsk))

        assert math.isclose(rp_minsk[0], p_minsk[0], rel_tol=1e-06)
        assert math.isclose(rp_minsk[1], p_minsk[1], rel_tol=1e-06)
