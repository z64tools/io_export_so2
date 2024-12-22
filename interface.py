import bpy
from . import properties

def get_icon(attr):
        if attr:
            return 'DOWNARROW_HLT'
        else:
            return 'RIGHTARROW'

def foldable_menu(element, data, attr):
    element.prop(data, attr, icon=get_icon(getattr(data, attr)), emboss=False)
    if getattr(data, attr) == True:
        return True
    return False

def dependant_row_prop(element: bpy.types.UILayout, data, setter, value, disabler_value = False):
    row = element.row()
    row.prop(data, setter)
    col = row.column()
    if getattr(data, setter) == disabler_value:
        col.enabled = False
    col.prop(data, value)

def draw_collision_params(xcol:properties.Properties_Collision, box:bpy.types.UILayout, is_obj:bool):
    if not is_obj:
        box.prop(xcol, "sound_type")

    dependant_row_prop(box, xcol, "has_floor_flags", "floor_flags")
    dependant_row_prop(box, xcol, "has_wall_flags", "wall_flags")
    dependant_row_prop(box, xcol, "has_special_flags", "special_flags")
    dependant_row_prop(box, xcol, "has_exit", "exit")
    dependant_row_prop(box, xcol, "has_env", "env")
    dependant_row_prop(box, xcol, "has_camera", "camera")
    box.prop(xcol, "echo", slider=True)
    
    if not is_obj:
        row = box.row()
        row.prop(xcol, "hookshot")
        row.prop(xcol, "steep")

        box.label(text="Ignore:")
        row = box.row()
        row.prop(xcol, "ignore_cam", text="Camera")
        row.prop(xcol, "ignore_actor", text="Actor")
        row.prop(xcol, "ignore_proj", text="Projectile")

    dependant_row_prop(box, xcol, "conveyor_speed", "conveyor_dir", "#Speed0")
    row = box.row()
    if xcol.conveyor_speed == "#Speed0":
        row.enabled = False
    row.prop(xcol, "waterstream")

def set_object_properties(context:bpy.types.Context, object:bpy.types.Object = None):
    if object != None:
        dummy_context:bpy.types.Context = context.copy()
        dummy_context["object"] = object

        bpy.ops.object.shade_smooth(dummy_context)
        
        if object.modifiers.get("EdgeSplit") == None:
            bpy.ops.object.modifier_add(dummy_context, type="EDGE_SPLIT")
            object.modifiers["EdgeSplit"].use_edge_angle = False

    else:
        bpy.ops.object.shade_smooth()

        if context.object.modifiers.get("EdgeSplit") == None:
            bpy.ops.object.modifier_add(type="EDGE_SPLIT")
            context.object.modifiers["EdgeSplit"].use_edge_angle = False


class UI_OT_MaterialInitializer(bpy.types.Operator):
    bl_idname = "ocarina.material_initializer"
    bl_label = 'Initialize material'
    bl_options = {"INTERNAL", "UNDO"}

    def execute(self, context):
        material = mat = context.material
        object = context.object
        mat_data: properties.Properties_Material = material.ocarina
        obj_data: properties.Properties_Object = object.ocarina
        swap_mode = False

        if context.object.mode != "OBJECT":
            swap_mode = True
            if bpy.ops.object.mode_set.poll():
                bpy.ops.object.mode_set(mode="OBJECT")

        #We remove Alpha attribute from Fast64 objects if it exists
        if hasattr(object.data, 'attributes'):
            if 'Alpha' in object.data.attributes:
                object.data.attributes.remove(object.data.attributes['Alpha'])

        obj_data.is_ocarina_object = True
        mat_data.is_ocarina_material = True
        material.use_nodes = True
        mat_data.alpha_method = "CLIP"


        # Use any texture having the same name as the
        # material, if there is one, for convenience.
        # also we take care of removing the mtl_ prefix of io_import plugin

        material_name = material.name.replace("mtl_", "")
        for img in bpy.data.images:
            if material_name in img.name:
                mat_data.texture_0 = img
                break


        set_object_properties(context=context)

        if swap_mode:
            if bpy.ops.object.mode_set.poll():
                bpy.ops.object.mode_set(mode="EDIT")

        #fast64 data transfer

        if 'is_f3d' in mat and mat.is_f3d:

            if mat.f3d_mat.tex0.tex_set:
                mat.ocarina.texture_0 = mat.f3d_mat.tex0.tex
                mat.ocarina.shift_x_0 = mat.f3d_mat.tex0.S.shift
                mat.ocarina.shift_y_0 = mat.f3d_mat.tex0.T.shift
                mat.ocarina.texel_format_0 = "#" + mat.f3d_mat.tex0.tex_format if mat.f3d_mat.tex0.tex_format != "IA4" else "Auto"
            if mat.f3d_mat.tex1.tex_set:
                mat.ocarina.texture_1 = mat.f3d_mat.tex1.tex
                mat.ocarina.shift_x_1 = mat.f3d_mat.tex1.S.shift
                mat.ocarina.shift_y_1 = mat.f3d_mat.tex1.T.shift
                mat.ocarina.multi_alpha = int(mat.f3d_mat.env_color[3] * 255.0)
                mat.ocarina.texel_format_1 = "#" + mat.f3d_mat.tex1.tex_format if mat.f3d_mat.tex1.tex_format != "IA4" else "Auto"
            
            if (mat.f3d_mat.set_prim):
                mat.ocarina.alpha = int(mat.f3d_mat.prim_color[3] * 255.0)

            mat.ocarina.alpha_method = "BLEND" if mat.f3d_mat.draw_layer.oot != "Opaque" else "CLIP"
            mat.ocarina.culling = mat.f3d_mat.rdp_settings.g_cull_back

            mat.ocarina.repeat_x_0 = 'MIRROR' if mat.f3d_mat.tex0.S.mirror else ('CLAMP' if mat.f3d_mat.tex0.S.clamp else 'WRAP')
            mat.ocarina.repeat_y_0 = 'MIRROR' if mat.f3d_mat.tex0.T.mirror else ('CLAMP' if mat.f3d_mat.tex0.T.clamp else 'WRAP')
            mat.ocarina.repeat_x_1 = 'MIRROR' if mat.f3d_mat.tex1.S.mirror else ('CLAMP' if mat.f3d_mat.tex1.S.clamp else 'WRAP')
            mat.ocarina.repeat_y_1 = 'MIRROR' if mat.f3d_mat.tex1.T.mirror else ('CLAMP' if mat.f3d_mat.tex1.T.clamp else 'WRAP')

            mat.is_f3d = False
            del mat['f3d_mat']


        return {'FINISHED'}

class UI_OT_MassInit(bpy.types.Operator):
    bl_idname = "ocarina.massinit"
    bl_label = 'Mass Initialize'
    bl_description = "Initializes SharpOcarina material on all materials in the scene"
    bl_options = {"INTERNAL", "UNDO"}

    def execute(self, context):

          
            bpy.ops.mesh.primitive_cube_add(size=1)
            temp_obj = bpy.context.object
            temp_obj.name = "TempMaterialObject"


            original_materials = list(temp_obj.data.materials)

            for mat in bpy.data.materials:
                if not mat.users:
                    continue
                # Detect if its already an SO mat
                if 'ocarina' in mat and mat.ocarina.is_ocarina_material:
                    continue

                if len(temp_obj.data.materials) == 0:
                    temp_obj.data.materials.append(mat)
                else:
                    temp_obj.data.materials[0] = mat 

                with bpy.context.temp_override(object=temp_obj, material=mat):
                    bpy.ops.ocarina.material_initializer()

            temp_obj.data.materials.clear()
            for mat in original_materials:
                temp_obj.data.materials.append(mat)

            if temp_obj.name == "TempMaterialObject":
                bpy.data.objects.remove(temp_obj)

            # We remove attribute Alpha from Fast64
            for obj in bpy.context.scene.objects:
                if hasattr(obj.data, 'attributes'):
                    if 'Alpha' in obj.data.attributes:
                        obj.data.attributes.remove(obj.data.attributes['Alpha'])

            return {'FINISHED'}

class UI_OT_Refresh(bpy.types.Operator):
    bl_idname = "ocarina.refresh"
    bl_label = 'Update Materials'
    bl_options = {"INTERNAL", "UNDO"}

    def execute(self, context):

        for object_name in context.scene.objects.items():
            object = context.scene.objects[object_name[0]]

            for material_name in object.material_slots.items():
                material = bpy.data.materials[material_name[0]]
                mat_data: properties.Properties_Material = material.ocarina
                obj_data: properties.Properties_Object = object.ocarina

                properties.node_setup.set_simple_material(material)

                if mat_data.is_ocarina_material:
                    obj_data.is_ocarina_object = True

            if object.ocarina.is_ocarina_object:
                set_object_properties(context, object)

        return {'FINISHED'}

class UI_PT_Material(bpy.types.Panel):
    bl_label = "SharpOcarina"
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"
    bl_context = 'material'

    @classmethod
    def poll(self, context):
        material = context.material
        return material is not None
    
    def draw(self, context):
        material = context.material
        xscene: properties.Properties_Scene = context.scene.ocarina
        xmaterial: properties.Properties_Material = material.ocarina
        xcollision: properties.Properties_Collision = xmaterial.collision

        if xmaterial.is_ocarina_material == False:
            self.layout.box().operator(UI_OT_MaterialInitializer.bl_idname, text="Init Ocarina Material")
            return
        
        box = self.layout.box()
        row = box.row()
        row.prop(xmaterial, "is_mesh")
        row.prop(xmaterial, "is_collision")

        if getattr(xmaterial, "is_mesh") == True:
            box = self.layout.box()

            if foldable_menu(box, xscene, "ui_show_mesh"):

                row = box.row()
                row.prop(xmaterial, "alpha_method", expand=True)

                sub_box = box.box()
                sub_box.row().prop(xscene, "ui_material_tab", expand=True)

                if xscene.ui_material_tab == "TEXTURE":
                    def default_texture_draw(box:bpy.types.UILayout, index):
                        box.template_ID(xmaterial, "texture_" + index, open="image.open")
                        row = box.row()
                        row.prop(xmaterial, "repeat_x_" + index, text='', icon='EVENT_X')
                        row.prop(xmaterial, "repeat_y_" + index, text='', icon='EVENT_Y')
                        row = box.row()
                        row.prop(xmaterial, "shift_x_" + index, text='')
                        row.prop(xmaterial, "shift_y_" + index, text='')
                        row = box.row()
                        sub_box.prop(xmaterial, "texel_format_" + index)
                    
                    subsubbox = sub_box.box()
                    if foldable_menu(subsubbox, xscene, "io_show_texel0"):
                        default_texture_draw(subsubbox, "0")
                    else:
                        subsubbox.template_ID(xmaterial, "texture_0", open="image.open")

                    subsubbox = sub_box.box()
                    if foldable_menu(subsubbox, xscene, "io_show_texel1"):
                        default_texture_draw(subsubbox, "1")
                    else:
                        subsubbox.template_ID(xmaterial, "texture_1", open="image.open")

                    sub_box.prop(xmaterial, "multi_alpha", slider=True)

                elif xscene.ui_material_tab == "MATERIAL":
                    dependant_row_prop(sub_box, xmaterial, "is_animated", "segment")
                    sub_box.prop(xmaterial, "alpha", slider=True)

                    row = sub_box.row()
                    row.prop(xmaterial, "culling")
                    row.prop(xmaterial, "ignore_fog")
                    row = sub_box.row()
                    row.prop(xmaterial, "pixelated")
                    row.prop(xmaterial, "decal")
                    row = sub_box.row()
                    row.prop(xmaterial, "metallic")
                    row.prop(xmaterial, "alpha_mask")
                    row = sub_box.row()
                    row.prop(xmaterial, "env_color")
                    row.prop(xmaterial, "reverse_light")
                    row = sub_box.row()
                    row.prop(xmaterial, "billboard")
                    row.prop(xmaterial, "billboard2D")
                
                sub_box.separator(factor=0.0)
        
        if getattr(xmaterial, "is_collision") == True:
            box = self.layout.box()

            if foldable_menu(box, xscene, "ui_show_collision"):
                if xmaterial.is_mesh == False:
                    row = box.row()
                    color = material.node_tree.nodes["SOShader"].inputs[0]
                    alpha = material.node_tree.nodes["SOShader"].inputs[21]
                    row.prop(color, "default_value", text="")
                    row.prop(alpha, "default_value", text="")
                
                draw_collision_params(xcollision, box, False)

class UI_PT_3dview(bpy.types.Panel):
    bl_category = "SharpOcarina"
    bl_label = "SharpOcarina"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"

    def draw_object(self:bpy.types.Panel, context:bpy.types.Context, box:bpy.types.UILayout):
        object = context.object
        scene = context.scene
        obj_data:properties.Properties_Object = object.ocarina
        xscene:properties.Properties_Scene = scene.ocarina

        if foldable_menu(box, xscene, "ui_show_collision_3d"):
            box.prop(obj_data, 'override')
            box.separator()
            draw_collision_params(obj_data, box, True)

    def draw(self:bpy.types.Panel, context:bpy.types.Context):
        object = context.object
        obj_name = "none"

        if object != None:
            obj_name = object.name

        box = self.layout.box()
        box.operator('ocarina.massinit')
        box.operator('ocarina.refresh')
        box.operator("export_obj_so.export")
        box.label(text="Object: " + obj_name)

        if object != None and object.type == 'MESH':
            obj_data:properties.Properties_Object = object.ocarina

            if obj_data.is_ocarina_object:
                self.draw_object(context, box.box())

classes = (
    UI_OT_MaterialInitializer,
    UI_OT_Refresh,
    UI_OT_MassInit,

    UI_PT_Material,
    UI_PT_3dview,
)

def register():
    for clazz in classes:
        bpy.utils.register_class(clazz)

def unregister():
    for clazz in reversed(classes):
        bpy.utils.unregister_class(clazz)
