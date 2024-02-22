import os
import pandas as pd
import json

def excel_to_json(excel_file, json_file, constant_file):
    data = {"locals": {"vm_configs": []}}
    # Read Excel file
    df = pd.read_excel(excel_file)
    first_row = df.iloc[0]
    vm_segment = first_row["segment"]
    for index, row in df.iterrows():
        vm = {
            "name": row["vm-name"],
            "num_cpus": row["cpu"],
            "memory": row["ram"],
            "disks": []
        }

        for i in range(1, 5):
            disk_col = f"disk{i}_size"
            if disk_col in row and pd.notna(row[disk_col]):
                vm['disks'].append({
                    "unit_number": str(i),
                    "size": str(int(row[disk_col])),
                    "thin_provisionned": "true",
                    "eagerly_scrub": "false"
                })
        
        data['locals']['vm_configs'].append(vm)
    
    # Write data into JSON file
    if not os.path.exists(json_file):
        with open(json_file, 'w') as jsonfile:
            json.dump(data, jsonfile, indent=4)

    with open(constant_file, 'r') as tffile:
        tf_content = tffile.read()
        tf_content = tf_content.replace("vm_segment =", f"vm_segment = \"{vm_segment}\"")

    with open(constant_file, 'w') as tffile:
        tffile.write(tf_content)


# Paths to the Excel and JSON files
excel_file = 'vms.xlsx'
json_file = 'vms.json'
constant_file = './created_folder/constants.tf'

# Call the function to convert Excel to JSON
excel_to_json(excel_file, json_file, constant_file)
