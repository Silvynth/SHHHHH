import json
import os
import glob

os.chdir('c:/Users/basti/curseforge/minecraft/Instances/SHHHHH/config/paxi/datapacks/LostCitiesCustom/data/lostcities/lostcities/parts/')

for f in glob.glob('*.json'):
    with open(f, 'r') as file:
        data = json.load(file)
    
    changed = False
    
    if 'palette' in data and isinstance(data['palette'], list):
        # We need to wrap it and convert properties
        new_palette_list = []
        for entry in data['palette']:
            block_str = entry['block']
            if 'properties' in entry:
                props = entry['properties']
                if props:
                    prop_str = ','.join([f"{k}={v}" for k, v in props.items()])
                    block_str = f"{block_str}[{prop_str}]"
                del entry['properties']
            entry['block'] = block_str
            new_palette_list.append(entry)
            
        data['palette'] = {"palette": new_palette_list}
        changed = True

    if changed:
        with open(f, 'w') as file:
            json.dump(data, file, indent=2)
        print(f"Fixed palette format in {f}")
