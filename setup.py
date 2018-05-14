#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys

import django_sendinblue

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

version = django_sendinblue.__version__

if sys.argv[-1] == 'publish':
    # os.system('cd docs && make html')
    # os.system('python setup.py sdist bdist_wheel upload -r pypiypk')
    # print("You probably want to also tag the version now:")
    # print("  git tag -a %s -m 'version %s'" % (version, version))
    # print("  git push --tags")
    # sys.exit()
    print('TODO')

if 'DJANGO_SETTINGS_MODULE' not in os.environ:
    os.environ['DJANGO_SETTINGS_MODULE'] = 'testsettings'

with open('README.rst') as readme_file:
    readme = readme_file.read()

setup(
    name='django-sendinblue',
    version=version,
    description="""django backend for sendinblue using sendinblue/APIv3-python-library""",
    long_description=readme,
    author='Anis DAIMAR (Yupeek)',
    author_email='contact@yupeek.com',
    url='https://github.com/yupeek/django-sendinblue',
    packages=[
        'django_sendinblue',
    ],
    include_package_data=True,
    install_requires=[
        'django>=1.7,<=1.9.99',
        'sib-api-v3-sdk==3.0.1',
    ],
    dependency_links=[
        'git+https://github.com/sendinblue/APIv3-python-library.git#egg=sib-api-v3-sdk-3.0.1',
    ],
    tests_require=[
      'six',
    ],
    license="BSD 2-Clause License",
    zip_safe=False,
    keywords='django email backend sendinblue v3',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD 2-Clause License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Operating System :: OS Independent',
        'Topic :: Software Development :: Libraries',
        'Topic :: Utilities',
        'Environment :: Web Environment',
        'Framework :: Django',
    ],
)
