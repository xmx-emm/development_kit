import os
import platform

import bpy
from bpy.props import IntProperty
from bpy.types import Operator

from ..public import PublicClass


class RestartBlender(Operator,
                     PublicClass):
    bl_idname = 'wm.restart_blender'
    bl_label = 'Restart Blender'
    bl_description = '''
    Left                - Open a New Blender
    
    alt+Left         -Prompt to save file, Restart blender
    ctrl+Left        - Do not prompt to save files, Restart Blender
    shift+Left      - Open Tow Blender

    ctrl+alt+shift+Left Loop Open Blender, dedicated for explosion'''
    bl_options = {'REGISTER'}

    open_blender_number: IntProperty(name='Open Blender Number',
                                     default=20,
                                     max=114514,
                                     min=3,
                                     subtype='FACTOR')

    @staticmethod
    def for_open(num, cmd):
        bpy.ops.wm.save_mainfile()
        for _ in range(num):
            os.system(cmd)

    def run_cmd(self, event: bpy.types.Event):
        self.set_event_key(event)
        cmd = f'start {bpy.app.binary_path}'  # blender.exe path
        os.system(cmd)
        if self.not_key:
            # bpy.ops.wm.window_close()
            ...
        elif self.only_alt:
            bpy.ops.wm.window_close()
        elif self.only_ctrl:
            bpy.ops.wm.quit_blender()
        elif self.only_shift:
            os.system(cmd)
            self.os.system(self.os)
        elif self.ctrl_shift_alt and event.oskey:
            self.for_open(20, cmd)  # blender必炸
        elif self.ctrl_shift_alt:
            self.for_open(self.open_blender_number, cmd)
        else:
            self.report({'INFO'}, self.bl_description)

    def invoke(self, context, event):
        if platform.system() == 'Windows':
            self.run_cmd(event)
        elif platform.system() == 'Linux':
            print('This feature currently does not support Linux systems')
        else:
            print('This feature currently does not support this system')
        return {'FINISHED'}

    def draw_top_bar(self, context):
        layout = self.layout
        row = layout.row(align=True)
        a = row.row()
        a.alert = True
        a.operator(operator=RestartBlender.bl_idname,
                   text="", emboss=False, icon='QUIT')


register_class, unregister_class = bpy.utils.register_classes_factory(
    (
        RestartBlender,
    )
)


def register():
    register_class()
    if hasattr(bpy.types, 'TOPBAR_MT_editor_menus'):
        bpy.types.TOPBAR_MT_editor_menus.append(RestartBlender.draw_top_bar)  # 顶部标题栏


def unregister():
    unregister_class()
    if hasattr(bpy.types, 'TOPBAR_MT_editor_menus'):
        bpy.types.TOPBAR_MT_editor_menus.remove(RestartBlender.draw_top_bar)
