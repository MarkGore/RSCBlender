bl_info = {
    "name": "RSC Model Plugin",
    "author": "Mark Gore",
    "version": (1, 0),
    "blender": (3, 0, 0),
    "location": "View3D > Tool Shelf > Model Parser Tab",
    "description": "Parses a custom model format and renders it in the scene",
    "category": "Import-Export",
}

import bpy
from .operators import OBJECT_OT_import_model, OBJECT_OT_export_model
from .panel import VIEW3D_PT_model_parser_panel

# Register classes
classes = (OBJECT_OT_import_model, OBJECT_OT_export_model, VIEW3D_PT_model_parser_panel)

def register():
    """Registers all classes with Blender"""
    for cls in classes:
        bpy.utils.register_class(cls)

def unregister():
    """Unregisters all classes from Blender"""
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)

# Make sure this block is correctly indented
if __name__ == "__main__":  
    register()  # This must be indented properly
