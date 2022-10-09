import bpy
from . import properties

class MaterialNodes:
    shader_node: bpy.types.ShaderNodeBsdfPrincipled
    image: bpy.types.ShaderNodeTexImage
    uv_repeat_type_u: bpy.types.ShaderNodeValue
    uv_repeat_type_v: bpy.types.ShaderNodeValue

def ensure_setup_and_get_nodes(material: bpy.types.Material):
    node_tree = material.node_tree

    # ensure vertex colors data exists

    for mesh in bpy.data.meshes:
        mesh: bpy.types.Mesh
        if material in mesh.materials.values():
            if mesh.vertex_colors.active is None:
                mesh.vertex_colors.new(do_init=False)

    for object in bpy.data.objects:
        object: bpy.types.Object
        if object.type == "MESH" and material in (
            material_slot.material for material_slot in object.material_slots.values()
        ):
            if object.data.vertex_colors.active is None:
                object.data.vertex_colors.new(do_init=False)

    # output node

    output_node_name = "SMH Output Material"
    output_node = node_tree.nodes.get(output_node_name)
    if output_node is None:
        output_node = node_tree.nodes.new("ShaderNodeOutputMaterial")
        output_node.name = output_node_name
        output_node.location = -200, 0

    other_output_nodes = [
        node
        for node in node_tree.nodes
        if node.bl_idname == "ShaderNodeOutputMaterial" and node != output_node
    ]
    for other_output_node in other_output_nodes:
        node_tree.nodes.remove(other_output_node)

    # shader node

    shader_node_name = "SMH Principled BSDF"
    shader_node = node_tree.nodes.get(shader_node_name)
    if shader_node is None:
        shader_node = node_tree.nodes.new("ShaderNodeBsdfPrincipled")
        shader_node.name = shader_node_name
        shader_node.location = -500, 0
        shader_node.inputs["Specular"].default_value = 0

    # image node

    image_node_name = "SMH Image Texture"
    image_node = node_tree.nodes.get(image_node_name)
    if image_node is None:
        image_node = node_tree.nodes.new("ShaderNodeTexImage")
        image_node.name = image_node_name
        image_node.location = -1300, 0

    # vertex color node

    vertex_color_node_name = "SMH Vertex Color"
    vertex_color_node = node_tree.nodes.get(vertex_color_node_name)
    if vertex_color_node is None:
        vertex_color_node = node_tree.nodes.new("ShaderNodeVertexColor")
        vertex_color_node.name = vertex_color_node_name
        vertex_color_node.location = -1300, -500
    
    # shader mixer

    shader_mixer_node_name = "SMH Shader Mixer"
    shader_mixer_node = node_tree.nodes.get(shader_mixer_node_name)
    if shader_mixer_node is None:
        shader_mixer_node = node_tree.nodes.new("ShaderNodeMixRGB")
        shader_mixer_node.name = shader_mixer_node_name
        shader_mixer_node.location = -1100, -300
        shader_mixer_node: bpy.types.ShaderNodeMixRGB
        shader_mixer_node.inputs[0].default_value = 1.0
        shader_mixer_node.inputs[1].default_value = 1.0, 1.0, 1.0, 1.0

    # multiply image color and vertex color node

    multiply_image_color_and_vertex_color_node_name = "SMH Image Color * Vertex Color"
    multiply_image_color_and_vertex_color_node = node_tree.nodes.get(
        multiply_image_color_and_vertex_color_node_name
    )
    if multiply_image_color_and_vertex_color_node is None:
        multiply_image_color_and_vertex_color_node = node_tree.nodes.new(
            "ShaderNodeMixRGB"
        )
        multiply_image_color_and_vertex_color_node.name = (
            multiply_image_color_and_vertex_color_node_name
        )
        multiply_image_color_and_vertex_color_node.location = -800, 0

        multiply_image_color_and_vertex_color_node: bpy.types.ShaderNodeMixRGB
        multiply_image_color_and_vertex_color_node.blend_type = "MULTIPLY"
        multiply_image_color_and_vertex_color_node.inputs[0].default_value = 1.0

    # multiply image alpha and vertex alpha node

    multiply_image_alpha_and_vertex_alpha_node_name = "SMH Image Alpha * Vertex Alpha"
    multiply_image_alpha_and_vertex_alpha_node = node_tree.nodes.get(
        multiply_image_alpha_and_vertex_alpha_node_name
    )
    if multiply_image_alpha_and_vertex_alpha_node is None:
        multiply_image_alpha_and_vertex_alpha_node = node_tree.nodes.new(
            "ShaderNodeMath"
        )
        multiply_image_alpha_and_vertex_alpha_node.name = (
            multiply_image_alpha_and_vertex_alpha_node_name
        )
        multiply_image_alpha_and_vertex_alpha_node.location = -800, -180
        multiply_image_alpha_and_vertex_alpha_node: bpy.types.ShaderNodeMath
        multiply_image_alpha_and_vertex_alpha_node.operation = "MULTIPLY"

    # uv map node

    uv_map_node_name = "SMH UV Map"
    uv_map_node = node_tree.nodes.get(uv_map_node_name)
    if uv_map_node is None:
        uv_map_node = node_tree.nodes.new("ShaderNodeUVMap")
        uv_map_node.name = uv_map_node_name
        uv_map_node.location = -2900, -400

    # separate uv components node

    uv_separate_node_name = "SMH Separate UV"
    uv_separate_node = node_tree.nodes.get(uv_separate_node_name)
    if uv_separate_node is None:
        uv_separate_node = node_tree.nodes.new("ShaderNodeSeparateXYZ")
        uv_separate_node.name = uv_separate_node_name
        uv_separate_node.location = -2700, -400

    # uv mirror u node

    uv_mirror_u_node_name = "SMH UV Mirror U"
    uv_mirror_u_node = node_tree.nodes.get(uv_mirror_u_node_name)
    if uv_mirror_u_node is None:
        uv_mirror_u_node = node_tree.nodes.new("ShaderNodeMath")
        uv_mirror_u_node.name = uv_mirror_u_node_name
        uv_mirror_u_node.location = -2400, 0
        uv_mirror_u_node: bpy.types.ShaderNodeMath
        uv_mirror_u_node.operation = "PINGPONG"
        uv_mirror_u_node.inputs[1].default_value = 1

    # uv mirror v node

    uv_mirror_v_node_name = "SMH UV Mirror V"
    uv_mirror_v_node = node_tree.nodes.get(uv_mirror_v_node_name)
    if uv_mirror_v_node is None:
        uv_mirror_v_node = node_tree.nodes.new("ShaderNodeMath")
        uv_mirror_v_node.name = uv_mirror_v_node_name
        uv_mirror_v_node.location = -2400, -200
        uv_mirror_v_node: bpy.types.ShaderNodeMath
        uv_mirror_v_node.operation = "PINGPONG"
        uv_mirror_v_node.inputs[1].default_value = 1

    # uv clamp u node

    uv_clamp_u_node_name = "SMH UV Clamp U"
    uv_clamp_u_node = node_tree.nodes.get(uv_clamp_u_node_name)
    if uv_clamp_u_node is None:
        uv_clamp_u_node = node_tree.nodes.new("ShaderNodeClamp")
        uv_clamp_u_node.name = uv_clamp_u_node_name
        uv_clamp_u_node.location = -2400, -500
        uv_clamp_u_node: bpy.types.ShaderNodeClamp
        uv_clamp_u_node.clamp_type = "MINMAX"
        uv_clamp_u_node.inputs["Min"].default_value = 0
        uv_clamp_u_node.inputs["Max"].default_value = 1

    # uv clamp v node

    uv_clamp_v_node_name = "SMH UV Clamp V"
    uv_clamp_v_node = node_tree.nodes.get(uv_clamp_v_node_name)
    if uv_clamp_v_node is None:
        uv_clamp_v_node = node_tree.nodes.new("ShaderNodeClamp")
        uv_clamp_v_node.name = uv_clamp_v_node_name
        uv_clamp_v_node.location = -2400, -700
        uv_clamp_v_node: bpy.types.ShaderNodeClamp
        uv_clamp_v_node.clamp_type = "MINMAX"
        uv_clamp_v_node.inputs["Min"].default_value = 0
        uv_clamp_v_node.inputs["Max"].default_value = 1

    # uv repeat type u node

    uv_repeat_type_u_name = "SMH UV Repeat Type U"
    uv_repeat_type_u = node_tree.nodes.get(uv_repeat_type_u_name)
    if uv_repeat_type_u is None:
        uv_repeat_type_u = node_tree.nodes.new("ShaderNodeValue")
        uv_repeat_type_u.name = uv_repeat_type_u_name
        uv_repeat_type_u.location = -2200, 0

    # uv repeat pick u 1 node (picks wrap/mirror)

    uv_repeat_pick1_u_name = "SMH UV Pick U 1"
    uv_repeat_pick1_u = node_tree.nodes.get(uv_repeat_pick1_u_name)
    if uv_repeat_pick1_u is None:
        uv_repeat_pick1_u = node_tree.nodes.new("ShaderNodeMapRange")
        uv_repeat_pick1_u.name = uv_repeat_pick1_u_name
        uv_repeat_pick1_u.location = -2000, -200
        uv_repeat_pick1_u.inputs["From Min"].default_value = 0
        uv_repeat_pick1_u.inputs["From Max"].default_value = 1

    # uv repeat pick u 2 node (picks pick1/clamp)

    uv_repeat_pick2_u_name = "SMH UV Pick U 2"
    uv_repeat_pick2_u = node_tree.nodes.get(uv_repeat_pick2_u_name)
    if uv_repeat_pick2_u is None:
        uv_repeat_pick2_u = node_tree.nodes.new("ShaderNodeMapRange")
        uv_repeat_pick2_u.name = uv_repeat_pick2_u_name
        uv_repeat_pick2_u.location = -1700, -200
        uv_repeat_pick2_u.inputs["From Min"].default_value = 1
        uv_repeat_pick2_u.inputs["From Max"].default_value = 2

    # uv repeat type v node

    uv_repeat_type_v_name = "SMH UV Repeat Type V"
    uv_repeat_type_v = node_tree.nodes.get(uv_repeat_type_v_name)
    if uv_repeat_type_v is None:
        uv_repeat_type_v = node_tree.nodes.new("ShaderNodeValue")
        uv_repeat_type_v.name = uv_repeat_type_v_name
        uv_repeat_type_v.location = -2200, -600

    # uv repeat pick v 1 node (picks wrap/mirror)

    uv_repeat_pick1_v_name = "SMH UV Pick V 1"
    uv_repeat_pick1_v = node_tree.nodes.get(uv_repeat_pick1_v_name)
    if uv_repeat_pick1_v is None:
        uv_repeat_pick1_v = node_tree.nodes.new("ShaderNodeMapRange")
        uv_repeat_pick1_v.name = uv_repeat_pick1_v_name
        uv_repeat_pick1_v.location = -2000, -800
        uv_repeat_pick1_v.inputs["From Min"].default_value = 0
        uv_repeat_pick1_v.inputs["From Max"].default_value = 1

    # uv repeat pick v 2 node (picks pick1/clamp)

    uv_repeat_pick2_v_name = "SMH UV Pick V 2"
    uv_repeat_pick2_v = node_tree.nodes.get(uv_repeat_pick2_v_name)
    if uv_repeat_pick2_v is None:
        uv_repeat_pick2_v = node_tree.nodes.new("ShaderNodeMapRange")
        uv_repeat_pick2_v.name = uv_repeat_pick2_v_name
        uv_repeat_pick2_v.location = -1700, -800
        uv_repeat_pick2_v.inputs["From Min"].default_value = 1
        uv_repeat_pick2_v.inputs["From Max"].default_value = 2

    # combine uv components node

    uv_combine_node_name = "SMH Combine UV"
    uv_combine_node = node_tree.nodes.get(uv_combine_node_name)
    if uv_combine_node is None:
        uv_combine_node = node_tree.nodes.new("ShaderNodeCombineXYZ")
        uv_combine_node.name = uv_combine_node_name
        uv_combine_node.location = -1500, -400

    # Node links

    # UV wrap, mirror, clamp

    node_tree.links.new(
        uv_separate_node.inputs[0],
        uv_map_node.outputs["UV"],
        verify_limits=True,
    )

    node_tree.links.new(
        uv_mirror_u_node.inputs[0],
        uv_separate_node.outputs[0],
        verify_limits=True,
    )
    node_tree.links.new(
        uv_mirror_v_node.inputs[0],
        uv_separate_node.outputs[1],
        verify_limits=True,
    )

    node_tree.links.new(
        uv_clamp_u_node.inputs[0],
        uv_separate_node.outputs[0],
        verify_limits=True,
    )
    node_tree.links.new(
        uv_clamp_v_node.inputs[0],
        uv_separate_node.outputs[1],
        verify_limits=True,
    )

    # Pick U

    node_tree.links.new(
        uv_repeat_pick1_u.inputs["Value"],
        uv_repeat_type_u.outputs[0],
        verify_limits=True,
    )
    node_tree.links.new(
        uv_repeat_pick1_u.inputs["To Min"],
        uv_separate_node.outputs[0],
        verify_limits=True,
    )
    node_tree.links.new(
        uv_repeat_pick1_u.inputs["To Max"],
        uv_mirror_u_node.outputs[0],
        verify_limits=True,
    )

    node_tree.links.new(
        uv_repeat_pick2_u.inputs["Value"],
        uv_repeat_type_u.outputs[0],
        verify_limits=True,
    )
    node_tree.links.new(
        uv_repeat_pick2_u.inputs["To Min"],
        uv_repeat_pick1_u.outputs[0],
        verify_limits=True,
    )
    node_tree.links.new(
        uv_repeat_pick2_u.inputs["To Max"],
        uv_clamp_u_node.outputs[0],
        verify_limits=True,
    )

    # Pick V

    node_tree.links.new(
        uv_repeat_pick1_v.inputs["Value"],
        uv_repeat_type_v.outputs[0],
        verify_limits=True,
    )
    node_tree.links.new(
        uv_repeat_pick1_v.inputs["To Min"],
        uv_separate_node.outputs[1],
        verify_limits=True,
    )
    node_tree.links.new(
        uv_repeat_pick1_v.inputs["To Max"],
        uv_mirror_v_node.outputs[0],
        verify_limits=True,
    )

    node_tree.links.new(
        uv_repeat_pick2_v.inputs["Value"],
        uv_repeat_type_v.outputs[0],
        verify_limits=True,
    )
    node_tree.links.new(
        uv_repeat_pick2_v.inputs["To Min"],
        uv_repeat_pick1_v.outputs[0],
        verify_limits=True,
    )
    node_tree.links.new(
        uv_repeat_pick2_v.inputs["To Max"],
        uv_clamp_v_node.outputs[0],
        verify_limits=True,
    )

    # UV output

    node_tree.links.new(
        uv_combine_node.inputs[0],
        uv_repeat_pick2_u.outputs[0],
        verify_limits=True,
    )
    node_tree.links.new(
        uv_combine_node.inputs[1],
        uv_repeat_pick2_v.outputs[0],
        verify_limits=True,
    )

    node_tree.links.new(
        image_node.inputs[0],
        uv_combine_node.outputs[0],
        verify_limits=True,
    )

    # Color

    node_tree.links.new(
        multiply_image_color_and_vertex_color_node.inputs[1],
        shader_mixer_node.outputs["Color"],
        verify_limits=True,
    )
    node_tree.links.new(
        multiply_image_color_and_vertex_color_node.inputs[2],
        image_node.outputs["Color"],
        verify_limits=True,
    )

    # Mixer

    node_tree.links.new(
        shader_mixer_node.inputs[2],
        vertex_color_node.outputs["Color"],
        verify_limits=True,
    )

    # Alpha

    node_tree.links.new(
        multiply_image_alpha_and_vertex_alpha_node.inputs[0],
        image_node.outputs["Alpha"],
        verify_limits=True,
    )
    node_tree.links.new(
        multiply_image_alpha_and_vertex_alpha_node.inputs[1],
        vertex_color_node.outputs["Alpha"],
        verify_limits=True,
    )
    node_tree.links.new(
        shader_node.inputs["Alpha"],
        multiply_image_alpha_and_vertex_alpha_node.outputs[0],
        verify_limits=True,
    )

    # Output

    node_tree.links.new(
        output_node.inputs["Surface"],
        shader_node.outputs["BSDF"],
        verify_limits=True,
    )

    node_tree.links.new(
        shader_node.inputs["Base Color"],
        multiply_image_color_and_vertex_color_node.outputs[0],
        verify_limits=True,
    )

    material.preview_render_type = "FLAT"
    material.use_backface_culling = material.ocarina.culling

    # return nodes

    nodes = MaterialNodes()
    nodes.shader_node = shader_node
    nodes.image = image_node
    nodes.uv_repeat_type_u = uv_repeat_type_u
    nodes.uv_repeat_type_v = uv_repeat_type_v

    return nodes

def set_simple_material(mat: bpy.types.Material):
    props: properties.Properties_Material = mat.ocarina

    nodes = ensure_setup_and_get_nodes(mat)

    set_simple_material_image(mat, nodes, props)

    set_simple_material_uv_repeats(nodes, props)

def set_simple_material_image(
    mat: bpy.types.Material,
    nodes: MaterialNodes,
    props,  # type: properties.Properties_Material
):
    nodes.image.image = props.texture_0

    if props.texture_0 is None:
        mat.node_tree.links.remove(nodes.shader_node.inputs["Base Color"].links[0])
        nodes.shader_node.inputs["Base Color"].default_value = 1, 0, 0, 1
        mat.node_tree.links.remove(nodes.shader_node.inputs["Alpha"].links[0])
        nodes.shader_node.inputs["Alpha"].default_value = 1

def set_simple_material_uv_repeats(
    nodes: MaterialNodes,
    props,  # type: properties.Properties_Material
):
    values = {
        "WRAP": 0,
        "MIRROR": 1,
        "CLAMP": 2,
    }
    nodes.uv_repeat_type_u.outputs[0].default_value = values[props.uv_repeat_u]
    nodes.uv_repeat_type_v.outputs[0].default_value = values[props.uv_repeat_v]

def on_material_image_update(self, context):
    mat: bpy.types.Material = context.material

    set_simple_material(mat)

def on_material_use_transparency_update(self, context):
    mat: bpy.types.Material = context.material
    data: properties.Properties_Material = mat.ocarina

    mat.blend_method = data.alpha_method
    mat.alpha_threshold = 0.5

def on_material_use_blend_transparency_update(self, context):
    on_material_use_transparency_update(self, context)

def on_material_uv_repeat_update(self, context):
    mat: bpy.types.Material = context.material

    set_simple_material(mat)

def on_material_update_culling(self, context):
    mat: bpy.types.Material = context.material
    data: properties.Properties_Material = mat.ocarina

    mat.use_backface_culling = data.culling

def on_material_update_shading(self, context):
    material: bpy.types.Material = context.material
    data: properties.Properties_Material = material.ocarina
    node_tree = material.node_tree

    shader_mixer_node_name = "SMH Shader Mixer"
    shader_mixer_node = node_tree.nodes.get(shader_mixer_node_name)
    if shader_mixer_node is None:
        return
    
    if data.shading == "VERTEX":
        shader_mixer_node.inputs[0].default_value = 1.0
        return
    shader_mixer_node.inputs[0].default_value = 0.0

def on_material_update_pixelating(self, context):
    material: bpy.types.Material = context.material
    data: properties.Properties_Material = material.ocarina
    node_tree = material.node_tree

    shader_mixer_node_name = "SMH Image Texture"
    shader_mixer_node = node_tree.nodes.get(shader_mixer_node_name)
    shader_mixer_node: bpy.types.ShaderNodeTexImage

    if data.pixelated:
        shader_mixer_node.interpolation = "Closest"
    else:
        shader_mixer_node.interpolation = "Linear"