import bpy
from mathutils import Vector

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
        default=(5.0, 5.0, 5.0),
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