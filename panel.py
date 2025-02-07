import bpy

class VIEW3D_PT_model_parser_panel(bpy.types.Panel):
    bl_label = "RSC Models"
    bl_idname = "VIEW3D_PT_model_parser_panel"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "RSC Models"

    def draw(self, context):
        layout = self.layout
        layout.operator("object.import_model", text="Import and Render Model")
        layout.operator("object.export_model", text="Export Parsed Model")
