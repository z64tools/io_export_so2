import bpy
import os

class MaterialNodes:
    shader: bpy.types.ShaderNodeBsdfPrincipled
    texel0: bpy.types.ShaderNodeTexImage
    texel1: bpy.types.ShaderNodeTexImage
    uv0: bpy.types.ShaderNodeGroup
    uv1: bpy.types.ShaderNodeGroup
    alpha: bpy.types.ShaderNodeMath

def create_uv_group():
    group: bpy.types.NodeTree = bpy.data.node_groups.get("SOUVGroup")

    if group == None:
        group = bpy.data.node_groups.new("SOUVGroup", "ShaderNodeTree")

    def add_node(name, type, x, y):
        n = group.nodes.get(name)
        if n == None:
            n = group.nodes.new(type)
        n.name = name
        n.label = name
        n.location = x, y

        return n
    
    def add_input(type, name):
        # https://wiki.blender.org/wiki/Reference/Release_Notes/4.0/Python_API
        if bpy.app.version < (4,0,0):
            n = group.inputs.get(name)
            if n == None:
                n = group.inputs.new(type, name)
        else:
            n = group.interface.items_tree.get(name)
            if n == None:
                n = group.interface.new_socket(name, in_out="INPUT", socket_type=type)
            assert isinstance(n, bpy.types.NodeTreeInterfaceSocket)
            assert n.in_out == "INPUT"

        return n
    
    def add_output(type, name):
        if bpy.app.version < (4,0,0):
            n = group.outputs.get(name)
            if n == None:
                n = group.outputs.new(type, name)
        else:
            n = group.interface.items_tree.get(name)
            if n == None:
                n = group.interface.new_socket(name, in_out="OUTPUT", socket_type=type)
            assert isinstance(n, bpy.types.NodeTreeInterfaceSocket)
            assert n.in_out == "OUTPUT"

        return n
    
    inputs = add_node("Input", "NodeGroupInput", -500, 0)
    outputs = add_node("Output", "NodeGroupOutput", 750, 0)
    add_input("NodeSocketFloat", "StateX")
    add_input("NodeSocketFloat", "StateY")
    shf = add_input("NodeSocketFloat", "ShiftX")
    shf = add_input("NodeSocketFloat", "ShiftY")
    add_output("NodeSocketVector", "Normal")
    
    uvmap = add_node("UVMap", "ShaderNodeUVMap", -500, -100)
    sepa = add_node("UVSeparator", "ShaderNodeSeparateXYZ", -300, 0)
    group.links.new(uvmap.outputs[0], sepa.inputs[0])

    mirx = add_node("UVMirrorX", "ShaderNodeMath", -100, 300)
    mirx.operation = "PINGPONG"
    mirx.inputs[1].default_value = 1
    group.links.new(sepa.outputs[0], mirx.inputs[0])

    miry = add_node("UVMirrorY", "ShaderNodeMath", -100, 150)
    miry.operation = "PINGPONG"
    miry.inputs[1].default_value = 1
    group.links.new(sepa.outputs[1], miry.inputs[0])

    clmx = add_node("UVClampX", "ShaderNodeClamp", -100, 0)
    clmx.clamp_type = "MINMAX"
    clmx.inputs["Min"].default_value = 0
    clmx.inputs["Max"].default_value = 1
    group.links.new(sepa.outputs[0], clmx.inputs[0])

    clmy = add_node("UVClampY", "ShaderNodeClamp", -100, -150)
    clmy.clamp_type = "MINMAX"
    clmy.inputs["Min"].default_value = 0
    clmy.inputs["Max"].default_value = 1
    group.links.new(sepa.outputs[1], clmy.inputs[0])
    
    mapmirx = add_node("UVMapMirrorX", "ShaderNodeMapRange", 75, 300)
    mapmirx.inputs["From Min"].default_value = 0
    mapmirx.inputs["From Max"].default_value = 1
    group.links.new(inputs.outputs[0], mapmirx.inputs[0])
    group.links.new(sepa.outputs[0], mapmirx.inputs["To Min"])
    group.links.new(mirx.outputs[0], mapmirx.inputs["To Max"])

    mapmiry = add_node("UVMapMirrorY", "ShaderNodeMapRange", 75, 0)
    mapmiry.inputs["From Min"].default_value = 0
    mapmiry.inputs["From Max"].default_value = 1
    group.links.new(inputs.outputs[1], mapmiry.inputs[0])
    group.links.new(sepa.outputs[1], mapmiry.inputs["To Min"])
    group.links.new(miry.outputs[0], mapmiry.inputs["To Max"])

    mapclmx = add_node("UVMapClampX", "ShaderNodeMapRange", 225, 300)
    mapclmx.inputs["From Min"].default_value = 1
    mapclmx.inputs["From Max"].default_value = 2
    group.links.new(inputs.outputs[0], mapclmx.inputs[0])
    group.links.new(mapmirx.outputs[0], mapclmx.inputs["To Min"])
    group.links.new(clmx.outputs[0], mapclmx.inputs["To Max"])
    
    mapclmy = add_node("UVMapClampY", "ShaderNodeMapRange", 225, 0)
    mapclmy.inputs["From Min"].default_value = 1
    mapclmy.inputs["From Max"].default_value = 2
    group.links.new(inputs.outputs[1], mapclmy.inputs[0])
    group.links.new(mapmiry.outputs[0], mapclmy.inputs["To Min"])
    group.links.new(clmy.outputs[0], mapclmy.inputs["To Max"])

    shfx = add_node("UVShiftX", "ShaderNodeMath", 400, 150)
    shfx.operation = "MULTIPLY"
    group.links.new(mapclmx.outputs[0], shfx.inputs[1])
    group.links.new(inputs.outputs[2], shfx.inputs[0])

    shfy = add_node("UVShiftY", "ShaderNodeMath", 400, 0)
    shfy.operation = "MULTIPLY"
    group.links.new(mapclmy.outputs[0], shfy.inputs[1])
    group.links.new(inputs.outputs[3], shfy.inputs[0])

    combiner = add_node("UVCombiner", "ShaderNodeCombineXYZ", 575, 0)
    group.links.new(shfx.outputs[0], combiner.inputs[0])
    group.links.new(shfy.outputs[0], combiner.inputs[1])

    group.links.new(combiner.outputs[0], outputs.inputs[0])

 # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

def sodata_alpha(node:bpy.types.ShaderNode, so_data):
    node.inputs[0].default_value = so_data.alpha / 255

def sodata_multi_alpha(node:bpy.types.ShaderNode, so_data):
    node.inputs[0].default_value = 1.0 if so_data.alpha_mask else so_data.multi_alpha / 255

def sodata_pixelated(node:bpy.types.ShaderNode, so_data):
    if so_data.pixelated:
        node.interpolation = "Closest"
    else:
        node.interpolation = "Linear"

def sodata_shift(node:bpy.types.ShaderNode, so_data):
    node.node_tree = bpy.data.node_groups['SOUVGroup']

    def value(val):
        if val == -3:
            return 8
        if val == -2:
            return 4
        if val == -1:
            return 2
        if val == 0:
            return 1
        if val == 1:
            return 0.5
        if val == 2:
            return 0.25
        if val == 3:
            return 0.125
    
    if node.name == "UV0":
        node.inputs[2].default_value = value(so_data.shift_x_0)
        node.inputs[3].default_value = value(so_data.shift_y_0)
    else:
        node.inputs[2].default_value = value(so_data.shift_x_1)
        node.inputs[3].default_value = value(so_data.shift_y_1)


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

def ensure_setup_and_get_nodes(material: bpy.types.Material):
    node_tree = material.node_tree
    node_tree.nodes.clear()
    so_data = material.ocarina

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

    create_uv_group()

    other_output_nodes = [
        node
        for node in node_tree.nodes
        if node.bl_idname == "ShaderNodeOutputMaterial"
    ]
    for other_output_node in other_output_nodes:
        node_tree.nodes.remove(other_output_node)
    
    def init_func_input0_1(node:bpy.types.ShaderNode, so_data):
        node.inputs[0].default_value = 1
    
    def init_ramp(node:bpy.types.ShaderNodeValToRGB, so_data):
        elements = node.color_ramp.elements

        while len(elements) < 4:
            elements.new(0.5)

        elements[0].color = 0, 0, 0, 0
        elements[0].position = 0.0
        elements[1].color = 0.5, 0.5, 0.5, 0.5
        elements[1].position = 0.35
        elements[2].color = 0.75, 0.75, 0.75, 0.75
        elements[2].position = 0.6
        elements[3].color = 1, 1, 1, 1
        elements[3].position = 0.8

    data = {
         "SOOutput":      ( 300,    0, "ShaderNodeOutputMaterial", None),
         # TODO it would be better to use a Diffuse shader and mix it with a transparent shader for alpha,
         # rather than relying on the complicated BSDF Principled shader
         "SOShader":      (  50,    0, "ShaderNodeBsdfPrincipled", None),
         "SOTexel0":      (-500,    0, "ShaderNodeTexImage",       sodata_pixelated),
         "SOTexel1":      (-500, -200, "ShaderNodeTexImage",       sodata_pixelated),
         "UV0":           (-650,    0, "ShaderNodeGroup",          sodata_shift),
         "UV1":           (-650, -200, "ShaderNodeGroup",          sodata_shift),
         "SOVtxCol":      (-400, -405, "ShaderNodeVertexColor",    None),
         "SOTexColMixer": (-250,    0, "ShaderNodeMixRGB",         sodata_multi_alpha),
         "SOTexAlpMixer": (-250, -175, "ShaderNodeMixRGB",         sodata_multi_alpha),
         "SOVtxColMixer": (-100,    0, "ShaderNodeMixRGB",         init_func_input0_1),
         "SOVtxAlpMixer": (-100, -175, "ShaderNodeMixRGB",         init_func_input0_1),
         "SOAlpAlpMixer": (-100, -350, "ShaderNodeMath",           sodata_alpha),
         "SOAlphaAdjust": (-200, -510, "ShaderNodeValToRGB",       init_ramp),
    }
    nodes = {}

    for name, (x, y, node_type, init_func) in data.items():
        nodes[name] = node_tree.nodes.get(name)

        if nodes[name] == None:
            nodes[name] = node_tree.nodes.new(node_type)
            nodes[name].name = name
            nodes[name].label = name
        if init_func != None:
            init_func(nodes[name], so_data)
        nodes[name].location = x + 200, y
    
    node_tree.links.new(nodes["UV0"].outputs[0], nodes["SOTexel0"].inputs[0])
    node_tree.links.new(nodes["UV1"].outputs[0], nodes["SOTexel1"].inputs[0])

    node_tree.links.new(nodes["SOTexel0"].outputs[0], nodes["SOTexColMixer"].inputs[1])
    node_tree.links.new(nodes["SOTexel1"].outputs[0], nodes["SOTexColMixer"].inputs[2])
    node_tree.links.new(nodes["SOTexel0"].outputs[1], nodes["SOTexAlpMixer"].inputs[1])
    node_tree.links.new(nodes["SOTexel1"].outputs[1], nodes["SOTexAlpMixer"].inputs[2])

    node_tree.links.new(nodes["SOVtxCol"].outputs[0], nodes["SOVtxColMixer"].inputs[2])
    node_tree.links.new(nodes["SOTexColMixer"].outputs[0], nodes["SOVtxColMixer"].inputs[1])
    node_tree.links.new(nodes["SOVtxCol"].outputs[1], nodes["SOVtxAlpMixer"].inputs[2])
    node_tree.links.new(nodes["SOTexAlpMixer"].outputs[0], nodes["SOVtxAlpMixer"].inputs[1])
    nodes["SOVtxColMixer"].inputs[0].default_value = 1
    nodes["SOVtxAlpMixer"].inputs[0].default_value = 1
    nodes["SOVtxColMixer"].blend_type = "MULTIPLY"
    nodes["SOVtxAlpMixer"].blend_type = "MULTIPLY"

    node_tree.links.new(nodes["SOVtxAlpMixer"].outputs[0], nodes["SOAlpAlpMixer"].inputs[1])
    nodes["SOAlpAlpMixer"].operation = "MULTIPLY"

    node_tree.links.new(nodes["SOAlpAlpMixer"].outputs[0], nodes["SOAlphaAdjust"].inputs[0])

    node_tree.links.new(nodes["SOVtxColMixer"].outputs[0], nodes["SOShader"].inputs["Base Color"])
    node_tree.links.new(nodes["SOAlphaAdjust"].outputs[1], nodes["SOShader"].inputs["Alpha"])
    if bpy.app.version < (4, 0, 0):
        nodes["SOShader"].inputs["Specular"].default_value = 0
    else:
        nodes["SOShader"].inputs["Specular IOR Level"].default_value = 0

    node_tree.links.new(nodes["SOShader"].outputs[0], nodes["SOOutput"].inputs[0])

    material.preview_render_type = "SPHERE"
    material.preview_render_type = "FLAT"
    material.use_backface_culling = material.ocarina.culling

    # return nodes

    n = MaterialNodes()
    n.shader = nodes["SOShader"]
    n.texel0 = nodes["SOTexel0"]
    n.texel1 = nodes["SOTexel1"]
    n.uv0 =  nodes["UV0"]
    n.uv1 =  nodes["UV1"]

    return n

 # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

def set_simple_material(mat: bpy.types.Material):
    data = mat.ocarina
    nodes = ensure_setup_and_get_nodes(mat)

    set_simple_material_image(mat, nodes, data)

    set_simple_material_uv_repeats(nodes, data)

def set_simple_material_image(mat:bpy.types.Material, nodes:MaterialNodes, data):
    nodes.texel0.image = data.texture_0
    nodes.texel1.image = data.texture_1

    if data.texture_0 is None or mat.ocarina.is_mesh == False:
        mat.node_tree.links.remove(nodes.shader.inputs["Base Color"].links[0])
        nodes.shader.inputs["Base Color"].default_value = 1, 0, 0, 1
        mat.node_tree.links.remove(nodes.shader.inputs["Alpha"].links[0])
        nodes.shader.inputs["Alpha"].default_value = 1
    elif mat.name.startswith("Material"):
        new_name:str = data.texture_0.name

        new_name = new_name.replace("#", "\0")
        mat.name = new_name.removesuffix(".png")

def set_simple_material_uv_repeats(nodes:MaterialNodes, data):
    values = {
        "WRAP":   0,
        "MIRROR": 1,
        "CLAMP":  2,
    }
    nodes.uv0.inputs[0].default_value = values[data.repeat_x_0]
    nodes.uv0.inputs[1].default_value = values[data.repeat_y_0]
    nodes.uv1.inputs[0].default_value = values[data.repeat_x_1]
    nodes.uv1.inputs[1].default_value = values[data.repeat_y_1]

 # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

def on_material_image_update(self, context):
    mat: bpy.types.Material = context.material

    set_simple_material(mat)

def on_material_use_transparency_update(self, context):
    mat: bpy.types.Material = context.material
    data = mat.ocarina

    mat.blend_method = data.alpha_method
    mat.alpha_threshold = 0.5

def on_material_use_blend_transparency_update(self, context):
    on_material_use_transparency_update(self, context)

def on_material_uv_repeat_update(self, context):
    mat: bpy.types.Material = context.material

    set_simple_material(mat)

def on_material_update_culling(self, context):
    mat: bpy.types.Material = context.material
    data = mat.ocarina

    mat.use_backface_culling = data.culling

def on_material_update_pixelating(self, context):
    material: bpy.types.Material = context.material
    data = material.ocarina
    node_tree = material.node_tree

    texel0 = node_tree.nodes.get("SOTexel0")
    texel0: bpy.types.ShaderNodeTexImage

    sodata_pixelated(texel0, data)

def on_material_update_alphamask(self, context):
    material: bpy.types.Material = context.material
    data = material.ocarina
    node_tree = material.node_tree
    sodata_multi_alpha(node_tree.nodes.get("SOTexAlpMixer"), data)

def on_material_disable_mesh(self, context):
    material: bpy.types.Material = context.material
    data = material.ocarina
    nodes = ensure_setup_and_get_nodes(material)

    set_simple_material_image(material, nodes, data)

    if data.is_mesh:
        material.blend_method = data.alpha_method
    else:
        nodes.shader.inputs["Base Color"].default_value = 0.82, 0.55, 0.35, 1
        material.blend_method = "BLEND"
        nodes.shader.inputs["Alpha"].default_value = 0.05

def on_material_update_alpha(self, context):
    material: bpy.types.Material = context.material
    data = material.ocarina
    node_tree = material.node_tree

    main_alpha_node = node_tree.nodes.get("SOAlpAlpMixer")

    sodata_alpha(main_alpha_node, data)

    return

def on_material_update_multi_alpha(self, context):
    material: bpy.types.Material = context.material
    data = material.ocarina
    node_tree = material.node_tree

    sodata_multi_alpha(node_tree.nodes.get("SOTexColMixer"), data)
    sodata_multi_alpha(node_tree.nodes.get("SOTexAlpMixer"), data)

    return

def on_material_update_shift(self, context):
    material: bpy.types.Material = context.material
    data = material.ocarina

    node = material.node_tree.nodes.get("UV0")
    sodata_shift(node, data)
    node = material.node_tree.nodes.get("UV1")
    sodata_shift(node, data)

    return