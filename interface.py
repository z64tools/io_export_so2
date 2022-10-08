import bpy

class UI_PT_Mesh(bpy.types.Panel):
    bl_label = "SharpOcarina"
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"
    bl_context = "data"

    @classmethod
    def poll(self, context):
        object = context.object
        return object.type == "MESH"
    
    def draw(self, context):
        box = self.layout.box()
        box.label(text='WOW')

class UI_PT_Collection(bpy.types.Panel):
    bl_label = "SharpOcarina"
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"
    bl_context = "collection"

    @classmethod
    def poll(cls, context):
        return context.collection != context.scene.collection
    
    def draw(self, context):
        box = self.layout.box()
        box.label(text="Wow")
        box.label(text="Wow")
        box.label(text="Wow")

classes = (
    UI_PT_Mesh,
    UI_PT_Collection,
)

def register():
    for clazz in classes:
        bpy.utils.register_class(clazz)

def unregister():
    for clazz in reversed(classes):
        bpy.utils.unregister_class(clazz)