import bpy.utils
from bpy.props import BoolProperty, IntProperty, StringProperty
from bpy.types import AddonPreferences

from .public import PublicClass
from .tool import (auto_reload_script,
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


def update_tool(un_register=False):
    pref = PublicClass.pref_()
    for prop_name, tool in tool_mod.items():
        is_enable = getattr(pref, prop_name, False)
        if un_register or (not is_enable):
            tool.unregister()
        elif is_enable:
            tool.register()


class ToolPreferences(AddonPreferences):
    bl_idname = __package__

    @staticmethod
    def update_by_tool_name(tool_name):
        """Change prop update tool"""

        def update(self, context):
            prop = getattr(self, tool_name, None)
            if prop:
                tool_mod[tool_name].register()
            elif prop is False:
                tool_mod[tool_name].unregister()

        return update

    fast_open_addon_code: BoolProperty(
        default=False,
        name='Feat Open Addon Script or Folder',
        description='Rewrite the drawing method of the addon section,'
                    ' and display it in the expansion of the addon',
        update=update_by_tool_name('fast_open_addon_code'), )
    restart_blender: BoolProperty(
        default=True,
        name='Restart Blender',
        description='Enabled Multiple Blender,or Restart Blender',
        update=update_by_tool_name('restart_blender'),
    )
    custom_key: BoolProperty(
        default=True,
        name='Development Key',
        description='alt+Space              Toggle Full Screen'
                    'ctrl+alt+MiddleMouse   Show Console'
                    'ctrl+alt+RightMouse    Switch User Translate Interface'
                    'ctrl+alt+AccentGrave   Save Home File',
        update=update_by_tool_name('custom_key'),
    )
    save_addon_search: BoolProperty(
        default=True,
        name='Save addon search',
        description='',
        update=update_by_tool_name('save_addon_search'),
    )
    addon_search: StringProperty()

    enabled_reload_script: BoolProperty(
        default=True,
        name='ReLoad Script Tool',
        description='',
        update=update_by_tool_name('enabled_reload_script'),
    )

    # Auto Reload
    def update_reload_script(self, context):
        text = context.space_data.text
        try:
            bpy.ops.text.reload()
            if self.auto_run_script:
                try:
                    bpy.ops.text.run_script()
                    print(f'Reload Script {text.name},and Run Script!!!')
                except Exception as e:
                    print('Run Error!!', e.args)
        except Exception as e:
            print(f'Reload Script {text.name} Error,Perhaps this script does not exist', e.args)
            self.auto_reload_script = False

    reload_script_number: IntProperty(default=True,
                                      update=update_reload_script)
    auto_run_script: BoolProperty(name='Auto run script switch, only when auto reload script is turned on can it run',
                                  options={'SKIP_SAVE'},
                                  default=False)

    auto_reload_script: BoolProperty(name="Whether to automatically reload scripts", default=True, )

    def draw(self, context):
        for i in ('fast_open_addon_code',
                  'enabled_reload_script',
                  'restart_blender',
                  'custom_key',
                  'save_addon_search',
                  ):
            self.layout.prop(self, i)


def register():
    bpy.utils.register_class(ToolPreferences)
    update_tool()


def unregister():
    bpy.utils.unregister_class(ToolPreferences)
    update_tool(un_register=True)
