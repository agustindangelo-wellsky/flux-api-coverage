import json
import git
import os

f = open('api-urls.json', encoding='UTF-8')
apis = json.load(f)
flux_projects_base = './flux-projects'

if not os.path.exists(flux_projects_base):
    os.mkdir(flux_projects_base)

for api in apis:
    api_name = api['name']
    flux_project_name = f'Flux.{api_name}'

    if os.path.exists(os.path.join(flux_projects_base, flux_project_name)):
        print(f'--> {flux_project_name} already cloned. Running git pull...')
        repo = git.Repo(os.path.join(flux_projects_base, flux_project_name))
        repo.remotes.origin.pull()
    else:
        flux_project_url = api['projectUrl']
        print(f'--> Cloning {flux_project_name} into {flux_projects_base}...')
        git.Git(flux_projects_base).clone(flux_project_url)
