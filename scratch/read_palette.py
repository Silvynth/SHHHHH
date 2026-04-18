import zipfile
import json
with zipfile.ZipFile('c:/Users/basti/curseforge/minecraft/Instances/SHHHHH/mods/lostcities-1.20-7.4.11.jar', 'r') as z:
    data = z.read('data/lostcities/lostcities/palettes/rails.json')
    print(data.decode('utf-8'))
