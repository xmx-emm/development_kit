import bpy

from .tool import update_by_tool_name
from .tool.auto_reload_script import AutoReloadScriptPreferences


class ShowExpandedItem(bpy.types.PropertyGroup):
    """Used to record the expansion status of the addon"""
    show_expanded: bpy.props.BoolProperty(default=False)


class ToolPreferences(bpy.types.AddonPreferences, AutoReloadScriptPreferences):
    bl_idname = __package__

    activate_auto_reload_script: bpy.props.BoolProperty(
        default=True,
        name="ReLoad Script Tool",
        description="",
        update=update_by_tool_name("auto_reload_script"),
    )

    activate_development_key: bpy.props.BoolProperty(
        default=True,
        name="Development Key",
        description="alt+Space              Toggle Full Screen"
                    "ctrl+alt+MiddleMouse   Show Console"
                    "ctrl+alt+RightMouse    Switch User Translate Interface"
                    "ctrl+alt+AccentGrave   Save Home File",
        update=update_by_tool_name("development_key"),
    )

    activate_open_addon_script: bpy.props.BoolProperty(
        default=False,
        name="Feat Open Addon Script or Folder",
        description="Rewrite the drawing method of the addon section,"
                    " and display it in the expansion of the addon",
        update=update_by_tool_name("open_addon_script")
    )
    activate_remember_addon_expanded: bpy.props.BoolProperty(
        default=True,
        name="Remember addon expanded",
        description="",
        update=update_by_tool_name("remember_addon_expanded"),
    )

    activate_remember_addon_search: bpy.props.BoolProperty(
        default=True,
        name="Remember addon search",
        description="",
        update=update_by_tool_name("remember_addon_search"),
    )

    activate_restart_blender: bpy.props.BoolProperty(
        default=True,
        name="Restart Blender",
        description="Enabled Multiple Blender,or Restart Blender",
        update=update_by_tool_name("restart_blender"),
    )

    # Other Property
    addon_show_expanded: bpy.props.CollectionProperty(type=ShowExpandedItem)
    addon_search: bpy.props.StringProperty(default="")

    def draw(self, context):
        column = self.layout.column(align=True)
        for prop in self.bl_rna.properties:
            if prop.identifier.startswith("activate_"):
                column.prop(self, prop.identifier)


def register():
    bpy.utils.register_class(ShowExpandedItem)
    bpy.utils.register_class(ToolPreferences)


def unregister():
    bpy.utils.unregister_class(ToolPreferences)
    bpy.utils.unregister_class(ShowExpandedItem)
