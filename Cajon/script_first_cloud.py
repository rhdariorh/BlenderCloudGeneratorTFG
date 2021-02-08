import bpy

C = bpy.context
D = bpy.data

# ---------------------------------------
# ------------Initialization-------------
# ---------------------------------------
DOMAIN_SIZE = (3.0, 3.0, 3.0)
CLOUD_SIZE = (7.0, 7.0, 7.0)
# Create cloud domain object
bpy.ops.mesh.primitive_cube_add()
obj = C.active_object
obj.name = 'Cloud'

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
elem.color = (2.163, 2.163, 2.163, 1) # HSV -> V = 1.4

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

obj.scale = DOMAIN_SIZE
C.view_layer.objects.active = obj
bpy.ops.object.transform_apply(location=False, rotation=False, scale=True, properties=True)
obj.scale = CLOUD_SIZE                     

