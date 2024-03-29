# -*- coding: utf-8 -*-

#  Quickstarted Options:
#
#  sqlalchemy: True
#  auth:       
#  mako:       False
#
#

# This is just a work-around for a Python2.7 issue causing
# interpreter crash at exit when trying to log an info message.
try:
    import logging
    import multiprocessing
except:
    pass

import sys
py_version = sys.version_info[:2]

try:
    from setuptools import setup, find_packages
except ImportError:
    from ez_setup import use_setuptools
    use_setuptools()
    from setuptools import setup, find_packages

testpkgs = [
    'WebTest >= 1.2.3',
    'nose',
    'coverage',
    'gearbox',
    'pyquery'
]

install_requires = [
    "TurboGears2 >= 2.4.3",
    "Beaker >= 1.8.0",
    "Kajiki >= 0.6.3",
    "zope.sqlalchemy >= 1.2",
    "sqlalchemy",
    "sqlalchemy-utils",
    "phonenumbers",
    "alembic",
    "wtforms",
    "repoze.who",
    "tgext.admin >= 0.6.1",
    "tgext.pluggable",
    "tgapp-registration",
    "tgext.mailer",
    "tw2.forms",
    "WebHelpers2"
]

if py_version != (3, 2):
    # Babel not available on 3.2
    install_requires.append("Babel")
if py_version == (3, 2):
    # jinja2 2.7 is incompatible with Python 3.2
    install_requires.append('jinja2 < 2.7')
else:
    install_requires.append('jinja2')

setup(
    name='axantaddressbook',
    version='0.1',
    description='',
    author='',
    author_email='',
    url='',
    packages=find_packages(exclude=['ez_setup']),
    install_requires=install_requires,
    include_package_data=True,
    test_suite='nose.collector',
    tests_require=testpkgs,
    extras_require={
        'testing': testpkgs
    },
    package_data={'axantaddressbook': [
        'i18n/*/LC_MESSAGES/*.mo',
        'templates/*/*',
        'public/*/*'
    ]},
    message_extractors={'axantaddressbook': [
        ('**.py', 'python', None),
        ('templates/**.xhtml', 'kajiki', {'strip_text': False, 'extract_python': True}),
        ('templates/**.jinja', 'jinja2', None),
        ('public/**', 'ignore', None)
    ]},
    entry_points={
        'paste.app_factory': [
            'main = axantaddressbook.config.application:make_app'
        ],
        'gearbox.plugins': [
            'turbogears-devtools = tg.devtools'
        ]
    },
    zip_safe=False
)
