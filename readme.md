# Measure API Coverage by Flux projects

Steps:

1. Install python
2. On powershell, create a Python virtual environment: `python -m venv .venv`
3. Activate the virtual environment: `.\.venv\Scripts\activate`
4. Install dependencies: `pip install -r requirements.txt`

Execute the scripts in the following order:

## setup-flux-projects.py

This script clones all Flux repositories into the `./flux-projects` directory. Project urls should be provided in the `api-urls.json` file.

`python setup-flux-projects.py`

## get-api-specs.py

This script requests OpenAPI specifications from Swagger for all the APIs. Swagger urls should be provided in the `api-urls.json` file.

`python get-api-specs.py`

## measure-coverage.py

This script ingests the swagger file of each API and parses its corresponding Flux project to see which endpoints are being exercised by at least one Flux test.

`python measure-coverage.py`
