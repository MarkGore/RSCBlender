import bpy
from .utils import get_rs_color

def export_model(filepath):
    obj = bpy.context.active_object

    if not obj or obj.type != "MESH":
        print("No valid mesh object selected for export!")
        return

    if bpy.context.object.mode != 'OBJECT':
        bpy.ops.object.mode_set(mode='OBJECT')

    bpy.ops.object.select_all(action='DESELECT')
    bpy.context.view_layer.objects.active = obj
    obj.select_set(True)

    try:
        bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
    except RuntimeError as e:
        print(f"Error applying transformations: {e}")

    mesh = obj.data

    min_x, max_x = min(v.co.x for v in mesh.vertices), max(v.co.x for v in mesh.vertices)
    min_y, max_y = min(v.co.y for v in mesh.vertices), max(v.co.y for v in mesh.vertices)
    min_z, max_z = min(v.co.z for v in mesh.vertices), max(v.co.z for v in mesh.vertices)
    center_x, center_y, center_z = (min_x + max_x) / 2, (min_y + max_y) / 2, (min_z + max_z) / 2

    # Adjust vertices
    vertices = [
        (int((v.co.x - center_x) * 1000),
         int((v.co.z - center_z) * 1000),
         int((-(v.co.y - center_y)) * 1000))
        for v in mesh.vertices
    ]

    faces, face_vert_cnt, texture_front, texture_back, face_shade = [], [], [], [], []
    materials = obj.data.materials

    for poly in mesh.polygons:
        faces.append([v for v in poly.vertices])
        face_vert_cnt.append(len(poly.vertices))

        material = materials[poly.material_index] if poly.material_index < len(materials) else None
        if material:
            if material.name.startswith("Texture_"):
                try:
                    texture_id = int(material.name.split("_")[1].split(".")[0])
                except ValueError:
                    texture_id = -55
                texture_front.append(texture_id)
                texture_back.append(texture_id)
            else:
                rsc_color = get_rs_color(material)
                texture_front.append(rsc_color)
                texture_back.append(rsc_color)
        else:
            texture_front.append(-92)
            texture_back.append(-92)

        face_shade.append(0)

    with open(filepath, "wb") as f:
        f.write(len(vertices).to_bytes(2, "big"))
        f.write(len(faces).to_bytes(2, "big"))


        z_offset = abs(center_z+3) * 1000  # Offset the Z-axis to ensure no negative values
        
        for x, y, z in vertices:
            # Write the rotated coordinates to the file
            f.write(int(x / 100).to_bytes(4, byteorder="big", signed=True))  # Signed int
            f.write(int(-(y+z_offset) / 100).to_bytes(4, byteorder="big", signed=True))
            f.write(int((z) / 100).to_bytes(4, byteorder="big", signed=True))
            f.write(int(0).to_bytes(4, byteorder="big", signed=True))

        for i in range(len(faces)):
            f.write(face_vert_cnt[i].to_bytes(4, "big", signed=True))
            f.write(texture_front[i].to_bytes(4, "big", signed=True))
            f.write(texture_back[i].to_bytes(4, "big", signed=True))
            f.write(face_shade[i].to_bytes(4, "big", signed=True))

        for face in faces:
            for vertex_index in face:
                f.write(vertex_index.to_bytes(4, "big", signed=False))

    print(f"Model successfully exported to {filepath}")
