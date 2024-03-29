import json
import re
import datetime
import os


def get_test_file_paths_on_flux_project(tests_path):
    test_file_paths = []
    for root, _, files in os.walk(tests_path):
        for file in files:
            test_file_paths.append(os.path.join(root, file))
    return test_file_paths


def get_interface_file_paths_on_flux_project(interfaces_path):
    interface_file_paths = []
    for root, _, files in os.walk(interfaces_path):
        for file in files:
            interface_file_paths.append(os.path.join(root, file))
    return interface_file_paths


def count_method_calls(method, test_file_paths):
    count = 0
    for file in test_file_paths:
        with open(file, encoding='UTF-8') as f:
            try:
                lines = f.readlines()
                for line in lines:
                    if f'{method}' in line:
                        count += 1
            except:
                print(f'Error reading file: {file}')
    return count


def get_endpoints_calls_from_flux_project(interfaces):
    flux_operations = []
    flux_paths = []

    for interface in interfaces:
        flux_operations.append(
            re.search('\[Get|\[Post|\[Patch|\[Put|\[Delete', interface).group(0)[1:].lower())
        flux_paths.append(re.search('(?<=\").*(?=\")',
                          interface).group(0).lower())

    return flux_paths, flux_operations


def get_api_endpoints_and_operations_from_swagger_data(swagger_data):
    api_endpoints = []
    api_operations = []

    for path in swagger_data['paths']:
        lowercased_path = path.lower()
        if lowercased_path != '/' and 'servicediagnostics' not in lowercased_path:
            for operation in swagger_data['paths'][path]:
                api_endpoints.append(path.lower())
                api_operations.append(operation)
    return api_endpoints, api_operations


def generate_report(api_endpoints, flux_api_calls, report_lines):
    exercised_endpoints = 0
    total_of_api_endpoints_operations = len(api_endpoints)

    for endpoint in flux_api_calls:
        if flux_api_calls[endpoint]["count"] > 0:
            exercised_endpoints += 1

    report_lines += f"""
    ---------------------------------- {flux_project_name} / {datetime.datetime.now().strftime("%x")} ----------------------------------
    Endpoints-Operations In API: {total_of_api_endpoints_operations}
    Endpoints-Operations Exercised By Tests: {exercised_endpoints}
    Coverage Percentage: {round((exercised_endpoints / total_of_api_endpoints_operations * 100), 1)}%

    Endpoints-Operations Covered:
    """
    for endpoint in flux_api_calls:
        if flux_api_calls[endpoint]["count"] > 0:
            report_lines += f"""
            {endpoint} 
                    (exercised by {flux_api_calls[endpoint]["count"]} tests)
            """

    report_lines += f"""
    Endpoints-Operations Not Covered:"""
    for endpoint in api_endpoints:
        if endpoint not in flux_api_calls:
            report_lines += f"""
            {endpoint}""" 
    return report_lines

def get_flux_api_methods_and_interfaces(interfaces_file_paths):
    interfaces = []
    flux_api_methods = []

    for interface_file_path in interfaces_file_paths:
        text_file = open(interface_file_path, 'r', encoding='UTF-8')
        lines = text_file.readlines()

        for i, line in enumerate(lines):
            if re.search('\[Post|\[Get|\[Put|\[Patch|\[Delete', line):
                if not line.lstrip().startswith('//'): # skip commented-out lines
                    interfaces.append(line)
                    method = re.search('\w*\(', lines[i+1]).group(0)[:-1]
                    flux_api_methods.append(method)

    return flux_api_methods, interfaces


def read_api_specification(api_specifications_base, api_name):
    f = open(os.path.join(api_specifications_base,
             f'{api_name}.json'), encoding='UTF-8')
    return json.load(f)


if __name__ == '__main__':
    flux_projects_base = './flux-projects'
    api_specifications_base = './api-specs'
    report_lines = "";

    if not os.path.exists(flux_projects_base):
        print(
            f'Flux projects base directory not found in {flux_projects_base}. Aborting...')
        exit(1)

    if not os.path.exists('api-urls.json'):
        print(f'File api-urls.json not found in {os.getcwd()}. Aborting...')
        exit(1)

    f = open('api-urls.json', encoding='UTF-8')
    apis = json.load(f)

    base_path = os.getcwd()

    for api in apis:
        api_name = api['name']

        api_specification_file_path = os.path.join(
            api_specifications_base, f'{api_name}.json')
        if not os.path.exists(api_specification_file_path):
            print(
                f'API specification file {api_name}.json not found in {api_specifications_base}. Aborting...')
            exit(1)

    for api in apis:
        api_name = api['name']
        flux_project_name = f'Flux.{api_name}'
        flux_project_base_path = os.path.join(
            flux_projects_base, flux_project_name)

        # Find the base path of the Flux project
        if not os.path.exists(os.path.join(flux_project_base_path, 'TestScripts')):
            flux_project_base_path = os.path.join(
                flux_project_base_path, flux_project_name)
            if not os.path.exists(os.path.join(flux_project_base_path, 'TestScripts')):
                flux_project_base_path = os.path.join(
                    flux_project_base_path, flux_project_name)
                if not os.path.exists(os.path.join(flux_project_base_path, 'TestScripts')):
                    flux_project_base_path = os.path.join(
                        flux_project_base_path, flux_project_name)

        api_specification = read_api_specification(
            api_specifications_base, api_name)

        method_counts = {}
        flux_api_methods = []
        interfaces = []

        tests_path = os.path.join(flux_project_base_path, 'TestScripts')
        interfaces_path = os.path.join(flux_project_base_path, 'Interfaces')

        tests_file_paths = get_test_file_paths_on_flux_project(tests_path)
        interfaces_file_paths = get_interface_file_paths_on_flux_project(
            interfaces_path)

        flux_api_methods, interfaces = get_flux_api_methods_and_interfaces(
            interfaces_file_paths)

        for method in flux_api_methods:
            method_counts[method] = count_method_calls(
                method, tests_file_paths)

        api_endpoints, api_operations = get_api_endpoints_and_operations_from_swagger_data(
            api_specification)

        endpoints_on_flux_project, endpoint_operations_on_flux_project = get_endpoints_calls_from_flux_project(
            interfaces)

        flux_api_calls = {}
        api_endpoints_operations = []

        for i, endpoint in enumerate(endpoints_on_flux_project):
            # if '{facility}' in endpoint:

            endpoint = endpoint.replace('{facility}', '{sitecode}')
            endpoint = endpoint.replace('{facilitycode}', '{sitecode}')
            endpoint = endpoint.rstrip('/')
            operation_endpoint = f"{endpoint_operations_on_flux_project[i]} {endpoint}"
            flux_api_calls[operation_endpoint] = {
                'method': flux_api_methods[i],
                'count': method_counts[flux_api_methods[i]],
            }

        for i in range(len(api_endpoints)):
            api_endpoint = api_endpoints[i]
            api_endpoint = api_endpoint.replace('{facility}', '{sitecode}')
            api_endpoint = api_endpoint.replace('{facilitycode}', '{sitecode}')
            api_endpoint = api_endpoint.rstrip('/')
            operation_endpoint = f"{api_operations[i]} {api_endpoint}"
            api_endpoints_operations.append(operation_endpoint)

        report_lines = generate_report(api_endpoints_operations, flux_api_calls, report_lines)

    print(report_lines)
    with open('coverage-report.txt', 'w', encoding='UTF-8') as report_file:
        report_file.write(report_lines)
    print('--> Coverage report has been saved in coverage-report.txt')
