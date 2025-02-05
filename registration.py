from . import preferences
from . import tool
from . import translation
from .tool.remember_addon_expanded import restore_addons_expanded
from .tool.remember_addon_search import restore_addon_search
from .utils import clear_cache

DEVELOPMENT_KEY_MAPS = {
    "Window": [
        {"idname": "wm.window_fullscreen_toggle", "type": "SPACE", "value": "PRESS", "alt": True},
        {"idname": "wm.console_toggle", "type": "MIDDLEMOUSE", "value": "PRESS", "ctrl": True, "alt": True},
        {"idname": "wm.save_homefile", "type": "ACCENT_GRAVE", "value": "PRESS", "ctrl": True, "alt": True},
        {"idname": "wm.context_toggle", "type": "RIGHTMOUSE", "value": "PRESS", "ctrl": True, "alt": True,
         "properties": {"data_path": "preferences.view.use_translate_interface"}
         },
    ],
    "Screen": [
        {"idname": "screen.userpref_show", "type": "U", "value": "PRESS", "ctrl": True, "alt": True},
        {"idname": "screen.region_flip", "type": "RIGHTMOUSE", "value": "PRESS", "shift": True, "ctrl": True}
    ]
}


def register():
    clear_cache()
    preferences.register()
    tool.register()

    restore_addon_search()
    restore_addons_expanded()
    translation.register()


def unregister():
    clear_cache()
    tool.unregister()
    preferences.unregister()
    translation.unregister()
