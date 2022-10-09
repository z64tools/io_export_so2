import bpy

class Properties_Scene(bpy.types.PropertyGroup):
    ui_show_collision: bpy.props.BoolProperty(default=False, name="Collision")
    ui_show_other_flags: bpy.props.BoolProperty(default=False, name="Flags")
    ui_show_wall_flags: bpy.props.BoolProperty(default=False, name="Wall Flags")
    ui_show_floor_flags: bpy.props.BoolProperty(default=False, name="Floor Flags")

class Properties_Material(bpy.types.PropertyGroup):
    is_ocarina_material: bpy.props.BoolProperty(
        default=False
    )

    sound_type: bpy.props.EnumProperty(
        items=[
            ("DIRT",          "Dirt",          ""),
            ("SAND",          "Sand",          ""),
            ("STONE",         "Stone",         ""),
            ("WETSTONE",      "WetStone",      ""),
            ("SHALLOWWATER1", "ShallowWater1", ""),
            ("SHALLOWWATER2", "ShallowWater2", ""),
            ("TALLGRASS",     "TallGrass",     ""),
            ("SNOW",          "Snow",          ""),
            ("WOOD",          "Wood",          ""),
            ("PLANKWOOD",     "PlankWood",     ""),
            ("GRASS",         "Grass",         ""),
            ("CERAMIC",       "Ceramic",       ""),
            ("CARPET",        "Carpet",        ""),
        ],
        default="DIRT",
        name="Sound Type"
    )

    interaction_flag_ladder_top: bpy.props.BoolProperty(default=False, name="")
    interaction_flag_ladder: bpy.props.BoolProperty(default=False, name="")
    interaction_flag_climbable: bpy.props.BoolProperty(default=False, name="")
    interaction_flag_crawl: bpy.props.BoolProperty(default=False, name="")
    interaction_flag_no_ledge_climb: bpy.props.BoolProperty(default=False, name="")

    wall_flags: bpy.props.EnumProperty(
        items=[
            ("LADDER",            "Ladder",         "#Ladder"),
            ("LADDER_TOP",        "Ladder Top",     "#TopLadder"),
            ("DAMAGE",            "Damage",         "#WallDamage"),
            ("CLIMBABLE",         "Climbable",      "#Climbable"),
            ("FORCECLIMB",        "Force Climb",    "#ForceClimb"),
            ("AUTOGRAB",          "Autograb Climb", "#AutograbClimb"),
            ("NO_LEDGE_CLIMB",    "No Ledge Climb", "#NoLedgeClimb"),
            ("CRAWL",             "Crawl",          "#Crawl"),
        ],
        options={"ENUM_FLAG"},
    )

    floor_flags: bpy.props.EnumProperty(
        items=[
            ("NO_JUMP",           "No Ledge Jump",     "#NoLedgeJump"),
            ("STEEP",             "Steep",             "#Steep"),
            ("ICE",               "Ice",               "#Ice"),
            ("SAND",              "Sand",              "#Quicksand"),
            ("LAVA",              "Lava",              "#Lava"),
            ("DAMAGE",            "Damage",            "#GroundDamage"),
            ("NO_FALL_DAMAGE",    "No Fall Damage",    "#NoFallDamage"),
            ("LAVA_KILL",         "Kill Lava",         "#KillingLava"),
            ("SAND_KILL",         "Kill Sand",         "#KillingQuicksand"),
            ("SAND_KILL_NO_JUMP", "No Jump Kill Sand", "#NoJumpKillingQuicksand"),
            ("NO_EPONA",          "Block Epona",       "#BlockEpona"),
            ("JABU",              "Jabu",              "#JabuJabu"),
        ],
        options={"ENUM_FLAG"},
    )

    other_flags: bpy.props.EnumProperty(
        items=[
            ("VOID",           "Void (Scene)",     "#Void"),
            ("BIG_VOID",       "Void (Room)",      "#SmallVoid"),
            ("HOOKSHOT",       "Hookshot",         "#Hookshot"),
            ("DIVE",           "Dive",             "#Dive"),
            ("LOWER_UNIT",     "Lower by 1 unit",  "#Lower1Unit"),
        ],
        options={"ENUM_FLAG"},
    )

classes = (
    Properties_Scene,
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