import re
import requests
import os
import json

f = open(f'api-urls.json')
apiurls = json.load(f)

for apiurl in apiurls:
  url = apiurl['apiSpecificationUrl']
  project = apiurl['api']

  resp = requests.get(url)
  data = resp.json()
  with open(f'./temp/{project}.json', 'w') as outfile:
    json.dump(data, outfile)

print('--> Files saved')