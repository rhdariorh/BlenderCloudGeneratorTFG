"""
    cloud_settings.py is part of Cloud Generator Blender Addon.

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
from math import sin, cos, pi


def update_cloud_dimensions(self, context):
    """Cloud dimensions update function.

    It is responsible for transforming and applying transformations according
    to the size and domain custom properties of the cloud.
    """

    obj = context.active_object
    if (obj.cloud_settings.update_properties):
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
    """Cloud position update function.

    Change the position of the cloud within the domain based on
    the domain_cloud_position custom property.
    """

    obj = context.active_object
    if (obj.cloud_settings.update_properties):
        domain_cloud_position = obj.cloud_settings.domain_cloud_position
        material = bpy.context.active_object.active_material
        if "CloudMaterial_CG" not in material.name:
            bpy.ops.error.cloud_error("INVOKE_DEFAULT", error_type="MATERIAL_WRONG_NAME")
        else:
            initial_mapping = material.node_tree.nodes.get("Initial mapping")
            initial_mapping.inputs["Location"].default_value = domain_cloud_position


def update_cloud_density(self, context):
    """Cloud density update function.

    Change the cloud density according to the density custom property.
    """

    obj = context.active_object
    if (obj.cloud_settings.update_properties):
        density = obj.cloud_settings.density
        material = bpy.context.active_object.active_material
        if "CloudMaterial_CG" not in material.name:
            bpy.ops.error.cloud_error("INVOKE_DEFAULT", error_type="MATERIAL_WRONG_NAME")
        else:
            density_color_ramp = material.node_tree.nodes.get("ColorRamp - Cloud Density")
            elem = density_color_ramp.color_ramp.elements[1]
            elem.color = (density, density, density, 1)


def update_cloud_wind(self, context):
    """Cloud wind update function.

    Change the cloud wind according to the wind custom properties.
    """

    obj = context.active_object
    if (obj.cloud_settings.update_properties):
        wind_strength_value = obj.cloud_settings.wind_strength
        wind_big_turbulence = obj.cloud_settings.wind_big_turbulence
        wind_small_turbulence = obj.cloud_settings.wind_small_turbulence
        material = bpy.context.active_object.active_material
        if "CloudMaterial_CG" not in material.name:
            bpy.ops.error.cloud_error("INVOKE_DEFAULT", error_type="MATERIAL_WRONG_NAME")
        else:
            wind_strength = material.node_tree.nodes.get("RGB Add - Shape wind strength")
            wind_strength.inputs[1].default_value = (wind_strength_value, wind_strength_value, wind_strength_value)

            add_shape_wind_big = material.node_tree.nodes.get("Shape wind big turbulence")
            add_shape_wind_big.inputs["Fac"].default_value = wind_big_turbulence

            add_shape_wind_small = material.node_tree.nodes.get("Shape wind small turbulence")
            add_shape_wind_small.inputs["Fac"].default_value = wind_small_turbulence


def update_cloud_wind_turbulence_coords(self, context):
    """Cloud wind turbulence coords (seed) update function.

    Change the cloud wind turbulence coordinates according to the wind_big_turbulence_coords
    and wind_small_turbulence_coords custom properties or wind_turbulence_simple_seed custom
    property. The coordinates act as the seed of the voronoi noise that creates the roundness.
    """

    obj = context.active_object
    if (obj.cloud_settings.update_properties):
        wind_big_turbulence_coords = obj.cloud_settings.wind_big_turbulence_coords
        wind_small_turbulence_coords = obj.cloud_settings.wind_small_turbulence_coords
        wind_turbulence_simple_seed = obj.cloud_settings.wind_turbulence_simple_seed
        material = bpy.context.active_object.active_material
        if "CloudMaterial_CG" not in material.name:
            bpy.ops.error.cloud_error("INVOKE_DEFAULT", error_type="MATERIAL_WRONG_NAME")
        else:
            if (context.preferences.addons["clouds_generator"].preferences.advanced_settings):
                obj.cloud_settings.wind_turbulence_simple_seed = wind_big_turbulence_coords.x
                add_coords_wind_small = material.node_tree.nodes.get("Vector Add - Wind small turbulence coords")
                add_coords_wind_small.inputs[1].default_value = wind_small_turbulence_coords
                add_coords_wind_big = material.node_tree.nodes.get("Vector Add - Wind big turbulence coords")
                add_coords_wind_big.inputs[1].default_value = wind_big_turbulence_coords
            else:
                wind_turbulence_coords = (wind_turbulence_simple_seed,
                                          wind_turbulence_simple_seed,
                                          wind_turbulence_simple_seed)

                add_coords_wind_small = material.node_tree.nodes.get("Vector Add - Wind small turbulence coords")
                add_coords_wind_small.inputs[1].default_value = wind_turbulence_coords
                add_coords_wind_big = material.node_tree.nodes.get("Vector Add - Wind big turbulence coords")
                add_coords_wind_big.inputs[1].default_value = wind_turbulence_coords


def update_cloud_color(self, context):
    """Cloud color update function.

    Change the cloud color according to the color custom property.
    """

    obj = context.active_object
    if (obj.cloud_settings.update_properties):
        color = obj.cloud_settings.color
        material = bpy.context.active_object.active_material
        if "CloudMaterial_CG" not in material.name:
            bpy.ops.error.cloud_error("INVOKE_DEFAULT", error_type="MATERIAL_WRONG_NAME")
        else:
            principled_volume = material.node_tree.nodes.get("Cloud Principled Volume")
            principled_volume.inputs["Color"].default_value = color


def update_cloud_roundness(self, context):
    """Cloud roundness update function.

    Change the cloud roundness according to the roundness custom property.
    """

    obj = context.active_object
    if (obj.cloud_settings.update_properties):
        roundness = obj.cloud_settings.roundness
        material = bpy.context.active_object.active_material
        if "CloudMaterial_CG" not in material.name:
            bpy.ops.error.cloud_error("INVOKE_DEFAULT", error_type="MATERIAL_WRONG_NAME")
        else:
            overlay_roundness = material.node_tree.nodes.get("RGB Overlay - Roundness")
            overlay_roundness.inputs["Fac"].default_value = roundness


def update_cloud_roundness_coords(self, context):
    """Cloud roundness coords (seed) update function.

    Change the cloud roundness coordinates according to the roundness_coords or
    roundness_simple_seed custom property. The coordinates act as the seed of
    the voronoi noise that creates the roundness.
    """

    obj = context.active_object
    if (obj.cloud_settings.update_properties):
        roundness_coords = obj.cloud_settings.roundness_coords
        roundness_simple_seed = obj.cloud_settings.roundness_simple_seed
        material = bpy.context.active_object.active_material
        if "CloudMaterial_CG" not in material.name:
            bpy.ops.error.cloud_error("INVOKE_DEFAULT", error_type="MATERIAL_WRONG_NAME")
        else:
            if (context.preferences.addons["clouds_generator"].preferences.advanced_settings):
                obj.cloud_settings.roundness_simple_seed = roundness_coords.x
                add_coords_roundness = material.node_tree.nodes.get("Vector Add - Roundness coord")
                add_coords_roundness.inputs[1].default_value = roundness_coords
            else:
                roundness_coords = (roundness_simple_seed, roundness_simple_seed, roundness_simple_seed)
                obj.cloud_settings.roundness_coords = roundness_coords
                add_coords_roundness = material.node_tree.nodes.get("Vector Add - Roundness coord")
                add_coords_roundness.inputs[1].default_value = roundness_coords


def update_cloud_height_single(self, context):
    """Cloud height for single cloud update function.

    Change the cloud height in single clouds according
    to the height_single custom property.
    """

    obj = context.active_object
    if (obj.cloud_settings.update_properties):
        cloud_type = obj.cloud_settings.cloud_type
        material = bpy.context.active_object.active_material
        if "CloudMaterial_CG" not in material.name:
            bpy.ops.error.cloud_error("INVOKE_DEFAULT", error_type="MATERIAL_WRONG_NAME")
        elif (cloud_type == "SINGLE_CUMULUS"):
            height_single = 1 - obj.cloud_settings.height_single
            # Angle formed with the join point of the curve
            angle = ((pi/2 - 0.5) * height_single) + 0.3
            direction = Vector((0, 0))
            direction.x = 0.3*cos(angle)
            direction.y = 0.3*sin(angle)

            vector_curves = material.node_tree.nodes.get("Initial Shape Vector Curves")
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
    """Cloud width for single cloud update function.

    Change the cloud width in single clouds according
    to the width_x and width_y custom properties.
    """

    obj = context.active_object
    if (obj.cloud_settings.update_properties):
        cloud_type = obj.cloud_settings.cloud_type
        width_x = obj.cloud_settings.width_x
        width_y = obj.cloud_settings.width_y
        material = bpy.context.active_object.active_material
        if "CloudMaterial_CG" not in material.name:
            bpy.ops.error.cloud_error("INVOKE_DEFAULT", error_type="MATERIAL_WRONG_NAME")
        elif (cloud_type == "SINGLE_CUMULUS"):
            mapping = material.node_tree.nodes.get("Initial Shape Mapping")
            mapping.inputs["Scale"].default_value = (width_x, width_y, 0.7)


def update_cloud_add_shape_imperfection(self, context):
    """Cloud shape imperfection addition update function.

    Change the cloud shape imperfection addition according
    to the add_shape_imperfection custom property.
    """

    obj = context.active_object
    if (obj.cloud_settings.update_properties):
        add_shape_imperfection = obj.cloud_settings.add_shape_imperfection
        material = bpy.context.active_object.active_material
        if "CloudMaterial_CG" not in material.name:
            bpy.ops.error.cloud_error("INVOKE_DEFAULT", error_type="MATERIAL_WRONG_NAME")
        else:
            add_imperfection = material.node_tree.nodes.get("RGB Add - Shape imperfection")
            add_imperfection.inputs["Fac"].default_value = add_shape_imperfection


def update_cloud_add_shape_imperfection_coords(self, context):
    """Cloud shape imperfection addition coords (seed) update function.

    Change the cloud shape imperfection addition coordinates according
    to the add_shape_imperfection_coords  or add_shape_imperfection_simple_seed
    custom property. The coordinates act as the seed of the noise that is added to the volume.
    """

    obj = context.active_object
    if (obj.cloud_settings.update_properties):
        add_shape_imperfection_coords = obj.cloud_settings.add_shape_imperfection_coords
        add_shape_imperfection_simple_seed = obj.cloud_settings.add_shape_imperfection_simple_seed
        material = bpy.context.active_object.active_material
        if "CloudMaterial_CG" not in material.name:
            bpy.ops.error.cloud_error("INVOKE_DEFAULT", error_type="MATERIAL_WRONG_NAME")
        else:
            if (context.preferences.addons["clouds_generator"].preferences.advanced_settings):
                obj.cloud_settings.add_shape_imperfection_simple_seed = add_shape_imperfection_coords.x
                coords_add_shape_imperfection_1 = material.node_tree.nodes.get("Vector Add - Coords add shape imperfection 1")
                coords_add_shape_imperfection_1.inputs[1].default_value = add_shape_imperfection_coords
            else:
                add_shape_imperfection_coords = (add_shape_imperfection_simple_seed,
                                                 add_shape_imperfection_simple_seed,
                                                 add_shape_imperfection_simple_seed)
                obj.cloud_settings.add_shape_imperfection_coords = add_shape_imperfection_coords
                coords_add_shape_imperfection_1 = material.node_tree.nodes.get("Vector Add - Coords add shape imperfection 1")
                coords_add_shape_imperfection_1.inputs[1].default_value = add_shape_imperfection_coords


def update_cloud_subtract_shape_imperfection(self, context):
    """Cloud shape imperfection subtract update function.

    Change the cloud shape imperfection subtract according
    to the subtract_shape_imperfection custom property.
    """

    obj = context.active_object
    if (obj.cloud_settings.update_properties):
        subtract_shape_imperfection = obj.cloud_settings.subtract_shape_imperfection
        material = bpy.context.active_object.active_material
        if "CloudMaterial_CG" not in material.name:
            bpy.ops.error.cloud_error("INVOKE_DEFAULT", error_type="MATERIAL_WRONG_NAME")
        else:
            subtract_imperfection = material.node_tree.nodes.get("RGB Subtract - Shape imperfection")
            subtract_imperfection.inputs["Fac"].default_value = subtract_shape_imperfection


def update_cloud_subtract_shape_imperfection_coords(self, context):
    """Cloud shape imperfection subtract coords (seed) update function.

    Change the cloud shape imperfection subtract coordinates according
    to the subtract_shape_imperfection_coords or subtract_shape_imperfection_simple_seed
    custom property. The coordinates act as the seed of the noise that is subtracted to
    the volume.
    """

    obj = context.active_object
    if (obj.cloud_settings.update_properties):
        subtract_shape_imperfection_coords = obj.cloud_settings.subtract_shape_imperfection_coords
        subtract_shape_imperfection_simple_seed = obj.cloud_settings.subtract_shape_imperfection_simple_seed
        material = bpy.context.active_object.active_material
        if "CloudMaterial_CG" not in material.name:
            bpy.ops.error.cloud_error("INVOKE_DEFAULT", error_type="MATERIAL_WRONG_NAME")
        else:
            if (context.preferences.addons["clouds_generator"].preferences.advanced_settings):
                obj.cloud_settings.subtract_shape_imperfection_simple_seed = subtract_shape_imperfection_coords.x
                coords_subtract_shape_imperfection_1 = material.node_tree.nodes.get("Vector Add - Coods subtract shape imperfection 1")
                coords_subtract_shape_imperfection_1.inputs[1].default_value = subtract_shape_imperfection_coords
            else:
                subtract_shape_imperfection_coords = (subtract_shape_imperfection_simple_seed,
                                                      subtract_shape_imperfection_simple_seed,
                                                      subtract_shape_imperfection_simple_seed)
                obj.cloud_settings.subtract_shape_imperfection_coords = subtract_shape_imperfection_coords
                coords_subtract_shape_imperfection_1 = material.node_tree.nodes.get("Vector Add - Coods subtract shape imperfection 1")
                coords_subtract_shape_imperfection_1.inputs[1].default_value = subtract_shape_imperfection_coords


def update_cloud_detail_bump_strength(self, context):
    """Cloud detail bump strength update function.

    Change the cloud detail bump strength according
    to the detail_bump_strength custom property.
    """

    obj = context.active_object
    if (obj.cloud_settings.update_properties):
        detail_bump_strength = obj.cloud_settings.detail_bump_strength
        material = bpy.context.active_object.active_material
        if "CloudMaterial_CG" not in material.name:
            bpy.ops.error.cloud_error("INVOKE_DEFAULT", error_type="MATERIAL_WRONG_NAME")
        else:
            multiply_bump = material.node_tree.nodes.get("RGB Multiply - Bump")
            multiply_bump.inputs["Fac"].default_value = detail_bump_strength


def update_cloud_detail_bump_levels(self, context):
    """Cloud detail bump levels update function.

    Change the cloud detail bump levels according
    to the detail_bump_levels custom property.
    """

    obj = context.active_object
    if (obj.cloud_settings.update_properties):
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


def update_cloud_detail_wind_strength(self, context):
    """Cloud detail wind update function.

    Change the strength of wind effect in the details.
    """
    obj = context.active_object
    if (obj.cloud_settings.update_properties):
        detail_wind_strength = obj.cloud_settings.detail_wind_strength
        material = bpy.context.active_object.active_material
        if "CloudMaterial_CG" not in material.name:
            bpy.ops.error.cloud_error("INVOKE_DEFAULT", error_type="MATERIAL_WRONG_NAME")
        else:
            add_small_wind = material.node_tree.nodes.get("RGB Add - Small wind")
            add_small_wind.inputs["Fac"].default_value = detail_wind_strength


def update_cloud_detail_noise(self, context):
    """Cloud detail noise update function.

    Change the cloud detail noise according
    to the detail_noise custom property.
    """

    obj = context.active_object
    if (obj.cloud_settings.update_properties):
        detail_noise = obj.cloud_settings.detail_noise
        material = bpy.context.active_object.active_material
        if "CloudMaterial_CG" not in material.name:
            bpy.ops.error.cloud_error("INVOKE_DEFAULT", error_type="MATERIAL_WRONG_NAME")
        else:
            overlay_detail_noise = material.node_tree.nodes.get("RGB Overlay - Noise")
            overlay_detail_noise.inputs["Fac"].default_value = detail_noise


def update_cloud_cleaner_domain_size(self, context):
    """Cloud cleaner domain size function.

    Change the cloud cleaner domain size according
    to the cleaner_domain_size custom property.
    """

    obj = context.active_object
    if (obj.cloud_settings.update_properties):
        cleaner_domain_size = obj.cloud_settings.cleaner_domain_size
        material = bpy.context.active_object.active_material
        if "CloudMaterial_CG" not in material.name:
            bpy.ops.error.cloud_error("INVOKE_DEFAULT", error_type="MATERIAL_WRONG_NAME")
        else:
            color_ramp_cleaner = material.node_tree.nodes.get("Final cleaning range")
            elem = color_ramp_cleaner.color_ramp.elements[0]
            elem.position = 1.01 - cleaner_domain_size


def update_cloud_amount_of_clouds(self, context):
    """Amount of clouds in cloudscape update function.

    Change the amount of clouds in cloudscape according
    to the amount_of_clouds custom property.
    """

    obj = context.active_object
    if (obj.cloud_settings.update_properties):
        amount_of_clouds = 1 - obj.cloud_settings.amount_of_clouds
        material = bpy.context.active_object.active_material
        if "CloudMaterial_CG" not in material.name:
            bpy.ops.error.cloud_error("INVOKE_DEFAULT", error_type="MATERIAL_WRONG_NAME")
        else:
            subtract_gradient_noise = material.node_tree.nodes.get("RGB Subtract - Gradient and Noise")
            subtract_gradient_noise.inputs["Fac"].default_value = amount_of_clouds


def update_cloud_cloudscape_cloud_size(self, context):
    """Cloudscape cloud size update function.

    Change the size of the clouds in the cloudscape according
    to the cloudscape_cloud_size custom property.
    """

    obj = context.active_object
    if (obj.cloud_settings.update_properties):
        cloudscape_cloud_size = 10.1 - obj.cloud_settings.cloudscape_cloud_size
        material = bpy.context.active_object.active_material
        if "CloudMaterial_CG" not in material.name:
            bpy.ops.error.cloud_error("INVOKE_DEFAULT", error_type="MATERIAL_WRONG_NAME")
        else:
            noise_subtract = material.node_tree.nodes.get("Noise Tex - Subtract initial")
            noise_subtract.inputs["Scale"].default_value = cloudscape_cloud_size


def update_cloud_cloudscape_noise_coords(self, context):
    """Cloudscape noise coords update function.

    Change the cloudscape noise coords coordinates according
    to the cloudscape_noise_coords custom property.
    The coordinates act as the seed of the clodscape.
    """

    obj = context.active_object
    if (obj.cloud_settings.update_properties):
        cloud_type = obj.cloud_settings.cloud_type
        cloudscape_noise_coords = obj.cloud_settings.cloudscape_noise_coords
        cloudscape_noise_simple_seed = obj.cloud_settings.cloudscape_noise_simple_seed
        material = bpy.context.active_object.active_material
        if "CloudMaterial_CG" not in material.name:
            bpy.ops.error.cloud_error("INVOKE_DEFAULT", error_type="MATERIAL_WRONG_NAME")
        elif (cloud_type == "CLOUDSCAPE_CUMULUS"):
            if (context.preferences.addons["clouds_generator"].preferences.advanced_settings):
                obj.cloud_settings.cloudscape_noise_simple_seed = cloudscape_noise_coords.x
                mapping_noise = material.node_tree.nodes.get("Initial Shape Mapping Noise")
                mapping_noise.inputs["Location"].default_value = cloudscape_noise_coords
            else:
                cloudscape_noise_coords = (cloudscape_noise_simple_seed,
                                           cloudscape_noise_simple_seed,
                                           cloudscape_noise_simple_seed)
                obj.cloud_settings.cloudscape_noise_coords = cloudscape_noise_coords

                mapping_noise = material.node_tree.nodes.get("Initial Shape Mapping Noise")
                mapping_noise.inputs["Location"].default_value = cloudscape_noise_coords


def update_cloud_height_cloudscape(self, context):
    """Cloudscape height update function.

    Change the cloudscape height according
    to the height_cloudscape custom property.
    """

    obj = context.active_object
    if (obj.cloud_settings.update_properties):
        cloud_type = obj.cloud_settings.cloud_type
        height_cloudscape = obj.cloud_settings.height_cloudscape
        material = bpy.context.active_object.active_material
        if "CloudMaterial_CG" not in material.name:
            bpy.ops.error.cloud_error("INVOKE_DEFAULT", error_type="MATERIAL_WRONG_NAME")
        elif (cloud_type in ["CLOUDSCAPE_CUMULUS", "CLOUDSCAPE_CIRRUS"]):
            mapping_subtract = material.node_tree.nodes.get("Initial Shape Mapping Subtract")
            mapping_subtract.inputs["Location"].default_value = (-height_cloudscape, 0.0, 0.0)


def update_cloud_cut_softness_cloudscape(self, context):
    """Cloudscape cut softness update function.

    Change the softness in the top and bottom cloud cuts.
    """

    obj = context.active_object
    if (obj.cloud_settings.update_properties):
        cloud_type = obj.cloud_settings.cloud_type
        bottom_softness_cloudscape = obj.cloud_settings.bottom_softness_cloudscape
        top_softness_cloudscape = obj.cloud_settings.top_softness_cloudscape
        material = bpy.context.active_object.active_material
        if "CloudMaterial_CG" not in material.name:
            bpy.ops.error.cloud_error("INVOKE_DEFAULT", error_type="MATERIAL_WRONG_NAME")
        elif cloud_type == "CLOUDSCAPE_CUMULUS":
            color_ramp_gradient_base = material.node_tree.nodes.get("ColorRamp - Gradient Base")
            elem = color_ramp_gradient_base.color_ramp.elements[1]
            elem.position = bottom_softness_cloudscape

            color_ramp_gradient_subtract = material.node_tree.nodes.get("ColorRamp - Gradient Subtract")
            elem = color_ramp_gradient_subtract.color_ramp.elements[1]
            elem.position = top_softness_cloudscape


def update_cloud_use_shape_texture(self, context):
    """Use image texture shape update function.

    Changes needed if a image texture is to be used or not
    to shape a cloudscape.
    """

    obj = context.active_object
    if (obj.cloud_settings.update_properties):
        cloud_type = obj.cloud_settings.cloud_type
        material = bpy.context.active_object.active_material
        if "CloudMaterial_CG" not in material.name:
            bpy.ops.error.cloud_error("INVOKE_DEFAULT", error_type="MATERIAL_WRONG_NAME")
        elif (cloud_type in ["CLOUDSCAPE_CUMULUS", "CLOUDSCAPE_CIRRUS"]):
            use_shape_texture = obj.cloud_settings.use_shape_texture
            texture_image_shape_multiply = material.node_tree.nodes.get("RGB Multiply - Texture image shape")
            if use_shape_texture:
                texture_image_shape_multiply.inputs["Fac"].default_value = 1.0
            else:
                texture_image_shape_multiply.inputs["Fac"].default_value = 0.0


def update_cloud_shape_texture_image(self, context):
    """Image for shape cloudscape update function.

    Changes needed if the image texture to shape a cloudscape
    is modified.
    """

    obj = context.active_object
    if (obj.cloud_settings.update_properties):
        cloud_type = obj.cloud_settings.cloud_type
        material = bpy.context.active_object.active_material
        if "CloudMaterial_CG" not in material.name:
            bpy.ops.error.cloud_error("INVOKE_DEFAULT", error_type="MATERIAL_WRONG_NAME")
        elif (cloud_type in ["CLOUDSCAPE_CUMULUS", "CLOUDSCAPE_CIRRUS"]):
            shape_texture_image = obj.cloud_settings.shape_texture_image
            image_texture_shape = material.node_tree.nodes.get("Image texture - Shape of cloud")
            image_texture_shape.image = shape_texture_image


def update_cloud_cirrus(self, context):
    """Cirrus properties update function."""

    obj = context.active_object
    if (obj.cloud_settings.update_properties):
        cloud_type = obj.cloud_settings.cloud_type
        material = bpy.context.active_object.active_material
        if "CloudMaterial_CG" not in material.name:
            bpy.ops.error.cloud_error("INVOKE_DEFAULT", error_type="MATERIAL_WRONG_NAME")
        elif (cloud_type == "CLOUDSCAPE_CIRRUS"):
            cloudscape_cirrus_cirrus_amount = obj.cloud_settings.cloudscape_cirrus_cirrus_amount
            mapping_cirrus_shape = material.node_tree.nodes.get("Initial Shape Mapping Cirrus Shape")
            mapping_cirrus_shape.inputs["Scale"].default_value = (cloudscape_cirrus_cirrus_amount, 0, 0)

            cloudscape_cirrus_cirrus_width = 1 - obj.cloud_settings.cloudscape_cirrus_cirrus_width
            multiply_for_width_operation_cirrus = material.node_tree.nodes.get("Vector Multiply - Cirrus shape width operation")
            multiply_for_width_operation_cirrus.inputs[1].default_value = (cloudscape_cirrus_cirrus_width,
                                                                           cloudscape_cirrus_cirrus_width,
                                                                           cloudscape_cirrus_cirrus_width)


class CloudSettings(bpy.types.PropertyGroup):
    """Custom properties for clouds

    Attributes:
        is_cloud: The object is a cloud or not. Useful for displaying elements
            in the interface.

        update_properties: For internal use of the addon. If it is set to false
            the update functions of the properties does nothing.

        color: Color of the cloud volume.

        cloud_type: Specific cloud type

        size: Size of the cloud within the domain.

        domain: Size of the domain where the cloud is render.
            It corresponds to the size of the object.

        domain_cloud_position: Position of the cloud within the domain.

        density: Density of the cloud volume.

        wind_strength: Wind effect strength.

        wind_big_turbulence: Amount of big size turbulence in wind

        wind_small_turbulence: Amount of small size turbulence in wind

        wind_big_turbulence_coords: Mapping coordinates for wind big turbulence.
            It is used as a seed.

        wind_small_turbulence_coords: Mapping coordinates for wind small turbulence.
            It is used as a seed.

        wind_turbulence_simple_seed: Sets the value of this property as the value of the
        three mapping coordinates for both wind big and small turbulence coordinates.

        roundness: Strength of the effect of roughly rounded shapes in
            the cloud.

        roundness_coords: Mapping coordinates for roundness.
            Useful to change the shape of roundness, it is used as a seed.

        height_single: Vertical length of cloud for single clouds.

        width_x: Cloud length in X axis for single clouds.

        width_y: Cloud length in Y axis for single clouds.

        add_shape_imperfection: Amount of imperfectons added to the general
            shape of the cloud.

        add_shape_imperfection_coords: Mapping coordinates for add shape
            imperfection. Useful to change the shape of imperfections,
            it is used as a seed.

        subtract_shape_imperfection: Amount of imperfectons subtracted to
            the general shape of the cloud.

        subtract_shape_imperfection_coords: Mapping coordinates for subtract
            shape imperfection. Useful to change the shape of imperfections,
            it is used as a seed.

        detail_bump_strength: Strength of bump rounded effect. Similar to
            the roundness effect but on a smaller scale to add detail to
            the cloud.

        detail_bump_levels: Number of bump levels. Each level adds a
            smaller bump.

        detail_wind_strength: Strength of wind effect in the details.

        detail_noise: Amount of noise added to the entire cloud.

        cleaner_domain_size: Cleaning domain size.
            Useful to clean unwanted noise from areas outside the cloud.

        amount_of_clouds: Amount of clouds in a cloudscape. The less amount
            of clouds, the more noise is subtracted from the volume.

        height_cloudscape: Vertical length of clouds for cloudscapes.

        bottom_softness_cloudscape: Softness in the cloud cut at the bottom.

        top_softness_cloudscape: Softness in the cloud cut at the top.

        cloudscape_cloud_size: Size of the clouds in the cloudscape.

        cloudscape_noise_coords: Mapping coordinates for cloudscape shape.
            Used as a seed for the noise that shapes the cloudscaoe.

        cloudscape_noise_simple_seed: Sets the value of this property as the value of the
            three mapping coordinates for the cloudscape noise coordinates

        use_shape_texture: Indicates if a image texture is used to shape
            the cloudscape.

        shape_texture_image: Image used to shape a cloud with a Image Texture.

        cloudscape_cirrus_cirrus_amount: Amount of cirrus. A higher value will increase the
            density of cirrus clouds in the cloudscape.

        cloudscape_cirrus_cirrus_width: Width of the cirrus in a cloudscape.

    """

    is_cloud: bpy.props.BoolProperty(
        name="Is cloud",
        description="Indicates if the object is a cloud",
        default=False
    )

    update_properties: bpy.props.BoolProperty(
        name="Use update properties function",
        description="For internal use of the addon. " +
                    "If it is set to false the update " +
                    "functions of the properties does nothing",
        default=True
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
        description="Size of the cloud within the domain",
        default=10,
        min=0.01,
        update=update_cloud_dimensions
    )

    domain: bpy.props.FloatVectorProperty(
        name="Cloud domain size",
        description="Size of the domain where the cloud is render. " +
                    "It corresponds to the size of the object",
        subtype="TRANSLATION",
        default=(30.0, 30.0, 30.0),
        update=update_cloud_dimensions
    )

    domain_cloud_position: bpy.props.FloatVectorProperty(
        name="Position in domain",
        description="Position of the cloud within the domain",
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

    wind_strength: bpy.props.FloatProperty(
        name="Cloud wind strength",
        description="Amount of wind effect added to the cloud",
        default=1.0,
        min=1.0,
        soft_max=5.0,
        update=update_cloud_wind
    )

    wind_big_turbulence: bpy.props.FloatProperty(
        name="Cloud wind big turbulence",
        description="Amount of big size turbulence in wind",
        default=0.0,
        min=0.0,
        max=1.0,
        update=update_cloud_wind
    )

    wind_small_turbulence: bpy.props.FloatProperty(
        name="Cloud wind small turbulence",
        description="Amount of small size turbulence in wind",
        default=0.0,
        min=0.0,
        max=1.0,
        update=update_cloud_wind
    )

    wind_big_turbulence_coords: bpy.props.FloatVectorProperty(
        name="Cloud wind big turbulence coordinates",
        description="Mapping coordinates for wind big turbulence. " +
                    "It is used as a seed.",
        subtype="XYZ",
        default=(0.0, 0.0, 0.0),
        update=update_cloud_wind_turbulence_coords
    )

    wind_small_turbulence_coords: bpy.props.FloatVectorProperty(
        name="Cloud wind small turbulence coordinates",
        description="Mapping coordinates for wind small turbulence. " +
                    "It is used as a seed.",
        subtype="XYZ",
        default=(0.0, 0.0, 0.0),
        update=update_cloud_wind_turbulence_coords
    )

    wind_turbulence_simple_seed: bpy.props.FloatProperty(
        name="Cloud wind turbulence simple seed",
        description="Sets the value of this property as the value of the " +
        "three mapping coordinates for both wind big and small turbulence coordinates",
        default=0.0,
        update=update_cloud_wind_turbulence_coords
    )

    roundness: bpy.props.FloatProperty(
        name="Cloud roundness",
        description="Strength of the effect of rounded shapes " +
                    "in the cloud",
        default=0.5,
        min=0.0,
        max=1.0,
        update=update_cloud_roundness
    )

    roundness_coords: bpy.props.FloatVectorProperty(
        name="Cloud roundness coordinates",
        description="Mapping coordinates for roundness. " +
                    "Useful to change the shape of roundness, " +
                    "it is used as a seed.",
        subtype="XYZ",
        default=(0.0, 0.0, 0.0),
        update=update_cloud_roundness_coords
    )

    roundness_simple_seed: bpy.props.FloatProperty(
        name="Roundness simple seed",
        description="Sets the value of this property as the value of the " +
        "three mapping coordinates for roundness coordinates",
        default=0.0,
        update=update_cloud_roundness_coords
    )

    height_single: bpy.props.FloatProperty(
        name="Cloud height",
        description="Vertical length of cloud for single clouds",
        default=0.3,
        min=0,
        max=1,
        update=update_cloud_height_single
    )

    width_x: bpy.props.FloatProperty(
        name="Cloud X width",
        description="Cloud length in X axis for single clouds",
        default=0.7,
        min=0.1,
        max=10.0,
        update=update_cloud_width
    )

    width_y: bpy.props.FloatProperty(
        name="Cloud Y width",
        description="Cloud length in Y axis for single clouds",
        default=0.7,
        min=0.1,
        max=10.0,
        update=update_cloud_width
    )

    add_shape_imperfection: bpy.props.FloatProperty(
        name="Cloud add shape imperfection",
        description="Amount of imperfectons added to the general shape " +
                    "of the cloud",
        default=0.2,
        min=0.0,
        max=1.0,
        update=update_cloud_add_shape_imperfection
    )

    add_shape_imperfection_coords: bpy.props.FloatVectorProperty(
        name="Cloud add shape imperfection coordinates",
        description="Mapping coordinates for add shape imperfection. " +
                    "Useful to change the shape of imperfections, " +
                    "it is used as a seed.",
        subtype="XYZ",
        default=(0.0, 0.0, 0.0),
        update=update_cloud_add_shape_imperfection_coords
    )

    add_shape_imperfection_simple_seed: bpy.props.FloatProperty(
        name="Cloud add shape imperfection simple seed",
        description="Sets the value of this property as the value of the " +
        "three mapping coordinates for add shape imperfection",
        default=0.0,
        update=update_cloud_add_shape_imperfection_coords
    )

    subtract_shape_imperfection: bpy.props.FloatProperty(
        name="Cloud subtract shape imperfection",
        description="Amount of imperfectons subtracted to the general shape " +
                    "of the cloud",
        default=0.1,
        min=0.0,
        max=1.0,
        update=update_cloud_subtract_shape_imperfection
    )

    subtract_shape_imperfection_coords: bpy.props.FloatVectorProperty(
        name="Cloud subtract shape imperfection coordinates",
        description="Mapping coordinates for subtract shape imperfection. " +
                    "Useful to change the shape of imperfections, " +
                    "it is used as a seed.",
        subtype="XYZ",
        default=(5.0, 5.0, 5.0),
        update=update_cloud_subtract_shape_imperfection_coords
    )

    subtract_shape_imperfection_simple_seed: bpy.props.FloatProperty(
        name="Cloud subtract shape imperfection simple seed",
        description="Sets the value of this property as the value of the " +
        "three mapping coordinates for subtract shape imperfection",
        default=0.0,
        update=update_cloud_subtract_shape_imperfection_coords
    )

    detail_bump_strength: bpy.props.FloatProperty(
        name="Cloud detail bump strength",
        description="Strength of bump rounded effect. Similar to the " +
                    "roundness effect but on a smaller scale to add detail " +
                    "to the cloud",
        default=0.2,
        min=0.0,
        max=1.0,
        update=update_cloud_detail_bump_strength
    )

    detail_bump_levels: bpy.props.IntProperty(
        name="Cloud detail bump LOD",
        description="Number of bump levels. Each level adds a smaller bump",
        default=3,
        min=1,
        max=3,
        update=update_cloud_detail_bump_levels
    )

    detail_wind_strength: bpy.props.FloatProperty(
        name="Cloud detail wind strength",
        description="Strength of wind effect in the details",
        default=0.5,
        min=0.0,
        max=1.0,
        update=update_cloud_detail_wind_strength
    )

    detail_noise: bpy.props.FloatProperty(
        name="Detail noise",
        description="Amount of noise added to the entire cloud",
        default=0.05,
        min=0.0,
        max=1.0,
        update=update_cloud_detail_noise
    )

    cleaner_domain_size: bpy.props.FloatProperty(
        name="Cleaner domain size",
        description="Cleaning domain size. Useful to clean unwanted " +
                    "noise from areas outside the cloud",
        default=0.06,
        min=0.001,
        max=1.0,
        update=update_cloud_cleaner_domain_size
    )

    amount_of_clouds: bpy.props.FloatProperty(
        name="Amount of clouds",
        description="Amount of clouds in a cloudscape. The less amount " +
                    "of clouds, the more noise is subtracted from the volume.",
        default=0.4,
        min=0.0,
        max=1.0,
        update=update_cloud_amount_of_clouds
    )

    height_cloudscape: bpy.props.FloatProperty(
        name="Cloudscape cloud height",
        description="Vertical length of clouds for cloudscapes",
        default=1.2,
        min=0.0,
        soft_max=10.0,
        update=update_cloud_height_cloudscape
    )

    bottom_softness_cloudscape: bpy.props.FloatProperty(
        name="Cloudscape bottom softness",
        description="Softness in the cloud cut at the bottom",
        default=0.2,
        min=0.1,
        max=1.0,
        update=update_cloud_cut_softness_cloudscape
    )

    top_softness_cloudscape: bpy.props.FloatProperty(
        name="Cloudscape top softness",
        description="Softness in the cloud cut at the top",
        default=0.5,
        min=0.1,
        max=1.0,
        update=update_cloud_cut_softness_cloudscape
    )

    cloudscape_cloud_size: bpy.props.FloatProperty(
        name="Cloudscape cloud size",
        description="Size of the clouds in the cloudscape",
        default=8.5,
        min=0.0,
        max=10.0,
        update=update_cloud_cloudscape_cloud_size
    )

    cloudscape_noise_coords: bpy.props.FloatVectorProperty(
        name="Cloud cloudscape noise coordinates",
        description="Mapping coordinates for cloudscape shape. " +
                    "Used as a seed for the noise that shapes the cloudscape",
        subtype="XYZ",
        default=(0.0, 0.0, 0.0),
        update=update_cloud_cloudscape_noise_coords
    )

    cloudscape_noise_simple_seed: bpy.props.FloatProperty(
        name="Cloudscape simple seed",
        description="Sets the value of this property as the value of the " +
        "three mapping coordinates for the cloudscape noise coordinates",
        default=0.0,
        update=update_cloud_cloudscape_noise_coords
    )

    use_shape_texture: bpy.props.BoolProperty(
        name="To use texture shape",
        description="Indicates if a image texture is used to shape " +
        "the cloudscape",
        default=False,
        update=update_cloud_use_shape_texture
    )

    shape_texture_image: bpy.props.PointerProperty(
        name="Shape texture image",
        description="Image used to shape a cloud with a Image Texture",
        type=bpy.types.Image,
        update=update_cloud_shape_texture_image
    )

    cloudscape_cirrus_cirrus_amount: bpy.props.FloatProperty(
        name="Amount of cirrus",
        description="Amount of cirrus. A higher value will increase the " +
        "density of cirrus clouds in the cloudscape",
        default=10.0,
        min=0.0,
        update=update_cloud_cirrus
    )

    cloudscape_cirrus_cirrus_width: bpy.props.FloatProperty(
        name="Cirrus width",
        description="Width of the cirrus in a cloudscape",
        default=0.5,
        min=0.0,
        max=1.0,
        update=update_cloud_cirrus
    )
