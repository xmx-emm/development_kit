import bpy

from ..public import PublicClass


def set_key():
    pref = bpy.context.window_manager.keyconfigs['Blender'].preferences
    pref.use_select_all_toggle = True  # 使用全选切换
    pref.use_alt_click_leader = True  # 使用ALT点击工具提示
    pref.use_pie_click_drag = True  # 拖动显示饼菜单
    pref.use_use_v3d_shade_ex_pie = True  # 额外着色饼菜单
    pref.use_use_v3d_tab_menu = True  # 饼菜单选项卡
    pref.use_file_single_click = True  # 饼菜单选项卡
    pref.spacebar_action = 'TOOL'


def set_m3_prop():
    if PublicClass.get_addon_is_enabled('MACHIN3tools'):
        print('MACHIN3tools')
        m3 = PublicClass.get_addon_is_enabled('MACHIN3tools')
        tool_list = [
            'activate_smart_vert',
            'activate_smart_edge',
            'activate_smart_face',
            'activate_clean_up',
            'activate_clipping_toggle',
            'activate_align',
            'activate_apply',
            'activate_select',
            'activate_mesh_cut',
            'activate_surface_slide',
            'activate_filebrowser_tools',
            'activate_smart_drive',
            'activate_unity',
            'activate_material_picker',
            'activate_group',
            'activate_thread',
            'activate_spin',
            'activate_smooth',
            'activate_save_pie',
            'activate_shading_pie',
            'activate_views_pie',
            'activate_align_pie',
            'activate_cursor_pie',
            'activate_transform_pie',
            'activate_snapping_pie',
            'activate_collections_pie',
            'activate_workspace_pie',

            # 'activate_mirror',
            # 'activate_tools_pie',
            # 'activate_customize',
            # 'activate_focus',
            # 'activate_modes_pie',

            'snap_show_absolute_grid',
            'cursor_show_to_grid',
        ]
        m3_pref = 'bpy.context.preferences.addons["MACHIN3tools"].preferences'

        for i in tool_list:
            if hasattr(m3, i) and (not eval(f'{m3_pref}.{i}')):
                exec(f'{m3_pref}.{i} = {True}', )
        m3.cursor_set_transform_preset = False


class CustomKey:
    KEY_MAPS = {
        'Window': [
            {'idname': 'wm.window_fullscreen_toggle', 'type': 'SPACE', 'value': 'PRESS', 'alt': True},
            {'idname': 'wm.console_toggle', 'type': 'MIDDLEMOUSE', 'value': 'PRESS', 'ctrl': True, 'alt': True},
            {'idname': 'wm.save_homefile', 'type': 'ACCENT_GRAVE', 'value': 'PRESS', 'ctrl': True, 'alt': True},
            {'idname': 'wm.context_toggle',
             'type': 'RIGHTMOUSE',
             'value': 'PRESS',
             'ctrl': True,
             'alt': True,
             'properties': [
                 ('data_path', 'preferences.view.use_translate_interface'),
             ]
             },
        ],
        'Screen': [
            {'idname': 'screen.userpref_show', 'type': 'U', 'value': 'PRESS', 'ctrl': True, 'alt': True},
            {'idname': 'screen.region_flip', 'type': 'RIGHTMOUSE', 'value': 'PRESS', 'shift': True, 'ctrl': True}
        ]
    }
    register_keymap_items = []

    @classmethod
    def get_keymap(cls, keymap_name):
        k = bpy.context.window_manager.keyconfigs
        addon = k.addon
        a = k.active.keymaps.get(keymap_name, None)
        return addon.keymaps.new(
            keymap_name,
            space_type=a.space_type,
            region_type=a.region_type
        )

    @classmethod
    def register(cls):
        for keymap_name, keymap_items in cls.KEY_MAPS.items():
            km = cls.get_keymap(keymap_name)
            for item in keymap_items:

                idname = item.get("idname")
                key_type = item.get("type")
                value = item.get("value")

                shift = item.get("shift", False)
                ctrl = item.get("ctrl", False)
                alt = item.get("alt", False)

                kmi = km.keymap_items.new(idname, key_type, value, shift=shift, ctrl=ctrl, alt=alt)

                if kmi:
                    properties = item.get("properties")

                    if properties:
                        for name, value in properties:
                            setattr(kmi.properties, name, value)
                cls.register_keymap_items.append((km, kmi))

    @classmethod
    def unregister(cls):
        for keymap, kmi in cls.register_keymap_items:
            try:
                keymap.keymap_items.remove(kmi)
            except ReferenceError as r:
                print(r)
        cls.register_keymap_items.clear()


def register():
    CustomKey.register()


def unregister():
    CustomKey.unregister()
