from . import registration
bl_info = {
    "name": "Development Kit Tool",
    "version": (1, 0, 2),
    "blender": (4, 0, 0),
    "location": "All over the place",
    "support": "COMMUNITY",
    "description": "Blender development tool, used to improve development efficiency",
    "warning": "",
    "category": "Development",
}


def register():
    registration.register()


def unregister():
    registration.unregister()
