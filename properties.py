import bpy
from . import node_setup
from bpy.props import StringProperty

class Properties_Scene(bpy.types.PropertyGroup):
    ui_show_collision_3d: bpy.props.BoolProperty(default=False, name="Collision")
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
    io_show_texel0: bpy.props.BoolProperty(default=True, name="Texture 0")
    io_show_texel1: bpy.props.BoolProperty(default=False, name="Texture 1")


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
            ("#SFX_9",          "Plank Wood",    ""),
            ("#SFX_A",          "Wood",          ""),  
            ("#SFX_C",          "Ice",           ""),
            ("#SFX_D",          "Carpet",        ""),
            ("#SFX_B",          "~Unk B",      "Customize via code"),
            ("#SFX_E",          "~Unk E",      "Customize via code"),
            ("#SFX_F",          "~Unk F",       "Customize via code"),
        ],
        default="#SFX_2",
        name="Sound"
    )

    has_floor_flags: bpy.props.BoolProperty(default=False,name="Floor")
    floor_flags: bpy.props.EnumProperty(
        items=[
            ("#FLOORPROPERTY_SMALL_VOID",        "Small Void",        ""),
            ("#FLOORPROPERTY_HANG_LEDGE",        "Hand Ledge",        ""),
            ("#FLOORPROPERTY_STOP_AIR_MOMENTUM", "Stop Air Momentum", ""),
            ("#FLOORPROPERTY_NO_LEDGE_JUMP",     "No Ledge Jump",     ""),
            ("#FLOORPROPERTY_DIVE",              "Dive",              ""),
            ("#FLOORPROPERTY_VOID",              "Void",              ""),
            ("#FLOORPROPERTY_UNK01",             "~Unk 1",             ""),
            ("#FLOORPROPERTY_UNK02",             "~Unk 2",             ""),
            ("#FLOORPROPERTY_UNK03",             "~Unk 3",             ""),
            ("#FLOORPROPERTY_UNK04",             "~Unk 4",             ""),
            ("#FLOORPROPERTY_UNK07",             "~Unk 7",             ""),
            ("#FLOORPROPERTY_UNK0A",             "~Unk A",             ""),
        ],
        default="#FLOORPROPERTY_SMALL_VOID",
        name=""
    )

    has_wall_flags: bpy.props.BoolProperty(default=False,name="Wall")
    wall_flags: bpy.props.EnumProperty(
        items=[
            ("#WALLPROPERTY_NO_LEDGE_GRAB", "No Ledge Grab", ""),
            ("#WALLPROPERTY_LADDER",        "Ladder",        ""),
            ("#WALLPROPERTY_LADDER_TOP",    "Ladder Top",    ""),
            ("#WALLPROPERTY_VINE",          "Climbable",     ""),
            ("#WALLPROPERTY_CRAWL_A",       "Crawl A",       ""),
            ("#WALLPROPERTY_CRAWL_B",       "Crawl B",       "No difference between A and B"),
            ("#WALLPROPERTY_PUSH",          "Push",          ""),
            ("#WALLPROPERTY_UNK08",          "~Unk 8",          ""),
            ("#WALLPROPERTY_UNK09",          "~Unk 9",          ""),
            ("#WALLPROPERTY_UNK0A",          "~Unk A",          ""),
            ("#WALLPROPERTY_UNK0B",          "~Unk B",          ""),
            ("#WALLPROPERTY_UNK0C",          "~Unk C",          ""),
            ("#WALLPROPERTY_UNK0D",          "~Unk D",          ""),
            ("#WALLPROPERTY_UNK0E",          "~Unk E",          ""),
            ("#WALLPROPERTY_UNK0F",          "~Unk F",          ""),
        ],
        default="#WALLPROPERTY_NO_LEDGE_GRAB",
        name=""
    ) 

    has_special_flags: bpy.props.BoolProperty(default=False,name="Special")
    special_flags: bpy.props.EnumProperty(
        items=[
            ("#FLOORSPECIAL_UNK01",           "Haunted Wasteland", ""),
            ("#FLOORSPECIAL_HURT_SPIKES",     "Hurt",              ""),
            ("#FLOORSPECIAL_HURT_LAVA",       "Hurt (Lava)",       ""),
            ("#FLOORSPECIAL_SAND",            "Sand",              ""),
            ("#FLOORSPECIAL_SLIPPERY",        "Slippery",          ""),
            ("#FLOORSPECIAL_NO_FALL_DAMAGE",  "No Fall Damage",    ""),
            ("#FLOORSPECIAL_QUICKSAND",       "Quicksand",         ""),
            ("#FLOORSPECIAL_JABU_WALL",       "Jabu Wall",         ""),
            ("#FLOORSPECIAL_VOID_ON_CONTACT", "Void on Contact",   ""),
            ("#FLOORSPECIAL_LINK_LOOK_UP",    "Look Up",           ""),
            ("#FLOORSPECIAL_QUICKSAND_EPONA", "Quicksand (Epona Crossable)", ""),
            ("#FLOORSPECIAL_UNK0C",           "~Unk C",            ""),
        ],
        default="#FLOORSPECIAL_HURT_SPIKES",
        name=""
    )

    has_exit: bpy.props.BoolProperty(default=False,name="ExitID")
    exit: bpy.props.IntProperty(default=0,min=0,max=31,name="")

    has_env: bpy.props.BoolProperty(default=False,name="EnvID")
    env: bpy.props.IntProperty(default=0,min=0,max=31,name="")

    has_camera: bpy.props.BoolProperty(default=False,name="CameraID")
    camera: bpy.props.IntProperty(default=0,min=0,max=255,name="")

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
    steep: bpy.props.BoolProperty(default=False, name="Steep")
    block_epona: bpy.props.BoolProperty(default=False, name="Block Epona")
    priority: bpy.props.BoolProperty(default=False, name="Priority")
    wall_damage: bpy.props.BoolProperty(default=False, name="Wall Damage")
    ignore_cam: bpy.props.BoolProperty(default=False, name="Ignore Cam")
    ignore_actor: bpy.props.BoolProperty(default=False, name="Ignore Actor")
    ignore_proj: bpy.props.BoolProperty(default=False, name="Ignore Projectile")

    echo: bpy.props.IntProperty(default=0, min=0, max=63, name="Echo")



class Properties_Material(bpy.types.PropertyGroup):
    is_ocarina_material: bpy.props.BoolProperty(
        default=False,
        update=node_setup.on_material_image_update
    )
    is_mesh: bpy.props.BoolProperty(default=True, name="Mesh", description="#NoCollision", update=node_setup.on_material_disable_mesh)
    is_collision: bpy.props.BoolProperty(default=True, name="Collision", description="#NoMesh")

    texture_0: bpy.props.PointerProperty(
        type=bpy.types.Image,
        update=node_setup.on_material_image_update,
    )

    texture_1: bpy.props.PointerProperty(
        type=bpy.types.Image,
        update=node_setup.on_material_image_update,
    )

    shift_x_0: bpy.props.IntProperty(name="ShiftX", default=0, min=-3, max=3, update=node_setup.on_material_update_shift)
    shift_y_0: bpy.props.IntProperty(name="ShiftY", default=0, min=-3, max=3, update=node_setup.on_material_update_shift)
    shift_x_1: bpy.props.IntProperty(name="ShiftX", default=0, min=-3, max=3, update=node_setup.on_material_update_shift)
    shift_y_1: bpy.props.IntProperty(name="ShiftY", default=0, min=-3, max=3, update=node_setup.on_material_update_shift)

    texel_format_0: bpy.props.EnumProperty(
        items=[
            ("Auto",    "Auto",   ""),
            ("#RGBA16", "RGBA16", ""),
            ("#RGBA32", "RGBA32", ""),
            ("#CI4",    "CI4",    ""),
            ("#CI8",    "CI8",    ""),
            ("#I4",     "I4",     ""),
            ("#I8",     "I8",     ""),
            ("#IA4",    "IA4",    ""),
            ("#IA8",    "IA8",    ""),
            ("#IA16",   "IA16",   ""),
        ],
        name="Format",
        default="Auto"
    )

    texel_format_1: bpy.props.EnumProperty(
        items=[
            ("Auto",    "Auto",   ""),
            ("#RGBA16", "RGBA16", ""),
            ("#RGBA32", "RGBA32", ""),
            ("#CI4",    "CI4",    ""),
            ("#CI8",    "CI8",    ""),
            ("#I4",     "I4",     ""),
            ("#I8",     "I8",     ""),
            ("#IA4",    "IA4",    ""),
            ("#IA8",    "IA8",    ""),
            ("#IA16",   "IA16",   ""),
        ],
        name="Format",
        default="Auto"
    )

    alpha: bpy.props.IntProperty(
        name="Alpha",
        default=255,
        min=0,
        max=255,
        update=node_setup.on_material_update_alpha
    )
    multi_alpha: bpy.props.IntProperty(
        name="Mix",
        default=0,
        min=0,
        max=255,
        update=node_setup.on_material_update_multi_alpha
    )

    is_animated: bpy.props.BoolProperty(default=False, name="Animated")

    segment: bpy.props.EnumProperty(
        items=[
            ("Animated8", "Segment 8", ""),
            ("Animated9", "Segment 9", ""),
            ("AnimatedA", "Segment A", ""),
            ("AnimatedB", "Segment B", ""),
            ("AnimatedC", "Segment C", ""),
            ("AnimatedD", "Segment D", ""),
            ("AnimatedE", "Segment E", ""),
            ("AnimatedF", "Segment F", ""),
        ],
        default="Animated8",
        name=""
    )

    repeat_x_0: bpy.props.EnumProperty(
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
    repeat_y_0: bpy.props.EnumProperty(
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
    repeat_x_1: bpy.props.EnumProperty(
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
    repeat_y_1: bpy.props.EnumProperty(
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
            # ("OPAQUE", "Opaque",     ""),
            ("CLIP",   "Opaque",      ""),
            ("BLEND",  "Transparent", ""),
        ],
        default="CLIP",
        name="Blend Method",
        update=node_setup.on_material_use_transparency_update,
    )

    ignore_fog: bpy.props.BoolProperty(name="Ignore Fog")
    pixelated: bpy.props.BoolProperty(name="Pixelated",update=node_setup.on_material_update_pixelating)
    decal: bpy.props.BoolProperty(name="Decal")
    metallic: bpy.props.BoolProperty(name="Metallic")
    env_color: bpy.props.BoolProperty(name="Env Color")
    reverse_light: bpy.props.BoolProperty(name="Reverse Light")
    billboard: bpy.props.BoolProperty(name="Billboard")
    billboard2D: bpy.props.BoolProperty(name="2D Billboard")
    alpha_mask: bpy.props.BoolProperty(name="Alpha Mask",update=node_setup.on_material_update_alphamask)

    label_alpha: bpy.props.BoolProperty(name="Alpha")
    label_shade: bpy.props.BoolProperty(name="Shade")

    collision: bpy.props.PointerProperty(type=Properties_Collision)

class Properties_Object(Properties_Collision):
    is_ocarina_object: bpy.props.BoolProperty(default=False)
    override: bpy.props.BoolProperty(
        default=False,
        name="Override",
        description="Override material settings")

classes = (
    Properties_Scene,
    Properties_Collision,
    Properties_Material,
    Properties_Object,
)

def register():
    for clazz in classes:
        bpy.utils.register_class(clazz)
    
    bpy.types.Scene.ocarina = bpy.props.PointerProperty(type=Properties_Scene)
    bpy.types.Material.ocarina = bpy.props.PointerProperty(type=Properties_Material)
    bpy.types.Object.ocarina = bpy.props.PointerProperty(type=Properties_Object)
    bpy.types.Scene.SO_last_export_path = StringProperty(
        name="Export Path",
        description="Path used to automatically export the .obj, it autofills",
        default=""
    )

def unregister():
    del bpy.types.Material.ocarina
    del bpy.types.Scene.ocarina
    del bpy.types.Scene.SO_last_export_path

    for clazz in reversed(classes):
        bpy.utils.unregister_class(clazz)
