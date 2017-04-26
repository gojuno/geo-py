import os
import sys
from setuptools import setup, Extension

try:
    from Cython.Build import cythonize
    ext = '.pyx'
except ImportError:
    def cythonize(extensions): return extensions
    ext = '.c'

MIN_PYTHON = (3, 0)
if sys.version_info < MIN_PYTHON:
    sys.stderr.write("Python {}.{} or later is required\n".format(*MIN_PYTHON))
    sys.exit(1)

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

extensions = cythonize([
    Extension('geo._sphere', ['geo/_sphere' + ext]),
    Extension('geo._ellipsoid', ['geo/_ellipsoid' + ext]),
])


setup(
    name='geo-py',
    version='0.4',
    author='Alexander Verbitsky',
    author_email='habibutsu@gmail.com',
    maintainer='Alexander Verbitsky',
    maintainer_email='habibutsu@gmail.com',
    description='Set of algorithms and structures related to geodesy and geospatial data',
    long_description=read('README.rst'),
    keywords='geodesy, haversine distance, great circle distance, vincenty\'s formula',
    url='https://github.com/gojuno/geo-py',
    packages=['geo'],
    ext_modules = extensions,
    test_suite='test',
    license='BSD',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Topic :: Utilities',
        'Programming Language :: Python',
        'License :: OSI Approved :: BSD License',
    ],
)
