import requests
import json
import os

if not os.path.exists('api-urls.json'):
    print(f'File api-urls.json not found in {os.getcwd()}. Aborting...')
    exit(1)

f = open(f'api-urls.json', encoding='UTF-8')
apiurls = json.load(f)
api_specs_base_path = './api-specs'

if not os.path.exists(api_specs_base_path):
    os.mkdir(api_specs_base_path)

for apiurl in apiurls:
    url = apiurl['specUrl']
    project = apiurl['name']

    print(f'--> Retrieving {project} OpenAPI specification...')
    resp = requests.get(url)
    data = resp.json()
    with open(os.path.join(api_specs_base_path, f'{project}.json'), 'w', encoding='UTF-8') as outfile:
        json.dump(data, outfile)

print(f'--> API Specification files have been saved in {api_specs_base_path}')
