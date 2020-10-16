"""pyramid_https_session_redis installation script.
"""
import os

from setuptools import setup
from setuptools import find_packages

# store version in the init.py
import re

with open(
    os.path.join(
        os.path.dirname(__file__), "pyramid_https_session_redis", "__init__.py"
    )
) as v_file:
    VERSION = re.compile(r'.*__VERSION__ = "(.*?)"', re.S).match(v_file.read()).group(1)

try:
    here = os.path.abspath(os.path.dirname(__file__))
    README = open(os.path.join(here, "README.md")).read()
    README = README.split("\n\n", 1)[0] + "\n"
except:
    README = ""

# Pyramid Requirements:
# 1.4 add_request_method
install_requires = [
    "pyramid>=1.4",
    "pyramid_session_redis>=1.4.0",
    "pyramid_https_session_core>=0.0.7",
]
tests_require = [
    "pytest",
]
testing_extras = tests_require + []


setup(
    name="pyramid_https_session_redis",
    version=VERSION,
    description="provides for a 'session_https' secure session object for redis",
    long_description=README,
    classifiers=[
        "Intended Audience :: Developers",
        "Framework :: Pyramid",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
    keywords="web pyramid redis session",
    packages=["pyramid_https_session_redis"],
    author="Jonathan Vanasco",
    author_email="jonathan@findmeon.com",
    url="https://github.com/jvanasco/pyramid_https_session_redis",
    license="MIT",
    include_package_data=True,
    zip_safe=False,
    install_requires=install_requires,
    tests_require=tests_require,
    extras_require={
        "testing": testing_extras,
    },
    test_suite="tests",
)
