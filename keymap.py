import bpy

from mathutils import Vector, Euler, Matrix


def get_keymap(keymap_name) -> "bpy.types.KeyMap":
    kc = bpy.context.window_manager.keyconfigs
    addon = kc.addon
    keymap = kc.default.keymaps.get(keymap_name, None)
    return addon.keymaps.new(
        keymap_name,
        space_type=keymap.space_type,
        region_type=keymap.region_type
    )


def get_kmi_operator_properties(kmi: 'bpy.types.KeyMapItem') -> dict:
    """获取kmi操作符的属性"""
    properties = kmi.properties
    prop_keys = dict(properties.items()).keys()
    dictionary = {i: getattr(properties, i, None) for i in prop_keys}
    del_key = []
    for item in dictionary:
        prop = getattr(properties, item, None)
        typ = type(prop)
        if prop:
            if typ == Vector:
                # 属性阵列-浮点数组
                dictionary[item] = dictionary[item].to_tuple()
            elif typ == Euler:
                dictionary[item] = dictionary[item][:]
            elif typ == Matrix:
                dictionary[item] = tuple(i[:] for i in dictionary[item])
            elif typ == bpy.types.bpy_prop_array:
                dictionary[item] = dictionary[item][:]
            elif typ in (str, bool, float, int, set, list, tuple):
                ...
            elif typ.__name__ in [
                'TRANSFORM_OT_shrink_fatten',
                'TRANSFORM_OT_translate',
                'TRANSFORM_OT_edge_slide',
                'NLA_OT_duplicate',
                'ACTION_OT_duplicate',
                'GRAPH_OT_duplicate',
                'TRANSFORM_OT_translate',
                'OBJECT_OT_duplicate',
                'MESH_OT_loopcut',
                'MESH_OT_rip_edge',
                'MESH_OT_rip',
                'MESH_OT_duplicate',
                'MESH_OT_offset_edge_loops',
                'MESH_OT_extrude_faces_indiv',
            ]:  # 一些奇怪的操作符属性,不太好解析也用不上
                ...
                del_key.append(item)
            else:
                print('emm 未知属性,', typ, dictionary[item])
                del_key.append(item)
    for i in del_key:
        dictionary.pop(i)
    return dictionary


def draw_key(layout: bpy.types.UILayout):
    """在偏好设置绘制插件快捷键"""
    import rna_keymap_ui
    from .tool.development_key import register_keymap_items

    kc = bpy.context.window_manager.keyconfigs.user

    for km, kmi in register_keymap_items:
        kmm = kc.keymaps.get(km.name)
        if kmm:
            is_find = False
            for kmii in kmm.keymap_items:
                if kmi.idname == kmii.idname:
                    if get_kmi_operator_properties(kmi) == get_kmi_operator_properties(kmii):
                        col = layout.column(align=True)
                        if (not kmii.is_user_defined) and kmii.is_user_modified:
                            col.context_pointer_set("keymap", kmm)
                        is_find = True
                        rna_keymap_ui.draw_kmi(["ADDON", "USER", "DEFAULT"], kc, kmm, kmii, col, 0)
                        break  # 找到了,但有可能会找到多个
            if not is_find:
                column = layout.column(align=True)
                column.label(text="Not Found Keymap, Please check the shortcut keys that have been changed")
