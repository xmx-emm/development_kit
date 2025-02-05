import os
from functools import cache

import bpy


@cache
def get_pref():
    return bpy.context.preferences.addons[__package__].preferences


def get_event_key(event: bpy.types.Event):
    alt = event.alt
    shift = event.shift
    ctrl = event.ctrl

    not_key = ((not ctrl) and (not alt) and (not shift))

    only_ctrl = (ctrl and (not alt) and (not shift))
    only_alt = ((not ctrl) and alt and (not shift))
    only_shift = ((not ctrl) and (not alt) and shift)

    shift_alt = ((not ctrl) and alt and shift)
    ctrl_alt = (ctrl and alt and (not shift))

    ctrl_shift = (ctrl and (not alt) and shift)
    ctrl_shift_alt = (ctrl and alt and shift)
    return not_key, only_ctrl, only_alt, only_shift, shift_alt, ctrl_alt, ctrl_shift, ctrl_shift_alt


def get_keymap(keymap_name) -> "bpy.types.KeyMap":
    kc = bpy.context.window_manager.keyconfigs
    addon = kc.addon
    keymap = kc.default.keymaps.get(keymap_name, None)
    return addon.keymaps.new(
        keymap_name,
        space_type=keymap.space_type,
        region_type=keymap.region_type
    )


def tag_redraw():
    for area in bpy.context.screen.areas:
        area.tag_redraw()


def addon_keys() -> "[str]":
    """获取插件所有id"""
    import addon_utils
    if bpy.app.version >= (4, 2, 0):
        return addon_utils.modules().mapping.keys()
    else:
        return [addon.__name__ for addon in addon_utils.modules()]


def clear_cache():
    get_pref.cache_clear()


class PublicEvent:
    not_key: bool
    only_ctrl: bool
    only_alt: bool
    only_shift: bool
    shift_alt: bool
    ctrl_alt: bool
    ctrl_shift: bool
    ctrl_shift_alt: bool

    def set_event_key(self, event):
        self.not_key, self.only_ctrl, self.only_alt, self.only_shift, self.shift_alt, self.ctrl_alt, self.ctrl_shift, self.ctrl_shift_alt = \
            self.get_event_key(event)


class PublicClass(
    PublicEvent,
    PublicPref,
):

    @property
    def pref(self):
        return get_pref()

    @staticmethod
    def get_addon_is_enabled(module_name, rsc_type=None):
        if rsc_type is None:
            return module_name in {ext.module for ext in bpy.context.preferences.addons}
        elif rsc_type == 'str':
            return f"'{module_name}'" + " in {ext.module for ext in bpy.context.preferences.addons}"

    @staticmethod
    def get_addon_user_dirs():
        version = bpy.app.version
        if version >= (3, 6, 0):  # 4.0以上
            addon_user_dirs = tuple(
                i for i in (
                    *[os.path.join(pref_p, "addons") for pref_p in bpy.utils.script_paths_pref()],
                    bpy.utils.user_resource('SCRIPTS', path="addons"),
                )
                if i
            )
        elif bpy.app.version >= (2, 94, 0):  # 3.0 version
            addon_user_dirs = tuple(
                i for i in (
                    os.path.join(bpy.context.preferences.filepaths.script_directory, "addons"),
                    bpy.utils.user_resource('SCRIPTS', path="addons"),
                )
                if i
            )
        else:  # 2.93 version
            addon_user_dirs = tuple(
                i for i in (
                    os.path.join(bpy.context.preferences.filepaths.script_directory, "addons"),
                    bpy.utils.user_resource('SCRIPTS', "addons"),
                )
                if i
            )
        return addon_user_dirs
