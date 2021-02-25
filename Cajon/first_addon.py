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
    size = obj.cloud_settings.size
    domain = obj.cloud_settings.domain

    # Restablecer dominio
    previous_size = Vector(obj.cloud_settings["auxiliar_size_vector"].to_list())
    obj.scale = Vector((1.0/previous_size.x, 1.0/previous_size.y, 1.0/previous_size.z))
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True, properties=True)

    # Nuevo dominio
    adapted_size = Vector((domain.x/size, domain.y/size, domain.z/size))
    obj.scale = (adapted_size.x, adapted_size.y, adapted_size.z)
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True, properties=True)
    obj.cloud_settings["auxiliar_size_vector"] = adapted_size

    cube_size = Vector((domain.x / adapted_size.x, domain.y / adapted_size.y, domain.z / adapted_size.z))
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

    size: bpy.props.FloatProperty(
        name="Cloud size",
        description="Size of the cloud",
        default=4,
        min=0.01,
        update=update_cloud_dimensions
    )

    domain: bpy.props.FloatVectorProperty(
        name="Cloud domain size",
        description="Size of the cloud object, therefore the rendering domain",
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
            column.prop(cloud_settings, "density", text="Density")
            column = layout.column()
            column.prop(cloud_settings, "size", text="Size")
            column = layout.column()
            column.prop(cloud_settings, "domain", text="Domain")


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

    # -----------------------------------------------
    # -------------Material construction-------------
    # -----------------------------------------------
    # From final node to beginning

    # Reroutes
    reroute_1 = mat_nodes.new(type='NodeReroute')
    reroute_1.location = (-4050, -1500)

    reroute_2 = mat_nodes.new(type='NodeReroute')
    reroute_2.location = (-4050, -2300)

    reroute_3 = mat_nodes.new(type='NodeReroute')
    reroute_3.location = (-3050, -2300)

    reroute_4 = mat_nodes.new(type='NodeReroute')
    reroute_4.location = (-1550, -2300)

    # -------------BEGINNING MAIN BRANCH-------------
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
    color_ramp_density = mat_nodes.new("ShaderNodeValToRGB")
    color_ramp_density.name = "ColorRamp - Cloud Density"
    color_ramp_density.label = "ColorRamp - Cloud Density"
    color_ramp_density.location = (100, 0)
    color_ramp_density.color_ramp.interpolation = 'CONSTANT'
    elem = color_ramp_density.color_ramp.elements[0]
    elem.position = 0.2
    elem.color = (0, 0, 0, 1)
    elem = color_ramp_density.color_ramp.elements[1]
    elem.position = 0.3
    elem.color = (2.0, 2.0, 2.0, 1)

    mat.node_tree.links.new(color_ramp_density.outputs["Color"],
                            principled_volume.inputs["Density"])

    # RGB Subtract - Final Cleaner
    subtract_final_cleaner = mat_nodes.new("ShaderNodeMixRGB")
    subtract_final_cleaner.name = "RGB Subtract - Final Cleaner"
    subtract_final_cleaner.label = "RGB Subtract - Final Cleaner"
    subtract_final_cleaner.location = (-100, 0)
    subtract_final_cleaner.blend_type = "SUBTRACT"
    subtract_final_cleaner.inputs["Fac"].default_value = 1.0

    mat.node_tree.links.new(subtract_final_cleaner.outputs["Color"],
                            color_ramp_density.inputs["Fac"])

    # RGB Overlay - Detail noise
    overlay_detail_noise = mat_nodes.new("ShaderNodeMixRGB")
    overlay_detail_noise.name = "RGB Overlay - Noise"
    overlay_detail_noise.label = "RGB Overlay - Noise"
    overlay_detail_noise.location = (-1300, 0)
    overlay_detail_noise.blend_type = "OVERLAY"
    overlay_detail_noise.inputs["Fac"].default_value = 0.2

    mat.node_tree.links.new(overlay_detail_noise.outputs["Color"],
                            subtract_final_cleaner.inputs["Color1"])

    # RGB Multiply - Bump
    multiply_bump = mat_nodes.new("ShaderNodeMixRGB")
    multiply_bump.name = "RGB Multiply - Bump"
    multiply_bump.label = "RGB Multiply - Bump"
    multiply_bump.location = (-1500, 0)
    multiply_bump.blend_type = "MULTIPLY"
    multiply_bump.inputs["Fac"].default_value = 0.3

    mat.node_tree.links.new(multiply_bump.outputs["Color"],
                            overlay_detail_noise.inputs["Color1"])

    # Vector Multiply - Simple cleaner
    multiply_cleaner = mat_nodes.new("ShaderNodeVectorMath")
    multiply_cleaner.location = (-2200, 0)
    multiply_cleaner.name = "Vector Multiply - Simple cleaner"
    multiply_cleaner.label = "Vector Multiply - Simple cleaner"
    multiply_cleaner.operation = "MULTIPLY"

    mat.node_tree.links.new(multiply_cleaner.outputs["Vector"],
                            multiply_bump.inputs["Color1"])

    # BEGINNING SIMPLE CLEANER FRAME
    frame = mat_nodes.new(type='NodeFrame')
    frame.name = "Not Visible To 0"
    frame.label = "If not visible then 0"

    # Greater Than
    length_greater_than = mat_nodes.new("ShaderNodeMath")
    length_greater_than.parent = frame
    length_greater_than.location = (-2400, -200)
    length_greater_than.operation = "GREATER_THAN"
    length_greater_than.inputs[1].default_value = 0.520

    mat.node_tree.links.new(length_greater_than.outputs["Value"],
                            multiply_cleaner.inputs[1])
    # Vector Length
    lenght = mat_nodes.new("ShaderNodeVectorMath")
    lenght.parent = frame
    lenght.location = (-2600, -200)
    lenght.operation = "LENGTH"

    mat.node_tree.links.new(lenght.outputs["Value"],
                            length_greater_than.inputs["Value"])

    # END SIMPLE CLEANER FRAME

    # RGB Subtract - Big imperfection
    subtract_imperfection = mat_nodes.new("ShaderNodeMixRGB")
    subtract_imperfection.name = "RGB Subtract - Big imperfection"
    subtract_imperfection.label = "RGB Subtract - Big imperfection"
    subtract_imperfection.location = (-2800, 0)
    subtract_imperfection.blend_type = "SUBTRACT"
    subtract_imperfection.inputs["Fac"].default_value = 0.2

    mat.node_tree.links.new(subtract_imperfection.outputs["Color"],
                            lenght.inputs[0])
    mat.node_tree.links.new(subtract_imperfection.outputs["Color"],
                            multiply_cleaner.inputs[0])

    # RGB Add - Big imperfection
    add_imperfection = mat_nodes.new("ShaderNodeMixRGB")
    add_imperfection.name = "RGB Add - Big imperfection"
    add_imperfection.label = "RGB Add - Big imperfection"
    add_imperfection.location = (-3000, 0)
    add_imperfection.blend_type = "ADD"
    add_imperfection.inputs["Fac"].default_value = 0.25

    mat.node_tree.links.new(add_imperfection.outputs["Color"],
                            subtract_imperfection.inputs["Color1"])

    # RGB Overlay - Roundness
    overlay_roundness = mat_nodes.new("ShaderNodeMixRGB")
    overlay_roundness.name = "RGB Overlay - Roundness"
    overlay_roundness.label = "RGB Overlay - Roundness"
    overlay_roundness.location = (-3200, 0)
    overlay_roundness.blend_type = "OVERLAY"
    overlay_roundness.inputs["Fac"].default_value = 0.85

    mat.node_tree.links.new(overlay_roundness.outputs["Color"],
                            add_imperfection.inputs["Color1"])

    # BEGINNING INITIAL SHAPE FRAME
    frame = mat_nodes.new(type='NodeFrame')
    frame.name = "Initial shape"
    frame.label = "Initial shape"
    # Gradient Texture
    gradient_texture = mat_nodes.new("ShaderNodeTexGradient")
    gradient_texture.parent = frame
    gradient_texture.name = "Initial Shape Gradient Texture"
    gradient_texture.location = (-3450, 0)
    gradient_texture.gradient_type = "SPHERICAL"

    mat.node_tree.links.new(gradient_texture.outputs["Color"],
                            overlay_roundness.inputs["Color1"])
    # Vector curves
    vector_curves = mat_nodes.new("ShaderNodeVectorCurve")
    vector_curves.parent = frame
    vector_curves.name = "Initial Shape Vector Curves"
    vector_curves.location = (-3750, 0)
    vector_curves.mapping.curves[2].points[0].location = (-0.77, -1.0)
    vector_curves.mapping.curves[2].points.new(-0.12, 0.55)

    mat.node_tree.links.new(vector_curves.outputs["Vector"],
                            gradient_texture.inputs["Vector"])

    # Mapping
    mapping = mat_nodes.new("ShaderNodeMapping")
    mapping.parent = frame
    mapping.name = "Initial Shape Mapping"
    mapping.location = (-3950, 0)
    mapping.inputs["Location"].default_value = (0.0, 0.0, -0.3)
    mapping.inputs["Scale"].default_value = (0.7, 0.6, 0.7)

    mat.node_tree.links.new(mapping.outputs["Vector"],
                            vector_curves.inputs["Vector"])
    # END INITIAL SHAPE FRAME

    # RGB Add - Big wind
    add_big_wind = mat_nodes.new("ShaderNodeMixRGB")
    add_big_wind.name = "RGB Add - Big wind"
    add_big_wind.label = "RGB Add - Big wind"
    add_big_wind.location = (-4250, 0)
    add_big_wind.blend_type = "ADD"
    add_big_wind.inputs["Fac"].default_value = 0.35

    mat.node_tree.links.new(add_big_wind.outputs["Color"],
                            mapping.inputs[0])
    mat.node_tree.links.new(add_big_wind.outputs["Color"],
                            reroute_1.inputs[0])

    # Noise Tex - Big wind
    noise_big_wind = mat_nodes.new("ShaderNodeTexNoise")
    noise_big_wind.name = "Noise Tex - Big wind"
    noise_big_wind.label = "Noise Tex - Big wind"
    noise_big_wind.location = (-4450, -150)
    noise_big_wind.inputs["Scale"].default_value = 2.2
    noise_big_wind.inputs["Detail"].default_value = 0.0
    noise_big_wind.inputs["Roughness"].default_value = 0.0
    noise_big_wind.inputs["Distortion"].default_value = 3.0

    mat.node_tree.links.new(noise_big_wind.outputs["Fac"],
                            add_big_wind.inputs["Color2"])

    # Texture Coordinate
    texture_coordinate = mat_nodes.new("ShaderNodeTexCoord")
    texture_coordinate.location = (-4650, 0)

    mat.node_tree.links.new(texture_coordinate.outputs["Object"],
                            add_big_wind.inputs["Color1"])
    mat.node_tree.links.new(texture_coordinate.outputs["Object"],
                            noise_big_wind.inputs["Vector"])
    # ----------------END MAIN BRANCH----------------

    mat.node_tree.links.new(texture_coordinate.outputs["Object"],
                            reroute_2.inputs[0])
    mat.node_tree.links.new(reroute_2.outputs[0],
                            reroute_3.inputs[0])
    mat.node_tree.links.new(reroute_3.outputs[0],
                            reroute_4.inputs[0])

    # --------BEGINNING FINAL CLEANER BRANCH---------
    frame = mat_nodes.new(type='NodeFrame')
    frame.name = "Final cleaner"
    frame.label = "Final cleaner"

    # Color Ramp
    color_ramp_cleaner = mat_nodes.new("ShaderNodeValToRGB")
    color_ramp_cleaner.parent = frame
    color_ramp_cleaner.name = "Final cleaning range"
    color_ramp_cleaner.label = "Final cleaning range"
    color_ramp_cleaner.location = (-400, -500)
    color_ramp_cleaner.color_ramp.interpolation = 'LINEAR'
    elem = color_ramp_cleaner.color_ramp.elements[0]
    elem.position = 0.9
    elem.color = (0, 0, 0, 1)
    elem = color_ramp_cleaner.color_ramp.elements[1]
    elem.position = 1.0
    elem.color = (1.0, 1.0, 1.0, 1)

    mat.node_tree.links.new(color_ramp_cleaner.outputs["Color"],
                            subtract_final_cleaner.inputs["Color2"])

    # Invert color
    invert_color = mat_nodes.new("ShaderNodeInvert")
    invert_color.parent = frame
    invert_color.location = (-600, -500)
    mat.node_tree.links.new(invert_color.outputs["Color"],
                            color_ramp_cleaner.inputs["Fac"])

    # Gradient Texture
    gradient_texture = mat_nodes.new("ShaderNodeTexGradient")
    gradient_texture.parent = frame
    gradient_texture.name = "Final Cleaner Gradient Texture"
    gradient_texture.location = (-800, -500)
    gradient_texture.gradient_type = "SPHERICAL"

    mat.node_tree.links.new(gradient_texture.outputs["Color"],
                            invert_color.inputs["Color"])

    # Vector curves coordinates for cleaner
    vector_curves = mat_nodes.new("ShaderNodeVectorCurve")
    vector_curves.parent = frame
    vector_curves.name = "Cleaner Vector Curves"
    vector_curves.location = (-1100, -500)
    vector_curves.mapping.curves[2].points[0].location = (-0.77, -1.0)
    vector_curves.mapping.curves[2].points.new(-0.12, 0.55)

    mat.node_tree.links.new(vector_curves.outputs["Vector"],
                            gradient_texture.inputs["Vector"])

    # Mapping coordinates for cleaner
    mapping = mat_nodes.new("ShaderNodeMapping")
    mapping.parent = frame
    mapping.name = "Cleaning Mapping"
    mapping.location = (-1300, -500)
    mapping.inputs["Location"].default_value = (0.0, 0.0, -0.3)
    mapping.inputs["Scale"].default_value = (0.7, 0.6, 0.7)

    mat.node_tree.links.new(mapping.outputs["Vector"],
                            vector_curves.inputs["Vector"])

    mat.node_tree.links.new(reroute_4.outputs[0],
                            mapping.inputs["Vector"])
    # -----------END FINAL CLEANER BRANCH------------


    # -------------BEGINNING BUMP BRANCH-------------
    frame = mat_nodes.new(type='NodeFrame')
    frame.name = "Bump"
    frame.label = "Bump"

    # Invert color
    invert_color = mat_nodes.new("ShaderNodeInvert")
    invert_color.parent = frame
    invert_color.location = (-1800, -500)
    mat.node_tree.links.new(invert_color.outputs["Color"],
                            multiply_bump.inputs["Color2"])
    # RGB Overlay - Bump level 3
    overlay_bump_3 = mat_nodes.new("ShaderNodeMixRGB")
    overlay_bump_3.parent = frame
    overlay_bump_3.name = "RGB Overlay - Bump level 3"
    overlay_bump_3.label = "RGB Overlay - Bump level 3"
    overlay_bump_3.location = (-2000, -500)
    overlay_bump_3.blend_type = "OVERLAY"
    overlay_bump_3.inputs["Fac"].default_value = 1.0

    mat.node_tree.links.new(overlay_bump_3.outputs["Color"],
                            invert_color.inputs["Color"])

    # RGB Overlay - Bump level 2
    overlay_bump_2 = mat_nodes.new("ShaderNodeMixRGB")
    overlay_bump_2.parent = frame
    overlay_bump_2.name = "RGB Overlay - Bump level 2"
    overlay_bump_2.label = "RGB Overlay - Bump level 2"
    overlay_bump_2.location = (-2200, -500)
    overlay_bump_2.blend_type = "OVERLAY"
    overlay_bump_2.inputs["Fac"].default_value = 1.0

    mat.node_tree.links.new(overlay_bump_2.outputs["Color"],
                            overlay_bump_3.inputs["Color1"])
                            
    # Voronoi tex - Bump level 1
    voronoi_bump_1 = mat_nodes.new("ShaderNodeTexVoronoi")
    voronoi_bump_1.parent = frame
    voronoi_bump_1.name = "Voronoi tex - Bump level 1"
    voronoi_bump_1.label = "Voronoi tex - Bump level 1"
    voronoi_bump_1.location = (-2400, -500)

    mat.node_tree.links.new(voronoi_bump_1.outputs["Distance"],
                            overlay_bump_2.inputs["Color1"])

    # Voronoi tex - Bump level 2
    voronoi_bump_2 = mat_nodes.new("ShaderNodeTexVoronoi")
    voronoi_bump_2.parent = frame
    voronoi_bump_2.name = "Voronoi tex - Bump level 2"
    voronoi_bump_2.label = "Voronoi tex - Bump level 2"
    voronoi_bump_2.location = (-2400, -800)
    voronoi_bump_2.inputs["Scale"].default_value = 10.3

    mat.node_tree.links.new(voronoi_bump_2.outputs["Distance"],
                            overlay_bump_2.inputs["Color2"])

    # Voronoi tex - Bump level 3
    voronoi_bump_3 = mat_nodes.new("ShaderNodeTexVoronoi")
    voronoi_bump_3.parent = frame
    voronoi_bump_3.name = "Voronoi tex - Bump level 3"
    voronoi_bump_3.label = "Voronoi tex - Bump level 3"
    voronoi_bump_3.location = (-2400, -1100)
    voronoi_bump_3.inputs["Scale"].default_value = 30.0

    mat.node_tree.links.new(voronoi_bump_3.outputs["Distance"],
                            overlay_bump_3.inputs["Color2"])
                            
    # RGB Add - Small wind
    add_small_wind = mat_nodes.new("ShaderNodeMixRGB")
    add_small_wind.parent = frame
    add_small_wind.name = "RGB Add - Small wind"
    add_small_wind.label = "RGB Add - Small wind"
    add_small_wind.location = (-2600, -950)
    add_small_wind.blend_type = "ADD"
    add_small_wind.inputs["Fac"].default_value = 0.35

    mat.node_tree.links.new(add_small_wind.outputs["Color"],
                            voronoi_bump_1.inputs["Vector"])
    mat.node_tree.links.new(add_small_wind.outputs["Color"],
                            voronoi_bump_2.inputs["Vector"])
    mat.node_tree.links.new(add_small_wind.outputs["Color"],
                            voronoi_bump_3.inputs["Vector"])
                            
    # Vector Add - Bump coordinates
    add_coord_bump = mat_nodes.new("ShaderNodeVectorMath")
    add_coord_bump.parent = frame
    add_coord_bump.location = (-2800, -800)
    add_coord_bump.name = "Vector Add - Bump coordinates"
    add_coord_bump.label = "Vector Add - Bump coordinates"
    add_coord_bump.operation = "ADD"
    add_coord_bump.inputs[1].default_value = (5.0, 8.5, 11.0)

    mat.node_tree.links.new(add_coord_bump.outputs["Vector"],
                            add_small_wind.inputs["Color1"])

    # Noise Tex - Small wind
    noise_small_wind = mat_nodes.new("ShaderNodeTexNoise")
    noise_small_wind.name = "Noise Tex - Small wind"
    noise_small_wind.label = "Noise Tex - Small wind"
    noise_small_wind.location = (-2800, -1100)
    noise_small_wind.inputs["Scale"].default_value = 0.7
    noise_small_wind.inputs["Detail"].default_value = 0.0
    noise_small_wind.inputs["Roughness"].default_value = 0.0
    noise_small_wind.inputs["Distortion"].default_value = 3.0

    mat.node_tree.links.new(noise_small_wind.outputs["Fac"],
                            add_small_wind.inputs["Color2"])

    mat.node_tree.links.new(reroute_3.outputs[0],
                            add_coord_bump.inputs[0])
    mat.node_tree.links.new(reroute_3.outputs[0],
                            noise_small_wind.inputs[0])
    # ---------------END BUMP BRANCH-----------------


    # --------BEGINNING DETAIL NOISE BRANCH----------
    frame = mat_nodes.new(type='NodeFrame')
    frame.name = "Detail noise"
    frame.label = "Detail noise"

    # RGB Overlay - Detail noise combined
    overlay_noise_combine = mat_nodes.new("ShaderNodeMixRGB")
    overlay_noise_combine.parent = frame
    overlay_noise_combine.name = "RGB Overlay - Detail noise combined"
    overlay_noise_combine.label = "RGB Overlay - Detail noise combined"
    overlay_noise_combine.location = (-1800, -1500)
    overlay_noise_combine.blend_type = "OVERLAY"
    overlay_noise_combine.inputs["Fac"].default_value = 1.0

    mat.node_tree.links.new(overlay_noise_combine.outputs["Color"],
                            overlay_detail_noise.inputs["Color2"])

    # Noise Tex - Detail noise level 1
    detetail_noise_level_1 = mat_nodes.new("ShaderNodeTexNoise")
    detetail_noise_level_1.parent = frame
    detetail_noise_level_1.name = "Noise Tex - Detail noise level 1"
    detetail_noise_level_1.label = "Noise Tex - Detail noise level 1"
    detetail_noise_level_1.location = (-2000, -1500)
    detetail_noise_level_1.inputs["Scale"].default_value = 12.4
    detetail_noise_level_1.inputs["Detail"].default_value = 2.6
    detetail_noise_level_1.inputs["Roughness"].default_value = 1.0
    detetail_noise_level_1.inputs["Distortion"].default_value = 0.0

    mat.node_tree.links.new(detetail_noise_level_1.outputs["Fac"],
                            overlay_noise_combine.inputs["Color1"])

    # Noise Tex - Detail noise level 2
    detetail_noise_level_2 = mat_nodes.new("ShaderNodeTexNoise")
    detetail_noise_level_2.parent = frame
    detetail_noise_level_2.name = "Noise Tex - Detail noise level 2"
    detetail_noise_level_2.label = "Noise Tex - Detail noise level 2"
    detetail_noise_level_2.location = (-2000, -1800)
    detetail_noise_level_2.inputs["Scale"].default_value = 12.4
    detetail_noise_level_2.inputs["Detail"].default_value = 6.0
    detetail_noise_level_2.inputs["Roughness"].default_value = 1.0
    detetail_noise_level_2.inputs["Distortion"].default_value = 0.0

    mat.node_tree.links.new(detetail_noise_level_2.outputs["Fac"],
                            overlay_noise_combine.inputs["Color2"])

    mat.node_tree.links.new(reroute_3.outputs[0],
                            detetail_noise_level_1.inputs["Vector"])
    mat.node_tree.links.new(reroute_3.outputs[0],
                            detetail_noise_level_2.inputs["Vector"])
    # -----------END DETAIL NOISE BRANCH-------------


    # ----------BEGINNING ROUNDNESS BRANCH-----------
    frame = mat_nodes.new(type='NodeFrame')
    frame.name = "Roundness"
    frame.label = "Roundness"

    # Invert color
    invert_color = mat_nodes.new("ShaderNodeInvert")
    invert_color.parent = frame
    invert_color.location = (-3450, -500)
    mat.node_tree.links.new(invert_color.outputs["Color"],
                            overlay_roundness.inputs["Color2"])

    # Voronoi tex - Roundness
    voronoi_roundness = mat_nodes.new("ShaderNodeTexVoronoi")
    voronoi_roundness.parent = frame
    voronoi_roundness.name = "Voronoi tex - Roundness"
    voronoi_roundness.label = "Voronoi tex - Roundness"
    voronoi_roundness.location = (-3850, -500)
    voronoi_roundness.inputs["Scale"].default_value = 1.2

    mat.node_tree.links.new(voronoi_roundness.outputs["Distance"],
                            invert_color.inputs["Color"])

    mat.node_tree.links.new(reroute_1.outputs[0],
                            voronoi_roundness.inputs["Vector"])
    # -------------END ROUNDNESS BRANCH--------------


    # -----BEGINNING ADD BIG IMPERFECTION BRANCH-----
    frame = mat_nodes.new(type='NodeFrame')
    frame.name = "Add big imperfection"
    frame.label = "Add big imperfection"

    # RGB Color Burn - Combine noises
    color_burn_noises = mat_nodes.new("ShaderNodeMixRGB")
    color_burn_noises.parent = frame
    color_burn_noises.name = "RGB Color Burn - Combine noises"
    color_burn_noises.label = "RGB Color Burn - Combine noises"
    color_burn_noises.location = (-3450, -900)
    color_burn_noises.blend_type = "BURN"
    color_burn_noises.inputs["Fac"].default_value = 1.0

    mat.node_tree.links.new(color_burn_noises.outputs["Color"],
                            add_imperfection.inputs["Color2"])

    # Noise Tex - Add big imperfection 1
    noise_add_big_imperfection_1 = mat_nodes.new("ShaderNodeTexNoise")
    noise_add_big_imperfection_1.parent = frame
    noise_add_big_imperfection_1.name = "Noise Tex - Add big imperfection 1"
    noise_add_big_imperfection_1.label = "Noise Tex - Add big imperfection 1"
    noise_add_big_imperfection_1.location = (-3650, -900)
    noise_add_big_imperfection_1.inputs["Scale"].default_value = 1.9
    noise_add_big_imperfection_1.inputs["Detail"].default_value = 0.0
    noise_add_big_imperfection_1.inputs["Roughness"].default_value = 0.0

    mat.node_tree.links.new(noise_add_big_imperfection_1.outputs["Fac"],
                            color_burn_noises.inputs["Color1"])

    # Noise Tex - Add big imperfection 2
    noise_add_big_imperfection_2 = mat_nodes.new("ShaderNodeTexNoise")
    noise_add_big_imperfection_2.parent = frame
    noise_add_big_imperfection_2.name = "Noise Tex - Add big imperfection 1"
    noise_add_big_imperfection_2.label = "Noise Tex - Add big imperfection 1"
    noise_add_big_imperfection_2.location = (-3650, -1150)
    noise_add_big_imperfection_2.inputs["Scale"].default_value = 1.9
    noise_add_big_imperfection_2.inputs["Detail"].default_value = 16.0
    noise_add_big_imperfection_2.inputs["Roughness"].default_value = 0.0
    noise_add_big_imperfection_2.inputs["Distortion"].default_value = 0.0

    mat.node_tree.links.new(noise_add_big_imperfection_2.outputs["Fac"],
                            color_burn_noises.inputs["Color2"])

    # Vector Add - Add big imperfection 1
    add_big_imperfection_1 = mat_nodes.new("ShaderNodeVectorMath")
    add_big_imperfection_1.parent = frame
    add_big_imperfection_1.location = (-3850, -900)
    add_big_imperfection_1.name = "Vector Add - Add big imperfection 1"
    add_big_imperfection_1.label = "Vector Add - Add big imperfection 1"
    add_big_imperfection_1.operation = "ADD"

    mat.node_tree.links.new(add_big_imperfection_1.outputs["Vector"],
                            noise_add_big_imperfection_1.inputs["Vector"])
    mat.node_tree.links.new(reroute_1.outputs[0],
                            add_big_imperfection_1.inputs["Vector"])

    # Vector Add - Add big imperfection 1
    add_big_imperfection_2 = mat_nodes.new("ShaderNodeVectorMath")
    add_big_imperfection_2.parent = frame
    add_big_imperfection_2.location = (-3850, -1150)
    add_big_imperfection_2.name = "Vector Add - Add big imperfection 2"
    add_big_imperfection_2.label = "Vector Add - Add big imperfection 2"
    add_big_imperfection_2.operation = "ADD"
    add_big_imperfection_2.inputs[1].default_value = (5.0, 5.0, 5.0)

    mat.node_tree.links.new(add_big_imperfection_2.outputs["Vector"],
                            noise_add_big_imperfection_2.inputs["Vector"])
    mat.node_tree.links.new(reroute_1.outputs[0],
                            add_big_imperfection_2.inputs["Vector"])
    # --------END ADD BIG IMPERFECTION BRANCH--------


    # --BEGINNING SUBTRACT BIG IMPERFECTION BRANCH---
    frame = mat_nodes.new(type='NodeFrame')
    frame.name = "Subtract big imperfection"
    frame.label = "Subtract big imperfection"

    # RGB Color Burn - Combine noises
    color_burn_noises = mat_nodes.new("ShaderNodeMixRGB")
    color_burn_noises.parent = frame
    color_burn_noises.name = "RGB Color Burn - Combine noises"
    color_burn_noises.label = "RGB Color Burn - Combine noises"
    color_burn_noises.location = (-3450, -1500)
    color_burn_noises.blend_type = "BURN"
    color_burn_noises.inputs["Fac"].default_value = 1.0

    mat.node_tree.links.new(color_burn_noises.outputs["Color"],
                            subtract_imperfection.inputs["Color2"])

    # Noise Tex - Subtract big imperfection 1
    noise_subtract_big_imperfection_1 = mat_nodes.new("ShaderNodeTexNoise")
    noise_subtract_big_imperfection_1.parent = frame
    noise_subtract_big_imperfection_1.name = "Noise Tex - Subtract big imperfection 1"
    noise_subtract_big_imperfection_1.label = "Noise Tex - Subtract big imperfection 1"
    noise_subtract_big_imperfection_1.location = (-3650, -1500)
    noise_subtract_big_imperfection_1.inputs["Scale"].default_value = 1.9
    noise_subtract_big_imperfection_1.inputs["Detail"].default_value = 0.0
    noise_subtract_big_imperfection_1.inputs["Roughness"].default_value = 0.0

    mat.node_tree.links.new(noise_subtract_big_imperfection_1.outputs["Fac"],
                            color_burn_noises.inputs["Color1"])

    # Noise Tex - Subtract big imperfection 2
    noise_subtract_big_imperfection_2 = mat_nodes.new("ShaderNodeTexNoise")
    noise_subtract_big_imperfection_2.parent = frame
    noise_subtract_big_imperfection_2.name = "Noise Tex - Subtract big imperfection 1"
    noise_subtract_big_imperfection_2.label = "Noise Tex - Subtract big imperfection 1"
    noise_subtract_big_imperfection_2.location = (-3650, -1750)
    noise_subtract_big_imperfection_2.inputs["Scale"].default_value = 1.9
    noise_subtract_big_imperfection_2.inputs["Detail"].default_value = 16.0
    noise_subtract_big_imperfection_2.inputs["Roughness"].default_value = 0.0
    noise_subtract_big_imperfection_2.inputs["Distortion"].default_value = 0.0

    mat.node_tree.links.new(noise_subtract_big_imperfection_2.outputs["Fac"],
                            color_burn_noises.inputs["Color2"])

    # Vector Add - Add big imperfection 1
    subtract_big_imperfection_1 = mat_nodes.new("ShaderNodeVectorMath")
    subtract_big_imperfection_1.parent = frame
    subtract_big_imperfection_1.location = (-3850, -1500)
    subtract_big_imperfection_1.name = "Vector Add - Subtract big imperfection 1"
    subtract_big_imperfection_1.label = "Vector Add - Subtract big imperfection 1"
    subtract_big_imperfection_1.operation = "ADD"
    subtract_big_imperfection_1.inputs[1].default_value = (13.1, 4.4, 8.7)

    mat.node_tree.links.new(subtract_big_imperfection_1.outputs["Vector"],
                            noise_subtract_big_imperfection_1.inputs["Vector"])
    mat.node_tree.links.new(reroute_1.outputs[0],
                            subtract_big_imperfection_1.inputs["Vector"])

    # Vector Add - Add big imperfection 1
    subtract_big_imperfection_2 = mat_nodes.new("ShaderNodeVectorMath")
    subtract_big_imperfection_2.parent = frame
    subtract_big_imperfection_2.location = (-3850, -1750)
    subtract_big_imperfection_2.name = "Vector Add - Subtract big imperfection 2"
    subtract_big_imperfection_2.label = "Vector Add - Subtract big imperfection 2"
    subtract_big_imperfection_2.operation = "ADD"
    subtract_big_imperfection_2.inputs[1].default_value = (5.0, 5.0, 5.0)

    mat.node_tree.links.new(subtract_big_imperfection_2.outputs["Vector"],
                            noise_subtract_big_imperfection_2.inputs["Vector"])
    mat.node_tree.links.new(reroute_1.outputs[0],
                            subtract_big_imperfection_2.inputs["Vector"])
    # -----END SUBTRACT BIG IMPERFECTION BRANCH------

    turbulence_big_imperfection = mat_nodes.new("ShaderNodeValue")
    turbulence_big_imperfection.location = (-3950, -1400)
    turbulence_big_imperfection.outputs[0].default_value = 0.0

    mat.node_tree.links.new(turbulence_big_imperfection.outputs["Value"],
                            noise_add_big_imperfection_1.inputs["Distortion"])
    mat.node_tree.links.new(turbulence_big_imperfection.outputs["Value"],
                            noise_subtract_big_imperfection_1.inputs["Distortion"])

    # ---------------------------------------
    # --------Domain and size config---------
    # ---------------------------------------
    obj.scale = (0.5, 0.5, 0.5) # Default cube is 2 meters
    C.view_layer.objects.active = obj
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True, properties=True)

    adapted_size = Vector((domain.x/size, domain.y/size, domain.z/size))
    obj.scale = (adapted_size.x, adapted_size.y, adapted_size.z)
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True, properties=True)
    obj.cloud_settings["auxiliar_size_vector"] = adapted_size

    cube_size = Vector((domain.x / adapted_size.x, domain.y / adapted_size.y, domain.z / adapted_size.z))
    obj.scale = cube_size



