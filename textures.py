import os
import bpy

def find_texture(texture_id):
    plugin_dir = os.path.dirname(os.path.abspath(__file__))
    texture_folder = os.path.join(plugin_dir, "textures")

    if not os.path.exists(texture_folder):
        print(f"Texture folder not found: {texture_folder}")
        return None

    texture_file = os.path.join(texture_folder, f"{texture_id}.png")
    
    if os.path.exists(texture_file):
        return texture_file

    print(f"Texture {texture_id} not found.")
    return None


def apply_texture(material, texture_path):
    if not texture_path or not os.path.exists(texture_path):
        print(f"Invalid texture path: {texture_path}")
        return

    material.use_nodes = True
    bsdf = material.node_tree.nodes.get("Principled BSDF")

    tex_image = material.node_tree.nodes.new("ShaderNodeTexImage")
    tex_image.image = bpy.data.images.load(texture_path)

    material.node_tree.links.new(bsdf.inputs["Base Color"], tex_image.outputs["Color"])
