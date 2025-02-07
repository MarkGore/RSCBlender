import bpy
import os
from .utils import get_color

def find_texture(texture_id):
    plugin_dir = os.path.dirname(os.path.abspath(__file__))
    texture_folder = os.path.join(plugin_dir, "textures")

    if not os.path.exists(texture_folder):
        print(f"Texture folder not found: {texture_folder}")
        return None

    texture_file = os.path.join(texture_folder, f"{texture_id}.png")
    print(f"Looking for texture: {texture_file}")

    return texture_file if os.path.exists(texture_file) else None


def create_mesh_from_data(parsed_data, name="ParsedModel"):
    vertices = parsed_data["vertices"]
    faces = parsed_data["faces"]
    face_colors = parsed_data["face_colors"]
    face_textures = parsed_data["face_texture"]

    scale_factor = 1000.0
    vertices = [(x / scale_factor, y / scale_factor, z / scale_factor) for x, y, z in vertices]

    mesh = bpy.data.meshes.new(name)
    mesh.from_pydata(vertices, [], faces)
    uv_layer = mesh.uv_layers.new(name="UVMap")

    mesh.update()
    mesh.validate()

    obj = bpy.data.objects.new(name, mesh)
    bpy.context.scene.collection.objects.link(obj)

    materials = {}
    default_black_color = (0.0, 0.0, 0.0, 1.0)

    for i, color in enumerate(face_colors):
        material = None

        if color is None:
            texture_id = face_textures[i]
            if texture_id not in materials:
                texture_file = find_texture(texture_id)
                if texture_file:
                    mat = bpy.data.materials.new(name=f"Texture_{texture_id}")
                    mat.use_nodes = True
                    bsdf = mat.node_tree.nodes.get("Principled BSDF")
                    tex_image = mat.node_tree.nodes.new("ShaderNodeTexImage")
                    tex_image.image = bpy.data.images.load(texture_file)
                    mat.node_tree.links.new(bsdf.inputs["Base Color"], tex_image.outputs["Color"])
                    materials[texture_id] = mat
                else:
                    color = default_black_color

        if color is not None:
            if color not in materials:
                mat = bpy.data.materials.new(name=f"Material_RGB_{color}")
                mat.use_nodes = True
                bsdf = mat.node_tree.nodes.get("Principled BSDF")
                if bsdf:
                    bsdf.inputs["Base Color"].default_value = color
                materials[color] = mat

        material = materials.get(texture_id if color is None else color)
        if material and material.name not in [mat.name for mat in obj.data.materials]:
            obj.data.materials.append(material)

        for poly in mesh.polygons:
            if poly.index == i:
                poly.material_index = obj.data.materials.find(material.name)

            uv_coordinates = []
            for loop_index in poly.loop_indices:
                vertex_index = mesh.loops[loop_index].vertex_index
                u, v = vertices[vertex_index][0] % 1, vertices[vertex_index][1] % 1
                uv_coordinates.append((u, v))

            for loop_index, uv in zip(poly.loop_indices, uv_coordinates):
                uv_layer.data[loop_index].uv = uv

    obj.location = (0, 0, 0)

    for area in bpy.context.screen.areas:
        if area.type == "VIEW_3D":
            for space in area.spaces:
                if space.type == "VIEW_3D":
                    space.shading.type = "MATERIAL"
