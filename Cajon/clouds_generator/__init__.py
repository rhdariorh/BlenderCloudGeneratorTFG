import bpy
from mathutils import Vector
import bpy.utils.previews

from . import materials
from .cloud_settings import CloudSettings
from .materials import initial_shape_single_cumulus, initial_shape_cloudscape_cumulus

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


class CloudGeneratorPreferences(bpy.types.AddonPreferences):
    """Addon preferences panel."""
    bl_idname = __name__

    advanced_settings: bpy.props.BoolProperty(
        name="Advanced settings",
        description="Add more control over the shape of the clouds",
        default=False,
    )

    def draw(self, context):
        layout = self.layout
        layout.prop(self, "advanced_settings")


class CloudErrorOperator(bpy.types.Operator):
    """Operator that throws custom errors for clouds.

    Attributes:
        error_type: Name of the error to be executed.
    """

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
    """Operator that generates and add a single cumulus cloud to the scene."""

    bl_idname = "object.cloud_add_single_cumulus"
    bl_label = "Generate single cumulus"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        return context.area.type == "VIEW_3D"

    def execute(self, context):
        materials.generate_cloud(context, -1000, 0, initial_shape_single_cumulus)
        return {'FINISHED'}


class OBJECT_OT_cloud_cloudscape_cumulus(bpy.types.Operator):
    """Operator that generates and add a cumulus cloudscape to the scene."""

    bl_idname = "object.cloud_add_cloudscape_cumulus"
    bl_label = "Generate cumulus cloudscape"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        return context.area.type == "VIEW_3D"

    def execute(self, context):
        materials.generate_cloud(context, -1000, 0, initial_shape_cloudscape_cumulus)
        return {'FINISHED'}


class OBJECT_PT_cloud(bpy.types.Panel):
    """Creates a Panel in the scene context of the properties editor.

    It allows the user to modify the different properties of the clouds
    from the Blender inerface. Inside contains some properties to modify
    and subpanels. Only displayed for cloud objects.
    """
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
    """Creates a subpanel within cloud panel to modify general properties
    of the cloud."""

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

            if cloud_settings.cloud_type == "CLOUDSCAPE_CUMULUS":
                column.prop(cloud_settings, "amount_of_clouds", text="Amount of clouds")
                column.prop(cloud_settings, "cloudscape_cloud_size", text="Clouds size")
                if (context.preferences.addons[__name__].preferences.advanced_settings):
                    column.prop(cloud_settings, "cloudscape_noise_coords", text="Seed")
                else:
                    column.prop(cloud_settings, "cloudscape_noise_simple_seed", text="Seed")


class OBJECT_PT_cloud_general_wind(bpy.types.Panel):
    """Creates a subpanel within general panel to modify wind properties."""

    bl_label = "Wind"
    bl_parent_id = "OBJECT_PT_cloud_general"
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
            column.prop(cloud_settings, "wind_strength", text="Strength")
            column.prop(cloud_settings, "wind_big_turbulence", text="Big size turbulence")
            column.prop(cloud_settings, "wind_small_turbulence", text="Small size turbulence")
            # FALTA AÑADIR SEED DEL VIENTOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO


class OBJECT_PT_cloud_shape(bpy.types.Panel):
    """Creates a subpanel within cloud panel to modify shape
    properties of the cloud.
    """

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
            elif(cloud_settings.cloud_type == "CLOUDSCAPE_CUMULUS"):
                column.prop(cloud_settings, "height_cloudscape", text="Height")
                column.prop(cloud_settings, "use_shape_texture", text="Use shape texture")
                if cloud_settings.use_shape_texture:
                    column.template_ID(cloud_settings, "shape_texture_image", new="image.new", open="image.open")


class OBJECT_PT_cloud_shape_roundness(bpy.types.Panel):
    """Creates a subpanel within shape panel to modify roundness
    properties of the cloud.
    """

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
            if (context.preferences.addons[__name__].preferences.advanced_settings):
                column.prop(cloud_settings, "roundness_coords", text="Seed")
            else:
                column.prop(cloud_settings, "roundness_simple_seed", text="Seed")


class OBJECT_PT_cloud_shape_add_imperfection(bpy.types.Panel):
    """Creates a subpanel within shape panel to modify the addition
    of imperfection properties of the cloud.
    """

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
            if (context.preferences.addons[__name__].preferences.advanced_settings):
                column.prop(cloud_settings, "add_shape_imperfection_coords", text="Seed")
            else:
                column.prop(cloud_settings, "add_shape_imperfection_simple_seed", text="Seed")


class OBJECT_PT_cloud_shape_subtract_imperfection(bpy.types.Panel):
    """Creates a subpanel within shape panel to modify the subtraction
    of imperfection properties of the cloud.
    """

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
            if (context.preferences.addons[__name__].preferences.advanced_settings):
                column.prop(cloud_settings, "subtract_shape_imperfection_coords", text="Seed")
            else:
                column.prop(cloud_settings, "subtract_shape_imperfection_simple_seed", text="Seed")


class OBJECT_PT_cloud_detail(bpy.types.Panel):
    """Creates a subpanel within cloud panel to modify detail shapes
    properties of the cloud.
    """

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
    """Creates a subpanel within cloud panel to modify extra
    properties of the cloud.

    The properties displayed in this panel do not fit in the rest
    ot the panels.
    """
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
    """Add operator buttons in the 'View 3D -> add -> Volume' menu.

    Allows the user to add any type of cloud in a direct way.
    """
    bl_idname = "VIEW3D_MT_cloud_add"
    bl_label = "Cloud"

    def draw(self, _context):
        layout = self.layout

        layout.operator("object.cloud_add_single_cumulus", text="Simple cumulus", icon="OUTLINER_DATA_VOLUME")
        layout.operator("object.cloud_add_cloudscape_cumulus", text="Cumulus cloudscape", icon="MOD_OCEAN")
        layout.operator("object.cloud_add_single_cumulus", text="Cirrus", icon="OUTLINER_DATA_VOLUME")
        layout.operator("object.cloud_add_single_cumulus", text="Cirrocumulus", icon="OUTLINER_DATA_VOLUME")
        layout.operator("object.cloud_add_single_cumulus", text="Stratus", icon="OUTLINER_DATA_VOLUME")


def add_menu_cloud(self, context):
    """Adds a submenu Cloud"""
    self.layout.separator()
    self.layout.menu("VIEW3D_MT_cloud_add", text="Cloud", icon="OUTLINER_OB_VOLUME")


def register():
    """Register classes and do other necessary tasks when registering the Addon."""
    bpy.utils.register_class(CloudErrorOperator)
    bpy.utils.register_class(CloudGeneratorPreferences)
    bpy.utils.register_class(CloudSettings)
    bpy.utils.register_class(OBJECT_OT_cloud_single_cumulus)
    bpy.utils.register_class(OBJECT_OT_cloud_cloudscape_cumulus)

    bpy.utils.register_class(OBJECT_PT_cloud)
    bpy.utils.register_class(OBJECT_PT_cloud_general)
    bpy.utils.register_class(OBJECT_PT_cloud_general_wind)
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
    """Unregister classes and do other necessary tasks when unregistering
    the Addon.
    """
    bpy.utils.unregister_class(CloudErrorOperator)
    bpy.utils.unregister_class(CloudGeneratorPreferences)
    bpy.utils.unregister_class(CloudSettings)
    bpy.utils.unregister_class(OBJECT_OT_cloud_single_cumulus)
    bpy.utils.unregister_class(OBJECT_OT_cloud_cloudscape_cumulus)

    bpy.utils.unregister_class(OBJECT_PT_cloud)
    bpy.utils.unregister_class(OBJECT_PT_cloud_general)
    bpy.utils.unregister_class(OBJECT_PT_cloud_general_wind)
    bpy.utils.unregister_class(OBJECT_PT_cloud_shape)
    bpy.utils.unregister_class(OBJECT_PT_cloud_shape_roundness)
    bpy.utils.unregister_class(OBJECT_PT_cloud_shape_add_imperfection)
    bpy.utils.unregister_class(OBJECT_PT_cloud_shape_subtract_imperfection)
    bpy.utils.unregister_class(OBJECT_PT_cloud_detail)
    bpy.utils.unregister_class(OBJECT_PT_cloud_extra)

    bpy.utils.unregister_class(VIEW3D_MT_cloud_add)
    bpy.types.VIEW3D_MT_volume_add.remove(add_menu_cloud)

    del bpy.types.Object.cloud_settings
