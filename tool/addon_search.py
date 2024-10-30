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
    bpy.context.window_manager.addon_search = "test"


@persistent
def load_post(self, context):
    msgbus()


def set_addon_search():
    bpy.context.window_manager.addon_search = PublicPref.pref_().addon_search


def register():
    msgbus()
    bpy.app.handlers.load_post.append(load_post)
    bpy.app.timers.register(set_addon_search, first_interval=1)


def unregister():
    bpy.msgbus.clear_by_owner(owner)
