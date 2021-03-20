import bpy
from mathutils import Vector
from math import sin, cos, pi

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

def update_cloud_domain_cloud_position(self, context):
    obj = context.active_object
    domain_cloud_position = obj.cloud_settings.domain_cloud_position
    material = bpy.context.active_object.active_material
    if "CloudMaterial_CG" not in material.name:
        bpy.ops.error.cloud_error("INVOKE_DEFAULT", error_type="MATERIAL_WRONG_NAME")
    else:
        initial_mapping = material.node_tree.nodes.get("Initial mapping")
        initial_mapping.inputs["Location"].default_value = domain_cloud_position

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

def update_cloud_color(self, context):
    obj = context.active_object
    color = obj.cloud_settings.color
    material = bpy.context.active_object.active_material
    if "CloudMaterial_CG" not in material.name:
        bpy.ops.error.cloud_error("INVOKE_DEFAULT", error_type="MATERIAL_WRONG_NAME")
    else:
        principled_volume = material.node_tree.nodes.get("Cloud Principled Volume")
        principled_volume.inputs["Color"].default_value = color

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

def update_cloud_height_single(self, context):
    obj = context.active_object
    cloud_type = obj.cloud_settings.cloud_type
    height_single = 1 - obj.cloud_settings.height_single
    angle = ((pi/2 - 0.5) * height_single) + 0.3
    material = bpy.context.active_object.active_material
    if "CloudMaterial_CG" not in material.name:
        bpy.ops.error.cloud_error("INVOKE_DEFAULT", error_type="MATERIAL_WRONG_NAME")
    elif (cloud_type == "SINGLE_CUMULUS"):
        direction = Vector((0, 0))
        direction.x = 0.3*cos(angle)
        direction.y = 0.3*sin(angle)

        vector_curves = material.node_tree.nodes.get("Initial Shape Vector Curves")
        join_point = vector_curves.mapping.curves[2].points[1].location
        last_point = join_point + direction
        vector_curves.mapping.curves[2].points[2].location = (last_point.x, last_point.y)
        vector_curves.mapping.update()

        vector_curves = material.node_tree.nodes.get("Final Cleaner Vector Curves")
        join_point = vector_curves.mapping.curves[2].points[1].location
        last_point = join_point + direction
        vector_curves.mapping.curves[2].points[2].location = (last_point.x, last_point.y)
        vector_curves.mapping.update()

        # Blender is bugged and when the vector curves changes the shader is not updated
        # so I update another property to update the shader:
        roundness = obj.cloud_settings.roundness
        overlay_roundness = material.node_tree.nodes.get("RGB Overlay - Roundness")
        overlay_roundness.inputs["Fac"].default_value = roundness

def update_cloud_width(self, context):
    obj = context.active_object
    cloud_type = obj.cloud_settings.cloud_type
    width_x = obj.cloud_settings.width_x
    width_y = obj.cloud_settings.width_y
    material = bpy.context.active_object.active_material
    if "CloudMaterial_CG" not in material.name:
        bpy.ops.error.cloud_error("INVOKE_DEFAULT", error_type="MATERIAL_WRONG_NAME")
    elif (cloud_type == "SINGLE_CUMULUS"):
        mapping = material.node_tree.nodes.get("Initial Shape Mapping")
        mapping.inputs["Scale"].default_value = (width_x, width_y, 0.7)

        mapping = material.node_tree.nodes.get("Final Cleaner Shape Mapping")
        mapping.inputs["Scale"].default_value = (width_x, width_y, 0.7)

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

def update_cloud_cleaner_domain_size(self, context):
    obj = context.active_object
    cleaner_domain_size = obj.cloud_settings.cleaner_domain_size
    material = bpy.context.active_object.active_material
    if "CloudMaterial_CG" not in material.name:
        bpy.ops.error.cloud_error("INVOKE_DEFAULT", error_type="MATERIAL_WRONG_NAME")
    else:
        color_ramp_cleaner = material.node_tree.nodes.get("Final cleaning range")
        elem = color_ramp_cleaner.color_ramp.elements[0]
        elem.position = 1.01 - cleaner_domain_size

def update_cloud_amount_of_clouds(self, context):
    obj = context.active_object
    amount_of_clouds = 1 - obj.cloud_settings.amount_of_clouds
    material = bpy.context.active_object.active_material
    if "CloudMaterial_CG" not in material.name:
        bpy.ops.error.cloud_error("INVOKE_DEFAULT", error_type="MATERIAL_WRONG_NAME")
    else:
        subtract_gradient_noise = material.node_tree.nodes.get("RGB Subtract - Gradient and Noise")
        subtract_gradient_noise.inputs["Fac"].default_value = amount_of_clouds
        subtract_gradient_noise = material.node_tree.nodes.get("RGB Subtract - Gradient and Noise Final Cleaner")
        subtract_gradient_noise.inputs["Fac"].default_value = amount_of_clouds

def update_cloud_landscape_cloud_size(self, context):
    obj = context.active_object
    landscape_cloud_size = 10.1 - obj.cloud_settings.landscape_cloud_size
    material = bpy.context.active_object.active_material
    if "CloudMaterial_CG" not in material.name:
        bpy.ops.error.cloud_error("INVOKE_DEFAULT", error_type="MATERIAL_WRONG_NAME")
    else:
        noise_subtract = material.node_tree.nodes.get("Noise Tex - Subtract initial")
        noise_subtract.inputs["Scale"].default_value = landscape_cloud_size
        noise_subtract = material.node_tree.nodes.get("Noise Tex - Subtract initial Final Cleaner")
        noise_subtract.inputs["Scale"].default_value = landscape_cloud_size

def update_cloud_landscape_noise_coords(self, context):
    obj = context.active_object
    cloud_type = obj.cloud_settings.cloud_type
    landscape_noise_coords = obj.cloud_settings.landscape_noise_coords
    material = bpy.context.active_object.active_material
    if "CloudMaterial_CG" not in material.name:
        bpy.ops.error.cloud_error("INVOKE_DEFAULT", error_type="MATERIAL_WRONG_NAME")
    elif (cloud_type == "LANDSCAPE_CUMULUS"):
        mapping_noise = material.node_tree.nodes.get("Initial Shape Mapping Noise")
        mapping_noise.inputs["Location"].default_value = landscape_noise_coords

        mapping_noise = material.node_tree.nodes.get("Final Cleaner Mapping Noise")
        mapping_noise.inputs["Location"].default_value = landscape_noise_coords

def update_cloud_height_landscape(self, context):
    obj = context.active_object
    cloud_type = obj.cloud_settings.cloud_type
    height_landscape = obj.cloud_settings.height_landscape
    material = bpy.context.active_object.active_material
    if "CloudMaterial_CG" not in material.name:
        bpy.ops.error.cloud_error("INVOKE_DEFAULT", error_type="MATERIAL_WRONG_NAME")
    elif (cloud_type == "LANDSCAPE_CUMULUS"):
        mapping_subtract = material.node_tree.nodes.get("Initial Shape Mapping Subtract")
        mapping_subtract.inputs["Location"].default_value = (-height_landscape ,0.0, 0.0)

        mapping_subtract = material.node_tree.nodes.get("Final Cleaner Mapping Subtract")
        mapping_subtract.inputs["Location"].default_value = (-height_landscape ,0.0, 0.0)

class CloudSettings(bpy.types.PropertyGroup):
    is_cloud: bpy.props.BoolProperty(
        name="Is cloud",
        description="Indicates if the object is a cloud",
        default=False
    )

    color: bpy.props.FloatVectorProperty(
        name="Cloud color",
        description="Color of the cloud volume",
        subtype="COLOR",
        size=4,
        default=(1.0, 1.0, 1.0, 1.0),
        update=update_cloud_color
    )

    cloud_type: bpy.props.StringProperty(
        name="Cloud type",
        description="Indicates the cloud type",
        default="NONE"
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

    domain_cloud_position: bpy.props.FloatVectorProperty(
        name="Position in domain",
        description="Position of the cloud inside the domain",
        subtype="XYZ",
        default=(0.0, 0.0, 0.0),
        update=update_cloud_domain_cloud_position
    )

    density: bpy.props.FloatProperty(
        name="Cloud density",
        description="Amount of light absorbed by the cloud",
        default=1.0,
        min=0.0,
        soft_max=5.0,
        update=update_cloud_density
    )

    wind: bpy.props.FloatProperty(
        name="Cloud wind",
        description="Wind effect",
        default=0.0,
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

    height_single: bpy.props.FloatProperty(
        name="Cloud height",
        description="Cloud length vertically",
        default=0.3,
        min=0,
        max= 1,
        update=update_cloud_height_single
    )

    width_x: bpy.props.FloatProperty(
        name="Cloud X width",
        description="Cloud length in X axis for single clouds",
        default=0.7,
        min=0.1,
        max= 10.0,
        update=update_cloud_width
    )

    width_y: bpy.props.FloatProperty(
        name="Cloud Y width",
        description="Cloud length in Y axis for single clouds",
        default=0.7,
        min=0.1,
        max= 10.0,
        update=update_cloud_width
    )

    add_shape_imperfection: bpy.props.FloatProperty(
        name="Cloud add shape imperfection",
        description="Add imperfection to the general shape",
        default=0.2,
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
        default=0.2,
        min=0.0,
        max=1.0,
        update=update_cloud_detail_bump_strength
    )

    detail_bump_levels: bpy.props.IntProperty(
        name="Cloud detail bump LOD",
        description="Number of bump levels",
        default=3,
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

    cleaner_domain_size: bpy.props.FloatProperty(
        name="Cleaner domain size",
        description="Size of the domain where the cloud is cleaned",
        default=0.06,
        min=0.001,
        max=1.0,
        update=update_cloud_cleaner_domain_size
    )

    amount_of_clouds: bpy.props.FloatProperty(
        name="Amount of clouds",
        description="Amount of clouds in landscape clouds",
        default=0.4,
        min=0.0,
        max=1.0,
        update=update_cloud_amount_of_clouds
    )

    height_landscape: bpy.props.FloatProperty(
        name="Landscape cloud height",
        description="Landscape length vertically",
        default=1.2,
        min=0.0,
        soft_max=10.0,
        update=update_cloud_height_landscape
    )

    landscape_cloud_size: bpy.props.FloatProperty(
        name="Landscape cloud size",
        description="Size of the clouds in the landscape",
        default=8.5,
        min=0.0,
        max=10.0,
        update=update_cloud_landscape_cloud_size
    )

    landscape_noise_coords: bpy.props.FloatVectorProperty(
        name="Cloud landscape noise coordinates",
        description="Mapping coordinates for landscape noise coordinates",
        subtype="XYZ",
        default=(0.0, 0.0, 0.0),
        update=update_cloud_landscape_noise_coords
    )