# Measure API Coverage by Flux projects

Steps:

1. Install python
2. On powershell, create a Python virtual environment: `python -m venv .venv`
3. Activate the virtual environment in the current shell: `.\.venv\Scripts\activate`
4. Install Python dependencies: `pip install -r requirements.txt`

Execute the scripts in the following order:

## setup-flux-projects.py

This script clones all Flux repositories into the `./flux-projects` directory. Project urls should be provided in the `api-urls.json` file.

`python setup-flux-projects.py`

## get-api-specs.py

This script requests OpenAPI specifications from Swagger for all the APIs. Swagger urls should be provided in the `api-urls.json` file.

`python get-api-specs.py`

## measure-coverage.py

  This script ingests the OpenAPI specification .json file of each API on `api-urls.json` and parses its corresponding Flux project to see which endpoints are being exercised by the tests, printing a coverage report afterwards.

`python measure-coverage.py`
