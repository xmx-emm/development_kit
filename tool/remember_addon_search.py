import bpy
from bpy.app.handlers import persistent

from ..utils import get_pref, tag_redraw

owner = object()


def remember_addon_search():
    """if bpy.context.window_manager.addon_search change then call remember"""
    get_pref().addon_search = bpy.context.window_manager.addon_search


def restore_addon_search():
    """delayed set addon search property"""
    pref = get_pref()

    def restore():
        bpy.context.window_manager.addon_search = pref.addon_search
        tag_redraw()

    if pref.activate_remember_addon_search:
        bpy.app.timers.register(restore, first_interval=1, persistent=True)


def addon_search_msgbus():
    """msgbus wm addon search"""
    bpy.msgbus.subscribe_rna(
        key=(bpy.types.WindowManager, "addon_search"),
        owner=owner,
        args=(),
        notify=remember_addon_search,
    )


@persistent
def load_post_handler(self, context):
    """if load file reregister msgbus 避免丢失监听"""
    addon_search_msgbus()


def register():
    addon_search_msgbus()

    bpy.app.handlers.load_post.append(load_post_handler)


def unregister():
    bpy.msgbus.clear_by_owner(owner)
