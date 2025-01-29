from . import preferences, public
from .tool.addon_search import remember_expanded

bl_info = {
    "name": "Development Kit Tool",
    "version": (1, 0, 1),
    "blender": (4, 0, 0),
    "location": "All over the place",
    "support": "COMMUNITY",
    "description": "Blender development tool, used to improve development efficiency",
    "warning": "",
    "category": "Development",
}


def register():
    public.PublicClass.clear_cache()
    preferences.register()


def unregister():
    remember_expanded()
    public.PublicClass.clear_cache()
    preferences.unregister()
