import gzip, struct, json, os, glob

def read_val(data, tag_type, p):
    if tag_type == 1: return data[p], p + 1
    if tag_type == 2: return struct.unpack('>h', data[p:p+2])[0], p + 2
    if tag_type == 3: return struct.unpack('>i', data[p:p+4])[0], p + 4
    if tag_type == 4: return struct.unpack('>q', data[p:p+8])[0], p + 8
    if tag_type == 5: return struct.unpack('>f', data[p:p+4])[0], p + 4
    if tag_type == 6: return struct.unpack('>d', data[p:p+8])[0], p + 8
    if tag_type == 7:
        l = struct.unpack('>i', data[p:p+4])[0]
        return data[p+4:p+4+l], p + 4 + l
    if tag_type == 8:
        l = struct.unpack('>H', data[p:p+2])[0]
        return data[p+2:p+2+l].decode('utf-8', 'ignore'), p + 2 + l
    if tag_type == 9:
        sub_type = data[p]
        l = struct.unpack('>i', data[p+1:p+5])[0]
        p += 5
        res = []
        for _ in range(l):
            v, p = read_val(data, sub_type, p)
            res.append(v)
        return res, p
    if tag_type == 10:
        res = {}
        while True:
            tt = data[p]
            p += 1
            if tt == 0: return res, p
            name_len = struct.unpack('>H', data[p:p+2])[0]
            name = data[p+2:p+2+name_len].decode('utf-8', 'ignore')
            p += 2 + name_len
            v, p = read_val(data, tt, p)
            res[name] = v
    if tag_type == 11:
        l = struct.unpack('>i', data[p:p+4])[0]
        res = []
        for i in range(l):
            res.append(struct.unpack('>i', data[p+4+i*4:p+8+i*4])[0])
        return res, p + 4 + l * 4
    return None, p

def convert_one(nbt_path, output_path):
    print(f"Converting {os.path.basename(nbt_path)}...")
    with gzip.open(nbt_path, 'rb') as f:
        raw = f.read()
        p = 1
        name_len = struct.unpack('>H', raw[p:p+2])[0]
        p += 2 + name_len
        nbt_data, _ = read_val(raw, 10, p)

    size = nbt_data.get('size') # [x, y, z]
    palette = nbt_data.get('palette', [])
    blocks = nbt_data.get('blocks', [])

    nx, ny, nz = size
    # Grid [y][z][x]
    grid = [[[' ' for _ in range(16)] for _ in range(16)] for _ in range(ny)]

    # Centering X (Standard LC parts are 16 wide)
    off_x = (16 - nx) // 2
    # Standard LC parts are 16 deep
    off_z = (16 - nz) // 2

    chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()_+-=[]{}|;:,.<>?"
    char_map = {} # char -> palette_index
    palette_to_char = {} # palette_index -> char

    for b in blocks:
        pos = b.get('pos')
        state = b.get('state')
        x, y, z = pos
        
        if state not in palette_to_char:
            c = chars[len(palette_to_char)]
            palette_to_char[state] = c
            char_map[c] = state
        
        char = palette_to_char[state]
        grid[y][z + off_z][x + off_x] = char

    # Generate Lost Cities Palette
    lc_palette = []
    for char, state_idx in char_map.items():
        p_entry = palette[state_idx]
        block_name = p_entry.get('Name')
        props = p_entry.get('Properties', {})
        
        entry = {"char": char, "block": block_name}
        if props:
            entry["properties"] = props
        lc_palette.append(entry)

    # Generate Slices
    slices = []
    for y in range(ny):
        slice_rows = []
        for z in range(16):
            row = "".join(grid[y][z])
            slice_rows.append(row)
        slices.append(slice_rows)

    result = {
        "exportedpart": {
            "xsize": 16,
            "zsize": 16,
            "slices": slices
        },
        "palette": lc_palette
    }

    with open(output_path, 'w') as f:
        json.dump(result, f, indent=2)

def batch_convert(input_dir, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    files = glob.glob(os.path.join(input_dir, "*.nbt"))
    for f in files:
        basename = os.path.basename(f)
        json_name = basename.replace(".nbt", ".json")
        convert_one(f, os.path.join(output_dir, json_name))
    print(f"Finished! Processed {len(files)} files.")

if __name__ == "__main__":
    schem_dir = 'c:/Users/basti/curseforge/minecraft/Instances/SHHHHH/schematics'
    out_dir = 'c:/Users/basti/curseforge/minecraft/Instances/SHHHHH/convertidos'
    batch_convert(schem_dir, out_dir)
