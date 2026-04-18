import zipfile
import os

def zip_dir(path, zip_h):
    for root, dirs, files in os.walk(path):
        for file in files:
            file_path = os.path.join(root, file)
            # Use relative path for the zip archive
            arcname = os.path.relpath(file_path, path)
            zip_h.write(file_path, arcname)

mod_dir = 'c:/Users/basti/curseforge/minecraft/Instances/SHHHHH/mods/LostCitiesCustomMod'
out_jar = 'c:/Users/basti/curseforge/minecraft/Instances/SHHHHH/mods/LostCitiesCustomMod.jar'

with zipfile.ZipFile(out_jar, 'w', zipfile.ZIP_DEFLATED) as zipf:
    zip_dir(mod_dir, zipf)

print(f"Created {out_jar} successfully.")
