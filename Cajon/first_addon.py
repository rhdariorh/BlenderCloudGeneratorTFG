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

def update_cloud_size(self, context):
    obj = context.active_object
    domain = obj.cloud_settings.domain
    size = obj.cloud_settings.size
    cube_size = Vector((size.x / domain.x, size.y / domain.y, size.z / domain.z))
    obj.scale = cube_size

def update_cloud_domain(self, context):
    obj = context.active_object
    domain = obj.cloud_settings.domain
    size = obj.cloud_settings.size

    previous_domain = Vector(obj.cloud_settings["auxiliar_domain"].to_list())
    obj.scale = Vector((1.0/previous_domain.x, 1.0/previous_domain.y, 1.0/previous_domain.z))
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True, properties=True)

    obj.scale = domain
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True, properties=True)
    obj.cloud_settings["auxiliar_domain"] = domain

    cube_size = Vector((size.x / domain.x, size.y / domain.y, size.z / domain.z))
    obj.scale = cube_size



class CloudSettings(bpy.types.PropertyGroup):
    is_cloud: bpy.props.BoolProperty(
        name="Is cloud",
        description="Indicates if the object is a cloud",
        default=False
    )

    domain: bpy.props.FloatVectorProperty(
        name="Cloud domain",
        description="Render domain for the cloud object",
        subtype="XYZ",
        default=(4.0, 4.0, 4.0),
        min=0.01,
        update=update_cloud_domain
    )

    size: bpy.props.FloatVectorProperty(
        name="Cloud size",
        description="Size of the cloud object",
        subtype="TRANSLATION",
        default=(30.0, 30.0, 30.0),
        update=update_cloud_size
    )

class OBJECT_OT_cloud(bpy.types.Operator):
    """Add a cumulus cloud"""
    bl_idname = "object.cloud_add"
    bl_label = "Generate cloud"
    bl_options = {"REGISTER", "UNDO"}

    """
    domain: bpy.props.FloatVectorProperty(
        name="Domain size",
        description="Domain size where the cloud is rendered.",
        default=(4.0, 4.0, 4.0),
        min=0
    )

    size: bpy.props.FloatVectorProperty(
        name="Cloud size",
        description="Cloud size regardless of domain.",
        default=(30.0, 30.0, 30.0),
        min=0
    )
    """
    @classmethod
    def poll(cls, context):
        return context.area.type == "VIEW_3D"

    def execute(self, context):
        generate_cloud(context)
        return {'FINISHED'}


class OBJECT_PT_cloud(bpy.types.Panel):
    """Creates a Panel in the scene context of the properties editor"""
    bl_label = "Cloud settings"
    bl_idname = "OBJECT_PT_cloud"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "object"

    def draw(self, context):
        layout = self.layout
        layout.use_property_split = True
        obj = context.object
        cloud_settings = obj.cloud_settings
        if not obj.cloud_settings.is_cloud:
            layout.label(text="The selected object is not a cloud.",
                icon="ERROR")
        else:
            scene = context.scene

            # Create a simple row.

            column = layout.column()
            column.prop(cloud_settings, "size", text="Size")
            column = layout.column()
            column.prop(cloud_settings, "domain", text="Domain")
            """
            layout.use_property_split = False
            # Create an row where the buttons are aligned to each other.
            layout.label(text=" Aligned Row:")

            row = layout.row(align=True)
            row.prop(scene, "frame_start")
            row.prop(scene, "frame_end")

            # Create two columns, by using a split layout.
            split = layout.split()

            # First column
            col = split.column()
            col.label(text="Column One:")
            col.prop(scene, "frame_end")
            col.prop(scene, "frame_start")

            # Second column, aligned
            col = split.column(align=True)
            col.label(text="Column Two:")
            col.prop(scene, "frame_start")
            col.prop(scene, "frame_end")

            # Big render button
            layout.label(text="Big Button:")
            row = layout.row()
            row.scale_y = 3.0
            row.operator("render.render")

            # Different sizes in a row
            layout.label(text="Different button sizes:")
            row = layout.row(align=True)
            row.operator("render.render")

            sub = row.row()
            sub.scale_x = 2.0
            sub.operator("render.render")

            row.operator("render.render")
            """

class VIEW3D_MT_cloud_add(bpy.types.Menu):
    bl_idname = "VIEW3D_MT_cloud_add"
    bl_label = "Cloud"

    def draw(self, _context):
        layout = self.layout

        layout.operator("object.cloud_add", text="Cumulus", icon="OUTLINER_DATA_VOLUME")
        layout.operator("object.cloud_add", text="Cumulunimbus", icon="OUTLINER_DATA_VOLUME")
        layout.operator("object.cloud_add", text="Cirrus", icon="MOD_OCEAN")
        layout.operator("object.cloud_add", text="Cirrocumulus", icon="OUTLINER_DATA_VOLUME")
        layout.operator("object.cloud_add", text="Stratus", icon="OUTLINER_DATA_VOLUME")


def add_menu_cloud(self, context):
    self.layout.separator()
    self.layout.menu("VIEW3D_MT_cloud_add", text="Cloud", icon="OUTLINER_OB_VOLUME")


def register():
    bpy.utils.register_class(CloudSettings)
    bpy.utils.register_class(OBJECT_OT_cloud)
    bpy.utils.register_class(OBJECT_PT_cloud)
    bpy.utils.register_class(VIEW3D_MT_cloud_add)
    bpy.types.VIEW3D_MT_volume_add.append(add_menu_cloud)
    
    bpy.types.Object.cloud_settings = bpy.props.PointerProperty(type=CloudSettings)


def unregister():
    bpy.utils.unregister_class(CloudSettings)
    bpy.utils.unregister_class(OBJECT_OT_cloud)
    bpy.utils.unregister_class(OBJECT_PT_cloud)
    bpy.utils.unregister_class(VIEW3D_MT_cloud_add)
    bpy.types.VIEW3D_MT_volume_add.remove(add_menu_cloud)

    del bpy.types.Object.cloud_settings


def generate_cloud(context):
    C = context
    D = bpy.data
    # ---------------------------------------
    # ------------Initialization-------------
    # ---------------------------------------
    # Create cloud object
    bpy.ops.mesh.primitive_cube_add()
    obj = C.active_object
    obj.name = 'Cloud'
    obj.cloud_settings.is_cloud = True
    domain = obj.cloud_settings.domain
    size = obj.cloud_settings.size

    # Create cloud material
    mat = D.materials.new("CloudMaterial")
    mat.use_nodes = True

    # Cleaning material
    mat_nodes = mat.node_tree.nodes
    for node in mat_nodes:
        mat.node_tree.nodes.remove(node)

    # Assign
    obj.active_material = mat

    # ---------------------------------------
    # ---------Material construction---------
    # ---------------------------------------
    # From final node to beginning

    # Material Output
    material_output = mat_nodes.new("ShaderNodeOutputMaterial")
    material_output.location = (700, 0)
    # Principled Volume
    principled_volume = mat_nodes.new("ShaderNodeVolumePrincipled")
    principled_volume.location = (400, 0)
    principled_volume.inputs["Color"].default_value = (1, 1, 1, 1)

    # Connection between Principled Volume and Material Output.
    mat.node_tree.links.new(principled_volume.outputs["Volume"],
                            material_output.inputs["Volume"])

    # Final density Color Ramp
    density_color_ramp = mat_nodes.new("ShaderNodeValToRGB")
    density_color_ramp.location = (100, 0)
    elem = density_color_ramp.color_ramp.elements[0]
    elem.position = 0.3
    elem.color = (0, 0, 0, 1)
    elem = density_color_ramp.color_ramp.elements[1]
    elem.position = 0.4
    elem.color = (2.163, 2.163, 2.163, 1)  # HSV -> V = 1.4

    mat.node_tree.links.new(density_color_ramp.outputs["Color"],
                            principled_volume.inputs["Density"])

    # Gradient Texture
    gradient_texture = mat_nodes.new("ShaderNodeTexGradient")
    gradient_texture.location = (-100, 0)
    gradient_texture.gradient_type = "SPHERICAL"

    mat.node_tree.links.new(gradient_texture.outputs["Color"],
                            density_color_ramp.inputs["Fac"])

    # Overlay Curve and Noises
    overlay_curve_noises = mat_nodes.new("ShaderNodeMixRGB")
    overlay_curve_noises.location = (-300, 0)
    overlay_curve_noises.blend_type = "OVERLAY"
    overlay_curve_noises.inputs["Fac"].default_value = 0.23

    mat.node_tree.links.new(overlay_curve_noises.outputs["Color"],
                            gradient_texture.inputs["Vector"])

    # Color Ramp noises
    noise_color_ramp = mat_nodes.new("ShaderNodeValToRGB")
    noise_color_ramp.location = (-600, -200)
    elem = noise_color_ramp.color_ramp.elements[0]
    elem.position = 0.3
    elem.color = (0, 0, 0, 1)
    elem = noise_color_ramp.color_ramp.elements[1]
    elem.position = 1.0
    elem.color = (1, 1, 1, 1)

    mat.node_tree.links.new(noise_color_ramp.outputs["Color"],
                            overlay_curve_noises.inputs["Color2"])

    # Vector curves
    vector_curves = mat_nodes.new("ShaderNodeVectorCurve")
    vector_curves.location = (-600, 300)
    vector_curves.mapping.curves[2].points[0].location = (-0.77, -1.0)
    vector_curves.mapping.curves[2].points.new(-0.12, 0.55)
    vector_curves.mapping.curves[2].points.new(0.55, 0.8)

    mat.node_tree.links.new(vector_curves.outputs["Vector"],
                            overlay_curve_noises.inputs["Color1"])

    # Mapping
    mapping = mat_nodes.new("ShaderNodeMapping")
    mapping.location = (-800, 300)
    mapping.inputs["Location"].default_value = (0.0, 0.0, -0.3)
    mapping.inputs["Scale"].default_value = (0.7, 0.6, 1.0)

    mat.node_tree.links.new(mapping.outputs["Vector"],
                            vector_curves.inputs["Vector"])

    # Overlay Voronoi and Noise Texture
    overlay_voronoi_noise = mat_nodes.new("ShaderNodeMixRGB")
    overlay_voronoi_noise.location = (-800, -350)
    overlay_voronoi_noise.blend_type = "OVERLAY"
    overlay_voronoi_noise.inputs["Fac"].default_value = 1.0

    mat.node_tree.links.new(overlay_voronoi_noise.outputs["Color"],
                            noise_color_ramp.inputs["Fac"])

    # Voronoi noise
    voronoi = mat_nodes.new("ShaderNodeTexVoronoi")
    voronoi.location = (-1000, -250)
    voronoi.inputs["Scale"].default_value = 2.0

    mat.node_tree.links.new(voronoi.outputs["Distance"],
                            overlay_voronoi_noise.inputs["Color1"])

    # Noise
    noise_tex = mat_nodes.new("ShaderNodeTexNoise")
    noise_tex.location = (-1000, -500)
    noise_tex.inputs["Distortion"].default_value = 0.2

    mat.node_tree.links.new(noise_tex.outputs["Fac"],
                            overlay_voronoi_noise.inputs["Color2"])

    # Texture Coordinate
    texture_coordinate = mat_nodes.new("ShaderNodeTexCoord")
    texture_coordinate.location = (-1300, 0)

    mat.node_tree.links.new(texture_coordinate.outputs["Object"],
                            mapping.inputs["Vector"])
    mat.node_tree.links.new(texture_coordinate.outputs["Object"],
                            voronoi.inputs["Vector"])
    mat.node_tree.links.new(texture_coordinate.outputs["Object"],
                            noise_tex.inputs["Vector"])

    # ---------------------------------------
    # --------Domain and size config---------
    # ---------------------------------------
    obj.cloud_settings["auxiliar_domain"] = domain
    obj.scale = (0.5, 0.5, 0.5) # Default cube is 2 meters
    C.view_layer.objects.active = obj
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True, properties=True)
    obj.scale = domain
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True, properties=True)
    cube_size = Vector((size.x / domain.x, size.y / domain.y, size.z / domain.z))
    obj.scale = cube_size


