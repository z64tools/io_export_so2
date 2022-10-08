import bpy

class Properties_Object(bpy.types.PropertyGroup):
    tags = 0

class Properties_Collection(bpy.types.PropertyGroup):
    meshType = bpy.props.EnumProperty(
        items=[
            ("BOTH",      "Mesh + Collision", "", 0),
            ("MESH",      "Mesh",             "", 1),
            ("COLLISION", "Collision",        "", 2),
        ],
        name="Type",
        default="BOTH"
    )

classes = (
    Properties_Object,
    Properties_Collection,
)

def register():
    for clazz in classes:
        bpy.utils.register_class(clazz)
    
    bpy.types.Object.ocarina = bpy.props.PointerProperty(type=Properties_Object)
    bpy.types.Collection.ocarina = bpy.props.PointerProperty(type=Properties_Collection)

def unregister():
    del bpy.types.Object.ocarina
    del bpy.types.Collection.ocarina

    for clazz in reversed(classes):
        bpy.utils.unregister_class(clazz)