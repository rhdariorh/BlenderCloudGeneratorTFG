"""
    __init__.py is part of Cloud Generator Blender Addon.

    Foobar is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    any later version.

    Foobar is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with Foobar.  If not, see <https://www.gnu.org/licenses/>.
"""
import bpy
from mathutils import Vector
import bpy.utils.previews

from . import materials
from .cloud_settings import CloudSettings
from .materials import initial_shape_single_cumulus, initial_shape_cloudscape_cumulus, initial_shape_cloudscape_cirrus

bl_info = {
    "name": "Clouds generator",
    "author": "Darío R.H. <rhdariorh@gmail.com>",
    "version": (2021, 1, 0),
    "blender": (2, 83, 1),
    "category": "Object",
    "location": "View 3D > Add > Volume",
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
        column = layout.column_flow(columns=2, align=True)
        column.operator("render.cloud_edit_settings", text="Set edition settings")
        column.operator("render.cloud_render_settings", text="Set render settings")


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


class RENDER_OT_cloud_edit_settings(bpy.types.Operator):
    """Operator that sets the Blender settings for a more comfortable and faster cloud editing"""

    bl_idname = "render.cloud_edit_settings"
    bl_label = "Set settings to cloud edit mode"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        context.scene.eevee.volumetric_tile_size = '8'
        context.scene.eevee.volumetric_samples = 64
        context.scene.eevee.use_volumetric_lights = True
        context.scene.eevee.use_volumetric_shadows = True
        context.scene.eevee.volumetric_end = 200.0
        self.report({'INFO'}, "Blender settings adapted for editing atmospheric clouds.")
        return {'FINISHED'}


class RENDER_OT_cloud_render_settings(bpy.types.Operator):
    """Operator that sets the optimal Blender settings for rendering clouds"""

    bl_idname = "render.cloud_render_settings"
    bl_label = "Set settings to render clouds"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        context.scene.eevee.volumetric_tile_size = '2'
        context.scene.eevee.volumetric_samples = 64
        context.scene.eevee.use_volumetric_lights = True
        context.scene.eevee.use_volumetric_shadows = True
        context.scene.eevee.volumetric_end = 500.0
        self.report({'INFO'}, "Blender settings adapted for rendering clouds.")
        return {'FINISHED'}


class OBJECT_OT_cloud_single_cumulus(bpy.types.Operator):
    """Operator that generates and add a single cumulus cloud to the scene"""

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
    """Operator that generates and add a cumulus cloudscape to the scene"""

    bl_idname = "object.cloud_add_cloudscape_cumulus"
    bl_label = "Generate cumulus cloudscape"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        return context.area.type == "VIEW_3D"

    def execute(self, context):
        materials.generate_cloud(context, -1000, 0, initial_shape_cloudscape_cumulus)
        return {'FINISHED'}


class OBJECT_OT_cloud_cloudscape_cirrus(bpy.types.Operator):
    """Operator that generates and add a cirrus cloudscape to the scene"""

    bl_idname = "object.cloud_add_cloudscape_cirrus"
    bl_label = "Generate cirrus cloudscape"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        return context.area.type == "VIEW_3D"

    def execute(self, context):
        materials.generate_cloud(context, -1000, 0, initial_shape_cloudscape_cirrus)
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
            column.prop(cloud_settings, "color", text="Color")
            if cloud_settings.cloud_type == "CLOUDSCAPE_CUMULUS":
                column.prop(cloud_settings, "amount_of_clouds", text="Amount of clouds")
                column.prop(cloud_settings, "cloudscape_cloud_size", text="Clouds size")
                if (context.preferences.addons[__name__].preferences.advanced_settings):
                    column.prop(cloud_settings, "cloudscape_noise_coords", text="Seed")
                else:
                    column.prop(cloud_settings, "cloudscape_noise_simple_seed", text="Seed")


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
            elif(cloud_settings.cloud_type in ["CLOUDSCAPE_CUMULUS", "CLOUDSCAPE_CIRRUS"]):
                column.prop(cloud_settings, "height_cloudscape", text="Height")

                if cloud_settings.cloud_type == "CLOUDSCAPE_CUMULUS":
                    column.prop(cloud_settings, "bottom_softness_cloudscape", text="Bottom softness")
                    column.prop(cloud_settings, "top_softness_cloudscape", text="Top softness")

                if cloud_settings.cloud_type == "CLOUDSCAPE_CIRRUS":
                    column.prop(cloud_settings, "cloudscape_cirrus_cirrus_amount", text="Amount of cirrus")
                    column.prop(cloud_settings, "cloudscape_cirrus_cirrus_width", text="Cirrus width")

                column.prop(cloud_settings, "use_shape_texture", text="Use shape texture")
                if cloud_settings.use_shape_texture:
                    column.template_ID(cloud_settings, "shape_texture_image", new="image.new", open="image.open")


class OBJECT_PT_cloud_shape_wind(bpy.types.Panel):
    """Creates a subpanel within shape panel to modify wind properties."""

    bl_label = "Wind"
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
            column.prop(cloud_settings, "wind_strength", text="Strength")
            column.prop(cloud_settings, "wind_big_turbulence", text="Big turbulence")
            if (context.preferences.addons[__name__].preferences.advanced_settings):
                column.prop(cloud_settings, "wind_big_turbulence_coords", text="Big turbulence seed")
            column.prop(cloud_settings, "wind_small_turbulence", text="Small turbulence")
            if (context.preferences.addons[__name__].preferences.advanced_settings):
                column.prop(cloud_settings, "wind_small_turbulence_coords", text="Small turbulence seed")
            if not context.preferences.addons[__name__].preferences.advanced_settings:
                column.prop(cloud_settings, "wind_turbulence_simple_seed", text="Seed")


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
            column.prop(cloud_settings, "detail_wind_strength", text="Wind strength")


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
        layout.operator("object.cloud_add_cloudscape_cumulus", text="Cumulus cloudscape", icon="OUTLINER_DATA_VOLUME")
        layout.operator("object.cloud_add_cloudscape_cirrus", text="Cirrus cloudscape", icon="MOD_OCEAN")


def add_menu_cloud(self, context):
    """Adds a submenu Cloud"""

    self.layout.separator()
    self.layout.menu("VIEW3D_MT_cloud_add", text="Cloud", icon="OUTLINER_OB_VOLUME")


def register():
    """Register classes and do other necessary tasks when registering the Addon."""

    bpy.utils.register_class(CloudErrorOperator)
    bpy.utils.register_class(CloudGeneratorPreferences)
    bpy.utils.register_class(RENDER_OT_cloud_edit_settings)
    bpy.utils.register_class(RENDER_OT_cloud_render_settings)
    bpy.utils.register_class(CloudSettings)
    bpy.utils.register_class(OBJECT_OT_cloud_single_cumulus)
    bpy.utils.register_class(OBJECT_OT_cloud_cloudscape_cumulus)
    bpy.utils.register_class(OBJECT_OT_cloud_cloudscape_cirrus)

    bpy.utils.register_class(OBJECT_PT_cloud)
    bpy.utils.register_class(OBJECT_PT_cloud_general)
    bpy.utils.register_class(OBJECT_PT_cloud_shape)
    bpy.utils.register_class(OBJECT_PT_cloud_shape_wind)
    bpy.utils.register_class(OBJECT_PT_cloud_shape_roundness)
    bpy.utils.register_class(OBJECT_PT_cloud_shape_add_imperfection)
    bpy.utils.register_class(OBJECT_PT_cloud_shape_subtract_imperfection)
    bpy.utils.register_class(OBJECT_PT_cloud_detail)
    bpy.utils.register_class(OBJECT_PT_cloud_extra)

    bpy.utils.register_class(VIEW3D_MT_cloud_add)
    bpy.types.VIEW3D_MT_volume_add.append(add_menu_cloud)

    bpy.types.Object.cloud_settings = bpy.props.PointerProperty(type=CloudSettings)

    print("\n_____________________________________________________\n")
    print("Cloud Generator is a free and open source Add-on following the GNU General Public License.\n")
    print("If you are an addon developer and you can afford to create GNU-GPL addons, do so " +
          "(if you want). Blender has given you a lot for free, give a little bit back " +
          "to the community. :)")
    print("\nDario R.H.")
    print("_____________________________________________________\n")

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
    bpy.utils.unregister_class(RENDER_OT_cloud_edit_settings)
    bpy.utils.unregister_class(RENDER_OT_cloud_render_settings)
    bpy.utils.unregister_class(CloudSettings)
    bpy.utils.unregister_class(OBJECT_OT_cloud_single_cumulus)
    bpy.utils.unregister_class(OBJECT_OT_cloud_cloudscape_cumulus)
    bpy.utils.unregister_class(OBJECT_OT_cloud_cloudscape_cirrus)

    bpy.utils.unregister_class(OBJECT_PT_cloud)
    bpy.utils.unregister_class(OBJECT_PT_cloud_general)
    bpy.utils.unregister_class(OBJECT_PT_cloud_shape)
    bpy.utils.unregister_class(OBJECT_PT_cloud_shape_wind)
    bpy.utils.unregister_class(OBJECT_PT_cloud_shape_roundness)
    bpy.utils.unregister_class(OBJECT_PT_cloud_shape_add_imperfection)
    bpy.utils.unregister_class(OBJECT_PT_cloud_shape_subtract_imperfection)
    bpy.utils.unregister_class(OBJECT_PT_cloud_detail)
    bpy.utils.unregister_class(OBJECT_PT_cloud_extra)

    bpy.utils.unregister_class(VIEW3D_MT_cloud_add)
    bpy.types.VIEW3D_MT_volume_add.remove(add_menu_cloud)

    del bpy.types.Object.cloud_settings
