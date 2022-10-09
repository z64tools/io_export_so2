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
    
    def draw(self, context):
        material = context.material
        xscene: properties.Properties_Scene = context.scene.ocarina
        xmaterial: properties.Properties_Material = material.ocarina

        if xmaterial.is_ocarina_material == False:
            self.layout.box().operator(UI_OT_MaterialInitializer.bl_idname, text="Init Ocarina Material")
            return
        

        col_box = self.layout.box()
        col_box.prop(xscene, "ui_show_collision", icon=self.get_icon(getattr(xscene, "ui_show_collision")), emboss=False)
        if getattr(xscene, "ui_show_collision") == True:
            col_box.prop(xmaterial, "sound_type")
            for show_flag, flag in (
                ( "ui_show_other_flags", "other_flags" ),
                ( "ui_show_floor_flags", "floor_flags" ),
                ( "ui_show_wall_flags", "wall_flags" ),
            ):
                sub_box = col_box.box()
                sub_box.prop(xscene, show_flag, icon=self.get_icon(getattr(xscene, show_flag)), emboss=False)
                if getattr(xscene, show_flag) == True:
                    sub_box.prop(xmaterial, flag)


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