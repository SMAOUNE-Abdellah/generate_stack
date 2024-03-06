import re
import yaml

def parse_terraform_file(input_file):
    with open(input_file, 'r') as f:
        data = f.read()
    
    matches = re.findall(r'"(.*?)".*?=.*?\[(.*?)\]', data, re.DOTALL)

    result = {}
    for match in matches:
        vm_name = match[0]
        disks = match[1].strip().split('\n')
        disks = {f'sd{chr(ord("a") + idx)}': disk.strip('" ,') for idx, disk in enumerate(disks)}
        result[vm_name] = {'disks': disks}
    
    return result

def generate_yaml(data, output_file):
    with open(output_file, 'w') as f:
        yaml.dump(data, f, default_flow_style=False)


terraform_file_path = 'test.tf'
yaml_output_file_path = 'test.yaml'

terraform_data = parse_terraform_file(terraform_file_path)
generate_yaml(terraform_data, yaml_output_file_path)
