.. You should enable this project on travis-ci.org and coveralls.io to make
   these badges work. The necessary Travis and Coverage config files have been
   generated for you.

.. image:: https://travis-ci.org/berlinonline/ckanext-validationapi.svg?branch=master
    :target: https://travis-ci.org/berlinonline/ckanext-validationapi

.. image:: https://coveralls.io/repos/berlinonline/ckanext-validationapi/badge.svg
  :target: https://coveralls.io/r/berlinonline/ckanext-validationapi

=====================
ckanext-validationapi
=====================

.. Put a description of your extension here:
   What does it do? What features does it have?
   Consider including some screenshots or embedding a video!

-------------
Using the API
-------------

ckanext-validationapi provides a public wrapper around the internal validator functions
of CKAN. All validator functions that are available through
``ckan.plugins.toolkit.get_validator()`` can be used. The list of standard validators
that CKAN offers is available at https://docs.ckan.org/en/latest/extensions/validators.html.
Plugins can add more validators by implementing the 
`IValidators <https://docs.ckan.org/en/latest/extensions/plugin-interfaces.html#ckan.plugins.interfaces.IValidators>`_
interface.

The API is accessible via ``$CKAN_URL/api/validation``; currently its only method is 
``validate``. Only POST requests with content type ``application/json`` are accepted.

The expected payload to ``validate`` is a JSON object with two attributes:

- ``validator``: The name of the validator as it would be passed to ``ckan.plugins.toolkit.get_validator()``.
- ``value``: The value we want to submit for validation.

Here is an example:

.. code:: json

  {
    "validator": "email_validator" ,
    "value": "jane.doe@company.com"
  }

If the validator exists, ``validationapi`` will call the validator function with the provided
value. The response will be a JSON object with these attributes:

- ``validator``: The name of the validator as it would be passed to ``ckan.plugins.toolkit.get_validator()``.
- ``value``: The value that was submitted for validation.
- ``success``: Whether or not ``value`` passed the validation.

  - ``result``: If successful, the output of the validator. This will often be the same as ``value``, but sometimes the validator will perform some transformation as well.
  - ``message``: If not successful, this will contain an error message as provided by the validator.

Here are some examples for communicating with the validation API via curl:

Valid input, unchanged 
======================

::

  curl -X POST \
       --data '{ "validator": "email_validator", "value": "jane.doe@company.com" }' \
       -H "Content-Type: application/json" \
       $CKAN_URL/api/validation/validate

.. code:: json

  {
    "validator": "email_validator",
    "value": "jane.doe@company.com",
    "success": true,
    "result": "jane.doe@company.com"
  }

Valid input, changed 
====================

::

  curl -X POST \
       --data '{ "validator": "isodate", "value": "2004-10-10" }' \
       -H "Content-Type: application/json" \
       $CKAN_URL/api/validation/validate

.. code:: json

    {
      "validator": "isodate",
      "value": "2004-10-10",
      "success": true,
      "result": "2004-10-10 00:00:00"
    }

Invalid input
=============

::

  curl -X POST \
       --data '{ "validator": "isodate", "value": "2004-10-10x" }' \
       -H "Content-Type: application/json" \
       $CKAN_URL/api/validation/validate

.. code:: json

    {
      "message": "Invalid: u'Datumsformat ung\\xfcltig.'",
      "validator": "isodate",
      "value": "2004-10-10x",
      "success": false
    }

Errors
======

If possible, validationapi will catch errors and provide an error message in the same format as above, but with 
the HTTP Response Code 400 (Bad Request). Below are some examples:

Unknown Validator
-----------------

::

  curl -X POST \
       --data '{ "validator": "foolidator", "value": "barbar" }' \
       -H "Content-Type: application/json" \
       $CKAN_URL/api/validation/validate

.. code:: json

    {
      "validator": "foolidator",
      "value": "barbar",
      "success": false,
      "error": {
        "message": "Bad Request - Validator `foolidator` does not exist",
        "code": 7
      }
    }

Wrong Request Format
--------------------

::

  curl $CKAN_URL/api/validation/validate

.. code:: json

    {
      "validator": null,
      "value": null,
      "success": false,
      "error": {
        "message": "Bad Request - Validation API accepts only POST requests with content type 'application/json'.",
        "code": 1
      }
    }

Error Codes
-----------

The complete list of error codes is:

* Wrong HTTP method = 1
* Wrong content type = 2
* No request data found = 3
* Cannot decode JSON = 4
* Wrong type of JSON = 5
* Wrong JSON structure = 6
* Unknown validator = 7
* Validator has unexpected number of arguments = 8
* Unexpected error = 20


------------
Requirements
------------

* Has been tested with CKAN 2.7.3.


------------
Installation
------------

.. Add any additional install steps to the list below.
   For example installing any non-Python dependencies or adding any required
   config settings.

To install ckanext-validationapi:

1. Activate your CKAN virtual environment, for example::

     . /usr/lib/ckan/default/bin/activate

2. Install the ckanext-validationapi Python package into your virtual environment::

     pip install ckanext-validationapi

3. Add ``validationapi`` to the ``ckan.plugins`` setting in your CKAN
   config file (by default the config file is located at
   ``/etc/ckan/default/production.ini``).

4. Restart CKAN. For example if you've deployed CKAN with Apache on Ubuntu::

     sudo service apache2 reload

------------------------
Development Installation
------------------------

To install ckanext-validationapi for development, activate your CKAN virtualenv and
do::

    git clone https://github.com/berlinonline/ckanext-validationapi.git
    cd ckanext-validationapi
    python setup.py develop
    pip install -r dev-requirements.txt


-----------------
Running the Tests
-----------------

To run the tests, do::

    nosetests --nologcapture --with-pylons=test.ini

To run the tests and produce a coverage report, first make sure you have
coverage installed in your virtualenv (``pip install coverage``) then run::

    nosetests --nologcapture --with-pylons=test.ini --with-coverage --cover-package=ckanext.validationapi --cover-inclusive --cover-erase --cover-tests


-----------------------------------------
Registering ckanext-validationapi on PyPI
-----------------------------------------

ckanext-validationapi should be availabe on PyPI as
https://pypi.python.org/pypi/ckanext-validationapi. If that link doesn't work, then
you can register the project on PyPI for the first time by following these
steps:

1. Create a source distribution of the project::

     python setup.py sdist

2. Register the project::

     python setup.py register

3. Upload the source distribution to PyPI::

     python setup.py sdist upload

4. Tag the first release of the project on GitHub with the version number from
   the ``setup.py`` file. For example if the version number in ``setup.py`` is
   0.0.1 then do::

       git tag 0.0.1
       git push --tags


------------------------------------------------
Releasing a New Version of ckanext-validationapi
------------------------------------------------

ckanext-validationapi is availabe on PyPI as https://pypi.python.org/pypi/ckanext-validationapi.
To publish a new version to PyPI follow these steps:

1. Update the version number in the ``setup.py`` file.
   See `PEP 440 <http://legacy.python.org/dev/peps/pep-0440/#public-version-identifiers>`_
   for how to choose version numbers.

2. Create a source distribution of the new version::

     python setup.py sdist

3. Upload the source distribution to PyPI::

     python setup.py sdist upload

4. Tag the new release of the project on GitHub with the version number from
   the ``setup.py`` file. For example if the version number in ``setup.py`` is
   0.0.2 then do::

       git tag 0.0.2
       git push --tags
