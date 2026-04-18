import os
import json
import glob
from nbt.nbt import NBTFile

SCHEMATICS_DIR = 'c:/Users/basti/curseforge/minecraft/Instances/SHHHHH/schematics'
OUTPUT_DIR = 'c:/Users/basti/curseforge/minecraft/Instances/SHHHHH/config/paxi/datapacks/LostCitiesCustom/data/lostcities/lostcities/parts'

def get_block_state(block_state_tag):
    name = block_state_tag["Name"].value
    props = {}
    if "Properties" in block_state_tag:
        for k, v in block_state_tag["Properties"].items():
            props[k] = v.value
    return name, props

def convert_all():
    for f in glob.glob(os.path.join(SCHEMATICS_DIR, '*.nbt')):
        filename = os.path.basename(f)
        part_name = filename.replace('.nbt', '')
        
        nbt_file = NBTFile(f, 'rb')
        size = nbt_file["size"]
        x_size = size[0].value
        y_size = size[1].value
        z_size = size[2].value
        
        # 10 blocks high maximum
        max_y = min(y_size, 10)
        
        # Align to 16x16. 
        x_offset = (16 - x_size + 1) // 2 
        z_offset = (16 - z_size + 1) // 2
        
        palette_tag = nbt_file["palette"]
        block_palette = []
        for state in palette_tag:
            name, props = get_block_state(state)
            if "copycat_stairs" in name:
                name = "create:cut_deepslate_brick_stairs"
            elif "copycat_step" in name:
                name = "create:cut_deepslate_bricks"
                props = {}
            block_palette.append((name, props))
            
        grid = [[[" " for _ in range(16)] for _ in range(10)] for _ in range(16)]
        
        # Initialize bounding box with AIR instead of padding
        for x in range(x_size):
            for y in range(max_y):
                for z in range(z_size):
                    grid_x = x + x_offset
                    grid_z = z + z_offset
                    if 0 <= grid_x < 16 and 0 <= grid_z < 16:
                        grid[grid_x][y][grid_z] = "_"
        
        blocks_tag = nbt_file["blocks"]
        for block_tag in blocks_tag:
            pos = block_tag["pos"]
            x, y, z = pos[0].value, pos[1].value, pos[2].value
            state_idx = block_tag["state"].value
            
            grid_x = x + x_offset
            grid_z = z + z_offset
            
            if 0 <= grid_x < 16 and 0 <= grid_z < 16 and y < 10:
                name, props = block_palette[state_idx]
                if name == "minecraft:air":
                    grid[grid_x][y][grid_z] = "_"
                else:
                    grid[grid_x][y][grid_z] = str(state_idx)
                    
        # Generate palette mapping
        used_indices = set()
        for x in range(16):
            for y in range(10):
                for z in range(16):
                    val = grid[x][y][z]
                    if val != " " and val != "_":
                        used_indices.add(int(val))
                        
        char_map = {" ": " ", "_": "_"}
        palette_out = []
        
        palette_out.append({
            "char": "_",
            "block": "minecraft:air"
        })
        
        chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
        char_idx = 0
        
        for idx in used_indices:
            char = chars[char_idx]
            char_idx += 1
            char_map[str(idx)] = char
            
            name, props = block_palette[idx]
            
            if props:
                prop_str = ",".join([f"{k}={v}" for k, v in props.items()])
                name = f"{name}[{prop_str}]"
                
            palette_out.append({
                "char": char,
                "block": name
            })
            
        slices = []
        for y in range(10):
            slice_rows = []
            for z in range(16):
                row = ""
                for x in range(16):
                    val = grid[x][y][z]
                    row += char_map[val]
                slice_rows.append(row)
            slices.append(slice_rows)
            
        out_data = {
            "xsize": 16,
            "zsize": 16,
            "slices": slices,
            "palette": {"palette": palette_out}
        }
        
        out_path = os.path.join(OUTPUT_DIR, f"{part_name}.json")
        with open(out_path, 'w') as out_f:
            json.dump(out_data, out_f, indent=2)
        print(f"Converted {part_name} with AIR")

if __name__ == "__main__":
    convert_all()
