# -*- mode: python; coding: utf-8; -*-
from setuptools import setup, find_packages
import os, os.path
import sys

DIRNAME = os.path.dirname(__file__)

# Dynamically calculate the version based on django.VERSION.
version = "0.1.1"

setup(name='fsc',
    version=version,
    description="Freeswitch Client",
    long_description="FreeSWITCH client library",
    keywords='freeswitch',
    author='Oleg Dolya',
    author_email='oleg.dolya@gmail.com',
    url='http://github/jbo/fsc/',
    license='GPL',
    include_package_data=True,
    #package_dir = {
    #    '' : 'satchmo/apps',
    #    'static' : 'satchmo/static'
    #},
    packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
    #packages = packages,
    #data_files = data_files,
    zip_safe = False,
    #install_requires=[
    #    'Django>=1.1',
    #    'django-extensions',
    #    #'django-batchadmin',
    #    'BeautifulSoup',
    #    'userprofile',
    #    #'pycrypto',
    #    #'django-registration',
    #    #'django-threaded-multihost',
    #    #'PyYAML',
    #    #'Reportlab',
    #    #'trml2pdf',
    #    'elementtree',
    #    'docutils',
    #    'fsadmin'
    #],
    classifiers = [
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: GPL License',
        'Operating System :: OS Independent',
        'Topic :: Office/Business',
    ],
    scripts=['scripts/fsb'],
)
