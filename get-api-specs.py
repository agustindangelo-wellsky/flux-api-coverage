import requests
import json
import os

if not os.path.exists('api-urls.json'):
    print(f'File api-urls.json not found in {os.getcwd()}. Aborting...')
    exit(1)

f = open(f'api-urls.json', encoding='UTF-8')
apiurls = json.load(f)

if not os.path.exists('./api-specs'):
    os.mkdir('./api-specs')

for apiurl in apiurls:
    url = apiurl['apiSpecificationUrl']
    project = apiurl['api']

    resp = requests.get(url)
    data = resp.json()
    with open(f'./api-specs/{project}.json', 'w', encoding='UTF-8') as outfile:
        json.dump(data, outfile)

print('--> API Specification files were saved in ./temp/')
