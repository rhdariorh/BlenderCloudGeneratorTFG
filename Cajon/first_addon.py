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
        density_color_ramp = material.node_tree.nodes.get("ColorRamp - Cloud Density")
        elem = density_color_ramp.color_ramp.elements[1]
        elem.color = (density, density, density, 1)

def update_cloud_wind(self, context):
    obj = context.active_object
    wind = obj.cloud_settings.wind
    material = bpy.context.active_object.active_material
    if "CloudMaterial_CG" not in material.name:
        bpy.ops.error.cloud_error("INVOKE_DEFAULT", error_type="MATERIAL_WRONG_NAME")
    else:
        add_shape_wind = material.node_tree.nodes.get("RGB Add - Shape wind")
        add_shape_wind.inputs["Fac"].default_value = wind

        add_small_wind = material.node_tree.nodes.get("RGB Add - Small wind")
        add_small_wind.inputs["Fac"].default_value = wind

def update_cloud_roundness(self, context):
    obj = context.active_object
    roundness = obj.cloud_settings.roundness
    material = bpy.context.active_object.active_material
    if "CloudMaterial_CG" not in material.name:
        bpy.ops.error.cloud_error("INVOKE_DEFAULT", error_type="MATERIAL_WRONG_NAME")
    else:
        overlay_roundness = material.node_tree.nodes.get("RGB Overlay - Roundness")
        overlay_roundness.inputs["Fac"].default_value = roundness

def update_cloud_roundness_coords(self, context):
    obj = context.active_object
    roundness_coords = obj.cloud_settings.roundness_coords
    material = bpy.context.active_object.active_material
    if "CloudMaterial_CG" not in material.name:
        bpy.ops.error.cloud_error("INVOKE_DEFAULT", error_type="MATERIAL_WRONG_NAME")
    else:
        add_coords_roundness = material.node_tree.nodes.get("Vector Add - Roundness coord")
        add_coords_roundness.inputs[1].default_value = roundness_coords

def update_cloud_add_shape_imperfection(self, context):
    obj = context.active_object
    add_shape_imperfection = obj.cloud_settings.add_shape_imperfection
    material = bpy.context.active_object.active_material
    if "CloudMaterial_CG" not in material.name:
        bpy.ops.error.cloud_error("INVOKE_DEFAULT", error_type="MATERIAL_WRONG_NAME")
    else:
        add_imperfection = material.node_tree.nodes.get("RGB Add - Shape imperfection")
        add_imperfection.inputs["Fac"].default_value = add_shape_imperfection

def update_cloud_add_shape_imperfection_coords(self, context):
    obj = context.active_object
    add_shape_imperfection_coords = obj.cloud_settings.add_shape_imperfection_coords
    material = bpy.context.active_object.active_material
    if "CloudMaterial_CG" not in material.name:
        bpy.ops.error.cloud_error("INVOKE_DEFAULT", error_type="MATERIAL_WRONG_NAME")
    else:
        coords_add_shape_imperfection_1 = material.node_tree.nodes.get("Vector Add - Coords add shape imperfection 1")
        coords_add_shape_imperfection_1.inputs[1].default_value = add_shape_imperfection_coords

def update_cloud_subtract_shape_imperfection(self, context):
    obj = context.active_object
    subtract_shape_imperfection = obj.cloud_settings.subtract_shape_imperfection
    material = bpy.context.active_object.active_material
    if "CloudMaterial_CG" not in material.name:
        bpy.ops.error.cloud_error("INVOKE_DEFAULT", error_type="MATERIAL_WRONG_NAME")
    else:
        subtract_imperfection = material.node_tree.nodes.get("RGB Subtract - Shape imperfection")
        subtract_imperfection.inputs["Fac"].default_value = subtract_shape_imperfection

def update_cloud_subtract_shape_imperfection_coords(self, context):
    obj = context.active_object
    subtract_shape_imperfection_coords = obj.cloud_settings.subtract_shape_imperfection_coords
    material = bpy.context.active_object.active_material
    if "CloudMaterial_CG" not in material.name:
        bpy.ops.error.cloud_error("INVOKE_DEFAULT", error_type="MATERIAL_WRONG_NAME")
    else:
        coords_subtract_shape_imperfection_1 = material.node_tree.nodes.get("Vector Add - Coods subtract shape imperfection 1")
        coords_subtract_shape_imperfection_1.inputs[1].default_value = subtract_shape_imperfection_coords

def update_cloud_detail_bump_strength(self, context):
    obj = context.active_object
    detail_bump_strength = obj.cloud_settings.detail_bump_strength
    material = bpy.context.active_object.active_material
    if "CloudMaterial_CG" not in material.name:
        bpy.ops.error.cloud_error("INVOKE_DEFAULT", error_type="MATERIAL_WRONG_NAME")
    else:
        multiply_bump = material.node_tree.nodes.get("RGB Multiply - Bump")
        multiply_bump.inputs["Fac"].default_value = detail_bump_strength

def update_cloud_detail_bump_levels(self, context):
    obj = context.active_object
    detail_bump_levels = obj.cloud_settings.detail_bump_levels
    material = bpy.context.active_object.active_material
    if "CloudMaterial_CG" not in material.name:
        bpy.ops.error.cloud_error("INVOKE_DEFAULT", error_type="MATERIAL_WRONG_NAME")
    elif detail_bump_levels == 1:
        overlay_bump_2 = material.node_tree.nodes.get("RGB Overlay - Bump level 2")
        overlay_bump_2.inputs["Fac"].default_value = 0
        overlay_bump_3 = material.node_tree.nodes.get("RGB Overlay - Bump level 3")
        overlay_bump_3.inputs["Fac"].default_value = 0
    elif detail_bump_levels == 2:
        overlay_bump_2 = material.node_tree.nodes.get("RGB Overlay - Bump level 2")
        overlay_bump_2.inputs["Fac"].default_value = 1
        overlay_bump_3 = material.node_tree.nodes.get("RGB Overlay - Bump level 3")
        overlay_bump_3.inputs["Fac"].default_value = 0
    elif detail_bump_levels == 3:
        overlay_bump_2 = material.node_tree.nodes.get("RGB Overlay - Bump level 2")
        overlay_bump_2.inputs["Fac"].default_value = 1
        overlay_bump_3 = material.node_tree.nodes.get("RGB Overlay - Bump level 3")
        overlay_bump_3.inputs["Fac"].default_value = 1

def update_cloud_detail_noise(self, context):
    obj = context.active_object
    detail_noise = obj.cloud_settings.detail_noise
    material = bpy.context.active_object.active_material
    if "CloudMaterial_CG" not in material.name:
        bpy.ops.error.cloud_error("INVOKE_DEFAULT", error_type="MATERIAL_WRONG_NAME")
    else:
        overlay_detail_noise = material.node_tree.nodes.get("RGB Overlay - Noise")
        overlay_detail_noise.inputs["Fac"].default_value = detail_noise

class CloudSettings(bpy.types.PropertyGroup):
    is_cloud: bpy.props.BoolProperty(
        name="Is cloud",
        description="Indicates if the object is a cloud",
        default=False
    )

    size: bpy.props.FloatProperty(
        name="Cloud size",
        description="Size of the cloud",
        default=10,
        min=0.01,
        update=update_cloud_dimensions
    )

    domain: bpy.props.FloatVectorProperty(
        name="Cloud domain size",
        description="Size of the cloud object, therefore the rendering domain",
        subtype="TRANSLATION",
        default=(30.0, 30.0, 30.0),
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

    wind: bpy.props.FloatProperty(
        name="Cloud wind",
        description="Wind effect",
        default=0.1,
        min=0.0,
        max=1.0,
        update=update_cloud_wind
    )

    roundness: bpy.props.FloatProperty(
        name="Cloud roundness",
        description="Roundness of the general shape",
        default=0.5,
        min=0.0,
        max=1.0,
        update=update_cloud_roundness
    )

    roundness_coords: bpy.props.FloatVectorProperty(
        name="Cloud roundness coordinates",
        description="Mapping coordinates for roundness",
        subtype="XYZ",
        default=(0.0, 0.0, 0.0),
        update=update_cloud_roundness_coords
    )

    add_shape_imperfection: bpy.props.FloatProperty(
        name="Cloud add shape imperfection",
        description="Add imperfection to the general shape",
        default=0.3,
        min=0.0,
        max=1.0,
        update=update_cloud_add_shape_imperfection
    )

    add_shape_imperfection_coords: bpy.props.FloatVectorProperty(
        name="Cloud add shape imperfection coordinates",
        description="Mapping coordinates for add shape imperfection ",
        subtype="XYZ",
        default=(0.0, 0.0, 0.0),
        update=update_cloud_add_shape_imperfection_coords
    )

    subtract_shape_imperfection: bpy.props.FloatProperty(
        name="Cloud subtract shape imperfection",
        description="Subtract imperfection to the general shape",
        default=0.1,
        min=0.0,
        max=1.0,
        update=update_cloud_subtract_shape_imperfection
    )

    subtract_shape_imperfection_coords: bpy.props.FloatVectorProperty(
        name="Cloud subtract shape imperfection coordinates",
        description="Mapping coordinates for subtract shape imperfection ",
        subtype="XYZ",
        default=(0.0, 0.0, 0.0),
        update=update_cloud_subtract_shape_imperfection_coords
    )

    detail_bump_strength: bpy.props.FloatProperty(
        name="Cloud detail bump strength",
        description="Amount of bump effect applied",
        default=0.3,
        min=0.0,
        max=1.0,
        update=update_cloud_detail_bump_strength
    )

    detail_bump_levels: bpy.props.IntProperty(
        name="Cloud detail bump LOD",
        description="Number of bump levels",
        default=1,
        min=1,
        max=3,
        update=update_cloud_detail_bump_levels
    )

    detail_noise: bpy.props.FloatProperty(
        name="Detail noise",
        description="Amount of detail noise effect applied",
        default=0.05,
        min=0.0,
        max=1.0,
        update=update_cloud_detail_noise
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
        if not obj.cloud_settings.is_cloud:
            layout.label(text="The selected object is not a cloud.",
                icon="ERROR")
        else:
            scene = context.scene

            # Create a simple row.

            column = layout.column()
            column.prop(cloud_settings, "density", text="Density")
            column.prop(cloud_settings, "wind", text="Wind")

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
        if not obj.cloud_settings.is_cloud:
            layout.label(text="The selected object is not a cloud.",
                icon="ERROR")
        else:
            scene = context.scene

            # Create a simple row.
            #column = layout.column()

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
        if not obj.cloud_settings.is_cloud:
            layout.label(text="The selected object is not a cloud.",
                icon="ERROR")
        else:
            scene = context.scene

            # Create a simple row.
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
        if not obj.cloud_settings.is_cloud:
            layout.label(text="The selected object is not a cloud.",
                icon="ERROR")
        else:
            scene = context.scene

            # Create a simple row.
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
        if not obj.cloud_settings.is_cloud:
            layout.label(text="The selected object is not a cloud.",
                icon="ERROR")
        else:
            scene = context.scene

            # Create a simple row.
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
        if not obj.cloud_settings.is_cloud:
            layout.label(text="The selected object is not a cloud.",
                icon="ERROR")
        else:
            scene = context.scene

            # Create a simple row.
            column = layout.column()
            column.prop(cloud_settings, "detail_bump_strength", text="Bump strength")
            column.prop(cloud_settings, "detail_bump_levels", text="Bump levels")
            column.prop(cloud_settings, "detail_noise", text="Noise")


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
    bpy.utils.register_class(OBJECT_PT_cloud_general)
    bpy.utils.register_class(OBJECT_PT_cloud_shape)
    bpy.utils.register_class(OBJECT_PT_cloud_shape_roundness)
    bpy.utils.register_class(OBJECT_PT_cloud_shape_add_imperfection)
    bpy.utils.register_class(OBJECT_PT_cloud_shape_subtract_imperfection)
    bpy.utils.register_class(OBJECT_PT_cloud_detail)

    bpy.utils.register_class(VIEW3D_MT_cloud_add)
    bpy.types.VIEW3D_MT_volume_add.append(add_menu_cloud)
    
    bpy.types.Object.cloud_settings = bpy.props.PointerProperty(type=CloudSettings)


def unregister():
    bpy.utils.unregister_class(CloudErrorOperator)
    bpy.utils.unregister_class(CloudSettings)
    bpy.utils.unregister_class(OBJECT_OT_cloud)

    bpy.utils.unregister_class(OBJECT_PT_cloud)
    bpy.utils.unregister_class(OBJECT_PT_cloud_general)
    bpy.utils.unregister_class(OBJECT_PT_cloud_shape)
    bpy.utils.unregister_class(OBJECT_PT_cloud_shape_roundness)
    bpy.utils.unregister_class(OBJECT_PT_cloud_shape_add_imperfection)
    bpy.utils.unregister_class(OBJECT_PT_cloud_shape_subtract_imperfection)
    bpy.utils.unregister_class(OBJECT_PT_cloud_detail)
    
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
    reroute_1.location = (-4250, -1500)

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
    density = obj.cloud_settings.density
    elem.color = (density, density, density, 1)

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
    detail_noise = obj.cloud_settings.detail_noise
    overlay_detail_noise.inputs["Fac"].default_value = detail_noise

    mat.node_tree.links.new(overlay_detail_noise.outputs["Color"],
                            subtract_final_cleaner.inputs["Color1"])

    # RGB Multiply - Bump
    multiply_bump = mat_nodes.new("ShaderNodeMixRGB")
    multiply_bump.name = "RGB Multiply - Bump"
    multiply_bump.label = "RGB Multiply - Bump"
    multiply_bump.location = (-1500, 0)
    multiply_bump.blend_type = "MULTIPLY"
    detail_bump_strength = obj.cloud_settings.detail_bump_strength
    multiply_bump.inputs["Fac"].default_value = detail_bump_strength

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

    # RGB Subtract - Shape imperfection
    subtract_imperfection = mat_nodes.new("ShaderNodeMixRGB")
    subtract_imperfection.name = "RGB Subtract - Shape imperfection"
    subtract_imperfection.label = "RGB Subtract - Shape imperfection"
    subtract_imperfection.location = (-3000, 0)
    subtract_imperfection.blend_type = "SUBTRACT"
    subtract_shape_imperfection = obj.cloud_settings.subtract_shape_imperfection
    subtract_imperfection.inputs["Fac"].default_value = subtract_shape_imperfection

    mat.node_tree.links.new(subtract_imperfection.outputs["Color"],
                            lenght.inputs[0])
    mat.node_tree.links.new(subtract_imperfection.outputs["Color"],
                            multiply_cleaner.inputs[0])

    # RGB Add - Shape imperfection
    add_imperfection = mat_nodes.new("ShaderNodeMixRGB")
    add_imperfection.name = "RGB Add - Shape imperfection"
    add_imperfection.label = "RGB Add - Shape imperfection"
    add_imperfection.location = (-3200, 0)
    add_imperfection.blend_type = "ADD"
    add_shape_imperfection = obj.cloud_settings.add_shape_imperfection
    add_imperfection.inputs["Fac"].default_value = add_shape_imperfection

    mat.node_tree.links.new(add_imperfection.outputs["Color"],
                            subtract_imperfection.inputs["Color1"])

    # RGB Overlay - Roundness
    overlay_roundness = mat_nodes.new("ShaderNodeMixRGB")
    overlay_roundness.name = "RGB Overlay - Roundness"
    overlay_roundness.label = "RGB Overlay - Roundness"
    overlay_roundness.location = (-3400, 0)
    overlay_roundness.blend_type = "OVERLAY"
    roundness = obj.cloud_settings.roundness
    overlay_roundness.inputs["Fac"].default_value = roundness

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
    gradient_texture.location = (-3650, 0)
    gradient_texture.gradient_type = "SPHERICAL"

    mat.node_tree.links.new(gradient_texture.outputs["Color"],
                            overlay_roundness.inputs["Color1"])
    # Vector curves
    vector_curves = mat_nodes.new("ShaderNodeVectorCurve")
    vector_curves.parent = frame
    vector_curves.name = "Initial Shape Vector Curves"
    vector_curves.location = (-3950, 0)
    vector_curves.mapping.curves[2].points[0].location = (-0.77, -1.0)
    vector_curves.mapping.curves[2].points.new(-0.12, 0.55)

    mat.node_tree.links.new(vector_curves.outputs["Vector"],
                            gradient_texture.inputs["Vector"])

    # Mapping
    mapping = mat_nodes.new("ShaderNodeMapping")
    mapping.parent = frame
    mapping.name = "Initial Shape Mapping"
    mapping.location = (-4150, 0)
    mapping.inputs["Location"].default_value = (0.0, 0.0, -0.3)
    mapping.inputs["Scale"].default_value = (0.7, 0.6, 0.7)

    mat.node_tree.links.new(mapping.outputs["Vector"],
                            vector_curves.inputs["Vector"])
    # END INITIAL SHAPE FRAME

    # RGB Add - Shape wind
    add_shape_wind = mat_nodes.new("ShaderNodeMixRGB")
    add_shape_wind.name = "RGB Add - Shape wind"
    add_shape_wind.label = "RGB Add - Shape wind"
    add_shape_wind.location = (-4450, 0)
    add_shape_wind.blend_type = "ADD"
    wind = obj.cloud_settings.wind
    add_shape_wind.inputs["Fac"].default_value = wind

    mat.node_tree.links.new(add_shape_wind.outputs["Color"],
                            mapping.inputs[0])
    mat.node_tree.links.new(add_shape_wind.outputs["Color"],
                            reroute_1.inputs[0])

    # Vector Subtract - Shape wind domain to -0.5 to 0.5
    domain_adjustment_shape_wind = mat_nodes.new("ShaderNodeVectorMath")
    domain_adjustment_shape_wind.location = (-4650, -150)
    domain_adjustment_shape_wind.name = "Vector Subtract - Shape wind domain adjustment"
    domain_adjustment_shape_wind.label = "Vector Subtract - Shape wind domain adjustment"
    domain_adjustment_shape_wind.operation = "SUBTRACT"
    domain_adjustment_shape_wind.inputs[1].default_value = (0.5, 0.5, 0.5)

    mat.node_tree.links.new(domain_adjustment_shape_wind.outputs["Vector"],
                            add_shape_wind.inputs["Color2"])

    # Noise Tex - Shape wind
    noise_shape_wind = mat_nodes.new("ShaderNodeTexNoise")
    noise_shape_wind.name = "Noise Tex - Shape wind"
    noise_shape_wind.label = "Noise Tex - Shape wind"
    noise_shape_wind.location = (-4850, -150)
    noise_shape_wind.inputs["Scale"].default_value = 1.5
    noise_shape_wind.inputs["Detail"].default_value = 0.0
    noise_shape_wind.inputs["Roughness"].default_value = 0.0
    noise_shape_wind.inputs["Distortion"].default_value = 3.0

    mat.node_tree.links.new(noise_shape_wind.outputs["Fac"],
                            domain_adjustment_shape_wind.inputs[0])

    # Texture Coordinate
    texture_coordinate = mat_nodes.new("ShaderNodeTexCoord")
    texture_coordinate.location = (-5150, 0)

    mat.node_tree.links.new(texture_coordinate.outputs["Object"],
                            add_shape_wind.inputs["Color1"])
    mat.node_tree.links.new(texture_coordinate.outputs["Object"],
                            noise_shape_wind.inputs["Vector"])
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

    mat.node_tree.links.new(overlay_bump_3.outputs["Color"],
                            invert_color.inputs["Color"])

    # RGB Overlay - Bump level 2
    overlay_bump_2 = mat_nodes.new("ShaderNodeMixRGB")
    overlay_bump_2.parent = frame
    overlay_bump_2.name = "RGB Overlay - Bump level 2"
    overlay_bump_2.label = "RGB Overlay - Bump level 2"
    overlay_bump_2.location = (-2200, -500)
    overlay_bump_2.blend_type = "OVERLAY"

    mat.node_tree.links.new(overlay_bump_2.outputs["Color"],
                            overlay_bump_3.inputs["Color1"])

    detail_bump_levels = obj.cloud_settings.detail_bump_levels
    if detail_bump_levels == 1:
        overlay_bump_2.inputs["Fac"].default_value = 0
        overlay_bump_3.inputs["Fac"].default_value = 0
    elif detail_bump_levels == 2:
        overlay_bump_2.inputs["Fac"].default_value = 1
        overlay_bump_3.inputs["Fac"].default_value = 0
    elif detail_bump_levels == 3:
        overlay_bump_2.inputs["Fac"].default_value = 1
        overlay_bump_3.inputs["Fac"].default_value = 1
                            
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
    wind = obj.cloud_settings.wind
    add_small_wind.inputs["Fac"].default_value = wind

    mat.node_tree.links.new(add_small_wind.outputs["Color"],
                            voronoi_bump_1.inputs["Vector"])
    mat.node_tree.links.new(add_small_wind.outputs["Color"],
                            voronoi_bump_2.inputs["Vector"])
    mat.node_tree.links.new(add_small_wind.outputs["Color"],
                            voronoi_bump_3.inputs["Vector"])
                            
    # Vector Add - Bump coordinates
    add_coords_bump = mat_nodes.new("ShaderNodeVectorMath")
    add_coords_bump.parent = frame
    add_coords_bump.location = (-3000, -800)
    add_coords_bump.name = "Vector Add - Bump coordinates"
    add_coords_bump.label = "Vector Add - Bump coordinates"
    add_coords_bump.operation = "ADD"
    add_coords_bump.inputs[1].default_value = (5.0, 8.5, 11.0)

    mat.node_tree.links.new(add_coords_bump.outputs["Vector"],
                            add_small_wind.inputs["Color1"])
    
    # Vector Subtract - Small wind domain to -0.5 to 0.5
    domain_adjustment_small_wind = mat_nodes.new("ShaderNodeVectorMath")
    domain_adjustment_small_wind.parent = frame
    domain_adjustment_small_wind.location = (-2800, -1100)
    domain_adjustment_small_wind.name = "Vector Subtract - Small wind domain adjustment"
    domain_adjustment_small_wind.label = "Vector Subtract - Small wind domain adjustment"
    domain_adjustment_small_wind.operation = "SUBTRACT"
    domain_adjustment_small_wind.inputs[1].default_value = (0.5, 0.5, 0.5)
    
    mat.node_tree.links.new(domain_adjustment_small_wind.outputs["Vector"],
                            add_small_wind.inputs["Color2"])
    
    # Noise Tex - Small wind
    noise_small_wind = mat_nodes.new("ShaderNodeTexNoise")
    noise_small_wind.parent = frame
    noise_small_wind.name = "Noise Tex - Small wind"
    noise_small_wind.label = "Noise Tex - Small wind"
    noise_small_wind.location = (-3000, -1100)
    noise_small_wind.inputs["Scale"].default_value = 0.7
    noise_small_wind.inputs["Detail"].default_value = 0.0
    noise_small_wind.inputs["Roughness"].default_value = 0.0
    noise_small_wind.inputs["Distortion"].default_value = 3.0

    mat.node_tree.links.new(noise_small_wind.outputs["Fac"],
                            domain_adjustment_small_wind.inputs[0])

    mat.node_tree.links.new(reroute_3.outputs[0],
                            add_coords_bump.inputs[0])
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
    invert_color.location = (-3650, -500)
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
    
    # Vector Add - Roundness coord
    add_coords_roundness = mat_nodes.new("ShaderNodeVectorMath")
    add_coords_roundness.parent = frame
    add_coords_roundness.location = (-4050, -500)
    add_coords_roundness.name = "Vector Add - Roundness coord"
    add_coords_roundness.label = "Vector Add - Roundness coord"
    add_coords_roundness.operation = "ADD"
    roundness_coords = obj.cloud_settings.roundness_coords
    add_coords_roundness.inputs[1].default_value = roundness_coords

    mat.node_tree.links.new(add_coords_roundness.outputs["Vector"],
                            voronoi_roundness.inputs["Vector"])

    mat.node_tree.links.new(reroute_1.outputs[0],
                            add_coords_roundness.inputs[0])
    # -------------END ROUNDNESS BRANCH--------------


    # -----BEGINNING ADD BIG IMPERFECTION BRANCH-----
    frame = mat_nodes.new(type='NodeFrame')
    frame.name = "Add shape imperfection"
    frame.label = "Add shape imperfection"

    # RGB Color Burn - Combine noises
    color_burn_noises = mat_nodes.new("ShaderNodeMixRGB")
    color_burn_noises.parent = frame
    color_burn_noises.name = "RGB Color Burn - Combine noises"
    color_burn_noises.label = "RGB Color Burn - Combine noises"
    color_burn_noises.location = (-3650, -900)
    color_burn_noises.blend_type = "BURN"
    color_burn_noises.inputs["Fac"].default_value = 1.0

    mat.node_tree.links.new(color_burn_noises.outputs["Color"],
                            add_imperfection.inputs["Color2"])

    # Noise Tex - Add shape imperfection 1
    noise_add_shape_imperfection_1 = mat_nodes.new("ShaderNodeTexNoise")
    noise_add_shape_imperfection_1.parent = frame
    noise_add_shape_imperfection_1.name = "Noise Tex - Add shape imperfection 1"
    noise_add_shape_imperfection_1.label = "Noise Tex - Add shape imperfection 1"
    noise_add_shape_imperfection_1.location = (-3850, -900)
    noise_add_shape_imperfection_1.inputs["Scale"].default_value = 1.9
    noise_add_shape_imperfection_1.inputs["Detail"].default_value = 0.0
    noise_add_shape_imperfection_1.inputs["Roughness"].default_value = 0.0

    mat.node_tree.links.new(noise_add_shape_imperfection_1.outputs["Fac"],
                            color_burn_noises.inputs["Color1"])

    # Noise Tex - Add shape imperfection 2
    noise_add_shape_imperfection_2 = mat_nodes.new("ShaderNodeTexNoise")
    noise_add_shape_imperfection_2.parent = frame
    noise_add_shape_imperfection_2.name = "Noise Tex - Add shape imperfection 1"
    noise_add_shape_imperfection_2.label = "Noise Tex - Add shape imperfection 1"
    noise_add_shape_imperfection_2.location = (-3850, -1150)
    noise_add_shape_imperfection_2.inputs["Scale"].default_value = 1.9
    noise_add_shape_imperfection_2.inputs["Detail"].default_value = 16.0
    noise_add_shape_imperfection_2.inputs["Roughness"].default_value = 0.0
    noise_add_shape_imperfection_2.inputs["Distortion"].default_value = 0.0

    mat.node_tree.links.new(noise_add_shape_imperfection_2.outputs["Fac"],
                            color_burn_noises.inputs["Color2"])

    # Vector Add - Coords add shape imperfection 1
    coords_add_shape_imperfection_1 = mat_nodes.new("ShaderNodeVectorMath")
    coords_add_shape_imperfection_1.parent = frame
    coords_add_shape_imperfection_1.location = (-4050, -900)
    coords_add_shape_imperfection_1.name = "Vector Add - Coords add shape imperfection 1"
    coords_add_shape_imperfection_1.label = "Vector Add - Coords add shape imperfection 1"
    coords_add_shape_imperfection_1.operation = "ADD"
    add_shape_imperfection_coords = obj.cloud_settings.add_shape_imperfection_coords
    coords_add_shape_imperfection_1.inputs[1].default_value = add_shape_imperfection_coords

    mat.node_tree.links.new(coords_add_shape_imperfection_1.outputs["Vector"],
                            noise_add_shape_imperfection_1.inputs["Vector"])
    mat.node_tree.links.new(reroute_1.outputs[0],
                            coords_add_shape_imperfection_1.inputs["Vector"])

    # Vector Add - Coords add shape imperfection 2
    coords_add_shape_imperfection_2 = mat_nodes.new("ShaderNodeVectorMath")
    coords_add_shape_imperfection_2.parent = frame
    coords_add_shape_imperfection_2.location = (-4050, -1150)
    coords_add_shape_imperfection_2.name = "Vector Add - Coords add shape imperfection 2"
    coords_add_shape_imperfection_2.label = "Vector Add - Coords add shape imperfection 2"
    coords_add_shape_imperfection_2.operation = "ADD"
    coords_add_shape_imperfection_2.inputs[1].default_value = (5.0, 5.0, 5.0)

    mat.node_tree.links.new(coords_add_shape_imperfection_2.outputs["Vector"],
                            noise_add_shape_imperfection_2.inputs["Vector"])
    mat.node_tree.links.new(reroute_1.outputs[0],
                            coords_add_shape_imperfection_2.inputs["Vector"])
    # --------END ADD BIG IMPERFECTION BRANCH--------


    # --BEGINNING SUBTRACT BIG IMPERFECTION BRANCH---
    frame = mat_nodes.new(type='NodeFrame')
    frame.name = "Subtract shape imperfection"
    frame.label = "Subtract shape imperfection"

    # RGB Color Burn - Combine noises
    color_burn_noises = mat_nodes.new("ShaderNodeMixRGB")
    color_burn_noises.parent = frame
    color_burn_noises.name = "RGB Color Burn - Combine noises"
    color_burn_noises.label = "RGB Color Burn - Combine noises"
    color_burn_noises.location = (-3650, -1500)
    color_burn_noises.blend_type = "BURN"
    color_burn_noises.inputs["Fac"].default_value = 1.0

    mat.node_tree.links.new(color_burn_noises.outputs["Color"],
                            subtract_imperfection.inputs["Color2"])

    # Noise Tex - Subtract shape imperfection 1
    noise_subtract_shape_imperfection_1 = mat_nodes.new("ShaderNodeTexNoise")
    noise_subtract_shape_imperfection_1.parent = frame
    noise_subtract_shape_imperfection_1.name = "Noise Tex - Subtract shape imperfection 1"
    noise_subtract_shape_imperfection_1.label = "Noise Tex - Subtract shape imperfection 1"
    noise_subtract_shape_imperfection_1.location = (-3850, -1500)
    noise_subtract_shape_imperfection_1.inputs["Scale"].default_value = 1.9
    noise_subtract_shape_imperfection_1.inputs["Detail"].default_value = 0.0
    noise_subtract_shape_imperfection_1.inputs["Roughness"].default_value = 0.0

    mat.node_tree.links.new(noise_subtract_shape_imperfection_1.outputs["Fac"],
                            color_burn_noises.inputs["Color1"])

    # Noise Tex - Subtract shape imperfection 2
    noise_subtract_shape_imperfection_2 = mat_nodes.new("ShaderNodeTexNoise")
    noise_subtract_shape_imperfection_2.parent = frame
    noise_subtract_shape_imperfection_2.name = "Noise Tex - Subtract shape imperfection 1"
    noise_subtract_shape_imperfection_2.label = "Noise Tex - Subtract shape imperfection 1"
    noise_subtract_shape_imperfection_2.location = (-3850, -1750)
    noise_subtract_shape_imperfection_2.inputs["Scale"].default_value = 1.9
    noise_subtract_shape_imperfection_2.inputs["Detail"].default_value = 16.0
    noise_subtract_shape_imperfection_2.inputs["Roughness"].default_value = 0.0
    noise_subtract_shape_imperfection_2.inputs["Distortion"].default_value = 0.0

    mat.node_tree.links.new(noise_subtract_shape_imperfection_2.outputs["Fac"],
                            color_burn_noises.inputs["Color2"])

    # Vector Add - Coods subtract shape imperfection 1
    coords_subtract_shape_imperfection_1 = mat_nodes.new("ShaderNodeVectorMath")
    coords_subtract_shape_imperfection_1.parent = frame
    coords_subtract_shape_imperfection_1.location = (-4050, -1500)
    coords_subtract_shape_imperfection_1.name = "Vector Add - Coods subtract shape imperfection 1"
    coords_subtract_shape_imperfection_1.label = "Vector Add - Coods subtract shape imperfection 1"
    coords_subtract_shape_imperfection_1.operation = "ADD"
    subtract_shape_imperfection_coords = obj.cloud_settings.subtract_shape_imperfection_coords
    coords_subtract_shape_imperfection_1.inputs[1].default_value = subtract_shape_imperfection_coords

    mat.node_tree.links.new(coords_subtract_shape_imperfection_1.outputs["Vector"],
                            noise_subtract_shape_imperfection_1.inputs["Vector"])
    mat.node_tree.links.new(reroute_1.outputs[0],
                            coords_subtract_shape_imperfection_1.inputs["Vector"])

    # Vector Add - Add shape imperfection 2
    coords_subtract_shape_imperfection_2 = mat_nodes.new("ShaderNodeVectorMath")
    coords_subtract_shape_imperfection_2.parent = frame
    coords_subtract_shape_imperfection_2.location = (-4050, -1750)
    coords_subtract_shape_imperfection_2.name = "Vector Add - Coods subtract shape imperfection 2"
    coords_subtract_shape_imperfection_2.label = "Vector Add - Coods subtract shape imperfection 2"
    coords_subtract_shape_imperfection_2.operation = "ADD"
    coords_subtract_shape_imperfection_2.inputs[1].default_value = (5.0, 5.0, 5.0)

    mat.node_tree.links.new(coords_subtract_shape_imperfection_2.outputs["Vector"],
                            noise_subtract_shape_imperfection_2.inputs["Vector"])
    mat.node_tree.links.new(reroute_1.outputs[0],
                            coords_subtract_shape_imperfection_2.inputs["Vector"])
    # -----END SUBTRACT BIG IMPERFECTION BRANCH------

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



