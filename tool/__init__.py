from . import (auto_reload_script,
               custom_key,
               fast_open_addon_code,
               restart_blender,
               addon_search,
               )

tool_mod = {'fast_open_addon_code': fast_open_addon_code,
            'enabled_reload_script': auto_reload_script,
            'restart_blender': restart_blender,
            'custom_key': custom_key,
            'save_addon_search': addon_search
            }
from ..utils import get_pref


def update_tool(un_register=False):
    pref = get_pref()
    for prop_name, tool in tool_mod.items():
        is_enable = getattr(pref, prop_name, False)
        if un_register or (not is_enable):
            tool.unregister()
        elif is_enable:
            tool.register()


def update_by_tool_name(tool_name: str) -> function:
    """Change prop update tool"""

    def update(self, context):
        prop = getattr(self, tool_name, None)
        if prop:
            tool_mod[tool_name].register()
        elif prop is False:
            tool_mod[tool_name].unregister()

    return update


def register():
    ...


def unregister():
    ...
