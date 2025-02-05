from . import (
    auto_reload_script,
    development_key,
    open_addon_script,
    remember_addon_expanded,
    remember_addon_search,
    restart_blender,
)

tool_mods = {
    auto_reload_script,
    development_key,
    open_addon_script,
    remember_addon_expanded,
    remember_addon_search,
    restart_blender,
}


def update_tool(unregister_all=False):
    from ..utils import get_pref
    pref = get_pref()

    for tool in tool_mods:
        name = "activate_" + tool.__name__.split(".")[-1]
        is_enable = getattr(pref, name, False)
        if unregister_all or (not is_enable):
            """
            It is necessary to ensure that the module will not encounter errors
            when calling unregister even if it is not registered
            """
            tool.unregister()
        elif is_enable:
            tool.register()


def update_by_tool_name(tool_name: str):
    """Change prop update tool"""

    def update(self, context):
        prop = getattr(self, f"activate_{tool_name}", None)
        for tool in tool_mods:
            name = tool.__name__.split(".")[-1]
            if name == tool_name:
                print("udpate_tool", name, tool)
                if prop:
                    tool.register()
                elif prop is False:
                    tool.unregister()
                return

    return update


def register():
    update_tool()


def unregister():
    update_tool(unregister_all=True)
