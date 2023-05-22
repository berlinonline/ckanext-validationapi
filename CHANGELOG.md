# Changelog

## Development

## [0.2.2](https://github.com/berlinonline/ckanext-validationapi/releases/tag/0.2.2)

_(2023-05-22)_

- Define extension's version string in [VERSION](VERSION), make it available as `ckanext.validationapi.__version__` and in [setup.py](setup.py).


## [0.2.1](https://github.com/berlinonline/ckanext-validationapi/releases/tag/0.2.1)

_(2023-01-23)_

- Fix codecov configuration and add badge.
- Run tests on pushes, but not on pushing tags.
- Some improvements to documentation.
- Remove some empty folders.

## [0.2.0](https://github.com/berlinonline/ckanext-validationapi/releases/tag/0.2.0)

_(2021-12-03)_

- Convert from Python 2 to Python 3.
- Switch routing from IRoutes (Pylons) to IBlueprint (Flask).
- Switch testing framework from Nose to Pytest.
- This is the first version that requires Python 3 / CKAN >= 2.9.

## [0.1.0](https://github.com/berlinonline/ckanext-validationapi/releases/tag/0.1.0)

_(2018-11-07)_

- Introduced specific error classes with codes.
- Changed response format for errors: there is now an ``error`` attribute,
  containing an object with ``message`` and ``code`` attributes.
- Unit tests added.
- This is the last version that works with Python 2 / CKAN < 2.9.

## [0.0.2](https://github.com/berlinonline/ckanext-validationapi/releases/tag/0.0.2)

_(2018-11-06)_

- Small formatting fixes, mainly in documentation.

## [0.0.1](https://github.com/berlinonline/ckanext-validationapi/releases/tag/0.0.1)

_(2018-11-02)_

- First functional version of the validation API.