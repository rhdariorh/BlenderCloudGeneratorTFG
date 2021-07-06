"""
    materials.py is part of Cloud Generator Blender Addon.

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
import random


def initial_shape_single_cumulus(pos_x, pos_y, texture_coordinate, cleaner_out, out_node, in_node, mat, obj):
    """
    pos_x: relative x position of nodes in the material node graph
    pos_y: relative y position of nodes in the material node graph
    texture_coordinate: texture coordinate in for image shape texture 
    cleaner_out: out for final cleaner
    out_node: out for the initial shape values
    in_node: coordinates used for initial shape
    mat: material to include nodes
    out_node: nodo de salida
    in_node: nodo de entrada
    mat: material. Used to access node_tree and insert connections and nodes
    obj: cloud object that has the material applied
    """

    mat_nodes = mat.node_tree.nodes # Fast access to nodes

    obj.cloud_settings.cloud_type = "SINGLE_CUMULUS"
    frame = mat_nodes.new(type='NodeFrame')
    frame.name = "Initial shape"
    frame.label = "Initial shape"

    # Color Ramp
    color_ramp_cleaner = mat_nodes.new("ShaderNodeValToRGB")
    color_ramp_cleaner.name = "Final cleaning range"
    color_ramp_cleaner.label = "Final cleaning range"
    color_ramp_cleaner.location = (pos_x + 1100, pos_y + 300)
    color_ramp_cleaner.color_ramp.interpolation = 'LINEAR'
    elem = color_ramp_cleaner.color_ramp.elements[0]
    elem.position = 1.0 - obj.cloud_settings.cleaner_domain_size
    elem.color = (0, 0, 0, 1)
    elem = color_ramp_cleaner.color_ramp.elements[1]
    elem.position = 1.0
    elem.color = (1.0, 1.0, 1.0, 1)

    mat.node_tree.links.new(color_ramp_cleaner.outputs["Color"],
                            cleaner_out.inputs[1])

    # Invert color
    invert_color = mat_nodes.new("ShaderNodeInvert")
    invert_color.location = (pos_x + 900, pos_y + 300)
    mat.node_tree.links.new(invert_color.outputs["Color"],
                            color_ramp_cleaner.inputs["Fac"])

    # Gradient Texture
    gradient_texture = mat_nodes.new("ShaderNodeTexGradient")
    gradient_texture.parent = frame
    gradient_texture.name = "Initial Shape Gradient Texture"
    gradient_texture.location = (pos_x + 700, pos_y)
    gradient_texture.gradient_type = "SPHERICAL"

    mat.node_tree.links.new(gradient_texture.outputs["Color"],
                            out_node.inputs["Color1"])

    mat.node_tree.links.new(gradient_texture.outputs["Color"],
                            invert_color.inputs["Color"])

    # Vector curves
    vector_curves = mat_nodes.new("ShaderNodeVectorCurve")
    vector_curves.parent = frame
    vector_curves.name = "Initial Shape Vector Curves"
    vector_curves.location = (pos_x + 400, pos_y)
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
    mapping.name = "Initial Shape Mapping"
    mapping.location = (pos_x + 200, pos_y)
    mapping.inputs["Location"].default_value = (0.0, 0.0, 0)
    mapping.inputs["Scale"].default_value = (0.7, 0.7, 0.7)

    mat.node_tree.links.new(mapping.outputs["Vector"],
                            vector_curves.inputs["Vector"])

    mat.node_tree.links.new(in_node.outputs["Vector"],
                            mapping.inputs[0])


def initial_shape_cloudscape_cumulus(pos_x, pos_y, texture_coordinate, cleaner_out, out_node, in_node, mat, obj):
    """
    pos_x: relative x position of nodes in the material node graph
    pos_y: relative y position of nodes in the material node graph
    texture_coordinate: texture coordinate in for image shape texture 
    cleaner_out: out for final cleaner
    out_node: out for the initial shape values
    in_node: coordinates used for initial shape
    mat: material to include nodes
    out_node: nodo de salida
    in_node: nodo de entrada
    mat: material. Used to access node_tree and insert connections and nodes
    obj: cloud object that has the material applied
    """

    mat_nodes = mat.node_tree.nodes # Fast access to nodes

    obj.cloud_settings.domain_cloud_position = (0.0, 0.0, 1.0)

    obj.cloud_settings.cloud_type = "CLOUDSCAPE_CUMULUS"
    frame = mat_nodes.new(type='NodeFrame')
    frame.name = "Initial shape"
    frame.label = "Initial shape"

    # Este tipo de nube ocupa mas que el resto por lo que para que quepa bien se desplaza
    pos_y = pos_y + 1400
    pos_x = pos_x - 400

    reroute_1 = mat_nodes.new(type='NodeReroute')
    reroute_2 = mat_nodes.new(type='NodeReroute')
    reroute_3 = mat_nodes.new(type='NodeReroute')
    reroute_4 = mat_nodes.new(type='NodeReroute')

    # reroute_1.location = (pos_x + 900, pos_y - 1300)
    # reroute_2.location = (pos_x + 1400, pos_y - 1300)
    reroute_3.location = (pos_x + 600, pos_y - 1250)
    reroute_4.location = (pos_x - 800, pos_y - 1250)

    # Color Ramp
    color_ramp_cleaner = mat_nodes.new("ShaderNodeValToRGB")
    color_ramp_cleaner.name = "Final cleaning range"
    color_ramp_cleaner.label = "Final cleaning range"
    color_ramp_cleaner.location = (pos_x + 2500, pos_y - 500)
    color_ramp_cleaner.color_ramp.interpolation = 'LINEAR'
    elem = color_ramp_cleaner.color_ramp.elements[0]
    elem.position = 1.0 - obj.cloud_settings.cleaner_domain_size
    elem.color = (0, 0, 0, 1)
    elem = color_ramp_cleaner.color_ramp.elements[1]
    elem.position = 1.0
    elem.color = (1.0, 1.0, 1.0, 1)

    mat.node_tree.links.new(color_ramp_cleaner.outputs["Color"],
                            cleaner_out.inputs[1])

    # Invert color
    invert_color = mat_nodes.new("ShaderNodeInvert")
    invert_color.location = (pos_x + 2300, pos_y - 500)
    mat.node_tree.links.new(invert_color.outputs["Color"],
                            color_ramp_cleaner.inputs["Fac"])

    # RGB Multiply - Texture image shape
    texture_image_shape_multiply = mat_nodes.new("ShaderNodeMixRGB")
    texture_image_shape_multiply.parent = frame
    texture_image_shape_multiply.name = "RGB Multiply - Texture image shape"
    texture_image_shape_multiply.label = "RGB Multiply - Texture image shape"

    texture_image_shape_multiply.location = (pos_x + 1100, pos_y - 500)
    texture_image_shape_multiply.blend_type = "MULTIPLY"
    texture_image_shape_multiply.inputs["Fac"].default_value = 0.0

    """
    mat.node_tree.links.new(reroute_1.outputs[0],
                            out_node.inputs["Color1"])
    mat.node_tree.links.new(reroute_2.outputs[0],
                            reroute_1.inputs[0])
    mat.node_tree.links.new(texture_image_shape_multiply.outputs["Color"],
                            reroute_2.inputs[0])

    mat.node_tree.links.new(texture_image_shape_multiply.outputs["Color"],
                            invert_color.inputs["Color"])
    """

    mat.node_tree.links.new(texture_image_shape_multiply.outputs["Color"],
                            invert_color.inputs["Color"])
    mat.node_tree.links.new(texture_image_shape_multiply.outputs["Color"],
                            out_node.inputs["Color1"])

    # RGB Subtract - Gradient and Noise
    subtract_gradient_noise = mat_nodes.new("ShaderNodeMixRGB")
    subtract_gradient_noise.parent = frame
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
    color_ramp_gradient_base.name = "ColorRamp - Gradient Base"
    color_ramp_gradient_base.label = "ColorRamp - Gradient Base"
    color_ramp_gradient_base.location = (pos_x + 400, pos_y)
    color_ramp_gradient_base.color_ramp.interpolation = 'LINEAR'
    elem = color_ramp_gradient_base.color_ramp.elements[0]
    elem.position = 0.0
    elem.color = (0, 0, 0, 1)
    elem = color_ramp_gradient_base.color_ramp.elements[1]
    bottom_softness_cloudscape = obj.cloud_settings.bottom_softness_cloudscape
    elem.position = bottom_softness_cloudscape
    elem.color = (1, 1, 1, 1)

    mat.node_tree.links.new(color_ramp_gradient_base.outputs["Color"],
                            subtract_gradient_gradient.inputs["Color1"])

    # Color Ramp - Gradient subtract
    color_ramp_gradient_subtract = mat_nodes.new("ShaderNodeValToRGB")
    color_ramp_gradient_subtract.parent = frame
    color_ramp_gradient_subtract.name = "ColorRamp - Gradient Subtract"
    color_ramp_gradient_subtract.label = "ColorRamp - Gradient Subtract"
    color_ramp_gradient_subtract.location = (pos_x + 400, pos_y - 400)
    color_ramp_gradient_subtract.color_ramp.interpolation = 'LINEAR'
    elem = color_ramp_gradient_subtract.color_ramp.elements[0]
    elem.position = 0.0
    elem.color = (0, 0, 0, 1)
    elem = color_ramp_gradient_subtract.color_ramp.elements[1]
    top_softness_cloudscape = obj.cloud_settings.top_softness_cloudscape
    elem.position = top_softness_cloudscape
    elem.color = (1, 1, 1, 1)

    mat.node_tree.links.new(color_ramp_gradient_subtract.outputs["Color"],
                            subtract_gradient_gradient.inputs["Color2"])

    # Gradient Texture base
    gradient_texture_base = mat_nodes.new("ShaderNodeTexGradient")
    gradient_texture_base.parent = frame
    gradient_texture_base.name = "Initial Shape Gradient Texture Base"
    gradient_texture_base.location = (pos_x + 200, pos_y)
    gradient_texture_base.gradient_type = "LINEAR"

    mat.node_tree.links.new(gradient_texture_base.outputs["Color"],
                            color_ramp_gradient_base.inputs["Fac"])

    # Gradient Texture subtract
    gradient_texture_subtract = mat_nodes.new("ShaderNodeTexGradient")
    gradient_texture_subtract.parent = frame
    gradient_texture_subtract.name = "Initial Shape Gradient Texture Subtract"
    gradient_texture_subtract.location = (pos_x + 200, pos_y - 400)
    gradient_texture_subtract.gradient_type = "LINEAR"

    mat.node_tree.links.new(gradient_texture_subtract.outputs["Color"],
                            color_ramp_gradient_subtract.inputs["Fac"])

    # Vector Multiply - Noise subtract
    multiply_noise = mat_nodes.new("ShaderNodeVectorMath")
    multiply_noise.parent = frame
    multiply_noise.location = (pos_x + 400, pos_y - 800)
    multiply_noise.name = "Vector Multiply - Noise subtract"
    multiply_noise.label = "Vector Multiply - Noise subtract"
    multiply_noise.operation = "MULTIPLY"
    multiply_noise.inputs[1].default_value = (5.0, 5.0, 5.0)

    mat.node_tree.links.new(multiply_noise.outputs["Vector"],
                            subtract_gradient_noise.inputs["Color2"])

    # Mapping base
    mapping_base = mat_nodes.new("ShaderNodeMapping")
    mapping_base.parent = frame
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
    mapping_noise.name = "Initial Shape Mapping Noise"
    mapping_noise.location = (pos_x, pos_y - 800)
    cloudscape_noise_coords = obj.cloud_settings.cloudscape_noise_coords
    mapping_noise.inputs["Location"].default_value = cloudscape_noise_coords
    mapping_noise.inputs["Rotation"].default_value = (0, 0, 0)
    mapping_noise.inputs["Scale"].default_value = (1, 1, 1)

    # Noise Tex - Subtract initial
    noise_subtract = mat_nodes.new("ShaderNodeTexNoise")
    noise_subtract.parent = frame
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

    reroute_6 = mat_nodes.new(type='NodeReroute')
    reroute_6.location = (pos_x + 300, pos_y - 1300)
    mat.node_tree.links.new(reroute_6.outputs[0],
                            reroute_5.inputs[0])
    mat.node_tree.links.new(in_node.outputs["Vector"],
                            reroute_6.inputs[0])

    mat.node_tree.links.new(reroute_5.outputs[0],
                            mapping_base.inputs[0])
    mat.node_tree.links.new(reroute_5.outputs[0],
                            mapping_subtract.inputs[0])
    mat.node_tree.links.new(reroute_5.outputs[0],
                            mapping_noise.inputs["Vector"])


def initial_shape_cloudscape_cirrus(pos_x, pos_y, texture_coordinate, cleaner_out, out_node, in_node, mat, obj):
    """
    pos_x: relative x position of nodes in the material node graph
    pos_y: relative y position of nodes in the material node graph
    texture_coordinate: texture coordinate in for image shape texture 
    cleaner_out: out for final cleaner
    out_node: out for the initial shape values
    in_node: coordinates used for initial shape
    mat: material to include nodes
    out_node: nodo de salida
    in_node: nodo de entrada
    mat: material. Used to access node_tree and insert connections and nodes
    obj: cloud object that has the material applied
    """

    mat_nodes = mat.node_tree.nodes # Fast access to nodes

    obj.cloud_settings.domain_cloud_position = (0.0, 0.0, 1.0)
    obj.cloud_settings.amount_of_clouds = 1.0
    wind_application_direction_big = mat_nodes.get("Vector Multiply - Wind application direction big")
    wind_application_direction_big.inputs[1].default_value = (10.0, 10.0, 0.4)
    wind_application_direction_small = mat_nodes.get("Vector Multiply - Wind application direction small")
    wind_application_direction_small.inputs[1].default_value = (1.0, 1.0, 0.4)

    noise_shape_wind_big =  mat_nodes.get("Noise Tex - Shape wind big turbulence")
    noise_shape_wind_big.inputs["Scale"].default_value = 0.1

    obj.cloud_settings.cloud_type = "CLOUDSCAPE_CIRRUS"
    frame = mat_nodes.new(type='NodeFrame')
    frame.name = "Initial shape"
    frame.label = "Initial shape"

    # Este tipo de nube ocupa mas que el resto por lo que para que quepa bien se desplaza
    pos_y = pos_y + 2000
    pos_x = pos_x - 700

    reroute_1 = mat_nodes.new(type='NodeReroute')
    reroute_2 = mat_nodes.new(type='NodeReroute')
    reroute_3 = mat_nodes.new(type='NodeReroute')
    reroute_4 = mat_nodes.new(type='NodeReroute')

    reroute_1.location = (pos_x + 1600, pos_y - 1950)
    reroute_2.location = (pos_x + 1900, pos_y - 1950)
    reroute_3.location = (pos_x + 900, pos_y - 1900)
    reroute_4.location = (pos_x - 800, pos_y - 1900)

    # Color Ramp cleaner
    color_ramp_cleaner = mat_nodes.new("ShaderNodeValToRGB")
    color_ramp_cleaner.name = "Final cleaning range"
    color_ramp_cleaner.label = "Final cleaning range"
    color_ramp_cleaner.location = (pos_x + 2500, pos_y - 800)
    color_ramp_cleaner.color_ramp.interpolation = 'LINEAR'
    elem = color_ramp_cleaner.color_ramp.elements[0]
    elem.position = 1.0 - obj.cloud_settings.cleaner_domain_size
    elem.color = (0, 0, 0, 1)
    elem = color_ramp_cleaner.color_ramp.elements[1]
    elem.position = 1.0
    elem.color = (1.0, 1.0, 1.0, 1)

    mat.node_tree.links.new(color_ramp_cleaner.outputs["Color"],
                            cleaner_out.inputs[1])

    # Invert color cleaner
    invert_color = mat_nodes.new("ShaderNodeInvert")
    invert_color.location = (pos_x + 2300, pos_y - 800)
    mat.node_tree.links.new(invert_color.outputs["Color"],
                            color_ramp_cleaner.inputs["Fac"])

    # RGB Multiply - Texture image shape
    texture_image_shape_multiply = mat_nodes.new("ShaderNodeMixRGB")
    texture_image_shape_multiply.parent = frame
    texture_image_shape_multiply.name = "RGB Multiply - Texture image shape"
    texture_image_shape_multiply.label = "RGB Multiply - Texture image shape"

    texture_image_shape_multiply.location = (pos_x + 1600, pos_y - 800)
    texture_image_shape_multiply.blend_type = "MULTIPLY"
    texture_image_shape_multiply.inputs["Fac"].default_value = 0.0

    mat.node_tree.links.new(reroute_1.outputs[0],
                            out_node.inputs["Color1"])
    mat.node_tree.links.new(reroute_2.outputs[0],
                            reroute_1.inputs[0])
    mat.node_tree.links.new(texture_image_shape_multiply.outputs["Color"],
                            reroute_2.inputs[0])

    mat.node_tree.links.new(texture_image_shape_multiply.outputs["Color"],
                            invert_color.inputs["Color"])

    # RGB Multiply - Cirrus shape
    cirrus_shape_multiply = mat_nodes.new("ShaderNodeMixRGB")
    cirrus_shape_multiply.parent = frame
    cirrus_shape_multiply.name = "RGB Multiply - Cirrus shape"
    cirrus_shape_multiply.label = "RGB Multiply - Cirrus shape"

    cirrus_shape_multiply.location = (pos_x + 1400, pos_y - 800)
    cirrus_shape_multiply.blend_type = "MULTIPLY"
    cirrus_shape_multiply.inputs["Fac"].default_value = 1.0

    mat.node_tree.links.new(cirrus_shape_multiply.outputs["Color"],
                            texture_image_shape_multiply.inputs["Color1"])

    # RGB Subtract - Gradient and Noise
    subtract_gradient_noise = mat_nodes.new("ShaderNodeMixRGB")
    subtract_gradient_noise.parent = frame
    subtract_gradient_noise.name = "RGB Subtract - Gradient and Noise"
    subtract_gradient_noise.label = "RGB Subtract - Gradient and Noise"

    subtract_gradient_noise.location = (pos_x + 900, pos_y - 300)
    subtract_gradient_noise.blend_type = "SUBTRACT"
    amount_of_clouds = 1 - obj.cloud_settings.amount_of_clouds
    subtract_gradient_noise.inputs["Fac"].default_value = amount_of_clouds

    mat.node_tree.links.new(subtract_gradient_noise.outputs["Color"],
                            cirrus_shape_multiply.inputs["Color1"])

    # Image texture - Shape of cloud
    image_texture_shape = mat_nodes.new("ShaderNodeTexImage")
    image_texture_shape.parent = frame
    image_texture_shape.name = "Image texture - Shape of cloud"
    image_texture_shape.label = "Image texture - Shape of cloud"

    image_texture_shape.location = (pos_x + 1100, pos_y - 1600)

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
    color_ramp_gradient_base.name = "ColorRamp - Gradient Base"
    color_ramp_gradient_base.label = "ColorRamp - Gradient Base"
    color_ramp_gradient_base.location = (pos_x + 400, pos_y)
    color_ramp_gradient_base.color_ramp.interpolation = 'CONSTANT'
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
    color_ramp_gradient_subtract.name = "ColorRamp - Gradient Subtract"
    color_ramp_gradient_subtract.label = "ColorRamp - Gradient Subtract"
    color_ramp_gradient_subtract.location = (pos_x + 400, pos_y - 400)
    color_ramp_gradient_subtract.color_ramp.interpolation = 'CONSTANT'
    elem = color_ramp_gradient_subtract.color_ramp.elements[0]
    elem.position = 0.0
    elem.color = (0, 0, 0, 1)
    elem = color_ramp_gradient_subtract.color_ramp.elements[1]
    elem.position = 0.2
    elem.color = (1, 1, 1, 1)

    mat.node_tree.links.new(color_ramp_gradient_subtract.outputs["Color"],
                            subtract_gradient_gradient.inputs["Color2"])

    # Gradient Texture base
    gradient_texture_base = mat_nodes.new("ShaderNodeTexGradient")
    gradient_texture_base.parent = frame
    gradient_texture_base.name = "Initial Shape Gradient Texture Base"
    gradient_texture_base.location = (pos_x + 200, pos_y)
    gradient_texture_base.gradient_type = "LINEAR"

    mat.node_tree.links.new(gradient_texture_base.outputs["Color"],
                            color_ramp_gradient_base.inputs["Fac"])

    # Gradient Texture subtract
    gradient_texture_subtract = mat_nodes.new("ShaderNodeTexGradient")
    gradient_texture_subtract.parent = frame
    gradient_texture_subtract.name = "Initial Shape Gradient Texture Subtract"
    gradient_texture_subtract.location = (pos_x + 200, pos_y - 400)
    gradient_texture_subtract.gradient_type = "LINEAR"

    mat.node_tree.links.new(gradient_texture_subtract.outputs["Color"],
                            color_ramp_gradient_subtract.inputs["Fac"])


    # Vector Multiply - Cirrus coverage
    multiply_coverage = mat_nodes.new("ShaderNodeVectorMath")
    multiply_coverage.parent = frame
    multiply_coverage.location = (pos_x + 1000, pos_y - 700)
    multiply_coverage.name = "Vector Multiply - Cirrus coverage"
    multiply_coverage.label = "Vector Multiply - Cirrus coverage"
    multiply_coverage.operation = "MULTIPLY"

    mat.node_tree.links.new(multiply_coverage.outputs["Vector"],
                            subtract_gradient_noise.inputs["Color2"])

    # Greater Than
    length_greater_than_2 = mat_nodes.new("ShaderNodeMath")
    length_greater_than_2.parent = frame
    length_greater_than_2.location = (pos_x + 800, pos_y - 900)
    length_greater_than_2.operation = "GREATER_THAN"
    length_greater_than_2.inputs[1].default_value = 5.2

    mat.node_tree.links.new(length_greater_than_2.outputs["Value"],
                            multiply_coverage.inputs[1])
    # Vector Length
    lenght_2 = mat_nodes.new("ShaderNodeVectorMath")
    lenght_2.parent = frame
    lenght_2.location = (pos_x + 600, pos_y - 900)
    lenght_2.operation = "LENGTH"

    mat.node_tree.links.new(lenght_2.outputs["Value"],
                            length_greater_than_2.inputs["Value"])


    # Vector Multiply - Noise subtract
    multiply_noise = mat_nodes.new("ShaderNodeVectorMath")
    multiply_noise.parent = frame
    multiply_noise.location = (pos_x + 400, pos_y - 800)
    multiply_noise.name = "Vector Multiply - Noise subtract"
    multiply_noise.label = "Vector Multiply - Noise subtract"
    multiply_noise.operation = "MULTIPLY"
    multiply_noise.inputs[1].default_value = (5.0, 5.0, 5.0)

    mat.node_tree.links.new(multiply_noise.outputs["Vector"],
                            lenght_2.inputs[0])

    mat.node_tree.links.new(multiply_noise.outputs["Vector"],
                            multiply_coverage.inputs[0])

    # Mapping base
    mapping_base = mat_nodes.new("ShaderNodeMapping")
    mapping_base.parent = frame
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
    mapping_subtract.name = "Initial Shape Mapping Subtract"
    mapping_subtract.location = (pos_x, pos_y - 400)
    obj.cloud_settings.height_cloudscape = 0.2
    height_cloudscape = obj.cloud_settings.height_cloudscape
    mapping_subtract.inputs["Location"].default_value = (-height_cloudscape, 0.0, 0.0)
    mapping_subtract.inputs["Rotation"].default_value = (0, pi/2, 0)
    mapping_subtract.inputs["Scale"].default_value = (1, 1, 1)

    mat.node_tree.links.new(mapping_subtract.outputs["Vector"],
                            gradient_texture_subtract.inputs["Vector"])

    # Mapping noise
    mapping_noise = mat_nodes.new("ShaderNodeMapping")
    mapping_noise.parent = frame
    mapping_noise.name = "Initial Shape Mapping Noise"
    mapping_noise.location = (pos_x, pos_y - 800)
    cloudscape_noise_coords = obj.cloud_settings.cloudscape_noise_coords
    mapping_noise.inputs["Location"].default_value = cloudscape_noise_coords
    mapping_noise.inputs["Rotation"].default_value = (0, 0, 0)
    mapping_noise.inputs["Scale"].default_value = (1, 1, 1)

    # Noise Tex - Subtract initial
    noise_subtract = mat_nodes.new("ShaderNodeTexNoise")
    noise_subtract.parent = frame
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

    # Vector Multiply - Cirrus shape width operation
    multiply_for_width_operation_cirrus = mat_nodes.new("ShaderNodeVectorMath")
    multiply_for_width_operation_cirrus.parent = frame
    multiply_for_width_operation_cirrus.location = (pos_x + 800, pos_y - 1200)
    multiply_for_width_operation_cirrus.name = "Vector Multiply - Cirrus shape width operation"
    multiply_for_width_operation_cirrus.label = "Vector Multiply - Cirrus shape width operation"
    multiply_for_width_operation_cirrus.operation = "MULTIPLY"
    cloudscape_cirrus_cirrus_width = 1 - obj.cloud_settings.cloudscape_cirrus_cirrus_width
    multiply_for_width_operation_cirrus.inputs[1].default_value = (cloudscape_cirrus_cirrus_width,
                                                                   cloudscape_cirrus_cirrus_width,
                                                                   cloudscape_cirrus_cirrus_width)

    mat.node_tree.links.new(multiply_for_width_operation_cirrus.outputs["Vector"],
                            cirrus_shape_multiply.inputs["Color2"])

    # Vector Divide - Cirrus shape between 0 and 1 operation
    divide_two_operation_cirrus = mat_nodes.new("ShaderNodeVectorMath")
    divide_two_operation_cirrus.parent = frame
    divide_two_operation_cirrus.location = (pos_x + 600, pos_y - 1200)
    divide_two_operation_cirrus.name = "Vector Divide - Cirrus shape between 0 and 1 operation"
    divide_two_operation_cirrus.label = "Vector Divide - Cirrus shape between 0 and 1 operation"
    divide_two_operation_cirrus.operation = "DIVIDE"
    divide_two_operation_cirrus.inputs[1].default_value = (2.0, 2.0, 2.0)

    mat.node_tree.links.new(divide_two_operation_cirrus.outputs["Vector"],
                            multiply_for_width_operation_cirrus.inputs[0])

    # Vector Add - Cirrus shape between 0 and 1 operation
    add_one_operation_cirrus = mat_nodes.new("ShaderNodeVectorMath")
    add_one_operation_cirrus.parent = frame
    add_one_operation_cirrus.location = (pos_x + 400, pos_y - 1200)
    add_one_operation_cirrus.name = "Vector Add - Cirrus shape between 0 and 1 operation"
    add_one_operation_cirrus.label = "Vector Add - Cirrus shape between 0 and 1 operation"
    add_one_operation_cirrus.operation = "ADD"
    add_one_operation_cirrus.inputs[1].default_value = (1.0, 1.0, 1.0)

    mat.node_tree.links.new(add_one_operation_cirrus.outputs["Vector"],
                            divide_two_operation_cirrus.inputs[0])

    # Vector Sine - Cirrus shape
    sine_cirrus = mat_nodes.new("ShaderNodeVectorMath")
    sine_cirrus.parent = frame
    sine_cirrus.location = (pos_x + 200, pos_y - 1200)
    sine_cirrus.name = "Vector Sine - Cirrus Shape"
    sine_cirrus.label = "Vector Sine - Cirrus Shape"
    sine_cirrus.operation = "SINE"

    mat.node_tree.links.new(sine_cirrus.outputs["Vector"],
                            add_one_operation_cirrus.inputs[0])

    # Mapping cirrus shape
    mapping_cirrus_shape = mat_nodes.new("ShaderNodeMapping")
    mapping_cirrus_shape.parent = frame
    mapping_cirrus_shape.name = "Initial Shape Mapping Cirrus Shape"
    mapping_cirrus_shape.location = (pos_x, pos_y - 1200)
    cloudscape_cirrus_cirrus_amount = obj.cloud_settings.cloudscape_cirrus_cirrus_amount
    mapping_cirrus_shape.inputs["Scale"].default_value = (cloudscape_cirrus_cirrus_amount, 0, 0)

    mat.node_tree.links.new(mapping_cirrus_shape.outputs["Vector"],
                            sine_cirrus.inputs[0])

    reroute_5 = mat_nodes.new(type='NodeReroute')
    reroute_5.location = (pos_x - 100, pos_y - 1950)

    mat.node_tree.links.new(mapping_noise.outputs[0],
                            noise_subtract.inputs[0])

    reroute_6 = mat_nodes.new(type='NodeReroute')
    reroute_6.location = (pos_x + 600, pos_y - 1950)
    mat.node_tree.links.new(reroute_6.outputs[0],
                            reroute_5.inputs[0])
    mat.node_tree.links.new(in_node.outputs["Vector"],
                            reroute_6.inputs[0])

    mat.node_tree.links.new(reroute_5.outputs[0],
                            mapping_base.inputs["Vector"])
    mat.node_tree.links.new(reroute_5.outputs[0],
                            mapping_subtract.inputs["Vector"])
    mat.node_tree.links.new(reroute_5.outputs[0],
                            mapping_noise.inputs["Vector"])
    mat.node_tree.links.new(reroute_5.outputs[0],
                            mapping_cirrus_shape.inputs["Vector"])


def generate_cloud(context, pos_x, pos_y, initial_shape):
    """
    pos_x: x position of the material node graph
    pos_y: y position of the material node graph
    initial_shape: function that generates the part of the material 
        corresponding to the initial base shape of the clouds
    """
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
    obj.cloud_settings.update_properties = False  # Set to false because the nodes do not exist yet

    obj.cloud_settings.wind_big_turbulence = random.uniform(0.2, 1.0)
    obj.cloud_settings.wind_small_turbulence = random.uniform(0.2, 0.5)
    obj.cloud_settings.detail_wind_strength = random.uniform(0.0, 1.0)
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
    obj.cloud_settings.roundness_simple_seed = obj.cloud_settings.roundness_coords.x

    obj.cloud_settings.add_shape_imperfection_coords = (
                                                        random.uniform(0, 200),
                                                        random.uniform(0, 200),
                                                        random.uniform(0, 200)
                                                        )
    obj.cloud_settings.add_shape_imperfection_simple_seed = obj.cloud_settings.add_shape_imperfection_coords.x
    obj.cloud_settings.subtract_shape_imperfection_coords = (
                                                                random.uniform(0, 200),
                                                                random.uniform(0, 200),
                                                                random.uniform(0, 200)
                                                            )
    obj.cloud_settings.subtract_shape_imperfection_simple_seed = obj.cloud_settings.subtract_shape_imperfection_coords.x
    obj.cloud_settings.cloudscape_noise_coords = (
                                                    random.uniform(0, 200),
                                                    random.uniform(0, 200),
                                                    random.uniform(0, 200)
                                                )
    obj.cloud_settings.cloudscape_noise_simple_seed = obj.cloud_settings.cloudscape_noise_coords.x

    obj.cloud_settings.wind_big_turbulence_coords = (
                                                    random.uniform(0, 200),
                                                    random.uniform(0, 200),
                                                    random.uniform(0, 200)
                                                )
    obj.cloud_settings.wind_turbulence_simple_seed = obj.cloud_settings.wind_big_turbulence_coords.x

    obj.cloud_settings.wind_small_turbulence_coords = (
                                                    random.uniform(0, 200),
                                                    random.uniform(0, 200),
                                                    random.uniform(0, 200)
                                                )

    obj.cloud_settings.update_properties = True
    # -----------------------------------------------
    # -------------Material construction-------------
    # -----------------------------------------------
    # From final node to beginning

    # Reroutes
    reroute_1 = mat_nodes.new(type='NodeReroute')
    reroute_1.location = (pos_x + 2100, pos_y - 1500)

    reroute_2 = mat_nodes.new(type='NodeReroute')
    reroute_2.location = (pos_x + 2100, pos_y - 2300)

    reroute_3 = mat_nodes.new(type='NodeReroute')
    reroute_3.location = (pos_x + 3000, pos_y - 2300)

    reroute_4 = mat_nodes.new(type='NodeReroute')
    reroute_4.location = (pos_x + 500, pos_y - 1500)

    # -------------BEGINNING MAIN BRANCH-------------
    # Material Output
    material_output = mat_nodes.new("ShaderNodeOutputMaterial")
    material_output.name = "Cloud Output"
    material_output.location = (pos_x + 6300, pos_y)

    # Principled Volume
    principled_volume = mat_nodes.new("ShaderNodeVolumePrincipled")
    principled_volume.name = "Cloud Principled Volume"
    principled_volume.location = (pos_x + 6000, pos_y)
    principled_volume.inputs["Color"].default_value = (1, 1, 1, 1)

    # Connection between Principled Volume and Material Output.
    mat.node_tree.links.new(principled_volume.outputs["Volume"],
                            material_output.inputs["Volume"])

    # Final density Color Ramp
    color_ramp_density = mat_nodes.new("ShaderNodeValToRGB")
    color_ramp_density.name = "ColorRamp - Cloud Density"
    color_ramp_density.label = "ColorRamp - Cloud Density"
    color_ramp_density.location = (pos_x + 5650, pos_y)
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

    # Vector Subtract - Final Cleaner
    subtract_final_cleaner = mat_nodes.new("ShaderNodeVectorMath")
    subtract_final_cleaner.name = "Vector Subtract - Final Cleaner"
    subtract_final_cleaner.label = "Vector Subtract - Final Cleaner"
    subtract_final_cleaner.location = (pos_x + 5450, pos_y)
    subtract_final_cleaner.operation = "SUBTRACT"

    mat.node_tree.links.new(subtract_final_cleaner.outputs[0],
                            color_ramp_density.inputs["Fac"])

    # RGB Overlay - Detail noise
    overlay_detail_noise = mat_nodes.new("ShaderNodeMixRGB")
    overlay_detail_noise.name = "RGB Overlay - Noise"
    overlay_detail_noise.label = "RGB Overlay - Noise"
    overlay_detail_noise.location = (pos_x + 5050, pos_y)
    overlay_detail_noise.blend_type = "OVERLAY"
    detail_noise = obj.cloud_settings.detail_noise
    overlay_detail_noise.inputs["Fac"].default_value = detail_noise

    mat.node_tree.links.new(overlay_detail_noise.outputs["Color"],
                            subtract_final_cleaner.inputs[0])

    # RGB Multiply - Bump
    multiply_bump = mat_nodes.new("ShaderNodeMixRGB")
    multiply_bump.name = "RGB Multiply - Bump"
    multiply_bump.label = "RGB Multiply - Bump"
    multiply_bump.location = (pos_x + 4850, pos_y)
    multiply_bump.blend_type = "MULTIPLY"
    detail_bump_strength = obj.cloud_settings.detail_bump_strength
    multiply_bump.inputs["Fac"].default_value = detail_bump_strength

    mat.node_tree.links.new(multiply_bump.outputs["Color"],
                            overlay_detail_noise.inputs["Color1"])

    # BEGINNING SIMPLE CLEANER FRAME
    frame = mat_nodes.new(type='NodeFrame')
    frame.name = "Simple cleaner"
    frame.label = "Simple cleaner"

    # Vector Multiply - Simple cleaner
    multiply_cleaner = mat_nodes.new("ShaderNodeVectorMath")
    multiply_cleaner.parent = frame
    multiply_cleaner.location = (pos_x + 4200, pos_y)
    multiply_cleaner.name = "Vector Multiply - Simple cleaner"
    multiply_cleaner.label = "Vector Multiply - Simple cleaner"
    multiply_cleaner.operation = "MULTIPLY"

    mat.node_tree.links.new(multiply_cleaner.outputs["Vector"],
                            multiply_bump.inputs["Color1"])

    # Greater Than
    length_greater_than = mat_nodes.new("ShaderNodeMath")
    length_greater_than.parent = frame
    length_greater_than.location = (pos_x + 3950, pos_y - 200)
    length_greater_than.operation = "GREATER_THAN"
    length_greater_than.inputs[1].default_value = 0.520

    mat.node_tree.links.new(length_greater_than.outputs["Value"],
                            multiply_cleaner.inputs[1])
    # Vector Length
    lenght = mat_nodes.new("ShaderNodeVectorMath")
    lenght.parent = frame
    lenght.location = (pos_x + 3750, pos_y - 200)
    lenght.operation = "LENGTH"

    mat.node_tree.links.new(lenght.outputs["Value"],
                            length_greater_than.inputs["Value"])

    # END SIMPLE CLEANER FRAME

    # RGB Subtract - Shape imperfection
    subtract_imperfection = mat_nodes.new("ShaderNodeMixRGB")
    subtract_imperfection.name = "RGB Subtract - Shape imperfection"
    subtract_imperfection.label = "RGB Subtract - Shape imperfection"
    subtract_imperfection.location = (pos_x + 3350, pos_y)
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
    add_imperfection.location = (pos_x + 3150, pos_y)
    add_imperfection.blend_type = "ADD"
    add_shape_imperfection = obj.cloud_settings.add_shape_imperfection
    add_imperfection.inputs["Fac"].default_value = add_shape_imperfection

    mat.node_tree.links.new(add_imperfection.outputs["Color"],
                            subtract_imperfection.inputs["Color1"])

    # RGB Overlay - Roundness
    overlay_roundness = mat_nodes.new("ShaderNodeMixRGB")
    overlay_roundness.name = "RGB Overlay - Roundness"
    overlay_roundness.label = "RGB Overlay - Roundness"
    overlay_roundness.location = (pos_x + 2950, pos_y)
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

    # RGB Add - Shape wind strength
    add_shape_wind = mat_nodes.new("ShaderNodeVectorMath")
    add_shape_wind.parent = frame
    add_shape_wind.name = "Vector Add - Add shape wind"
    add_shape_wind.label = "Vector Add - Add shape wind"
    add_shape_wind.location = (pos_x + 1900, pos_y)
    add_shape_wind.operation = "ADD"

    # Wind strength
    wind_strength = mat_nodes.new("ShaderNodeVectorMath")
    wind_strength.parent = frame
    wind_strength.name = "Vector Multiply - Shape wind strength"
    wind_strength.label = "Vector Multiply - Shape wind strength"
    wind_strength.location = (pos_x + 1700, pos_y - 250)
    wind_strength.operation = "MULTIPLY"
    wind_strength_value = obj.cloud_settings.wind_strength
    wind_strength.inputs[1].default_value = (wind_strength_value, wind_strength_value, wind_strength_value)

    mat.node_tree.links.new(wind_strength.outputs["Vector"],
                            add_shape_wind.inputs[1])

    # Wind small turbulence

    # RGB Add - Shape wind small turbulence
    add_shape_wind_small = mat_nodes.new("ShaderNodeMixRGB")
    add_shape_wind_small.parent = frame
    add_shape_wind_small.name = "Shape wind small turbulence"
    add_shape_wind_small.label = "Shape wind small turbulence"
    add_shape_wind_small.location = (pos_x + 1300, pos_y - 150)
    add_shape_wind_small.blend_type = "ADD"
    add_shape_wind_small.inputs["Color1"].default_value = (0.0, 0.0, 0.0, 1.0)
    wind_small_turbulence = obj.cloud_settings.wind_small_turbulence
    add_shape_wind_small.inputs["Fac"].default_value = wind_small_turbulence

    # Vector Multiply - Wind application direction
    wind_application_direction_small = mat_nodes.new("ShaderNodeVectorMath")
    wind_application_direction_small.parent = frame
    wind_application_direction_small.location = (pos_x + 1100, pos_y - 150)
    wind_application_direction_small.name = "Vector Multiply - Wind application direction small"
    wind_application_direction_small.label = "Vector Multiply - Wind application direction small"
    wind_application_direction_small.operation = "MULTIPLY"
    wind_application_direction_small.inputs[1].default_value = (1.0, 1.0, 0.5)

    mat.node_tree.links.new(wind_application_direction_small.outputs["Vector"],
                            add_shape_wind_small.inputs["Color2"])

    # Vector Subtract - Shape wind small turbulence domain to -0.5 to 0.5
    domain_adjustment_shape_wind_small = mat_nodes.new("ShaderNodeVectorMath")
    domain_adjustment_shape_wind_small.parent = frame
    domain_adjustment_shape_wind_small.location = (pos_x + 900, pos_y - 150)
    domain_adjustment_shape_wind_small.name = "Vector Subtract - Shape wind small turbulence domain adjustment"
    domain_adjustment_shape_wind_small.label = "Vector Subtract - Shape wind small turbulence domain adjustment"
    domain_adjustment_shape_wind_small.operation = "SUBTRACT"
    domain_adjustment_shape_wind_small.inputs[1].default_value = (0.5, 0.5, 0.5)

    mat.node_tree.links.new(domain_adjustment_shape_wind_small.outputs["Vector"],
                            wind_application_direction_small.inputs[0])

    # Noise Tex - Shape wind small turbulence
    noise_shape_wind_small = mat_nodes.new("ShaderNodeTexNoise")
    noise_shape_wind_small.parent = frame
    noise_shape_wind_small.name = "Noise Tex - Shape wind small turbulence"
    noise_shape_wind_small.label = "Noise Tex - Shape wind small turbulence"
    noise_shape_wind_small.location = (pos_x + 700, pos_y - 150)
    noise_shape_wind_small.inputs["Scale"].default_value = 1.5
    noise_shape_wind_small.inputs["Detail"].default_value = 0.0
    noise_shape_wind_small.inputs["Roughness"].default_value = 0.0
    noise_shape_wind_small.inputs["Distortion"].default_value = 3.0

    mat.node_tree.links.new(noise_shape_wind_small.outputs["Fac"],
                            domain_adjustment_shape_wind_small.inputs[0])

    # Vector Add - Wind small coords
    add_coords_wind_small = mat_nodes.new("ShaderNodeVectorMath")
    add_coords_wind_small.parent = frame
    add_coords_wind_small.location = (pos_x + 500, pos_y - 150)
    add_coords_wind_small.name = "Vector Add - Wind small turbulence coords"
    add_coords_wind_small.label = "Vector Add - Wind small turbulence coords"
    add_coords_wind_small.operation = "ADD"
    wind_small_turbulence_coords = obj.cloud_settings.wind_small_turbulence_coords
    add_coords_wind_small.inputs[1].default_value = wind_small_turbulence_coords
    mat.node_tree.links.new(add_coords_wind_small.outputs["Vector"],
                            noise_shape_wind_small.inputs["Vector"])

    # Wind big turbulence

    # RGB Add - Shape wind big turbulence
    add_shape_wind_big = mat_nodes.new("ShaderNodeMixRGB")
    add_shape_wind_big.parent = frame
    add_shape_wind_big.name = "Shape wind big turbulence"
    add_shape_wind_big.label = "Shape wind big turbulence"
    add_shape_wind_big.location = (pos_x + 1500, pos_y - 250)
    add_shape_wind_big.blend_type = "ADD"
    add_shape_wind_big.inputs["Color1"].default_value = (0.0, 0.0, 0.0, 1.0)
    wind_big_turbulence = obj.cloud_settings.wind_big_turbulence
    add_shape_wind_big.inputs["Fac"].default_value = wind_big_turbulence

    mat.node_tree.links.new(add_shape_wind_small.outputs["Color"],
                            add_shape_wind_big.inputs["Color1"])
    mat.node_tree.links.new(add_shape_wind_big.outputs["Color"],
                            wind_strength.inputs[0])

    # Vector Multiply - Wind application direction
    wind_application_direction_big = mat_nodes.new("ShaderNodeVectorMath")
    wind_application_direction_big.parent = frame
    wind_application_direction_big.location = (pos_x + 1100, pos_y - 400)
    wind_application_direction_big.name = "Vector Multiply - Wind application direction big"
    wind_application_direction_big.label = "Vector Multiply - Wind application direction big"
    wind_application_direction_big.operation = "MULTIPLY"
    wind_application_direction_big.inputs[1].default_value = (1.0, 1.0, 0.5)

    mat.node_tree.links.new(wind_application_direction_big.outputs["Vector"],
                            add_shape_wind_big.inputs["Color2"])

    # Vector Subtract - Shape wind big turbulence domain to -0.5 to 0.5
    domain_adjustment_shape_wind_big = mat_nodes.new("ShaderNodeVectorMath")
    domain_adjustment_shape_wind_big.parent = frame
    domain_adjustment_shape_wind_big.location = (pos_x + 900, pos_y - 400)
    domain_adjustment_shape_wind_big.name = "Vector Subtract - Shape wind big turbulence domain adjustment"
    domain_adjustment_shape_wind_big.label = "Vector Subtract - Shape wind big turbulence domain adjustment"
    domain_adjustment_shape_wind_big.operation = "SUBTRACT"
    domain_adjustment_shape_wind_big.inputs[1].default_value = (0.5, 0.5, 0.5)

    mat.node_tree.links.new(domain_adjustment_shape_wind_big.outputs["Vector"],
                            wind_application_direction_big.inputs[0])

    # Noise Tex - Shape wind big turbulence
    noise_shape_wind_big = mat_nodes.new("ShaderNodeTexNoise")
    noise_shape_wind_big.parent = frame
    noise_shape_wind_big.name = "Noise Tex - Shape wind big turbulence"
    noise_shape_wind_big.label = "Noise Tex - Shape wind big turbulence"
    noise_shape_wind_big.location = (pos_x + 700, pos_y - 400)
    noise_shape_wind_big.inputs["Scale"].default_value = 0.2
    noise_shape_wind_big.inputs["Detail"].default_value = 0.0
    noise_shape_wind_big.inputs["Roughness"].default_value = 0.0
    noise_shape_wind_big.inputs["Distortion"].default_value = 3.0

    mat.node_tree.links.new(noise_shape_wind_big.outputs["Fac"],
                            domain_adjustment_shape_wind_big.inputs[0])

    # Vector Add - Wind big coords
    add_coords_wind_big = mat_nodes.new("ShaderNodeVectorMath")
    add_coords_wind_big.parent = frame
    add_coords_wind_big.location = (pos_x + 500, pos_y - 400)
    add_coords_wind_big.name = "Vector Add - Wind big turbulence coords"
    add_coords_wind_big.label = "Vector Add - Wind big turbulence coords"
    add_coords_wind_big.operation = "ADD"
    wind_big_turbulence_coords = obj.cloud_settings.wind_big_turbulence_coords
    add_coords_wind_big.inputs[1].default_value = wind_big_turbulence_coords
    mat.node_tree.links.new(add_coords_wind_big.outputs["Vector"],
                            noise_shape_wind_big.inputs["Vector"])

    # END WIND FRAME

    # Initial mapping
    initial_mapping = mat_nodes.new("ShaderNodeMapping")
    initial_mapping.name = "Initial mapping"
    initial_mapping.location = (pos_x + 200, pos_y)
    domain_cloud_position = obj.cloud_settings.domain_cloud_position
    initial_mapping.inputs["Location"].default_value = domain_cloud_position

    mat.node_tree.links.new(initial_mapping.outputs["Vector"],
                            add_shape_wind.inputs[0])
    mat.node_tree.links.new(initial_mapping.outputs["Vector"],
                            add_coords_wind_small.inputs[0])
    mat.node_tree.links.new(initial_mapping.outputs["Vector"],
                            add_coords_wind_big.inputs[0])
    mat.node_tree.links.new(initial_mapping.outputs["Vector"],
                            reroute_4.inputs[0])

    # Texture Coordinate
    texture_coordinate = mat_nodes.new("ShaderNodeTexCoord")
    texture_coordinate.location = (pos_x, pos_y)
    mat.node_tree.links.new(texture_coordinate.outputs["Object"],
                            initial_mapping.inputs["Vector"])

    initial_shape(pos_x + 2000, pos_y, texture_coordinate, subtract_final_cleaner, overlay_roundness, add_shape_wind, mat, obj)

    # ----------------END MAIN BRANCH----------------

    mat.node_tree.links.new(reroute_4.outputs[0],
                            reroute_1.inputs[0])
    mat.node_tree.links.new(reroute_1.outputs[0],
                            reroute_2.inputs[0])
    mat.node_tree.links.new(reroute_2.outputs[0],
                            reroute_3.inputs[0])

    # -------------BEGINNING BUMP BRANCH-------------
    frame = mat_nodes.new(type='NodeFrame')
    frame.name = "Bump"
    frame.label = "Bump"

    # Invert color
    invert_color = mat_nodes.new("ShaderNodeInvert")
    invert_color.parent = frame
    invert_color.location = (pos_x + 4550, pos_y - 500)
    mat.node_tree.links.new(invert_color.outputs["Color"],
                            multiply_bump.inputs["Color2"])
    # RGB Overlay - Bump level 3
    overlay_bump_3 = mat_nodes.new("ShaderNodeMixRGB")
    overlay_bump_3.parent = frame
    overlay_bump_3.name = "RGB Overlay - Bump level 3"
    overlay_bump_3.label = "RGB Overlay - Bump level 3"
    overlay_bump_3.location = (pos_x + 4350, pos_y - 500)
    overlay_bump_3.blend_type = "OVERLAY"

    mat.node_tree.links.new(overlay_bump_3.outputs["Color"],
                            invert_color.inputs["Color"])

    # RGB Overlay - Bump level 2
    overlay_bump_2 = mat_nodes.new("ShaderNodeMixRGB")
    overlay_bump_2.parent = frame
    overlay_bump_2.name = "RGB Overlay - Bump level 2"
    overlay_bump_2.label = "RGB Overlay - Bump level 2"
    overlay_bump_2.location = (pos_x + 4150, pos_y - 500)
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
    voronoi_bump_1.location = (pos_x + 3950, pos_y - 500)

    mat.node_tree.links.new(voronoi_bump_1.outputs["Distance"],
                            overlay_bump_2.inputs["Color1"])

    # Voronoi tex - Bump level 2
    voronoi_bump_2 = mat_nodes.new("ShaderNodeTexVoronoi")
    voronoi_bump_2.parent = frame
    voronoi_bump_2.name = "Voronoi tex - Bump level 2"
    voronoi_bump_2.label = "Voronoi tex - Bump level 2"
    voronoi_bump_2.location = (pos_x + 3950, pos_y - 800)
    voronoi_bump_2.inputs["Scale"].default_value = 10

    mat.node_tree.links.new(voronoi_bump_2.outputs["Distance"],
                            overlay_bump_2.inputs["Color2"])

    # Voronoi tex - Bump level 3
    voronoi_bump_3 = mat_nodes.new("ShaderNodeTexVoronoi")
    voronoi_bump_3.parent = frame
    voronoi_bump_3.name = "Voronoi tex - Bump level 3"
    voronoi_bump_3.label = "Voronoi tex - Bump level 3"
    voronoi_bump_3.location = (pos_x + 3950, pos_y - 1100)
    voronoi_bump_3.inputs["Scale"].default_value = 30.0

    mat.node_tree.links.new(voronoi_bump_3.outputs["Distance"],
                            overlay_bump_3.inputs["Color2"])

    # RGB Add - Small wind
    add_small_wind = mat_nodes.new("ShaderNodeMixRGB")
    add_small_wind.parent = frame
    add_small_wind.name = "RGB Add - Small wind"
    add_small_wind.label = "RGB Add - Small wind"
    add_small_wind.location = (pos_x + 3750, pos_y - 950)
    add_small_wind.blend_type = "ADD"
    detail_wind_strength = obj.cloud_settings.detail_wind_strength
    add_small_wind.inputs["Fac"].default_value = detail_wind_strength

    mat.node_tree.links.new(add_small_wind.outputs["Color"],
                            voronoi_bump_1.inputs["Vector"])
    mat.node_tree.links.new(add_small_wind.outputs["Color"],
                            voronoi_bump_2.inputs["Vector"])
    mat.node_tree.links.new(add_small_wind.outputs["Color"],
                            voronoi_bump_3.inputs["Vector"])

    # Vector Add - Bump coordinates
    add_coords_bump = mat_nodes.new("ShaderNodeVectorMath")
    add_coords_bump.parent = frame
    add_coords_bump.location = (pos_x + 3350, pos_y - 800)
    add_coords_bump.name = "Vector Add - Bump coordinates"
    add_coords_bump.label = "Vector Add - Bump coordinates"
    add_coords_bump.operation = "ADD"
    add_coords_bump.inputs[1].default_value = (5.0, 8.5, 11.0)

    mat.node_tree.links.new(add_coords_bump.outputs["Vector"],
                            add_small_wind.inputs["Color1"])

    # Vector Subtract - Small wind domain to -0.5 to 0.5
    domain_adjustment_small_wind = mat_nodes.new("ShaderNodeVectorMath")
    domain_adjustment_small_wind.parent = frame
    domain_adjustment_small_wind.location = (pos_x + 3550, pos_y - 1100)
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
    noise_small_wind.location = (pos_x + 3350, pos_y - 1100)
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

    # Noise Tex - Detail noise level
    detetail_noise = mat_nodes.new("ShaderNodeTexNoise")
    detetail_noise.parent = frame
    detetail_noise.name = "Noise Tex - Detail noise level 1"
    detetail_noise.label = "Noise Tex - Detail noise level 1"
    detetail_noise.location = (pos_x + 4550, pos_y - 1500)
    detetail_noise.inputs["Scale"].default_value = 12.0
    detetail_noise.inputs["Detail"].default_value = 4.0
    detetail_noise.inputs["Roughness"].default_value = 1.0
    detetail_noise.inputs["Distortion"].default_value = 0.0

    mat.node_tree.links.new(detetail_noise.outputs["Fac"],
                            overlay_detail_noise.inputs["Color2"])

    mat.node_tree.links.new(reroute_3.outputs[0],
                            detetail_noise.inputs["Vector"])
    # -----------END DETAIL NOISE BRANCH-------------

    # ----------BEGINNING ROUNDNESS BRANCH-----------
    frame = mat_nodes.new(type='NodeFrame')
    frame.name = "Roundness"
    frame.label = "Roundness"

    # Invert color
    invert_color = mat_nodes.new("ShaderNodeInvert")
    invert_color.parent = frame
    invert_color.location = (pos_x + 2700, pos_y - 500)
    mat.node_tree.links.new(invert_color.outputs["Color"],
                            overlay_roundness.inputs["Color2"])

    # Voronoi tex - Roundness
    voronoi_roundness = mat_nodes.new("ShaderNodeTexVoronoi")
    voronoi_roundness.parent = frame
    voronoi_roundness.name = "Voronoi tex - Roundness"
    voronoi_roundness.label = "Voronoi tex - Roundness"
    voronoi_roundness.location = (pos_x + 2500, pos_y - 500)
    voronoi_roundness.inputs["Scale"].default_value = 2.0

    mat.node_tree.links.new(voronoi_roundness.outputs["Distance"],
                            invert_color.inputs["Color"])

    # Vector Add - Roundness coord
    add_coords_roundness = mat_nodes.new("ShaderNodeVectorMath")
    add_coords_roundness.parent = frame
    add_coords_roundness.location = (pos_x + 2300, pos_y - 500)
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
    color_burn_noises.location = (pos_x + 2700, pos_y - 900)
    color_burn_noises.blend_type = "BURN"
    color_burn_noises.inputs["Fac"].default_value = 1.0

    mat.node_tree.links.new(color_burn_noises.outputs["Color"],
                            add_imperfection.inputs["Color2"])

    # Noise Tex - Add shape imperfection 1
    noise_add_shape_imperfection_1 = mat_nodes.new("ShaderNodeTexNoise")
    noise_add_shape_imperfection_1.parent = frame
    noise_add_shape_imperfection_1.name = "Noise Tex - Add shape imperfection 1"
    noise_add_shape_imperfection_1.label = "Noise Tex - Add shape imperfection 1"
    noise_add_shape_imperfection_1.location = (pos_x + 2500, pos_y - 900)
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
    noise_add_shape_imperfection_2.location = (pos_x + 2500, pos_y - 1150)
    noise_add_shape_imperfection_2.inputs["Scale"].default_value = 1.9
    noise_add_shape_imperfection_2.inputs["Detail"].default_value = 16.0
    noise_add_shape_imperfection_2.inputs["Roughness"].default_value = 0.0
    noise_add_shape_imperfection_2.inputs["Distortion"].default_value = 0.0

    mat.node_tree.links.new(noise_add_shape_imperfection_2.outputs["Fac"],
                            color_burn_noises.inputs["Color2"])

    # Vector Add - Coords add shape imperfection 1
    coords_add_shape_imperfection_1 = mat_nodes.new("ShaderNodeVectorMath")
    coords_add_shape_imperfection_1.parent = frame
    coords_add_shape_imperfection_1.location = (pos_x + 2300, pos_y - 900)
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
    coords_add_shape_imperfection_2.location = (pos_x + 2300, pos_y - 1150)
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
    color_burn_noises.location = (pos_x + 2700, pos_y - 1500)
    color_burn_noises.blend_type = "BURN"
    color_burn_noises.inputs["Fac"].default_value = 1.0

    mat.node_tree.links.new(color_burn_noises.outputs["Color"],
                            subtract_imperfection.inputs["Color2"])

    # Noise Tex - Subtract shape imperfection 1
    noise_subtract_shape_imperfection_1 = mat_nodes.new("ShaderNodeTexNoise")
    noise_subtract_shape_imperfection_1.parent = frame
    noise_subtract_shape_imperfection_1.name = "Noise Tex - Subtract shape imperfection 1"
    noise_subtract_shape_imperfection_1.label = "Noise Tex - Subtract shape imperfection 1"
    noise_subtract_shape_imperfection_1.location = (pos_x + 2500, pos_y - 1500)
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
    noise_subtract_shape_imperfection_2.location = (pos_x + 2500, pos_y - 1750)
    noise_subtract_shape_imperfection_2.inputs["Scale"].default_value = 1.9
    noise_subtract_shape_imperfection_2.inputs["Detail"].default_value = 16.0
    noise_subtract_shape_imperfection_2.inputs["Roughness"].default_value = 0.0
    noise_subtract_shape_imperfection_2.inputs["Distortion"].default_value = 0.0

    mat.node_tree.links.new(noise_subtract_shape_imperfection_2.outputs["Fac"],
                            color_burn_noises.inputs["Color2"])

    # Vector Add - Coods subtract shape imperfection 1
    coords_subtract_shape_imperfection_1 = mat_nodes.new("ShaderNodeVectorMath")
    coords_subtract_shape_imperfection_1.parent = frame
    coords_subtract_shape_imperfection_1.location = (pos_x + 2300, pos_y - 1500)
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
    coords_subtract_shape_imperfection_2.location = (pos_x + 2300, pos_y - 1750)
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
