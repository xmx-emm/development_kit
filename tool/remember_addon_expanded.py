import bpy

from ..utils import get_pref, addon_keys


def remember_addons_expanded():
    pref = get_pref()

    import addon_utils
    addon_utils.modules_refresh()

    addon_show_expanded = pref.addon_show_expanded

    for key, mod in addon_utils.modules().mapping.items():
        info = addon_utils.module_bl_info(mod)
        show_expanded = info.get("show_expanded", False)

        item = addon_show_expanded.get(key, None)
        if item is None:
            item = addon_show_expanded.add()
            item.name = key
        item.show_expanded = show_expanded

    bpy.ops.wm.save_userpref()


def restore_addons_expanded():
    def restore():
        pref = get_pref()

        if pref.activate_remember_addon_expanded:
            expanded_list = [addon.name for addon in pref.addon_show_expanded if addon.show_expanded]

            import addon_utils
            addon_utils.modules_refresh()
            for key in addon_keys():
                if key in expanded_list:
                    bpy.ops.preferences.addon_expand(module=key)

    bpy.app.timers.register(restore, first_interval=1, persistent=True)


def register():
    ...


def unregister():
    remember_addons_expanded()
