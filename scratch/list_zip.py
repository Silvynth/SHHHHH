import zipfile
with zipfile.ZipFile('c:/Users/basti/curseforge/minecraft/Instances/SHHHHH/mods/lostcities-1.20-7.4.11.jar', 'r') as z:
    for info in z.infolist():
        if 'rails_vertical.json' in info.filename:
            print(info.filename)
