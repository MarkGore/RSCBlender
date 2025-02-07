import bpy
from bpy.props import StringProperty
from bpy_extras.io_utils import ImportHelper, ExportHelper
from .parser import parse_model
from .exporter import export_model
from .mesh import create_mesh_from_data

class OBJECT_OT_import_model(bpy.types.Operator, ImportHelper):
    bl_idname = "object.import_model"
    bl_label = "Import and Render Model"
    bl_options = {"REGISTER", "UNDO"}

    filename_ext = ".dat"
    filter_glob: StringProperty(default="*.dat", options={"HIDDEN"}, maxlen=255)

    def execute(self, context):
        parsed_data = parse_model(self.filepath)
        if parsed_data:
            create_mesh_from_data(parsed_data)
            self.report({"INFO"}, "Model parsed and rendered successfully!")
        else:
            self.report({"ERROR"}, "Failed to parse model")
        return {"FINISHED"}

class OBJECT_OT_export_model(bpy.types.Operator, ExportHelper):
    bl_idname = "object.export_model"
    bl_label = "Export Parsed Model"
    bl_options = {"REGISTER", "UNDO"}

    filename_ext = ".dat"

    def execute(self, context):
        export_model(self.filepath)
        self.report({"INFO"}, f"Model exported to {self.filepath}")
        return {"FINISHED"}
