bl_info = {
    "name": "Clouds generator",
    "author": "Darío R.H. <rhdariorh@gmail.com>",
    "version": (0, 0),
    "blender": (2, 83, 1),
    "category": "Object",
    "location": "Operator Search",
    "description": "Automatic creation of different types of clouds.",
    "warning": "Development version",
    "doc_url": "",
    "tracker_url": "",
}

import bpy
from mathutils import Vector
import bpy.utils.previews

from . import materials
from .cloud_settings import CloudSettings
from .materials import initial_shape_single_cumulus, initial_shape_landscape_cumulus

class CloudErrorOperator(bpy.types.Operator):
    bl_idname = "error.cloud_error"
    bl_label = "Cloud Error Operator"

    error_type: bpy.props.StringProperty(
        name="Cloud error type"
    )

    def execute(self, context):
        if self.error_type == "MATERIAL_WRONG_NAME":
            self.report({'WARNING'}, "The active cloud material name is not correct")
        return {'FINISHED'}


class OBJECT_OT_cloud_single_cumulus(bpy.types.Operator):
    """Add a single cumulus cloud"""
    bl_idname = "object.cloud_add_single_cumulus"
    bl_label = "Generate single cumulus"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        return context.area.type == "VIEW_3D"

    def execute(self, context):
        materials.generate_cloud(context, -1000, 0, initial_shape_single_cumulus)
        return {'FINISHED'}

class OBJECT_OT_cloud_landscape_cumulus(bpy.types.Operator):
    """Add a cumulus landscape"""
    bl_idname = "object.cloud_add_landscape_cumulus"
    bl_label = "Generate cumulus landscape"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        return context.area.type == "VIEW_3D"

    def execute(self, context):
        materials.generate_cloud(context, -1000, 0, initial_shape_landscape_cumulus)
        return {'FINISHED'}


class OBJECT_PT_cloud(bpy.types.Panel):
    """Creates a Panel in the scene context of the properties editor"""
    bl_label = "Cloud settings"
    bl_idname = "OBJECT_PT_cloud"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "object"

    @classmethod
    def poll(cls, context):
        return context.object.cloud_settings.is_cloud

    def draw(self, context):
        layout = self.layout
        layout.use_property_split = True
        obj = context.object
        cloud_settings = obj.cloud_settings
        if obj.cloud_settings.is_cloud:
            column = layout.column()
            column.prop(cloud_settings, "domain", text="Domain")
            column.prop(cloud_settings, "size", text="Size")

class OBJECT_PT_cloud_general(bpy.types.Panel):
    bl_label = "General"
    bl_parent_id = "OBJECT_PT_cloud"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "object"
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        layout = self.layout
        layout.use_property_split = True

        obj = context.object
        cloud_settings = obj.cloud_settings
        if obj.cloud_settings.is_cloud:
            column = layout.column()
            column.prop(cloud_settings, "density", text="Density")
            column.prop(cloud_settings, "wind", text="Wind")
            if cloud_settings.cloud_type == "LANDSCAPE_CUMULUS":
                column.prop(cloud_settings, "amount_of_clouds", text="Amount of clouds")
                column.prop(cloud_settings, "landscape_cloud_size", text="Clouds size")
                column.prop(cloud_settings, "landscape_noise_coords", text="Seed")

class OBJECT_PT_cloud_shape(bpy.types.Panel):
    bl_label = "Shape"
    bl_parent_id = "OBJECT_PT_cloud"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "object"
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        layout = self.layout
        layout.use_property_split = True

        obj = context.object
        cloud_settings = obj.cloud_settings
        if obj.cloud_settings.is_cloud:
            column = layout.column()
            if (cloud_settings.cloud_type == "SINGLE_CUMULUS"):
                column.prop(cloud_settings, "height_single", text="Height")
                column.prop(cloud_settings, "width_x", text="Width X")
                column.prop(cloud_settings, "width_y", text="Width Y")
            elif(cloud_settings.cloud_type == "LANDSCAPE_CUMULUS"):
                column.prop(cloud_settings, "height_landscape", text="Height")

class OBJECT_PT_cloud_shape_roundness(bpy.types.Panel):
    bl_label = "Roundness"
    bl_parent_id = "OBJECT_PT_cloud_shape"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "object"
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        layout = self.layout
        layout.use_property_split = True

        obj = context.object
        cloud_settings = obj.cloud_settings
        if obj.cloud_settings.is_cloud:
            column = layout.column()
            column.prop(cloud_settings, "roundness", text="Strength")
            column.prop(cloud_settings, "roundness_coords", text="Seed")

class OBJECT_PT_cloud_shape_add_imperfection(bpy.types.Panel):
    bl_label = "Add imperfection"
    bl_parent_id = "OBJECT_PT_cloud_shape"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "object"
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        layout = self.layout
        layout.use_property_split = True

        obj = context.object
        cloud_settings = obj.cloud_settings
        if obj.cloud_settings.is_cloud:
            column = layout.column()
            column.prop(cloud_settings, "add_shape_imperfection", text="Strength")
            column.prop(cloud_settings, "add_shape_imperfection_coords", text="Seed")

class OBJECT_PT_cloud_shape_subtract_imperfection(bpy.types.Panel):
    bl_label = "Subtract imperfection"
    bl_parent_id = "OBJECT_PT_cloud_shape"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "object"
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        layout = self.layout
        layout.use_property_split = True

        obj = context.object
        cloud_settings = obj.cloud_settings
        if obj.cloud_settings.is_cloud:
            column = layout.column()
            column.prop(cloud_settings, "subtract_shape_imperfection", text="Strength")
            column.prop(cloud_settings, "subtract_shape_imperfection_coords", text="Seed")

class OBJECT_PT_cloud_detail(bpy.types.Panel):
    bl_label = "Detail"
    bl_parent_id = "OBJECT_PT_cloud"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "object"
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        layout = self.layout
        layout.use_property_split = True

        obj = context.object
        cloud_settings = obj.cloud_settings
        if obj.cloud_settings.is_cloud:
            column = layout.column()
            column.prop(cloud_settings, "detail_bump_strength", text="Bump strength")
            column.prop(cloud_settings, "detail_bump_levels", text="Bump levels")
            column.prop(cloud_settings, "detail_noise", text="Noise")

class OBJECT_PT_cloud_extra(bpy.types.Panel):
    bl_label = "Extra"
    bl_parent_id = "OBJECT_PT_cloud"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "object"
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        layout = self.layout
        layout.use_property_split = True

        obj = context.object
        cloud_settings = obj.cloud_settings
        if obj.cloud_settings.is_cloud:
            column = layout.column()
            column.prop(cloud_settings, "color", text="Color")
            column.prop(cloud_settings, "domain_cloud_position", text="Cloud position")
            column.prop(cloud_settings, "cleaner_domain_size", text="Clean strengh")


class VIEW3D_MT_cloud_add(bpy.types.Menu):
    bl_idname = "VIEW3D_MT_cloud_add"
    bl_label = "Cloud"

    def draw(self, _context):
        layout = self.layout

        layout.operator("object.cloud_add_single_cumulus", text="Simple cumulus", icon="OUTLINER_DATA_VOLUME")
        layout.operator("object.cloud_add_landscape_cumulus", text="Landscape cumulus", icon="MOD_OCEAN")
        layout.operator("object.cloud_add_single_cumulus", text="Cirrus", icon="OUTLINER_DATA_VOLUME")
        layout.operator("object.cloud_add_single_cumulus", text="Cirrocumulus", icon="OUTLINER_DATA_VOLUME")
        layout.operator("object.cloud_add_single_cumulus", text="Stratus", icon="OUTLINER_DATA_VOLUME")


def add_menu_cloud(self, context):
    self.layout.separator()
    self.layout.menu("VIEW3D_MT_cloud_add", text="Cloud", icon="OUTLINER_OB_VOLUME")


def register():
    bpy.utils.register_class(CloudErrorOperator)
    bpy.utils.register_class(CloudSettings)
    bpy.utils.register_class(OBJECT_OT_cloud_single_cumulus) 
    bpy.utils.register_class(OBJECT_OT_cloud_landscape_cumulus)

    bpy.utils.register_class(OBJECT_PT_cloud)
    bpy.utils.register_class(OBJECT_PT_cloud_general)
    bpy.utils.register_class(OBJECT_PT_cloud_shape)
    bpy.utils.register_class(OBJECT_PT_cloud_shape_roundness)
    bpy.utils.register_class(OBJECT_PT_cloud_shape_add_imperfection)
    bpy.utils.register_class(OBJECT_PT_cloud_shape_subtract_imperfection)
    bpy.utils.register_class(OBJECT_PT_cloud_detail)
    bpy.utils.register_class(OBJECT_PT_cloud_extra)

    bpy.utils.register_class(VIEW3D_MT_cloud_add)
    bpy.types.VIEW3D_MT_volume_add.append(add_menu_cloud)
    
    bpy.types.Object.cloud_settings = bpy.props.PointerProperty(type=CloudSettings)

    """
    preview_coll = bpy.utils.previews.new()
    icon_dir = os.path.join(os.path.dirname(__file__), "icons")
    preview_coll.load("mi_icono", os.path.join(icon_dir, "icon.png"), 'IMAGE')
    preview_collections["main"] = preview_coll
    """

def unregister():
    bpy.utils.unregister_class(CloudErrorOperator)
    bpy.utils.unregister_class(CloudSettings)
    bpy.utils.unregister_class(OBJECT_OT_cloud_single_cumulus)
    bpy.utils.unregister_class(OBJECT_OT_cloud_landscape_cumulus)

    bpy.utils.unregister_class(OBJECT_PT_cloud)
    bpy.utils.unregister_class(OBJECT_PT_cloud_general)
    bpy.utils.unregister_class(OBJECT_PT_cloud_shape)
    bpy.utils.unregister_class(OBJECT_PT_cloud_shape_roundness)
    bpy.utils.unregister_class(OBJECT_PT_cloud_shape_add_imperfection)
    bpy.utils.unregister_class(OBJECT_PT_cloud_shape_subtract_imperfection)
    bpy.utils.unregister_class(OBJECT_PT_cloud_detail)
    bpy.utils.unregister_class(OBJECT_PT_cloud_extra)
    
    bpy.utils.unregister_class(VIEW3D_MT_cloud_add)
    bpy.types.VIEW3D_MT_volume_add.remove(add_menu_cloud)

    del bpy.types.Object.cloud_settings




