import bpy.utils
from bpy.props import BoolProperty, StringProperty, CollectionProperty
from bpy.types import AddonPreferences

from .tool import update_by_tool_name
from .tool.auto_reload_script import AutoReloadScriptPreferences


class ShowExpandedItem(bpy.types.PropertyGroup):
    """Used to record the expansion status of the addon"""
    show_expanded: BoolProperty(default=False)


class ToolPreferences(AddonPreferences, AutoReloadScriptPreferences):
    bl_idname = __package__

    fast_open_addon_code: BoolProperty(
        default=False,
        name="Feat Open Addon Script or Folder",
        description="Rewrite the drawing method of the addon section,"
                    " and display it in the expansion of the addon",
        update=update_by_tool_name("fast_open_addon_code"))
    restart_blender: BoolProperty(
        default=True,
        name="Restart Blender",
        description="Enabled Multiple Blender,or Restart Blender",
        update=update_by_tool_name("restart_blender"),
    )
    custom_key: BoolProperty(
        default=True,
        name="Development Key",
        description="alt+Space              Toggle Full Screen"
                    "ctrl+alt+MiddleMouse   Show Console"
                    "ctrl+alt+RightMouse    Switch User Translate Interface"
                    "ctrl+alt+AccentGrave   Save Home File",
        update=update_by_tool_name("custom_key"),
    )
    save_addon_search: BoolProperty(
        default=True,
        name="Save addon search",
        description="",
        update=update_by_tool_name("save_addon_search"),
    )
    addon_search: StringProperty()

    enabled_reload_script: BoolProperty(
        default=True,
        name="ReLoad Script Tool",
        description="",
        update=update_by_tool_name("enabled_reload_script"),
    )

    addon_show_expanded: CollectionProperty(type=ShowExpandedItem)

    def draw(self, context):
        for i in ("fast_open_addon_code",
                  "enabled_reload_script",
                  "restart_blender",
                  "custom_key",
                  "save_addon_search",
                  ):
            self.layout.prop(self, i)


def register():
    bpy.utils.register_class(ShowExpandedItem)
    bpy.utils.register_class(ToolPreferences)


def unregister():
    bpy.utils.unregister_class(ToolPreferences)
    bpy.utils.unregister_class(ShowExpandedItem)
