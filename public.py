import os
from functools import cache

import bpy


def get_pref():
    return bpy.context.preferences.addons[__package__].preferences


class PublicEvent:
    not_key: bool
    only_ctrl: bool
    only_alt: bool
    only_shift: bool
    shift_alt: bool
    ctrl_alt: bool
    ctrl_shift: bool
    ctrl_shift_alt: bool

    @staticmethod
    def get_event_key(event):
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

    def set_event_key(self, event):
        self.not_key, self.only_ctrl, self.only_alt, self.only_shift, self.shift_alt, self.ctrl_alt, self.ctrl_shift, self.ctrl_shift_alt = \
            self.get_event_key(event)


class PublicPref:

    @staticmethod
    @cache
    def pref_():
        return get_pref()

    @property
    def pref(self):
        return self.pref_()


class PublicClass(PublicEvent,
                  PublicPref,
                  ):

    @staticmethod
    def clear_cache():
        PublicClass.pref_.cache_clear()

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
                p for p in (
                    *[os.path.join(pref_p, "addons") for pref_p in bpy.utils.script_paths_pref()],
                    bpy.utils.user_resource('SCRIPTS', path="addons"),
                )
                if p
            )
        elif bpy.app.version >= (2, 94, 0):  # 3.0 version
            addon_user_dirs = tuple(
                p for p in (
                    os.path.join(bpy.context.preferences.filepaths.script_directory, "addons"),
                    bpy.utils.user_resource('SCRIPTS', path="addons"),
                )
                if p
            )
        else:  # 2.93 version
            addon_user_dirs = tuple(
                p for p in (
                    os.path.join(bpy.context.preferences.filepaths.script_directory, "addons"),
                    bpy.utils.user_resource('SCRIPTS', "addons"),
                )
                if p
            )
        return addon_user_dirs
