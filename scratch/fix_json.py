import json
import os
import glob

os.chdir('c:/Users/basti/curseforge/minecraft/Instances/SHHHHH/config/paxi/datapacks/LostCitiesCustom/data/lostcities/lostcities/parts/')

for f in glob.glob('*.json'):
    with open(f, 'r') as file:
        data = json.load(file)
    
    if 'exportedpart' in data:
        new_data = data['exportedpart']
        if 'palette' in data:
            new_data['palette'] = data['palette']
            
        with open(f, 'w') as file:
            json.dump(new_data, file, indent=2)
        print(f"Fixed {f}")
