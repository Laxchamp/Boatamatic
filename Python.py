import bpy

# Create material
mat = bpy.data.materials.new(name="Rock_Texture")
mat.use_nodes = True
nodes = mat.node_tree.nodes
links = mat.node_tree.links

# Clear default nodes
nodes.clear()

# Create nodes
output = nodes.new(type="ShaderNodeOutputMaterial")
bsdf = nodes.new(type="ShaderNodeBsdfPrincipled")
noise = nodes.new(type="ShaderNodeTexNoise")
musgrave = nodes.new(type="ShaderNodeTexMusgrave")
color_ramp = nodes.new(type="ShaderNodeValToRGB")
bump = nodes.new(type="ShaderNodeBump")
mapping = nodes.new(type="ShaderNodeMapping")
tex_coord = nodes.new(type="ShaderNodeTexCoord")

# Position nodes (for readability)
tex_coord.location = (-800, 0)
mapping.location = (-600, 0)
noise.location = (-400, 100)
musgrave.location = (-400, -100)
color_ramp.location = (-200, 100)
bump.location = (-200, -100)
bsdf.location = (0, 0)
output.location = (200, 0)

# Configure Noise Texture
noise.inputs["Scale"].default_value = 8
noise.inputs["Detail"].default_value = 10
noise.inputs["Roughness"].default_value = 0.6

# Configure Musgrave
musgrave.inputs["Scale"].default_value = 12
musgrave.inputs["Detail"].default_value = 8
musgrave.inputs["Dimension"].default_value = 0.7

# Configure ColorRamp (rock colors)
color_ramp.color_ramp.elements[0].position = 0.35
color_ramp.color_ramp.elements[0].color = (0.15, 0.15, 0.15, 1)
color_ramp.color_ramp.elements[1].position = 0.75
color_ramp.color_ramp.elements[1].color = (0.4, 0.4, 0.4, 1)

# Configure Bump
bump.inputs["Strength"].default_value = 0.6
bump.inputs["Distance"].default_value = 0.1

# Configure Principled BSDF
bsdf.inputs["Roughness"].default_value = 0.85
bsdf.inputs["Specular"].default_value = 0.2

# Link nodes
links.new(tex_coord.outputs["Object"], mapping.inputs["Vector"])
links.new(mapping.outputs["Vector"], noise.inputs["Vector"])
links.new(mapping.outputs["Vector"], musgrave.inputs["Vector"])

links.new(noise.outputs["Fac"], color_ramp.inputs["Fac"])
links.new(musgrave.outputs["Fac"], bump.inputs["Height"])

links.new(color_ramp.outputs["Color"], bsdf.inputs["Base Color"])
links.new(bump.outputs["Normal"], bsdf.inputs["Normal"])

links.new(bsdf.outputs["BSDF"], output.inputs["Surface"])

print("Rock texture material created!")
