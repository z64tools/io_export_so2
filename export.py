import os
import bpy
from mathutils import Matrix, Vector, Color
from bpy_extras import io_utils, node_shader_utils
from . import properties

from bpy_extras.wm_utils.progress_report import (
    ProgressReport,
    ProgressReportSubstep,
)

from bpy.props import (
    BoolProperty,
    FloatProperty,
    StringProperty,
)

from bpy_extras.io_utils import (
    ExportHelper,
    orientation_helper,
    path_reference_mode,
    axis_conversion,
)

def name_compat(name):
    if name is None:
        return "None"
    else:
        return name.replace(" ", "_")

def mesh_triangulate(me):
    import bmesh

    bm = bmesh.new()
    bm.from_mesh(me)
    bmesh.ops.triangulate(bm, faces=bm.faces)
    bm.to_mesh(me)
    bm.free()

def write_mtl(scene, filepath, path_mode, copy_set, mtl_dict, copy_textures):
    source_dir = os.path.dirname(bpy.data.filepath)
    dest_dir = os.path.dirname(filepath)

    with open(filepath, "w", encoding="utf8", newline="\n") as f:
        fw = f.write

        fw("# Blender MTL File: %r\n" % (os.path.basename(bpy.data.filepath) or "None"))
        fw("# Material Count: %i\n" % len(mtl_dict))

        mtl_dict_values = list(mtl_dict.values())
        mtl_dict_values.sort(key=lambda m: m[0])

        # Write material/image combinations we have used.
        # Using mtl_dict.values() directly gives un-predictable order.
        for mtl_mat_name, mat in mtl_dict_values:
            # Get the Blender data for the material and the image.
            # Having an image named None will make a bug, dont do it :)

            fw("\nnewmtl %s\n" % mtl_mat_name)  # Define a new material: matname_imgname

            image = None

            if mat != None:
                data:properties.Properties_Material = mat.ocarina

                if data.is_ocarina_material:
                    if copy_textures:
                        image = data.texture_0
                
                        if image is not None:
                            filepath = io_utils.path_reference(
                                image.filepath,
                                source_dir,
                                dest_dir,
                                path_mode,
                                "",
                                copy_set,
                                image.library,
                            )
                            fw("map_Kd %s\n" % repr(filepath)[1:-1])

                        image = data.texture_1

                        if image is not None:
                            filepath = io_utils.path_reference(
                                image.filepath,
                                source_dir,
                                dest_dir,
                                path_mode,
                                "",
                                copy_set,
                                image.library,
                            )
                            fw("map_Ks %s\n" % repr(filepath)[1:-1])
                    
                    else:
                        image = data.texture_0
                
                        if image is not None:
                            filepath = io_utils.path_reference(
                                image.filepath,
                                source_dir,
                                dest_dir,
                                path_mode,
                                "",
                                copy_set,
                                image.library,
                            )
                            fw("map_Kd %s\n" % repr(filepath)[1:-1])

                        image = data.texture_1

                        if image is not None:
                            filepath = io_utils.path_reference(
                                image.filepath,
                                source_dir,
                                dest_dir,
                                path_mode,
                                "",
                                copy_set,
                                image.library,
                            )
                            fw("map_Ks %s\n" % repr(filepath)[1:-1])
                    tags_0 = ""
                    tags_1 = ""
                    if data.texture_0 is not None:
                        if data.texel_format_0 != "Auto":
                            tags_0 += data.texel_format_0
                        if data.repeat_x_0 == "MIRROR":
                            tags_0 += "#MirrorX"
                        elif data.repeat_x_0 == "CLAMP":
                            tags_0 += "#ClampX"
                        if data.repeat_y_0 == "MIRROR":
                            tags_0 += "#MirrorY"
                        elif data.repeat_y_0 == "CLAMP":
                            tags_0 += "#ClampY"
                    if data.texture_1 is not None:
                        if data.texel_format_1 != "Auto":
                            tags_1 += data.texel_format_1
                        if data.repeat_x_1 == "MIRROR":
                            tags_1 += "#MirrorX"
                        elif data.repeat_x_1 == "CLAMP":
                            tags_1 += "#ClampX"
                        if data.repeat_y_1 == "MIRROR":
                            tags_1 += "#MirrorY"
                        elif data.repeat_y_1 == "CLAMP":
                            tags_1 += "#ClampY"
                    if tags_0 != "":
                        fw("tags_0 %s\n" % tags_0)
                    if tags_1 != "":
                        fw("tags_1 %s\n" % tags_1)

import time

def write_file_material_info(object:bpy.types.Object, material_name:str, scene:bpy.types.Scene) -> str:
    result:str = ""
    
    if material_name != None and bpy.data.materials != None and material_name in bpy.data.materials:
        material:bpy.types.Material = bpy.data.materials[material_name]
    else:
        return result

    if material == None:
        return result
    if hasattr(material, "ocarina") == False:
        return result


    mat_data:properties.Properties_Material = material.ocarina
    obj_data:properties.Properties_Object = object.ocarina

    if mat_data.is_collision:
        mat_col:properties.Properties_Collision = mat_data.collision
        result = (result + mat_col.sound_type)
        arr = [
            [ 0, "has_wall_flags",    "wall_flags",     "" ],
            [ 0, "has_floor_flags",   "floor_flags",    "" ],
            [ 0, "has_special_flags", "special_flags",  "" ],
            [ 1, "conveyor_speed",    "conveyor_speed", "#Speed0" ],
            [ 6, "conveyor_speed",      "conveyor_dir",   "#Direction" ],
            [ 5, "has_camera",        "camera",         "#Camera" ],
            [ 2, "has_env",           "env",            "#IndoorEnv" ],
            [ 2, "has_exit",          "exit",           "#Exit" ],
            [ 4, "",                  "echo",           "#Echo" ],
            [ 3, "hookshot",          "",               "#Hookshot"],
            [ 3, "steep",             "",               "#Steep"],
            [ 3, "block_epona",          "",               "#BlockEpona"],
            [ 3, "priority",          "",               "#Priority"],
            [ 3, "wall_damage",          "",               "#WallDamage"],
            [ 3, "ignore_cam",        "",               "#IgnoreCamera"],
            [ 3, "ignore_actor",      "",               "#IgnoreActors"],
            [ 3, "ignore_proj",       "",               "#IgnoreProjectiles"],
        ]

        def read_flag(origin, type, check_attr, val_attr, param) -> str:
            result = ""

            if type == 0:
                if getattr(origin, check_attr):
                    result = result + getattr(origin, val_attr)

            elif type == 1:
                if getattr(origin, check_attr) != "#Speed0":
                    result = result + getattr(origin, val_attr)

            elif type == 2:
                if getattr(origin, check_attr):
                    result = result + param + "%02X" % getattr(origin, val_attr)

            elif type == 3:
                if getattr(origin, check_attr):
                    result = result + param

            elif type == 4:
                if getattr(origin, val_attr) > 0:
                    result = result + param + "%02X" % getattr(origin, val_attr)

            elif type == 5:
                if getattr(origin, check_attr):
                    result = result + param + "%01X" % getattr(origin, val_attr)

            elif type == 6:
                if getattr(origin, check_attr) != "#Speed0":
                    result = result + param + "%02X" % int(round(getattr(origin, val_attr) * 0x3F))
            
            return result

        for type, check_attr, val_attr, param in arr:
            flag_obj = read_flag(obj_data, type, check_attr, val_attr, param)
            flag_mtl = read_flag(mat_col, type, check_attr, val_attr, param)

            if obj_data.override:
                if flag_obj != "":
                    result = result + flag_obj
                else:
                    result = result + flag_mtl
            else:
                if flag_mtl != "":
                    result = result + flag_mtl
                else:
                    result = result + flag_obj

    if mat_data.is_mesh == True and mat_data.is_collision != True:
        result = (result + "#NoCollision")
    elif mat_data.is_mesh != True and mat_data.is_collision == True:
        result = (result + "#NoMesh")

    if mat_data.culling == False:
        result = (result + "#BackfaceCulling")

    if mat_data.ignore_fog:
        result = (result + "#IgnoreFog")

    if mat_data.decal:
        result = (result + "#Decal")

    if mat_data.pixelated:
        result = (result + "#Pixelated")

    if mat_data.metallic:
        result = (result + "#Metallic")

    if mat_data.alpha_mask:
        result = (result + "#MaskAlpha")

    if mat_data.env_color:
        result = (result + "#EnvColor")

    if mat_data.reverse_light:
        result = (result + "#ReverseLight")

    if mat_data.billboard:
        result = (result + "#Billboard")

    if mat_data.billboard2D:
        result = (result + "#2DBillboard")
    
    if mat_data.alpha < 255 or mat_data.alpha_method == "BLEND":
        alpha = mat_data.alpha
        if alpha == 255:
            alpha = 254
        result = (result + "#Alpha%X" % alpha)
    
    if mat_data.is_animated:
        result = (result + "#%s" % str(mat_data.segment))

    if mat_data.shift_x_0 != 0:
        result = result + "#ShiftS" + "%02d" % mat_data.shift_x_0
    if mat_data.shift_y_0 != 0:
        result = result + "#ShiftT" + "%02d" % mat_data.shift_y_0

    if mat_data.texture_1 != None:
        if mat_data.shift_x_1 != 0:
            result = result + "#MultiShiftS%02d" % mat_data.shift_x_1
        if mat_data.shift_y_1 != 0:
            result = result + "#MultiShiftT%02d" % mat_data.shift_y_1
        result = result + "#MultiAlpha%02X" % mat_data.multi_alpha

    return result

def write_file(
    filepath,
    objects,
    depsgraph,
    scene,
    EXPORT_NORMALS=False,
    EXPORT_VERTEX_COLORS=False,
    EXPORT_UV=True,
    EXPORT_MTL=True,
    EXPORT_APPLY_MODIFIERS=True,
    EXPORT_GROUP_BY_OB=True,
    EXPORT_GROUP_BY_MAT=True,
    EXPORT_GROUP_NAME_USE_COLLECTION=True,
    EXPORT_IGNORE_SO_GROUP_SETTINGS=False,
    EXPORT_KEEP_VERT_ORDER=False,
    EXPORT_POLYGROUPS=False,
    EXPORT_GLOBAL_MATRIX=None,
    EXPORT_COPY_TEXTURES=False,
    EXPORT_PATH_MODE="AUTO",
    progress=ProgressReport(),
):
    """
    Basic write function. The context and options must be already set
    This can be accessed externaly
    eg.
    write( 'c:\\test\\foobar.obj', Blender.Object.GetSelected() ) # Using default options.
    """
    if EXPORT_GLOBAL_MATRIX is None:
        EXPORT_GLOBAL_MATRIX = Matrix()

    def veckey3d(v):
        return round(v.x, 4), round(v.y, 4), round(v.z, 4)

    def veckey2d(v):
        return round(v[0], 4), round(v[1], 4)

    def findVertexGroupName(face, vWeightMap):
        """
        Searches the vertexDict to see what groups is assigned to a given face.
        We use a frequency system in order to sort out the name because a given vertex can
        belong to two or more groups at the same time. To find the right name for the face
        we list all the possible vertex group names with their frequency and then sort by
        frequency in descend order. The top element is the one shared by the highest number
        of vertices is the face's group
        """
        weightDict = {}
        for vert_index in face.vertices:
            vWeights = vWeightMap[vert_index]
            for vGroupName, weight in vWeights:
                weightDict[vGroupName] = weightDict.get(vGroupName, 0.0) + weight

        if weightDict:
            return max(
                (weight, vGroupName) for vGroupName, weight in weightDict.items()
            )[1]
        else:
            return "(null)"

    with ProgressReportSubstep(progress, 2, "OBJ Export path: %r" % filepath, "OBJ Export Finished") as subprogress1:
        with open(filepath, "w", encoding="utf8", newline="\n") as f:
            fw = f.write

            # Write Header
            fw(
                "# Blender v%s OBJ File: %r\n"
                % (bpy.app.version_string, os.path.basename(bpy.data.filepath))
            )
            fw("# www.blender.org\n")

            # Tell the obj file what material file to use.
            if EXPORT_MTL:
                mtlfilepath = os.path.splitext(filepath)[0] + ".mtl"
                # filepath can contain non utf8 chars, use repr
                fw("mtllib %s\n" % repr(os.path.basename(mtlfilepath))[1:-1])

            # Initialize totals, these are updated each object
            totverts = totuvco = totno = totvc = 1

            face_vert_index = 1

            # A Dict of Materials
            # (material.name, image.name):matname_imagename # matname_imagename has gaps removed.
            mtl_dict = {}
            # Used to reduce the usage of matname_texname materials, which can become annoying in case of
            # repeated exports/imports, yet keeping unique mat names per keys!
            # mtl_name: (material.name, image.name)
            mtl_rev_dict = {}

            copy_set = set()

            # Get all meshes
            subprogress1.enter_substeps(len(objects))
            for i, ob_main in enumerate(objects):
                # ignore dupli children
                if ob_main.parent and ob_main.parent.instance_type in {
                    "VERTS",
                    "FACES",
                }:
                    subprogress1.step("Ignoring %s, dupli child..." % ob_main.name)
                    continue

                if EXPORT_GROUP_NAME_USE_COLLECTION:
                    next_explore_collections = [scene.collection]
                    explored_collections = []
                    parent_collections = []

                    while next_explore_collections:
                        explore_collection = next_explore_collections.pop()

                        if explore_collection in explored_collections:
                            continue

                        if (
                            explore_collection != scene.collection
                            and ob_main in explore_collection.all_objects.values()
                        ):
                            parent_collections.append(explore_collection)

                        next_explore_collections.extend(
                            reversed(explore_collection.children.values())
                        )

                        explored_collections.append(explore_collection)

                    obj_group_name_collection_prefix = ""
                    prev_collection = None

                    for collection in parent_collections:
                        obj_group_name_collection_prefix += name_compat(collection.name)

                        prev_collection = collection

                obs = [(ob_main, ob_main.matrix_world)]
                if ob_main.is_instancer:
                    obs += [
                        (dup.instance_object.original, dup.matrix_world.copy())
                        for dup in depsgraph.object_instances
                        if dup.parent and dup.parent.original == ob_main
                    ]
                    # ~ print(ob_main.name, 'has', len(obs) - 1, 'dupli children')

                subprogress1.enter_substeps(len(obs))
                for ob, ob_mat in obs:
                    with ProgressReportSubstep(subprogress1, 7) as subprogress2:
                        uv_unique_count = no_unique_count = vc_unique_count = 0

                        ob_for_convert = (
                            ob.evaluated_get(depsgraph)
                            if EXPORT_APPLY_MODIFIERS
                            else ob.original
                        )

                        try:
                            me = ob_for_convert.to_mesh()
                        except RuntimeError:
                            me = None

                        if me is None:
                            continue

                        # _must_ do this before applying transformation, else tessellation may differ
                        # _must_ do this first since it re-allocs arrays
                        mesh_triangulate(me)

                        me.transform(EXPORT_GLOBAL_MATRIX @ ob_mat)
                        # If negative scaling, we have to invert the normals...
                        if ob_mat.determinant() < 0.0:
                            me.flip_normals()

                        if EXPORT_UV:
                            faceuv = len(me.uv_layers) > 0
                            if faceuv:
                                uv_layer = me.uv_layers.active.data[:]
                        else:
                            faceuv = False

                        me_verts = me.vertices[:]

                        if EXPORT_VERTEX_COLORS and me.vertex_colors.active is not None:
                            vertex_colors_data = me.vertex_colors.active.data[:]
                        else:
                            vertex_colors_data = None

                        # Make our own list so it can be sorted to reduce context switching
                        face_index_pairs = [
                            (face, index) for index, face in enumerate(me.polygons)
                        ]

                        if not (
                            len(face_index_pairs) + len(me.vertices)
                        ):  # Make sure there is something to write
                            # clean up
                            ob_for_convert.to_mesh_clear()
                            continue  # dont bother with this mesh.

                        if EXPORT_NORMALS and face_index_pairs:
                            # https://developer.blender.org/docs/release_notes/4.1/python_api/
                            if bpy.app.version < (4, 1, 0):
                                me.calc_normals_split()
                            # No need to call me.free_normals_split later, as this mesh is deleted anyway!

                        loops = me.loops

                        materials = me.materials[:]
                        material_names = [m.name if m else None for m in materials]

                        # avoid bad index errors
                        if not materials:
                            materials = [None]
                            material_names = [name_compat(None)]

                        # Sort by Material, then images
                        # so we dont over context switch in the obj file.
                        if EXPORT_KEEP_VERT_ORDER:
                            pass
                        else:
                            if len(materials) > 1:
                                face_index_pairs.sort(key=lambda a: a[0].material_index)
                            else:
                                # no materials
                                pass

                        # Set the default mat to no material and no image.
                        contextMat = (
                            0,
                            0,
                        )  # Can never be this, so we will label a new material the first chance we get.

                        obj_group_name_base = name_compat(ob.name)

                        if EXPORT_GROUP_NAME_USE_COLLECTION:
                            obj_group_name_base = (
                                obj_group_name_base + "_"
                                + obj_group_name_collection_prefix
                            )

                            if obj_group_name_collection_prefix.startswith("#Room"):
                                obj_group_name_base = obj_group_name_base + "#"

                        if EXPORT_GROUP_BY_OB:
                            fw("g %s\n" % obj_group_name_base)

                        subprogress2.step()

                        # Vert
                        for v in me_verts:
                            fw("v %.6f %.6f %.6f\n" % v.co[:])

                        subprogress2.step()

                        # UV
                        if faceuv:
                            # in case removing some of these dont get defined.
                            uv = f_index = uv_index = uv_key = uv_val = uv_ls = None

                            uv_face_mapping = [None] * len(face_index_pairs)

                            uv_dict = {}
                            uv_get = uv_dict.get
                            for f, f_index in face_index_pairs:
                                uv_ls = uv_face_mapping[f_index] = []
                                overflow = False
                                uv_median = [ 0, 0 ]

                                for uv_index, l_index in enumerate(f.loop_indices):
                                    uv = uv_layer[l_index].uv

                                    if abs(uv[0]) > 15 or abs(uv[1]) > 15:
                                        overflow = True
                                    
                                    uv_median[0] += uv[0]
                                    uv_median[1] += uv[1]
                                
                                uv_median[0] = int(uv_median[0] / 3)
                                uv_median[1] = int(uv_median[1] / 3)

                                for uv_index, l_index in enumerate(f.loop_indices):
                                    uv = uv_layer[l_index].uv
                                    uv_key = loops[l_index].vertex_index, veckey2d(uv)
                                    if overflow == False:
                                        fw("vt %.6f %.6f\n" % (uv[0], uv[1]))
                                    else:
                                        fw("vt %.6f %.6f\n" % (uv[0] - uv_median[0], uv[1] - uv_median[1]))
                                    uv_dict[uv_key] = uv_unique_count
                                    uv_ls.append(uv_unique_count)
                                    uv_unique_count += 1

                            del (
                                uv_dict,
                                uv,
                                f_index,
                                uv_index,
                                uv_ls,
                                uv_get,
                                uv_key,
                                uv_val,
                            )
                            # Only need uv_unique_count and uv_face_mapping

                        subprogress2.step()

                        # NORMAL, Smooth/Non smoothed.
                        if EXPORT_NORMALS:
                            no_key = no_val = None
                            normals_to_idx = {}
                            no_get = normals_to_idx.get
                            loops_to_normals = [0] * len(loops)
                            for f, f_index in face_index_pairs:
                                for l_idx in f.loop_indices:
                                    no_key = veckey3d(loops[l_idx].normal)
                                    no_val = no_get(no_key)
                                    if no_val is None:
                                        no_val = normals_to_idx[
                                            no_key
                                        ] = no_unique_count
                                        fw("vn %.4f %.4f %.4f\n" % no_key)
                                        no_unique_count += 1
                                    loops_to_normals[l_idx] = no_val
                            del normals_to_idx, no_get, no_key, no_val
                        else:
                            loops_to_normals = []

                        subprogress2.step()

                        # vertex colors
                        if vertex_colors_data is not None:
                            vc_key = vc_val = None
                            colors_to_idx = {}
                            vc_get = colors_to_idx.get
                            loops_to_colors = [0] * len(loops)
                            for f, f_index in face_index_pairs:
                                for l_idx in f.loop_indices:
                                    vc_key = vertex_colors_data[l_idx].color[:]
                                    vc_val = vc_get(vc_key)
                                    if vc_val is None:
                                        vc_val = colors_to_idx[vc_key] = vc_unique_count
                                        fw("vc %.4f %.4f %.4f %.4f\n" % vc_key)
                                        vc_unique_count += 1
                                    loops_to_colors[l_idx] = vc_val
                            del colors_to_idx, vc_get, vc_key, vc_val
                        else:
                            loops_to_colors = []

                        subprogress2.step()

                        # XXX
                        if EXPORT_POLYGROUPS:
                            # Retrieve the list of vertex groups
                            vertGroupNames = ob.vertex_groups.keys()
                            if vertGroupNames:
                                currentVGroup = ""
                                # Create a dictionary keyed by face id and listing, for each vertex, the vertex groups it belongs to
                                vgroupsMap = [[] for _i in range(len(me_verts))]
                                for v_idx, v_ls in enumerate(vgroupsMap):
                                    v_ls[:] = [
                                        (vertGroupNames[g.group], g.weight)
                                        for g in me_verts[v_idx].groups
                                    ]

                        for f, f_index in face_index_pairs:
                            f_mat = min(f.material_index, len(materials) - 1)

                            # MAKE KEY
                            key = (
                                material_names[f_mat],
                                None,
                            )  # No image, use None instead.

                            # Write the vertex group
                            if EXPORT_POLYGROUPS:
                                if vertGroupNames:
                                    # find what vertext group the face belongs to
                                    vgroup_of_face = findVertexGroupName(f, vgroupsMap)
                                    if vgroup_of_face != currentVGroup:
                                        currentVGroup = vgroup_of_face
                                        fw(
                                            "g %s#__%s\n"
                                            % (
                                                obj_group_name_base,
                                                name_compat(vgroup_of_face),
                                            )
                                        )

                            # CHECK FOR CONTEXT SWITCH
                            if key == contextMat:
                                pass  # Context already switched, dont do anything
                            else:
                                if key[0] is None and key[1] is None:
                                    # Write a null material, since we know the context has changed.
                                    if EXPORT_GROUP_BY_MAT:
                                        # can be mat_image or (null)
                                        fw("g %s\n" % obj_group_name_base)
                                    if EXPORT_MTL:
                                        fw("usemtl (null)\n")  # mat, image

                                else:
                                    mat_data = mtl_dict.get(key)
                                    if not mat_data:
                                        # First add to global dict so we can export to mtl
                                        # Then write mtl

                                        # Make a new names from the mat and image name,
                                        # converting any spaces to underscores with name_compat.

                                        # If none image dont bother adding it to the name
                                        # Try to avoid as much as possible adding texname (or other things)
                                        # to the mtl name (see [#32102])...
                                        mtl_name = "%s" % name_compat(key[0])
                                        if mtl_rev_dict.get(mtl_name, None) not in {
                                            key,
                                            None,
                                        }:
                                            if key[1] is None:
                                                tmp_ext = "_NONE"
                                            else:
                                                tmp_ext = "_%s" % name_compat(key[1])
                                            i = 0
                                            while mtl_rev_dict.get(
                                                mtl_name + tmp_ext, None
                                            ) not in {key, None}:
                                                i += 1
                                                tmp_ext = "_%3d" % i
                                            mtl_name += tmp_ext
                                        mat_data = mtl_dict[key] = (
                                            mtl_name,
                                            materials[f_mat],
                                        )
                                        mtl_rev_dict[mtl_name] = key

                                    if EXPORT_GROUP_BY_MAT:
                                        # can be mat_image or (null)
                                        if EXPORT_IGNORE_SO_GROUP_SETTINGS:
                                            fw("g SO%s_%s_%s" % (int(time.time()),obj_group_name_base,mat_data[0],))
                                        else:
                                            fw("g %s_%s" % (obj_group_name_base,mat_data[0],))

                                        fw(write_file_material_info(ob, material_names[f_mat], scene))

                                        fw("\n")
                                    if EXPORT_MTL:
                                        fw(
                                            "usemtl %s\n" % mat_data[0]
                                        )  # can be mat_image or (null)

                            contextMat = key

                            f_v = [
                                (vi, me_verts[v_idx], l_idx)
                                for vi, (v_idx, l_idx) in enumerate(
                                    zip(f.vertices, f.loop_indices)
                                )
                            ]

                            fw("f")
                            if faceuv:
                                if EXPORT_NORMALS:
                                    for vi, v, li in f_v:
                                        fw(
                                            " %d/%d/%d"
                                            % (
                                                totverts + v.index,
                                                totuvco + uv_face_mapping[f_index][vi],
                                                totno + loops_to_normals[li],
                                            )
                                        )  # vert, uv, normal
                                else:  # No Normals
                                    for vi, v, li in f_v:
                                        fw(
                                            " %d/%d"
                                            % (
                                                totverts + v.index,
                                                totuvco + uv_face_mapping[f_index][vi],
                                            )
                                        )  # vert, uv

                                face_vert_index += len(f_v)

                            else:  # No UV's
                                if EXPORT_NORMALS:
                                    for vi, v, li in f_v:
                                        fw(
                                            " %d//%d"
                                            % (
                                                totverts + v.index,
                                                totno + loops_to_normals[li],
                                            )
                                        )
                                else:  # No Normals
                                    for vi, v, li in f_v:
                                        fw(" %d" % (totverts + v.index))

                            fw("\n")

                            if vertex_colors_data is not None:
                                fw("fc")
                                for vi, v, li in f_v:
                                    fw(" %d" % (totvc + loops_to_colors[li]))
                                fw("\n")

                        subprogress2.step()

                        # Make the indices global rather then per mesh
                        totverts += len(me_verts)
                        totuvco += uv_unique_count
                        totno += no_unique_count
                        totvc += vc_unique_count

                        # clean up
                        ob_for_convert.to_mesh_clear()

                subprogress1.leave_substeps(
                    "Finished writing geometry of '%s'." % ob_main.name
                )
            subprogress1.leave_substeps()

        subprogress1.step("Finished exporting geometry, now exporting materials")

        # Now we have all our materials, save them
        if EXPORT_MTL:
            write_mtl(scene, mtlfilepath, EXPORT_PATH_MODE, copy_set, mtl_dict, EXPORT_COPY_TEXTURES)

        # copy all collected files.
        io_utils.path_reference_copy(copy_set)

def _write(
    context,
    filepath,
    EXPORT_NORMALS,  # ok
    EXPORT_VERTEX_COLORS,
    EXPORT_UV,  # ok
    EXPORT_MTL,
    EXPORT_APPLY_MODIFIERS,  # ok
    EXPORT_GROUP_BY_OB,
    EXPORT_GROUP_BY_MAT,
    EXPORT_GROUP_NAME_USE_COLLECTION,
    EXPORT_IGNORE_SO_GROUP_SETTINGS,
    EXPORT_KEEP_VERT_ORDER,
    EXPORT_POLYGROUPS,
    EXPORT_SEL_ONLY,  # ok
    EXPORT_GLOBAL_MATRIX,
    EXPORT_COPY_TEXTURES,
    EXPORT_PATH_MODE,  # Not used
):

    with ProgressReport(context.window_manager) as progress:
        depsgraph = context.evaluated_depsgraph_get()
        scene = context.scene

        # Exit edit mode before exporting, so current object states are exported properly.

        if bpy.ops.object.mode_set.poll():
            bpy.ops.object.mode_set(mode="OBJECT")

        if EXPORT_SEL_ONLY:
            objects = context.selected_objects
        else:
            objects = scene.objects

        # EXPORT THE FILE.
        progress.enter_substeps(1)
        write_file(
            filepath,
            objects,
            depsgraph,
            scene,
            EXPORT_NORMALS,
            EXPORT_VERTEX_COLORS,
            EXPORT_UV,
            EXPORT_MTL,
            EXPORT_APPLY_MODIFIERS,
            EXPORT_GROUP_BY_OB,
            EXPORT_GROUP_BY_MAT,
            EXPORT_GROUP_NAME_USE_COLLECTION,
            EXPORT_IGNORE_SO_GROUP_SETTINGS,
            EXPORT_KEEP_VERT_ORDER,
            EXPORT_POLYGROUPS,
            EXPORT_GLOBAL_MATRIX,
            EXPORT_COPY_TEXTURES,
            EXPORT_PATH_MODE,
            progress,
        )
        progress.leave_substeps()


def save(
    context,
    filepath,
    *,
    use_normals=False,
    use_vertex_colors=False,
    use_uvs=True,
    use_materials=True,
    use_mesh_modifiers=True,
    group_by_object=True,
    group_by_material=True,
    group_name_use_collection=True,
    ignore_SO_group_settings=False,
    keep_vertex_order=False,
    use_vertex_groups=False,
    use_selection=True,
    global_matrix=None,
    copy_textures=False,
    path_mode="AUTO",
    skip_dialog=False
):
    
    if path_mode == "AUTO":
        path_mode = "RELATIVE"

    _write(
        context,
        filepath,
        EXPORT_NORMALS=use_normals,
        EXPORT_VERTEX_COLORS=use_vertex_colors,
        EXPORT_UV=use_uvs,
        EXPORT_MTL=use_materials,
        EXPORT_APPLY_MODIFIERS=use_mesh_modifiers,
        EXPORT_GROUP_BY_OB=group_by_object,
        EXPORT_GROUP_BY_MAT=group_by_material,
        EXPORT_GROUP_NAME_USE_COLLECTION=group_name_use_collection,
        EXPORT_IGNORE_SO_GROUP_SETTINGS=ignore_SO_group_settings,
        EXPORT_KEEP_VERT_ORDER=keep_vertex_order,
        EXPORT_POLYGROUPS=use_vertex_groups,
        EXPORT_SEL_ONLY=use_selection,
        EXPORT_GLOBAL_MATRIX=global_matrix,
        EXPORT_COPY_TEXTURES=copy_textures,
        EXPORT_PATH_MODE=path_mode,
    )

    return {"FINISHED"}

@orientation_helper(axis_forward="-Z", axis_up="Y")
class ExportOBJ(bpy.types.Operator, ExportHelper):
    bl_idname = "export_obj_so.export"
    bl_label = "Export OBJ SO"
    bl_description = "Exports as SharpOcarina Object (.obj)"
    bl_options = {"PRESET"}

    filename_ext = ".obj"
    filter_glob: StringProperty(
        default="*.obj",
        options={"HIDDEN"},
    )

    skip_dialog: bpy.props.BoolProperty(default=False, options={"HIDDEN"})

    # context group
    use_selection: BoolProperty(
        name="Selection Only",
        description="Export selected objects only",
        default=False,
    )

    # object group
    use_mesh_modifiers: BoolProperty(
        name="Apply Modifiers",
        description="Apply modifiers",
        default=True,
    )
    # extra data group
    use_normals: BoolProperty(
        name="Write Normals",
        description="Export one normal per vertex and per face, to represent flat faces and sharp edges",
        default=True,
    )
    use_vertex_colors: BoolProperty(
        name="Write Vertex Colors",
        description="Export one color per vertex and per face, including vertex alpha",
        default=True,
    )
    use_uvs: BoolProperty(
        name="Include UVs",
        description="Write out the active UV coordinates",
        default=True,
    )
    use_materials: BoolProperty(
        name="Write Materials",
        description="Write out the MTL file",
        default=True,
    )
    use_vertex_groups: BoolProperty(
        name="Polygroups",
        description="",
        default=False,
    )

    # grouping group
    group_by_object: BoolProperty(
        name="OBJ Groups",
        description="Export Blender objects as OBJ groups",
        default=True,
    )
    group_by_material: BoolProperty(
        name="Material Groups",
        description="Generate an OBJ group for each part of a geometry using a different material",
        default=True,
    )
    group_name_use_collection: BoolProperty(
        name="Collection in Group Name",
        description="Put the collections the object belongs to in the OBJ group name",
        default=True,
    )
    ignore_SO_group_settings: BoolProperty(
        name="Ignore SO Group Settings",
        description="The changes made to the group settings in SO will be discarded on reloading this model",
        default=False,
    )
    keep_vertex_order: BoolProperty(
        name="Keep Vertex Order",
        description="",
        default=False,
    )
    copy_textures: BoolProperty(
        name="Copy Textures",
        description="",
        default=False,
    )

    global_scale: FloatProperty(
        name="Scale",
        min=0.01,
        max=1000.0,
        default=1.0,
    )

    path_mode: path_reference_mode

    check_extension = True

    def execute(self, context):

        from mathutils import Matrix

        keywords = self.as_keywords(
            ignore=(
                "axis_forward",
                "axis_up",
                "global_scale",
                "check_existing",
                "filter_glob",
            ),
        )

        global_matrix = (
            Matrix.Scale(self.global_scale, 4)
            @ axis_conversion(
                to_forward=self.axis_forward,
                to_up=self.axis_up,
            ).to_4x4()
        )

        keywords["global_matrix"] = global_matrix

        result = save(context, **keywords)

        # Save the chosen filepath
        context.scene.SO_last_export_path = bpy.path.relpath(self.filepath)

        return result

    def invoke(self, context, event):
        # If textbox already filled -> bypass file browser
        if self.skip_dialog and context.scene.SO_last_export_path:
            self.filepath = bpy.path.abspath(context.scene.SO_last_export_path)
            result = self.execute(context)
            self.report({'INFO'}, f"Exported to {self.filepath}")
            return result
        else:
            # No path stored yet -> open file browser as usual
            return ExportHelper.invoke(self, context, event)


    def draw(self, context):
        layout = self.layout
        layout.use_property_split = True
        layout.use_property_decorate = False  # No animation.

        sfile = context.space_data
        operator = sfile.active_operator

        layout.prop(operator, "global_scale")
        layout.prop(operator, "path_mode")
        layout.prop(operator, "copy_textures")
        layout.prop(operator, "group_by_material")
        layout.prop(operator, "group_name_use_collection")
        layout.prop(operator, "ignore_SO_group_settings")
        # pass

def menu_func_export(self, context):
    self.layout.operator(ExportOBJ.bl_idname, text="SharpOcarina Object (.obj)").skip_dialog = False

classes = (
    ExportOBJ,
)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)

    bpy.types.TOPBAR_MT_file_export.append(menu_func_export)

def unregister():
    bpy.types.TOPBAR_MT_file_export.remove(menu_func_export)

    for cls in classes:
        bpy.utils.unregister_class(cls)
