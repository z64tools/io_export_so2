import bpy

class Properties_Object(bpy.types.PropertyGroup):
    tags = 0

classes = (
    Properties_Object,
)

def register():
    for clazz in classes:
        bpy.utils.register_class(clazz)
    
    bpy.types.Object.sotm = bpy.props.PointerProperty(type=Properties_Object)

def unregister():
    del bpy.types.Object.sotm

    for clazz in reversed(classes):
        bpy.utils.unregister_class(clazz)