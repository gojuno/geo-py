python-geo
==========

Set of algorithms and structures related to geodesy.

API
---

geo.spheroid
~~~~~~~~~~~~

Functions onto sphere

geo.spheroid.approximate_distance
_________________________________

.. code-block:: python

    def approximate_distance(point1, point2):

Approximate calculation distance
(expanding the trigonometric functions around the midpoint)

geo.spheroid.haversine_distance
_______________________________

.. code-block:: python

    def _haversine_distance(point1, point2):

Calculating haversine distance between two points (see https://en.wikipedia.org/wiki/Haversine_formula, https://www.math.ksu.edu/~dbski/writings/haversine.pdf)

Is numerically better-conditioned for small distances

geo.spheroid.distance
_____________________

.. code-block:: python

    def distance(point1, point2):

Calculating great-circle distance (see https://en.wikipedia.org/wiki/Great-circle_distance)

geo.spheroid.bearing
____________________

.. code-block:: python

    def bearing(point1, point2):

Calculating initial bearing between two points
(see http://www.movable-type.co.uk/scripts/latlong.html)

geo.spheroid.final_bearing
__________________________

.. code-block:: python

    def final_bearing(point1, point2):

Calculating finatl bearing (initial bering + 180) between two points

geo.spheroid.destination
________________________

.. code-block:: python

    def destination(point, distance, bearing):

Given a start point, initial bearing, and distance, this will
calculate the destina­tion point and final bearing travelling
along a (shortest distance) great circle arc. (see http://www.movable-type.co.uk/scripts/latlong.htm)

geo.spheroid.approximate_destination
____________________________________

.. code-block:: python

    def approximate_destination(point, distance, theta):

geo.spheroid.from4326_to3857
____________________________

.. code-block:: python

    def from4326_to3857(point):

Reproject point from EPSG:4326 (https://epsg.io/4326) to EPSG:3857 (https://epsg.io/3857) (see http://wiki.openstreetmap.org/wiki/Mercator)

    Spherical Mercator:
        E = R*(λ - λo)
        N = R*ln(tan(π/4+φ/2))

geo.spheroid.from3857_to4326
____________________________

.. code-block:: python

    def from4326_to3857(point):

Reproject point from EPSG:3857 (https://epsg.io/3857) to EPSG:4326 (https://epsg.io/4326) (see http://wiki.openstreetmap.org/wiki/Mercator)

    Reverse Spherical Mercator:
        λ = E/R + λo
        φ = π/2 - 2*arctan(exp(-N/R))

geo.ellipsoid
~~~~~~~~~~~~~

Functions onto ellipsoid

geo.ellipsoid.distance
______________________

.. code-block:: python

    def distance(point1, point2, ellipsoid=WGS84):

Calculating distance with using vincenty's formula
(see https://en.wikipedia.org/wiki/Vincenty's_formulae)

geo.ellipsoid.from4326_to3395
_____________________________

.. code-block:: python

    def from4326_to3395(point, ellipsoid=WGS84):

Reproject point from EPSG:4326 (https://epsg.io/4326) to EPSG:3395 (https://epsg.io/3395) (see https://en.wikipedia.org/wiki/Mercator_projection#Generalization_to_the_ellipsoid)

    Ellipsoidal Mercator:
        E = a*(λ - λo)
        N = a*ln(tan(π/4+φ/2)*((1-e*sin(φ))/(1+e*sin(φ)))**e/2)

geo.ellipsoid.from3395_to4326
_____________________________

.. code-block:: python

    def from3395_to4326(point, ellipsoid=WGS84):

Reproject point from EPSG:3395 (https://epsg.io/3395) to EPSG:4326 (https://epsg.io/4326) (see https://en.wikipedia.org/wiki/Mercator_projection#Generalization_to_the_ellipsoid)

    Reverse Ellipsoidal Mercator:
        λ = E/a + λo
        φ = π/2 + 2*arctan(exp(-N/a)*((1-e*sin(φ))/(1+e*sin(φ))**e/2))
