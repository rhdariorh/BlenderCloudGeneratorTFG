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


def update_cloud_dimensions(self, context):
    obj = context.active_object
    domain = obj.cloud_settings.domain
    size = obj.cloud_settings.size
    min_size = min(size.x, size.y, size.z)

    # Restablecer dominio
    previous_domain = Vector(obj.cloud_settings["auxiliar_domain_vector"].to_list())
    obj.scale = Vector((1.0/previous_domain.x, 1.0/previous_domain.y, 1.0/previous_domain.z))
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True, properties=True)

    # Nuevo dominio
    adapted_domain = Vector((size.x/domain, size.y/domain, size.z/domain))
    obj.scale = (adapted_domain.x, adapted_domain.y, adapted_domain.z)
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True, properties=True)
    obj.cloud_settings["auxiliar_domain_vector"] = adapted_domain

    cube_size = Vector((size.x / adapted_domain.x, size.y / adapted_domain.y, size.z / adapted_domain.z))
    obj.scale = cube_size


def update_cloud_density(self, context):
    obj = context.active_object
    density = obj.cloud_settings.density
    material = bpy.context.active_object.active_material
    if "CloudMaterial_CG" not in material.name:
        bpy.ops.error.cloud_error("INVOKE_DEFAULT", error_type="MATERIAL_WRONG_NAME")
    else:
        density_color_ramp = material.node_tree.nodes.get("Cloud Density ColorRamp")
        elem = density_color_ramp.color_ramp.elements[1]
        elem.color = (density, density, density, 1)

class CloudSettings(bpy.types.PropertyGroup):
    is_cloud: bpy.props.BoolProperty(
        name="Is cloud",
        description="Indicates if the object is a cloud",
        default=False
    )

    domain: bpy.props.FloatProperty(
        name="Cloud domain",
        description="Render domain size for the cloud object",
        default=4,
        min=0.01,
        update=update_cloud_dimensions
    )

    size: bpy.props.FloatVectorProperty(
        name="Cloud size",
        description="Size of the cloud object",
        subtype="TRANSLATION",
        default=(20.0, 20.0, 20.0),
        update=update_cloud_dimensions
    )

    density: bpy.props.FloatProperty(
        name="Cloud density",
        description="Amount of light absorbed by the cloud",
        default=1.4,
        min=0.0,
        soft_max=5.0,
        update=update_cloud_density
    )

class OBJECT_OT_cloud(bpy.types.Operator):
    """Add a cumulus cloud"""
    bl_idname = "object.cloud_add"
    bl_label = "Generate cloud"
    bl_options = {"REGISTER", "UNDO"}

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
            column = layout.column()
            column.prop(cloud_settings, "density", text="Density")


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
    bpy.utils.register_class(CloudErrorOperator)
    bpy.utils.register_class(CloudSettings)
    bpy.utils.register_class(OBJECT_OT_cloud)
    bpy.utils.register_class(OBJECT_PT_cloud)
    bpy.utils.register_class(VIEW3D_MT_cloud_add)
    bpy.types.VIEW3D_MT_volume_add.append(add_menu_cloud)
    
    bpy.types.Object.cloud_settings = bpy.props.PointerProperty(type=CloudSettings)


def unregister():
    bpy.utils.unregister_class(CloudErrorOperator)
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
    mat = D.materials.new("CloudMaterial_CG")
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
    material_output.name = "Cloud Output"
    material_output.location = (700, 0)
    # Principled Volume
    principled_volume = mat_nodes.new("ShaderNodeVolumePrincipled")
    principled_volume.name = "Cloud Principled Volume"
    principled_volume.location = (400, 0)
    principled_volume.inputs["Color"].default_value = (1, 1, 1, 1)

    # Connection between Principled Volume and Material Output.
    mat.node_tree.links.new(principled_volume.outputs["Volume"],
                            material_output.inputs["Volume"])

    # Final density Color Ramp
    density_color_ramp = mat_nodes.new("ShaderNodeValToRGB")
    density_color_ramp.name = "Cloud Density ColorRamp"
    density_color_ramp.location = (100, 0)
    elem = density_color_ramp.color_ramp.elements[0]
    elem.position = 0.3
    elem.color = (0, 0, 0, 1)
    elem = density_color_ramp.color_ramp.elements[1]
    elem.position = 0.4
    elem.color = (2.0, 2.0, 2.0, 1)

    mat.node_tree.links.new(density_color_ramp.outputs["Color"],
                            principled_volume.inputs["Density"])

    # Gradient Texture
    gradient_texture = mat_nodes.new("ShaderNodeTexGradient")
    gradient_texture.name = "Cloud Gradient Texture"
    gradient_texture.location = (-100, 0)
    gradient_texture.gradient_type = "SPHERICAL"

    mat.node_tree.links.new(gradient_texture.outputs["Color"],
                            density_color_ramp.inputs["Fac"])

    # Overlay Curve and Noises
    overlay_curve_noises = mat_nodes.new("ShaderNodeMixRGB")
    overlay_curve_noises.name = "Cloud Overlay Curve and Noises"
    overlay_curve_noises.location = (-300, 0)
    overlay_curve_noises.blend_type = "OVERLAY"
    overlay_curve_noises.inputs["Fac"].default_value = 0.23

    mat.node_tree.links.new(overlay_curve_noises.outputs["Color"],
                            gradient_texture.inputs["Vector"])

    # Color Ramp noises
    noise_color_ramp = mat_nodes.new("ShaderNodeValToRGB")
    noise_color_ramp.name = "Cloud Noise ColorRamp"
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
    vector_curves.name = "Cloud Vector Curves"
    vector_curves.location = (-600, 300)
    vector_curves.mapping.curves[2].points[0].location = (-0.77, -1.0)
    vector_curves.mapping.curves[2].points.new(-0.12, 0.55)
    vector_curves.mapping.curves[2].points.new(0.55, 0.8)

    mat.node_tree.links.new(vector_curves.outputs["Vector"],
                            overlay_curve_noises.inputs["Color1"])

    # Mapping
    mapping = mat_nodes.new("ShaderNodeMapping")
    mapping.name = "Cloud Mapping"
    mapping.location = (-800, 300)
    mapping.inputs["Location"].default_value = (0.0, 0.0, -0.3)
    mapping.inputs["Scale"].default_value = (0.7, 0.6, 1.0)

    mat.node_tree.links.new(mapping.outputs["Vector"],
                            vector_curves.inputs["Vector"])

    # Overlay Voronoi and Noise Texture
    overlay_voronoi_noise = mat_nodes.new("ShaderNodeMixRGB")
    overlay_voronoi_noise.name = "Cloud Overlay Voronoi and Noise"
    overlay_voronoi_noise.location = (-800, -350)
    overlay_voronoi_noise.blend_type = "OVERLAY"
    overlay_voronoi_noise.inputs["Fac"].default_value = 1.0

    mat.node_tree.links.new(overlay_voronoi_noise.outputs["Color"],
                            noise_color_ramp.inputs["Fac"])

    # Voronoi noise
    voronoi = mat_nodes.new("ShaderNodeTexVoronoi")
    voronoi.name = "Cloud Voronoi Level 1"
    voronoi.location = (-1000, -250)
    voronoi.inputs["Scale"].default_value = 2.0

    mat.node_tree.links.new(voronoi.outputs["Distance"],
                            overlay_voronoi_noise.inputs["Color1"])

    # Noise
    noise_tex = mat_nodes.new("ShaderNodeTexNoise")
    noise_tex.name = "Cloud Noise Texture"
    noise_tex.location = (-1000, -500)
    noise_tex.inputs["Distortion"].default_value = 0.2

    mat.node_tree.links.new(noise_tex.outputs["Fac"],
                            overlay_voronoi_noise.inputs["Color2"])

    # Texture Coordinate
    texture_coordinate = mat_nodes.new("ShaderNodeTexCoord")
    texture_coordinate.name = "Cloud Texture Coordinate"
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
    obj.scale = (0.5, 0.5, 0.5) # Default cube is 2 meters
    C.view_layer.objects.active = obj
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True, properties=True)

    adapted_domain = Vector((size.x/domain, size.y/domain, size.z/domain))
    obj.scale = (adapted_domain.x, adapted_domain.y, adapted_domain.z)
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True, properties=True)
    obj.cloud_settings["auxiliar_domain_vector"] = adapted_domain

    cube_size = Vector((size.x / adapted_domain.x, size.y / adapted_domain.y, size.z / adapted_domain.z))
    obj.scale = cube_size



