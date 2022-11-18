import bpy
from . import properties

class UI_OT_MaterialInitializer(bpy.types.Operator):
    bl_idname = "ocarina.material_initializer"
    bl_label = 'Initialize material'
    bl_options = {"INTERNAL", "UNDO"}

    def execute(self, context):
        material = context.material
        data: properties.Properties_Material = material.ocarina

        data.is_ocarina_material = True
        data.alpha_method = "CLIP"

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
    
    def get_icon(self, attr):
        if attr:
            return 'DOWNARROW_HLT'
        else:
            return 'RIGHTARROW'
    
    def foldable_menu(self, element, data, attr):
        element.prop(data, attr, icon=self.get_icon(getattr(data, attr)), emboss=False)
        if getattr(data, attr) == True:
            return True
        return False
    
    def dependant_row_prop(self, element: bpy.types.UILayout, data, setter, value, disabler_value = False):
        row = element.row()
        row.prop(data, setter)
        col = row.column()
        if getattr(data, setter) == disabler_value:
            col.enabled = False
        col.prop(data, value)
    
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

            if self.foldable_menu(box, xscene, "ui_show_mesh"):

                row = box.row()
                row.prop(xmaterial, "alpha_method", expand=True)

                row = box.row()
                row.prop(xmaterial, "shading", expand=True)

                box.separator(factor=0.0)

                sub_box = box.box()
                sub_box.row().prop(xscene, "ui_material_tab", expand=True)
                sub_box.separator(factor=0.0)

                if xscene.ui_material_tab == "TEXTURE":
                    def default_texture_draw():
                        sub_box.template_ID(xmaterial, "texture_0", open="image.open")
                        row = sub_box.row()
                        row.prop(xmaterial, "uv_repeat_u", text='', icon='EVENT_X')
                        row.prop(xmaterial, "uv_repeat_v", text='', icon='EVENT_Y')

                    # if self.foldable_menu(sub_box, xscene, "ui_show_texture_params"):
                    #     default_texture_draw()
                    # else:
                    #     default_texture_draw()
                    
                    default_texture_draw()
                
                elif xscene.ui_material_tab == "MATERIAL":
                    self.dependant_row_prop(sub_box, xmaterial, "is_animated", "segment")
                    sub_box.prop(xmaterial, "alpha", slider=True)

                    row = sub_box.row()
                    row.prop(xmaterial, "culling")
                    row.prop(xmaterial, "ignore_fog")
                    row = sub_box.row()
                    row.prop(xmaterial, "pixelated")
                    row.prop(xmaterial, "decal")
                sub_box.separator(factor=0.0)
        
        if getattr(xmaterial, "is_collision") == True:
            box = self.layout.box()

            if self.foldable_menu(box, xscene, "ui_show_collision"):
                if xmaterial.is_mesh == False:
                    row = box.row()
                    color = material.node_tree.nodes["SMH Principled BSDF"].inputs[0]
                    alpha = material.node_tree.nodes["SMH Principled BSDF"].inputs[21]
                    row.prop(color, "default_value", text="")
                    row.prop(alpha, "default_value", text="")

                box.prop(xcollision, "sound_type")

                self.dependant_row_prop(box, xcollision, "has_floor_flags", "floor_flags")
                self.dependant_row_prop(box, xcollision, "has_wall_flags", "wall_flags")
                self.dependant_row_prop(box, xcollision, "has_special_flags", "special_flags")
                self.dependant_row_prop(box, xcollision, "has_exit", "exit")
                self.dependant_row_prop(box, xcollision, "has_env", "env")
                self.dependant_row_prop(box, xcollision, "has_camera", "camera")
                
                row = box.row()
                row.prop(xcollision, "hookshot")
                row.prop(xcollision, "ignore_cam")

                row = box.row()
                row.prop(xcollision, "ignore_actor")
                row.prop(xcollision, "ignore_proj")

                self.dependant_row_prop(box, xcollision, "conveyor_speed", "conveyor_dir", "#Speed0")
                row = box.row()
                if xcollision.conveyor_speed == "#Speed0":
                    row.enabled = False
                row.prop(xcollision, "waterstream")

classes = (
    UI_PT_Material,
    UI_OT_MaterialInitializer,
)

def register():
    for clazz in classes:
        bpy.utils.register_class(clazz)

def unregister():
    for clazz in reversed(classes):
        bpy.utils.unregister_class(clazz)