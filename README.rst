.. You should enable this project on travis-ci.org and coveralls.io to make
   these badges work. The necessary Travis and Coverage config files have been
   generated for you.

.. image:: https://github.com/berlinonline/ckanext-validationapi/workflows/Tests/badge.svg?branch=master
    :target: https://github.com/berlinonline/ckanext-validationapi/actions
    :alt: Tests


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
``validate``. Only POST request with content type ``application/json`` are accepted.

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

* Has been tested with CKAN 2.9.4 and requires Python 3.


License
=======

This material is copyright ©
`BerlinOnline Stadtportal GmbH & Co. KG <https://www.berlinonline.net/>`_
.

This extension is open and licensed under the GNU Affero General Public License (AGPL) v3.0.
Its full text may be found at:

http://www.fsf.org/licensing/licenses/agpl-3.0.html
