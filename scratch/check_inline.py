import zipfile
import json
with zipfile.ZipFile('c:/Users/basti/curseforge/minecraft/Instances/SHHHHH/mods/lostcities-1.20-7.4.11.jar', 'r') as z:
    for info in z.infolist():
        if info.filename.endswith('.json') and 'parts/' in info.filename:
            d = json.loads(z.read(info.filename).decode('utf-8', errors='ignore'))
            if 'palette' in d:
                print(info.filename, "has inline palette")
                print(json.dumps(d['palette'][:2], indent=2))
                break
