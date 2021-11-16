# Changelog

## Development

- Convert from Python 2 to Python 3:
  - Switch routing from IRoutes (Pylons) to IBluepring
  - Switch testing framework from Nose to Pytest.

## 0.1.0

- Introduced specific error classes with codes.
- Changed response format for errors: there is now an ``error`` attribute,
  containing an object with ``message`` and ``code`` attributes.
- Unit tests added.

## 0.0.2

- Small formatting fixes, mainly in documentation.

## 0.0.1

- First functional version of the validation API.