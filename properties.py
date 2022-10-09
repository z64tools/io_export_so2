import bpy
from . import node_setup

class Properties_Scene(bpy.types.PropertyGroup):
    ui_show_collision: bpy.props.BoolProperty(default=False, name="Collision")
    ui_show_mesh: bpy.props.BoolProperty(default=False, name="Mesh")
    ui_show_texture_params: bpy.props.BoolProperty(default=False, name="Texture")
    ui_material_tab: bpy.props.EnumProperty(
        items=[
            ("TEXTURE",  "Texture",  "", "TEXTURE", 0),
            ("MATERIAL", "Material", "", "SHADING_RENDERED", 1),
        ],
        default="TEXTURE",
        name="Material Tab",
    )

class Properties_Collision(bpy.types.PropertyGroup):
    sound_type: bpy.props.EnumProperty(
        items=[
            ("#SFX_0",          "Dirt",          ""),
            ("#SFX_1",          "Sand",          ""),
            ("#SFX_2",          "Stone",         ""),
            ("#SFX_3",          "WetStone",      ""),
            ("#SFX_4",          "Water",         ""),
            ("#SFX_5",          "Shallow Water", ""),
            ("#SFX_6",          "Bush",          ""),
            ("#SFX_7",          "Lava",          ""),
            ("#SFX_8",          "Grass",         ""),
            ("#SFX_9",          "Wood",          ""),
            ("#SFX_A",          "Plank Wood",    ""),
            ("#SFX_C",          "Ice",           ""),
            ("#SFX_D",          "Carpet",        ""),

            ("#SFX_8",          "0x08",          ""),
            ("#SFX_E",          "0x0E",          ""),
            ("#SFX_F",          "0x0F",          ""),
        ],
        default="#SFX_0",
        name="Sound"
    )

    has_floor_flags: bpy.props.BoolProperty(default=False,name="Wall")
    floor_flags: bpy.props.EnumProperty(
        items=[
            ("#FLOOR_VOID_SMALL",        "Small Void",        ""),
            ("#FLOOR_HANG_LEDGE",        "Hand Ledge",        ""),
            ("#FLOOR_STOP_AIR_MOMENTUM", "Stop Air Momentym", ""),
            ("#FLOOR_NO_LEDGE_JUMP",     "No Ledge Jump",     ""),
            ("#FLOOR_DIVE",              "Dive",              ""),
            ("#FLOOR_VOID",              "Void",              ""),
        ],
        default="#FLOOR_VOID_SMALL",
        name=""
    )

    has_wall_flags: bpy.props.BoolProperty(default=False,name="Floor")
    wall_flags: bpy.props.EnumProperty(
        items=[
            ("#WALL_NO_LEDGE_GRAP", "No Ledge Grab", ""),
            ("#WALL_LADDER",        "Ladder",        ""),
            ("#WALL_LADDER_TOP",    "Ladder Top",    ""),
            ("#WALL_VINE",          "Climbable",     ""),
            ("#WALL_CRAWL_A",       "Crawl A",       ""),
            ("#WALL_CRAWL_B",       "Crawl B",       ""),
            ("#WALL_PUSH",          "Push",          ""),
        ],
        default="#WALL_NO_LEDGE_GRAP",
        name=""
    ) 

    has_special_flags: bpy.props.BoolProperty(default=False,name="Special")
    special_flags: bpy.props.EnumProperty(
        items=[
            # ("#BEHAVIOUR_UNK_1",           "", ""),
            ("#BEHAVIOUR_HURT_SPIKES",     "Hurt",              ""),
            ("#BEHAVIOUR_HURT_LAVA",       "Hurt (Lava)",       ""),
            ("#BEHAVIOUR_SAND",            "Sand",              ""),
            ("#BEHAVIOUR_SLIPPERY",        "Slippery",          ""),
            ("#BEHAVIOUR_NO_FALL_DAMAGE",  "No Fall Damage",    ""),
            ("#BEHAVIOUR_QUICKSAND",       "Quicksand",         ""),
            ("#BEHAVIOUR_JABU_WALL",       "Jabu Wall",         ""),
            ("#BEHAVIOUR_VOID_ON_CONTACT", "Void on Contact",   ""),
            # ("#BEHAVIOUR_UNK_A",           "", ""),
            ("#BEHAVIOUR_LOOK_UP",         "Look Up",           ""),
            ("#BEHAVIOUR_QUICKSAND_EPONA", "Quicksand (Epona)", ""),
        ],
        default="#BEHAVIOUR_HURT_SPIKES",
        name=""
    )

    has_exit: bpy.props.BoolProperty(default=False,name="ExitID")
    exit: bpy.props.IntProperty(default=1,min=1,max=32,name="")

    has_env: bpy.props.BoolProperty(default=False,name="EnvID")
    env: bpy.props.IntProperty(default=1,min=1,max=32,name="")

    has_camera: bpy.props.BoolProperty(default=False,name="CameraID")
    camera: bpy.props.IntProperty(default=1,min=1,max=256,name="")

    conveyor_dir: bpy.props.FloatProperty(default=0,min=0,max=1.0,name="Dir")
    conveyor_speed: bpy.props.EnumProperty(
        items=[
            ("#Speed0", "Disabled", ""),
            ("#Speed1", "Slow", ""),
            ("#Speed2", "Medium", ""),
            ("#Speed3", "Fast", ""),
            ("#Speed4", "Preserve", ""),
        ],
        name="Speed",
        default="#Speed0",
    )

    waterstream: bpy.props.BoolProperty(default=False, name="Water Conveyor")
    hookshot: bpy.props.BoolProperty(default=False, name="Hookshot")
    ignore_cam: bpy.props.BoolProperty(default=False, name="Ignore Cam")
    ignore_actor: bpy.props.BoolProperty(default=False, name="Ignore Actor")
    ignore_proj: bpy.props.BoolProperty(default=False, name="Ignore Projectile")

class Properties_Material(bpy.types.PropertyGroup):
    is_ocarina_material: bpy.props.BoolProperty(
        default=False,
        update=node_setup.on_material_image_update
    )
    is_mesh: bpy.props.BoolProperty(default=True, name="Mesh", description="#NoCollision")
    is_collision: bpy.props.BoolProperty(default=True, name="Collision", description="#NoMesh")

    texture_0: bpy.props.PointerProperty(
        type=bpy.types.Image,
        update=node_setup.on_material_image_update,
    )

    texture_1: bpy.props.PointerProperty(
        type=bpy.types.Image,
        update=node_setup.on_material_image_update,
    )

    alpha: bpy.props.IntProperty(
        name="Alpha",
        default=255,
        min=0,
        max=255,
    )

    shading: bpy.props.EnumProperty(
        items=[
            ("SHADED", "Lighting", ""),
            ("VERTEX", "Vertex Color", ""),
        ],
        default="VERTEX",
        name="Shading",
        update=node_setup.on_material_update_shading
    )

    is_animated: bpy.props.BoolProperty(default=False, name="Animated")

    segment: bpy.props.EnumProperty(
        items=[
            ("SEG8", "Segment 8", ""),
            ("SEG9", "Segment 9", ""),
            ("SEGA", "Segment A", ""),
            ("SEGB", "Segment B", ""),
            ("SEGC", "Segment C", ""),
            ("SEGD", "Segment D", ""),
            ("SEGE", "Segment E", ""),
            ("SEGF", "Segment F", ""),
        ],
        default="SEG8",
        name=""
    )

    uv_repeat_u: bpy.props.EnumProperty(
        items=[
            (
                "WRAP",
                "Wrap",
                "Makes the image normally repeat along U",
                "TEXTURE",
                0,
            ),
            (
                "MIRROR",
                "Mirror",
                "Makes the image repeat along U, mirroring every other repetition",
                "MOD_MIRROR",
                1,
            ),
            (
                "CLAMP",
                "Clamp",
                "Makes the image not repeat along U, "
                "stretching the first and last columns of the image",
                "FULLSCREEN_EXIT",
                2,
            ),
        ],
        name="UV Repeat U",
        description="How to repeat the image along the U component of UVs",
        default="WRAP",
        update=node_setup.on_material_uv_repeat_update,
    )

    uv_repeat_v: bpy.props.EnumProperty(
        items=[
            (
                "WRAP",
                "Wrap",
                "Makes the image normally repeat along V",
                "TEXTURE",
                0,
            ),
            (
                "MIRROR",
                "Mirror",
                "Makes the image repeat along V, mirroring every other repetition",
                "MOD_MIRROR",
                1,
            ),
            (
                "CLAMP",
                "Clamp",
                "Makes the image not repeat along V, "
                "stretching the first and last lines of the image",
                "FULLSCREEN_EXIT",
                2,
            ),
        ],
        name="UV Repeat V",
        description="How to repeat the image along the V component of UVs",
        default="WRAP",
        update=node_setup.on_material_uv_repeat_update,
    )

    culling: bpy.props.BoolProperty(
        default=True, 
        name="Backface Culling",
        update=node_setup.on_material_update_culling
    )
    
    alpha_method: bpy.props.EnumProperty(
        items=[
            ("OPAQUE", "Opaque",     ""),
            ("CLIP",   "Clip Alpha", ""),
            ("BLEND",  "Soft Alpha", ""),
        ],
        default="OPAQUE",
        name="Blend Method",
        update=node_setup.on_material_use_transparency_update,
    )

    ignore_fog: bpy.props.BoolProperty(name="Ignore Fog")
    pixelated: bpy.props.BoolProperty(name="Pixelated",update=node_setup.on_material_update_pixelating)
    decal: bpy.props.BoolProperty(name="Decal")

    label_alpha: bpy.props.BoolProperty(name="Alpha")
    label_shade: bpy.props.BoolProperty(name="Shade")

    collision: bpy.props.PointerProperty(type=Properties_Collision)

classes = (
    Properties_Scene,
    Properties_Collision,
    Properties_Material,
)

def register():
    for clazz in classes:
        bpy.utils.register_class(clazz)
    
    bpy.types.Scene.ocarina = bpy.props.PointerProperty(type=Properties_Scene)
    bpy.types.Material.ocarina = bpy.props.PointerProperty(type=Properties_Material)

def unregister():
    del bpy.types.Material.ocarina
    del bpy.types.Scene.ocarina

    for clazz in reversed(classes):
        bpy.utils.unregister_class(clazz)
