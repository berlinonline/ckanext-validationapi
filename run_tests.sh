#! /bin/bash
nosetests -s --ckan --with-pylons=test.ini --with-coverage --cover-package=ckanext.validationapi --cover-erase --cover-html ckanext/validationapi/tests/
