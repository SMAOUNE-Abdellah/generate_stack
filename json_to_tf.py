import json

def convert_json_to_terraform(json_data, output_file):
    # Convert json data to terraform data
    terraform_code = "locals {\n  vm_configs = [\n"

    num_vm_configs = len(json_data["locals"]["vm_configs"])
    for i, vm_config in enumerate(json_data["locals"]["vm_configs"]):
        terraform_code += "    {\n"
        terraform_code += f'      name = "{vm_config["name"]}"\n'
        terraform_code += f'      num_cpus = {vm_config["num_cpus"]}\n'
        terraform_code += f'      memory = {vm_config["memory"]}\n'
        terraform_code += "      disks = [\n"
        for j, disk in enumerate(vm_config["disks"]):
            terraform_code += "        {\n"
            terraform_code += f'          unit_number = "{disk["unit_number"]}"\n'
            terraform_code += f'          size = {disk["size"]}\n'
            terraform_code += f'          thin_provisionned = {disk["thin_provisionned"]}\n'
            terraform_code += f'          eagerly_scrub = {disk["eagerly_scrub"]}\n'
            terraform_code += "        }"
            if j < len(vm_config["disks"]) - 1:
                terraform_code += ","
            terraform_code += "\n"
        terraform_code += "      ]\n"
        terraform_code += "    }"
        if i < num_vm_configs - 1:
            terraform_code += ","
        terraform_code += "\n"

    terraform_code += "  ]\n}"

    # Write data to terraform file
    with open(output_file, 'w') as f:
        f.write(terraform_code)

# Example usage
with open('vms.json', 'r') as f:
    json_data = json.load(f)

convert_json_to_terraform(json_data, 'locals.tf')






