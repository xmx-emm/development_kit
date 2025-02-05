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
        name="ReLoad Script",
        description="Automatically reload scripts and run them",
        update=update_by_tool_name("auto_reload_script"),
    )

    activate_development_key: bpy.props.BoolProperty(
        default=True,
        name="Development Keymap",
        description="Commonly used Keymaps to speed up the development process",
        update=update_by_tool_name("development_key"),
    )

    activate_open_addon_script: bpy.props.BoolProperty(
        default=False,
        name="Addon Open",
        description="Rewrite the drawing method of the addon section, and display it in the expansion of the addon",
        update=update_by_tool_name("open_addon_script")
    )
    activate_remember_addon_expanded: bpy.props.BoolProperty(
        default=True,
        name="Remember addon expanded",
        description="Record the expanded Addon and restore it the next time you open Blender",
        update=update_by_tool_name("remember_addon_expanded"),
    )

    activate_remember_addon_search: bpy.props.BoolProperty(
        default=True,
        name="Remember addon search",
        description="Record the Addon search and restore it the next time you start Blender",
        update=update_by_tool_name("remember_addon_search"),
    )

    activate_restart_blender: bpy.props.BoolProperty(
        default=True,
        name="Restart Blender",
        description="Enable multiple Blenders or restart Blender, please be careful to save the edit file!!!!",
        update=update_by_tool_name("restart_blender"),
    )

    # Other Property
    addon_show_expanded: bpy.props.CollectionProperty(type=ShowExpandedItem)
    addon_search: bpy.props.StringProperty(default="")

    def draw(self, context):
        from .keymap import draw_key

        column = self.layout.column(align=True)
        for prop in self.bl_rna.properties:
            if prop.identifier.startswith("activate_"):
                self.draw_prop(column, prop.identifier)

        if self.activate_development_key:
            column.separator()
            col = column.box().column(align=True)
            col.label(text="Keymap")
            draw_key(col)

    def draw_prop(self, layout, identifier) -> None:
        split = layout.row(align=True).split(factor=.2, align=True)
        prop = self.bl_rna.properties[identifier]
        split.prop(self, identifier, toggle=True, expand=True)
        split.label(text=prop.description)


def register():
    bpy.utils.register_class(ShowExpandedItem)
    bpy.utils.register_class(ToolPreferences)


def unregister():
    bpy.utils.unregister_class(ToolPreferences)
    bpy.utils.unregister_class(ShowExpandedItem)
