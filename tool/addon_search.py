import bpy
from bpy.app.handlers import persistent

from ..public import PublicPref

owner = object()


def msgbus_callback():
    PublicPref.pref_().addon_search = bpy.context.window_manager.addon_search


def msgbus():
    bpy.msgbus.subscribe_rna(
        key=(bpy.types.WindowManager, "addon_search"),
        owner=owner,
        args=(),
        notify=msgbus_callback,
    )


@persistent
def load_post(self, context):
    msgbus()


def addon_keys():
    """获取插件keys"""
    import addon_utils
    if bpy.app.version >= (4, 2, 0):
        return addon_utils.modules().mapping.keys()
    else:
        return [addon.__name__ for addon in addon_utils.modules()]


def set_addon_search():
    bpy.context.window_manager.addon_search = PublicPref.pref_().addon_search

    addon_show_expanded = PublicPref.pref_().addon_show_expanded
    expanded_list = [addon.name for addon in addon_show_expanded if addon.show_expanded]

    import addon_utils
    addon_utils.modules_refresh()
    for key in addon_keys():
        if key in expanded_list:
            bpy.ops.preferences.addon_expand(module=key)

    for area in bpy.context.screen.areas:
        area.tag_redraw()


def remember_expanded():
    addon_show_expanded = PublicPref.pref_().addon_show_expanded
    import addon_utils
    addon_utils.modules_refresh()
    for key, mod in addon_utils.modules().mapping.items():
        info = addon_utils.module_bl_info(mod)
        show_expanded = info.get("show_expanded", False)

        i = addon_show_expanded.get(key, None)
        if i is None:
            i = addon_show_expanded.add()
            i.name = key
        i.show_expanded = show_expanded
    bpy.ops.wm.save_userpref()


def register():
    msgbus()
    bpy.app.handlers.load_post.append(load_post)
    bpy.app.timers.register(set_addon_search, first_interval=1, persistent=True)


def unregister():
    bpy.msgbus.clear_by_owner(owner)
