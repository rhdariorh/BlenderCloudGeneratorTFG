import bpy
from mathutils import Vector
from math import sin, cos, pi
import random


def initial_shape_single_cumulus(pos_x, pos_y, texture_coordinate, out_node, in_node, mat, mat_nodes, obj, cleaner):
    """
    out_node: nodo de salida
    in_node: nodo de entrada
    """
    obj.cloud_settings.cloud_type = "SINGLE_CUMULUS"
    frame = mat_nodes.new(type='NodeFrame')
    frame.name = "Initial shape"
    frame.label = "Initial shape"

    if cleaner:
        # Color Ramp
        color_ramp_cleaner = mat_nodes.new("ShaderNodeValToRGB")
        color_ramp_cleaner.parent = frame
        color_ramp_cleaner.name = "Final cleaning range"
        color_ramp_cleaner.label = "Final cleaning range"
        color_ramp_cleaner.location = (pos_x + 900, pos_y)
        color_ramp_cleaner.color_ramp.interpolation = 'LINEAR'
        elem = color_ramp_cleaner.color_ramp.elements[0]
        elem.position = 1.0 - obj.cloud_settings.cleaner_domain_size
        elem.color = (0, 0, 0, 1)
        elem = color_ramp_cleaner.color_ramp.elements[1]
        elem.position = 1.0
        elem.color = (1.0, 1.0, 1.0, 1)

        mat.node_tree.links.new(color_ramp_cleaner.outputs["Color"],
                                out_node.inputs["Color2"])

        # Invert color
        invert_color = mat_nodes.new("ShaderNodeInvert")
        invert_color.parent = frame
        invert_color.location = (pos_x + 700, pos_y)
        mat.node_tree.links.new(invert_color.outputs["Color"],
                                color_ramp_cleaner.inputs["Fac"])

    # Gradient Texture
    gradient_texture = mat_nodes.new("ShaderNodeTexGradient")
    gradient_texture.parent = frame
    if cleaner:
        gradient_texture.name = "Final Cleaner Gradient Texture"
    else:
        gradient_texture.name = "Initial Shape Gradient Texture"
    gradient_texture.location = (pos_x + 500, pos_y)
    gradient_texture.gradient_type = "SPHERICAL"

    if cleaner:
        mat.node_tree.links.new(gradient_texture.outputs["Color"],
                                invert_color.inputs["Color"])
    else:
        mat.node_tree.links.new(gradient_texture.outputs["Color"],
                                out_node.inputs["Color1"])
    # Vector curves
    vector_curves = mat_nodes.new("ShaderNodeVectorCurve")
    vector_curves.parent = frame
    if cleaner:
        vector_curves.name = "Final Cleaner Vector Curves"
    else:
        vector_curves.name = "Initial Shape Vector Curves"
    vector_curves.location = (pos_x + 200, pos_y)
    vector_curves.mapping.curves[2].points[0].location = (-0.77, -1.0)
    join_point = Vector((-0.6, -0.25))
    vector_curves.mapping.curves[2].points.new(join_point.x, join_point.y)
    height_single = 1 - obj.cloud_settings.height_single
    angle = ((pi/2 - 0.5) * height_single) + 0.3
    direction = Vector((0, 0))
    direction.x = 0.3*cos(angle)
    direction.y = 0.3*sin(angle)
    last_point = join_point + direction
    vector_curves.mapping.curves[2].points[2].location = (last_point.x, last_point.y)

    mat.node_tree.links.new(vector_curves.outputs["Vector"],
                            gradient_texture.inputs["Vector"])

    # Mapping
    mapping = mat_nodes.new("ShaderNodeMapping")
    mapping.parent = frame
    if cleaner:
        mapping.name = "Final Cleaner Shape Mapping"
    else:
        mapping.name = "Initial Shape Mapping"
    mapping.location = (pos_x, pos_y)
    mapping.inputs["Location"].default_value = (0.0, 0.0, 0)
    mapping.inputs["Scale"].default_value = (0.7, 0.7, 0.7)

    mat.node_tree.links.new(mapping.outputs["Vector"],
                            vector_curves.inputs["Vector"])

    if cleaner:
        mat.node_tree.links.new(in_node.outputs[0],
                                mapping.inputs[0])
    else:
        mat.node_tree.links.new(in_node.outputs["Color"],
                                mapping.inputs[0])


def initial_shape_cloudscape_cumulus(pos_x, pos_y, texture_coordinate, out_node, in_node, mat, mat_nodes, obj, cleaner):
    """
    out_node: nodo de salida
    in_node: nodo de entrada
    """
    obj.cloud_settings.domain_cloud_position = (0.0, 0.0, 1.0)

    obj.cloud_settings.cloud_type = "CLOUDSCAPE_CUMULUS"
    frame = mat_nodes.new(type='NodeFrame')
    frame.name = "Initial shape"
    frame.label = "Initial shape"

    # Este tipo de nube ocupa mas que el resto por lo que para que quepa bien se desplaza
    if not cleaner:
        pos_y = pos_y + 1200
        pos_x = pos_x - 200

    reroute_1 = mat_nodes.new(type='NodeReroute')
    reroute_2 = mat_nodes.new(type='NodeReroute')
    reroute_3 = mat_nodes.new(type='NodeReroute')
    reroute_4 = mat_nodes.new(type='NodeReroute')

    if cleaner:
        reroute_1.location = (pos_x + 1000, pos_y + 100)
        reroute_2.location = (pos_x + 1600, pos_y + 100)
        reroute_3.location = (pos_x, pos_y - 1900)
        reroute_4.location = (pos_x - 3850, pos_y - 1900)
    else:
        reroute_1.location = (pos_x + 900, pos_y - 1300)
        reroute_2.location = (pos_x + 1400, pos_y - 1300)
        reroute_3.location = (pos_x + 600, pos_y - 1250)
        reroute_4.location = (pos_x - 800, pos_y - 1250)

    if cleaner:
        # Color Ramp
        color_ramp_cleaner = mat_nodes.new("ShaderNodeValToRGB")
        color_ramp_cleaner.parent = frame
        color_ramp_cleaner.name = "Final cleaning range"
        color_ramp_cleaner.label = "Final cleaning range"
        color_ramp_cleaner.location = (pos_x + 1300, pos_y)
        color_ramp_cleaner.color_ramp.interpolation = 'LINEAR'
        elem = color_ramp_cleaner.color_ramp.elements[0]
        elem.position = 1.0 - obj.cloud_settings.cleaner_domain_size
        elem.color = (0, 0, 0, 1)
        elem = color_ramp_cleaner.color_ramp.elements[1]
        elem.position = 1.0
        elem.color = (1.0, 1.0, 1.0, 1)

        mat.node_tree.links.new(color_ramp_cleaner.outputs["Color"],
                                out_node.inputs["Color2"])

        # Invert color
        invert_color = mat_nodes.new("ShaderNodeInvert")
        invert_color.parent = frame
        invert_color.location = (pos_x + 1100, pos_y)
        mat.node_tree.links.new(invert_color.outputs["Color"],
                                color_ramp_cleaner.inputs["Fac"])

    # RGB Multiply - Texture image shape
    texture_image_shape_multiply = mat_nodes.new("ShaderNodeMixRGB")
    texture_image_shape_multiply.parent = frame
    if cleaner:
        texture_image_shape_multiply.name = "RGB Multiply - Texture image shape Final Cleaner"
        texture_image_shape_multiply.label = "RGB Multiply - Texture image shape Final Cleaner"
    else:
        texture_image_shape_multiply.name = "RGB Multiply - Texture image shape"
        texture_image_shape_multiply.label = "RGB Multiply - Texture image shape"

    texture_image_shape_multiply.location = (pos_x + 1100, pos_y - 500)
    texture_image_shape_multiply.blend_type = "MULTIPLY"
    texture_image_shape_multiply.inputs["Fac"].default_value = 0.0

    if cleaner:
        mat.node_tree.links.new(texture_image_shape_multiply.outputs["Color"],
                                invert_color.inputs["Color"])
        mat.node_tree.links.new(reroute_1.outputs[0],
                                out_node.inputs["Color2"])
        mat.node_tree.links.new(reroute_2.outputs[0],
                                reroute_1.inputs[0])
        mat.node_tree.links.new(color_ramp_cleaner.outputs["Color"],
                                reroute_2.inputs[0])
    else:
        mat.node_tree.links.new(reroute_1.outputs[0],
                                out_node.inputs["Color1"])
        mat.node_tree.links.new(reroute_2.outputs[0],
                                reroute_1.inputs[0])
        mat.node_tree.links.new(texture_image_shape_multiply.outputs["Color"],
                                reroute_2.inputs[0])

    # RGB Subtract - Gradient and Noise
    subtract_gradient_noise = mat_nodes.new("ShaderNodeMixRGB")
    subtract_gradient_noise.parent = frame
    if cleaner:
        subtract_gradient_noise.name = "RGB Subtract - Gradient and Noise Final Cleaner"
        subtract_gradient_noise.label = "RGB Subtract - Gradient and Noise Final Cleaner"
    else:
        subtract_gradient_noise.name = "RGB Subtract - Gradient and Noise"
        subtract_gradient_noise.label = "RGB Subtract - Gradient and Noise"

    subtract_gradient_noise.location = (pos_x + 900, pos_y - 300)
    subtract_gradient_noise.blend_type = "SUBTRACT"
    amount_of_clouds = 1 - obj.cloud_settings.amount_of_clouds
    subtract_gradient_noise.inputs["Fac"].default_value = amount_of_clouds

    mat.node_tree.links.new(subtract_gradient_noise.outputs["Color"],
                            texture_image_shape_multiply.inputs["Color1"])

    # Image texture - Shape of cloud
    image_texture_shape = mat_nodes.new("ShaderNodeTexImage")
    image_texture_shape.parent = frame
    if cleaner:
        image_texture_shape.name = "Image texture - Shape of cloud Final Cleaner"
        image_texture_shape.label = "Image texture - Shape of cloud Final Cleaner"
    else:
        image_texture_shape.name = "Image texture - Shape of cloud"
        image_texture_shape.label = "Image texture - Shape of cloud"

    image_texture_shape.location = (pos_x + 800, pos_y - 800)

    mat.node_tree.links.new(image_texture_shape.outputs["Color"],
                            texture_image_shape_multiply.inputs["Color2"])

    mat.node_tree.links.new(reroute_3.outputs[0],
                            image_texture_shape.inputs["Vector"])
    mat.node_tree.links.new(reroute_4.outputs[0],
                            reroute_3.inputs[0])
    mat.node_tree.links.new(texture_coordinate.outputs["Generated"],
                            reroute_4.inputs[0])

    # RGB Subtract - Gradient and Gradient
    subtract_gradient_gradient = mat_nodes.new("ShaderNodeMixRGB")
    subtract_gradient_gradient.parent = frame
    if cleaner:
        subtract_gradient_gradient.name = "RGB Subtract - Gradient and Gradient Final Cleaner"
        subtract_gradient_gradient.label = "RGB Subtract - Gradient and Gradient Final Cleaner"
    else:
        subtract_gradient_gradient.name = "RGB Subtract - Gradient and Gradient"
        subtract_gradient_gradient.label = "RGB Subtract - Gradient and Gradient"

    subtract_gradient_gradient.location = (pos_x + 700, pos_y)
    subtract_gradient_gradient.blend_type = "SUBTRACT"
    subtract_gradient_gradient.inputs["Fac"].default_value = 1.0

    mat.node_tree.links.new(subtract_gradient_gradient.outputs["Color"],
                            subtract_gradient_noise.inputs["Color1"])

    # Color Ramp - Gradient base
    color_ramp_gradient_base = mat_nodes.new("ShaderNodeValToRGB")
    color_ramp_gradient_base.parent = frame
    if cleaner:
        color_ramp_gradient_base.name = "ColorRamp - Gradient Base Final Cleaner"
        color_ramp_gradient_base.label = "ColorRamp - Gradient Base Final Cleaner"
    else:
        color_ramp_gradient_base.name = "ColorRamp - Gradient Base"
        color_ramp_gradient_base.label = "ColorRamp - Gradient Base"
    color_ramp_gradient_base.location = (pos_x + 400, pos_y)
    color_ramp_gradient_base.color_ramp.interpolation = 'LINEAR'
    elem = color_ramp_gradient_base.color_ramp.elements[0]
    elem.position = 0.0
    elem.color = (0, 0, 0, 1)
    elem = color_ramp_gradient_base.color_ramp.elements[1]
    elem.position = 0.2
    elem.color = (1, 1, 1, 1)

    mat.node_tree.links.new(color_ramp_gradient_base.outputs["Color"],
                            subtract_gradient_gradient.inputs["Color1"])

    # Color Ramp - Gradient subtract
    color_ramp_gradient_subtract = mat_nodes.new("ShaderNodeValToRGB")
    color_ramp_gradient_subtract.parent = frame
    if cleaner:
        color_ramp_gradient_subtract.name = "ColorRamp - Gradient Subtract Final Cleaner"
        color_ramp_gradient_subtract.label = "ColorRamp - Gradient Subtract Final Cleaner"
    else:
        color_ramp_gradient_subtract.name = "ColorRamp - Gradient Subtract"
        color_ramp_gradient_subtract.label = "ColorRamp - Gradient Subtract"
    color_ramp_gradient_subtract.location = (pos_x + 400, pos_y - 400)
    color_ramp_gradient_subtract.color_ramp.interpolation = 'LINEAR'
    elem = color_ramp_gradient_subtract.color_ramp.elements[0]
    elem.position = 0.0
    elem.color = (0, 0, 0, 1)
    elem = color_ramp_gradient_subtract.color_ramp.elements[1]
    elem.position = 0.6
    elem.color = (1, 1, 1, 1)

    mat.node_tree.links.new(color_ramp_gradient_subtract.outputs["Color"],
                            subtract_gradient_gradient.inputs["Color2"])

    # Gradient Texture base
    gradient_texture_base = mat_nodes.new("ShaderNodeTexGradient")
    gradient_texture_base.parent = frame
    if cleaner:
        gradient_texture_base.name = "Final Cleaner Gradient Texture Base"
    else:
        gradient_texture_base.name = "Initial Shape Gradient Texture Base"
    gradient_texture_base.location = (pos_x + 200, pos_y)
    gradient_texture_base.gradient_type = "LINEAR"

    mat.node_tree.links.new(gradient_texture_base.outputs["Color"],
                            color_ramp_gradient_base.inputs["Fac"])

    # Gradient Texture subtract
    gradient_texture_subtract = mat_nodes.new("ShaderNodeTexGradient")
    gradient_texture_subtract.parent = frame
    if cleaner:
        gradient_texture_subtract.name = "Final Cleaner Gradient Texture Subtract"
    else:
        gradient_texture_subtract.name = "Initial Shape Gradient Texture Subtract"
    gradient_texture_subtract.location = (pos_x + 200, pos_y - 400)
    gradient_texture_subtract.gradient_type = "LINEAR"

    mat.node_tree.links.new(gradient_texture_subtract.outputs["Color"],
                            color_ramp_gradient_subtract.inputs["Fac"])

    # Vector Multiply - Noise subtract
    multiply_noise = mat_nodes.new("ShaderNodeVectorMath")
    multiply_noise.parent = frame
    multiply_noise.location = (pos_x + 400, pos_y - 800)
    if cleaner:
        multiply_noise.name = "Vector Multiply - Noise subtract Final Cleaner "
        multiply_noise.label = "Vector Multiply - Noise subtract Final Cleaner "
    else:
        multiply_noise.name = "Vector Multiply - Noise subtract"
        multiply_noise.label = "Vector Multiply - Noise subtract"
    multiply_noise.operation = "MULTIPLY"
    multiply_noise.inputs[1].default_value = (3.0, 3.0, 3.0)

    mat.node_tree.links.new(multiply_noise.outputs["Vector"],
                            subtract_gradient_noise.inputs["Color2"])

    # Mapping base
    mapping_base = mat_nodes.new("ShaderNodeMapping")
    mapping_base.parent = frame
    if cleaner:
        mapping_base.name = "Final Cleaner Mapping Base"
    else:
        mapping_base.name = "Initial Shape Mapping Base"
    mapping_base.location = (pos_x, pos_y)
    mapping_base.inputs["Location"].default_value = (0, 0, 0)
    mapping_base.inputs["Rotation"].default_value = (0, pi/2, 0)
    mapping_base.inputs["Scale"].default_value = (1, 1, 1)

    mat.node_tree.links.new(mapping_base.outputs["Vector"],
                            gradient_texture_base.inputs["Vector"])

    # Mapping subtract
    mapping_subtract = mat_nodes.new("ShaderNodeMapping")
    mapping_subtract.parent = frame
    if cleaner:
        mapping_subtract.name = "Final Cleaner Mapping Subtract"
    else:
        mapping_subtract.name = "Initial Shape Mapping Subtract"
    mapping_subtract.location = (pos_x, pos_y - 400)
    height_cloudscape = obj.cloud_settings.height_cloudscape
    mapping_subtract.inputs["Location"].default_value = (-height_cloudscape, 0.0, 0.0)
    mapping_subtract.inputs["Rotation"].default_value = (0, pi/2, 0)
    mapping_subtract.inputs["Scale"].default_value = (1, 1, 1)

    mat.node_tree.links.new(mapping_subtract.outputs["Vector"],
                            gradient_texture_subtract.inputs["Vector"])

    # Mapping noise
    mapping_noise = mat_nodes.new("ShaderNodeMapping")
    mapping_noise.parent = frame
    if cleaner:
        mapping_noise.name = "Final Cleaner Mapping Noise"
    else:
        mapping_noise.name = "Initial Shape Mapping Noise"
    mapping_noise.location = (pos_x, pos_y - 800)
    cloudscape_noise_coords = obj.cloud_settings.cloudscape_noise_coords
    mapping_noise.inputs["Location"].default_value = cloudscape_noise_coords
    mapping_noise.inputs["Rotation"].default_value = (0, 0, 0)
    mapping_noise.inputs["Scale"].default_value = (1, 1, 1)

    # Noise Tex - Subtract initial
    noise_subtract = mat_nodes.new("ShaderNodeTexNoise")
    noise_subtract.parent = frame
    if cleaner:
        noise_subtract.name = "Noise Tex - Subtract initial Final Cleaner"
        noise_subtract.label = "Noise Tex - Subtract initial Final Cleaner"
    else:
        noise_subtract.name = "Noise Tex - Subtract initial"
        noise_subtract.label = "Noise Tex - Subtract initial"
    noise_subtract.location = (pos_x + 200, pos_y - 800)
    cloudscape_cloud_size = 10.1 - obj.cloud_settings.cloudscape_cloud_size
    noise_subtract.inputs["Scale"].default_value = cloudscape_cloud_size
    noise_subtract.inputs["Detail"].default_value = 0.0
    noise_subtract.inputs["Roughness"].default_value = 0.0
    noise_subtract.inputs["Distortion"].default_value = 0.0

    mat.node_tree.links.new(noise_subtract.outputs["Fac"],
                            multiply_noise.inputs[0])

    reroute_5 = mat_nodes.new(type='NodeReroute')
    reroute_5.location = (pos_x - 100, pos_y - 1300)

    mat.node_tree.links.new(mapping_noise.outputs[0],
                            noise_subtract.inputs[0])

    if cleaner:
        mat.node_tree.links.new(in_node.outputs[0],
                                reroute_5.inputs[0])
    else:
        reroute_6 = mat_nodes.new(type='NodeReroute')
        reroute_6.location = (pos_x + 100, pos_y - 1300)
        mat.node_tree.links.new(reroute_6.outputs[0],
                                reroute_5.inputs[0])
        mat.node_tree.links.new(in_node.outputs["Color"],
                                reroute_6.inputs[0])

    mat.node_tree.links.new(reroute_5.outputs[0],
                            mapping_base.inputs[0])
    mat.node_tree.links.new(reroute_5.outputs[0],
                            mapping_subtract.inputs[0])
    mat.node_tree.links.new(reroute_5.outputs[0],
                            mapping_noise.inputs["Vector"])


def generate_cloud(context, pos_x, pos_y, initial_shape):
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

    # Initialization
    obj.cloud_settings.amount_of_clouds = random.uniform(0.2, 0.6)
    obj.cloud_settings.detail_bump_strength = random.uniform(0.1, 0.5)
    obj.cloud_settings.subtract_shape_imperfection = random.uniform(0, 1)
    obj.cloud_settings.add_shape_imperfection = random.uniform(0, 0.6)
    obj.cloud_settings.roundness = random.uniform(0, 1)
    obj.cloud_settings.roundness_coords = (
                                            random.uniform(0, 200),
                                            random.uniform(0, 200),
                                            random.uniform(0, 200)
                                        )
    obj.cloud_settings.add_shape_imperfection_coords = (
                                                        random.uniform(0, 200),
                                                        random.uniform(0, 200),
                                                        random.uniform(0, 200)
                                                        )
    obj.cloud_settings.subtract_shape_imperfection_coords = (
                                                                random.uniform(0, 200),
                                                                random.uniform(0, 200),
                                                                random.uniform(0, 200)
                                                            )
    obj.cloud_settings.cloudscape_noise_coords = (
                                                    random.uniform(0, 200),
                                                    random.uniform(0, 200),
                                                    random.uniform(0, 200)
                                                )

    # -----------------------------------------------
    # -------------Material construction-------------
    # -----------------------------------------------
    # From final node to beginning

    # Reroutes
    reroute_1 = mat_nodes.new(type='NodeReroute')
    reroute_1.location = (pos_x + 1400, pos_y - 1500)

    reroute_2 = mat_nodes.new(type='NodeReroute')
    reroute_2.location = (pos_x + 1400, pos_y - 2300)

    reroute_3 = mat_nodes.new(type='NodeReroute')
    reroute_3.location = (pos_x + 2600, pos_y - 2300)

    reroute_4 = mat_nodes.new(type='NodeReroute')
    reroute_4.location = (pos_x + 4100, pos_y - 2300)

    # -------------BEGINNING MAIN BRANCH-------------
    # Material Output
    material_output = mat_nodes.new("ShaderNodeOutputMaterial")
    material_output.name = "Cloud Output"
    material_output.location = (pos_x + 6350, pos_y)

    # Principled Volume
    principled_volume = mat_nodes.new("ShaderNodeVolumePrincipled")
    principled_volume.name = "Cloud Principled Volume"
    principled_volume.location = (pos_x + 6050, pos_y)
    principled_volume.inputs["Color"].default_value = (1, 1, 1, 1)

    # Connection between Principled Volume and Material Output.
    mat.node_tree.links.new(principled_volume.outputs["Volume"],
                            material_output.inputs["Volume"])

    # Final density Color Ramp
    color_ramp_density = mat_nodes.new("ShaderNodeValToRGB")
    color_ramp_density.name = "ColorRamp - Cloud Density"
    color_ramp_density.label = "ColorRamp - Cloud Density"
    color_ramp_density.location = (pos_x + 5750, pos_y)
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
    subtract_final_cleaner.location = (pos_x + 5550, pos_y)
    subtract_final_cleaner.blend_type = "SUBTRACT"
    subtract_final_cleaner.inputs["Fac"].default_value = 1.0

    mat.node_tree.links.new(subtract_final_cleaner.outputs["Color"],
                            color_ramp_density.inputs["Fac"])

    # RGB Overlay - Detail noise
    overlay_detail_noise = mat_nodes.new("ShaderNodeMixRGB")
    overlay_detail_noise.name = "RGB Overlay - Noise"
    overlay_detail_noise.label = "RGB Overlay - Noise"
    overlay_detail_noise.location = (pos_x + 4350, pos_y)
    overlay_detail_noise.blend_type = "OVERLAY"
    detail_noise = obj.cloud_settings.detail_noise
    overlay_detail_noise.inputs["Fac"].default_value = detail_noise

    mat.node_tree.links.new(overlay_detail_noise.outputs["Color"],
                            subtract_final_cleaner.inputs["Color1"])

    # RGB Multiply - Bump
    multiply_bump = mat_nodes.new("ShaderNodeMixRGB")
    multiply_bump.name = "RGB Multiply - Bump"
    multiply_bump.label = "RGB Multiply - Bump"
    multiply_bump.location = (pos_x + 4150, pos_y)
    multiply_bump.blend_type = "MULTIPLY"
    detail_bump_strength = obj.cloud_settings.detail_bump_strength
    multiply_bump.inputs["Fac"].default_value = detail_bump_strength

    mat.node_tree.links.new(multiply_bump.outputs["Color"],
                            overlay_detail_noise.inputs["Color1"])

    # Vector Multiply - Simple cleaner
    multiply_cleaner = mat_nodes.new("ShaderNodeVectorMath")
    multiply_cleaner.location = (pos_x + 3500, pos_y)
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
    length_greater_than.location = (pos_x + 3250, pos_y - 200)
    length_greater_than.operation = "GREATER_THAN"
    length_greater_than.inputs[1].default_value = 0.520

    mat.node_tree.links.new(length_greater_than.outputs["Value"],
                            multiply_cleaner.inputs[1])
    # Vector Length
    lenght = mat_nodes.new("ShaderNodeVectorMath")
    lenght.parent = frame
    lenght.location = (pos_x + 3050, pos_y - 200)
    lenght.operation = "LENGTH"

    mat.node_tree.links.new(lenght.outputs["Value"],
                            length_greater_than.inputs["Value"])

    # END SIMPLE CLEANER FRAME

    # RGB Subtract - Shape imperfection
    subtract_imperfection = mat_nodes.new("ShaderNodeMixRGB")
    subtract_imperfection.name = "RGB Subtract - Shape imperfection"
    subtract_imperfection.label = "RGB Subtract - Shape imperfection"
    subtract_imperfection.location = (pos_x + 2650, pos_y)
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
    add_imperfection.location = (pos_x + 2450, pos_y)
    add_imperfection.blend_type = "ADD"
    add_shape_imperfection = obj.cloud_settings.add_shape_imperfection
    add_imperfection.inputs["Fac"].default_value = add_shape_imperfection

    mat.node_tree.links.new(add_imperfection.outputs["Color"],
                            subtract_imperfection.inputs["Color1"])

    # RGB Overlay - Roundness
    overlay_roundness = mat_nodes.new("ShaderNodeMixRGB")
    overlay_roundness.name = "RGB Overlay - Roundness"
    overlay_roundness.label = "RGB Overlay - Roundness"
    overlay_roundness.location = (pos_x + 2250, pos_y)
    overlay_roundness.blend_type = "OVERLAY"
    roundness = obj.cloud_settings.roundness
    overlay_roundness.inputs["Fac"].default_value = roundness

    mat.node_tree.links.new(overlay_roundness.outputs["Color"],
                            add_imperfection.inputs["Color1"])

    # Following the order here, the initial_shape function should be here
    # but it is called after "Texture Coordinate" because this is needed.

    # BEGINNING WIND FRAME
    frame = mat_nodes.new(type='NodeFrame')
    frame.name = "Wind"
    frame.label = "Wind"

    # RGB Add - Shape wind small turbulence
    add_shape_wind_small = mat_nodes.new("ShaderNodeMixRGB")
    add_shape_wind_small.parent = frame
    add_shape_wind_small.name = "RGB Add - Shape wind small turbulence"
    add_shape_wind_small.label = "RGB Add - Shape wind small turbulence"
    add_shape_wind_small.location = (pos_x + 900, pos_y)
    add_shape_wind_small.blend_type = "ADD"
    wind = obj.cloud_settings.wind
    add_shape_wind_small.inputs["Fac"].default_value = wind

    mat.node_tree.links.new(add_shape_wind_small.outputs["Color"],
                            reroute_1.inputs[0])

    # Vector Subtract - Shape wind small turbulence domain to -0.5 to 0.5
    domain_adjustment_shape_wind = mat_nodes.new("ShaderNodeVectorMath")
    domain_adjustment_shape_wind.parent = frame
    domain_adjustment_shape_wind.location = (pos_x + 700, pos_y - 150)
    domain_adjustment_shape_wind.name = "Vector Subtract - Shape wind small turbulence domain adjustment"
    domain_adjustment_shape_wind.label = "Vector Subtract - Shape wind small turbulence domain adjustment"
    domain_adjustment_shape_wind.operation = "SUBTRACT"
    domain_adjustment_shape_wind.inputs[1].default_value = (0.5, 0.5, 0.5)

    mat.node_tree.links.new(domain_adjustment_shape_wind.outputs["Vector"],
                            add_shape_wind_small.inputs["Color2"])

    # Noise Tex - Shape wind small turbulence 
    noise_shape_wind = mat_nodes.new("ShaderNodeTexNoise")
    noise_shape_wind.parent = frame
    noise_shape_wind.name = "Noise Tex - Shape wind small turbulence"
    noise_shape_wind.label = "Noise Tex - Shape wind small turbulence"
    noise_shape_wind.location = (pos_x + 500, pos_y - 150)
    noise_shape_wind.inputs["Scale"].default_value = 1.5
    noise_shape_wind.inputs["Detail"].default_value = 0.0
    noise_shape_wind.inputs["Roughness"].default_value = 0.0
    noise_shape_wind.inputs["Distortion"].default_value = 3.0

    mat.node_tree.links.new(noise_shape_wind.outputs["Fac"],
                            domain_adjustment_shape_wind.inputs[0])

    # END WIND FRAME

    # Initial mapping
    initial_mapping = mat_nodes.new("ShaderNodeMapping")
    initial_mapping.name = "Initial mapping"
    initial_mapping.location = (pos_x + 200, pos_y)
    domain_cloud_position = obj.cloud_settings.domain_cloud_position
    initial_mapping.inputs["Location"].default_value = domain_cloud_position

    mat.node_tree.links.new(initial_mapping.outputs["Vector"],
                            add_shape_wind_small.inputs["Color1"])
    mat.node_tree.links.new(initial_mapping.outputs["Vector"],
                            noise_shape_wind.inputs["Vector"])

    # Texture Coordinate
    texture_coordinate = mat_nodes.new("ShaderNodeTexCoord")
    texture_coordinate.location = (pos_x, pos_y)
    mat.node_tree.links.new(texture_coordinate.outputs["Object"],
                            initial_mapping.inputs["Vector"])

    initial_shape(pos_x + 1500, pos_y + 200, texture_coordinate, overlay_roundness, add_shape_wind_small, mat, mat_nodes, obj, False)

    # ----------------END MAIN BRANCH----------------

    mat.node_tree.links.new(add_shape_wind_small.outputs["Color"],
                            reroute_2.inputs[0])
    mat.node_tree.links.new(reroute_2.outputs[0],
                            reroute_3.inputs[0])
    mat.node_tree.links.new(reroute_3.outputs[0],
                            reroute_4.inputs[0])

    # --------BEGINNING FINAL CLEANER BRANCH---------
    initial_shape(pos_x + 4350, pos_y - 500, texture_coordinate, subtract_final_cleaner, reroute_4, mat, mat_nodes, obj, True)
    # -----------END FINAL CLEANER BRANCH------------

    # -------------BEGINNING BUMP BRANCH-------------
    frame = mat_nodes.new(type='NodeFrame')
    frame.name = "Bump"
    frame.label = "Bump"

    # Invert color
    invert_color = mat_nodes.new("ShaderNodeInvert")
    invert_color.parent = frame
    invert_color.location = (pos_x + 3850, pos_y - 500)
    mat.node_tree.links.new(invert_color.outputs["Color"],
                            multiply_bump.inputs["Color2"])
    # RGB Overlay - Bump level 3
    overlay_bump_3 = mat_nodes.new("ShaderNodeMixRGB")
    overlay_bump_3.parent = frame
    overlay_bump_3.name = "RGB Overlay - Bump level 3"
    overlay_bump_3.label = "RGB Overlay - Bump level 3"
    overlay_bump_3.location = (pos_x + 3650, pos_y - 500)
    overlay_bump_3.blend_type = "OVERLAY"

    mat.node_tree.links.new(overlay_bump_3.outputs["Color"],
                            invert_color.inputs["Color"])

    # RGB Overlay - Bump level 2
    overlay_bump_2 = mat_nodes.new("ShaderNodeMixRGB")
    overlay_bump_2.parent = frame
    overlay_bump_2.name = "RGB Overlay - Bump level 2"
    overlay_bump_2.label = "RGB Overlay - Bump level 2"
    overlay_bump_2.location = (pos_x + 3450, pos_y - 500)
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
    voronoi_bump_1.location = (pos_x + 3250, pos_y - 500)

    mat.node_tree.links.new(voronoi_bump_1.outputs["Distance"],
                            overlay_bump_2.inputs["Color1"])

    # Voronoi tex - Bump level 2
    voronoi_bump_2 = mat_nodes.new("ShaderNodeTexVoronoi")
    voronoi_bump_2.parent = frame
    voronoi_bump_2.name = "Voronoi tex - Bump level 2"
    voronoi_bump_2.label = "Voronoi tex - Bump level 2"
    voronoi_bump_2.location = (pos_x + 3250, pos_y - 800)
    voronoi_bump_2.inputs["Scale"].default_value = 10.3

    mat.node_tree.links.new(voronoi_bump_2.outputs["Distance"],
                            overlay_bump_2.inputs["Color2"])

    # Voronoi tex - Bump level 3
    voronoi_bump_3 = mat_nodes.new("ShaderNodeTexVoronoi")
    voronoi_bump_3.parent = frame
    voronoi_bump_3.name = "Voronoi tex - Bump level 3"
    voronoi_bump_3.label = "Voronoi tex - Bump level 3"
    voronoi_bump_3.location = (pos_x + 3250, pos_y - 1100)
    voronoi_bump_3.inputs["Scale"].default_value = 30.0

    mat.node_tree.links.new(voronoi_bump_3.outputs["Distance"],
                            overlay_bump_3.inputs["Color2"])

    # RGB Add - Small wind
    add_small_wind = mat_nodes.new("ShaderNodeMixRGB")
    add_small_wind.parent = frame
    add_small_wind.name = "RGB Add - Small wind"
    add_small_wind.label = "RGB Add - Small wind"
    add_small_wind.location = (pos_x + 3050, pos_y - 950)
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
    add_coords_bump.location = (pos_x + 2650, pos_y - 800)
    add_coords_bump.name = "Vector Add - Bump coordinates"
    add_coords_bump.label = "Vector Add - Bump coordinates"
    add_coords_bump.operation = "ADD"
    add_coords_bump.inputs[1].default_value = (5.0, 8.5, 11.0)

    mat.node_tree.links.new(add_coords_bump.outputs["Vector"],
                            add_small_wind.inputs["Color1"])

    # Vector Subtract - Small wind domain to -0.5 to 0.5
    domain_adjustment_small_wind = mat_nodes.new("ShaderNodeVectorMath")
    domain_adjustment_small_wind.parent = frame
    domain_adjustment_small_wind.location = (pos_x + 2850, pos_y - 1100)
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
    noise_small_wind.location = (pos_x + 2650, pos_y - 1100)
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
    overlay_noise_combine.location = (pos_x + 3850, pos_y - 1500)
    overlay_noise_combine.blend_type = "OVERLAY"
    overlay_noise_combine.inputs["Fac"].default_value = 1.0

    mat.node_tree.links.new(overlay_noise_combine.outputs["Color"],
                            overlay_detail_noise.inputs["Color2"])

    # Noise Tex - Detail noise level 1
    detetail_noise_level_1 = mat_nodes.new("ShaderNodeTexNoise")
    detetail_noise_level_1.parent = frame
    detetail_noise_level_1.name = "Noise Tex - Detail noise level 1"
    detetail_noise_level_1.label = "Noise Tex - Detail noise level 1"
    detetail_noise_level_1.location = (pos_x + 3650, pos_y - 1500)
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
    detetail_noise_level_2.location = (pos_x + 3650, pos_y - 1800)
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
    invert_color.location = (pos_x + 2000, pos_y - 500)
    mat.node_tree.links.new(invert_color.outputs["Color"],
                            overlay_roundness.inputs["Color2"])

    # Voronoi tex - Roundness
    voronoi_roundness = mat_nodes.new("ShaderNodeTexVoronoi")
    voronoi_roundness.parent = frame
    voronoi_roundness.name = "Voronoi tex - Roundness"
    voronoi_roundness.label = "Voronoi tex - Roundness"
    voronoi_roundness.location = (pos_x + 1800, pos_y - 500)
    voronoi_roundness.inputs["Scale"].default_value = 2.0

    mat.node_tree.links.new(voronoi_roundness.outputs["Distance"],
                            invert_color.inputs["Color"])

    # Vector Add - Roundness coord
    add_coords_roundness = mat_nodes.new("ShaderNodeVectorMath")
    add_coords_roundness.parent = frame
    add_coords_roundness.location = (pos_x + 1600, pos_y - 500)
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
    color_burn_noises.location = (pos_x + 2000, pos_y - 900)
    color_burn_noises.blend_type = "BURN"
    color_burn_noises.inputs["Fac"].default_value = 1.0

    mat.node_tree.links.new(color_burn_noises.outputs["Color"],
                            add_imperfection.inputs["Color2"])

    # Noise Tex - Add shape imperfection 1
    noise_add_shape_imperfection_1 = mat_nodes.new("ShaderNodeTexNoise")
    noise_add_shape_imperfection_1.parent = frame
    noise_add_shape_imperfection_1.name = "Noise Tex - Add shape imperfection 1"
    noise_add_shape_imperfection_1.label = "Noise Tex - Add shape imperfection 1"
    noise_add_shape_imperfection_1.location = (pos_x + 1800, pos_y - 900)
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
    noise_add_shape_imperfection_2.location = (pos_x + 1800, pos_y - 1150)
    noise_add_shape_imperfection_2.inputs["Scale"].default_value = 1.9
    noise_add_shape_imperfection_2.inputs["Detail"].default_value = 16.0
    noise_add_shape_imperfection_2.inputs["Roughness"].default_value = 0.0
    noise_add_shape_imperfection_2.inputs["Distortion"].default_value = 0.0

    mat.node_tree.links.new(noise_add_shape_imperfection_2.outputs["Fac"],
                            color_burn_noises.inputs["Color2"])

    # Vector Add - Coords add shape imperfection 1
    coords_add_shape_imperfection_1 = mat_nodes.new("ShaderNodeVectorMath")
    coords_add_shape_imperfection_1.parent = frame
    coords_add_shape_imperfection_1.location = (pos_x + 1600, pos_y - 900)
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
    coords_add_shape_imperfection_2.location = (pos_x + 1600, pos_y - 1150)
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
    color_burn_noises.location = (pos_x + 2000, pos_y - 1500)
    color_burn_noises.blend_type = "BURN"
    color_burn_noises.inputs["Fac"].default_value = 1.0

    mat.node_tree.links.new(color_burn_noises.outputs["Color"],
                            subtract_imperfection.inputs["Color2"])

    # Noise Tex - Subtract shape imperfection 1
    noise_subtract_shape_imperfection_1 = mat_nodes.new("ShaderNodeTexNoise")
    noise_subtract_shape_imperfection_1.parent = frame
    noise_subtract_shape_imperfection_1.name = "Noise Tex - Subtract shape imperfection 1"
    noise_subtract_shape_imperfection_1.label = "Noise Tex - Subtract shape imperfection 1"
    noise_subtract_shape_imperfection_1.location = (pos_x + 1800, pos_y - 1500)
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
    noise_subtract_shape_imperfection_2.location = (pos_x + 1800, pos_y - 1750)
    noise_subtract_shape_imperfection_2.inputs["Scale"].default_value = 1.9
    noise_subtract_shape_imperfection_2.inputs["Detail"].default_value = 16.0
    noise_subtract_shape_imperfection_2.inputs["Roughness"].default_value = 0.0
    noise_subtract_shape_imperfection_2.inputs["Distortion"].default_value = 0.0

    mat.node_tree.links.new(noise_subtract_shape_imperfection_2.outputs["Fac"],
                            color_burn_noises.inputs["Color2"])

    # Vector Add - Coods subtract shape imperfection 1
    coords_subtract_shape_imperfection_1 = mat_nodes.new("ShaderNodeVectorMath")
    coords_subtract_shape_imperfection_1.parent = frame
    coords_subtract_shape_imperfection_1.location = (pos_x + 1600, pos_y - 1500)
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
    coords_subtract_shape_imperfection_2.location = (pos_x + 1600, pos_y - 1750)
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
    obj.scale = (0.5, 0.5, 0.5)  # Default cube is 2 meters
    C.view_layer.objects.active = obj
    bpy.ops.object.transform_apply(location=False,
                                   rotation=False,
                                   scale=True,
                                   properties=True)

    adapted_size = Vector((domain.x/size, domain.y/size, domain.z/size))
    obj.scale = (adapted_size.x, adapted_size.y, adapted_size.z)
    bpy.ops.object.transform_apply(location=False, rotation=False,
                                   scale=True, properties=True)
    obj.cloud_settings["auxiliar_size_vector"] = adapted_size

    cube_size = Vector((domain.x / adapted_size.x,
                        domain.y / adapted_size.y,
                        domain.z / adapted_size.z))
    obj.scale = cube_size
