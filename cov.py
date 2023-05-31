import json

f = open('swagger.json')
data = json.load(f)

for path in data['paths']:
  print(path)
  for operation in data[]:
    print('-- ' + operation)
