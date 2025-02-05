import platform

import bpy

from ..public import PublicClass


def start_blender():
    """Create a new Blender thread through subprocess"""
    import subprocess
    bpy.ops.wm.save_userpref()
    subprocess.Popen([bpy.app.binary_path])


class RestartBlender(bpy.types.Operator,
                     PublicClass):
    bl_idname = "wm.restart_blender"
    bl_label = "Restart Blender"
    bl_description = """
    Left                - Open a New Blender

    alt+Left         -Prompt to save file, Restart blender
    ctrl+Left        - Do not prompt to save files, Restart Blender
    shift+Left      - Open Tow Blender

    ctrl+alt+shift+Left Loop Open Blender, dedicated for explosion"""
    bl_options = {"REGISTER"}

    open_blender_number: bpy.props.IntProperty(
        name="Open Blender Number",
        default=20,
        max=114514,
        min=3,
        subtype="FACTOR"
    )

    @staticmethod
    def for_open(num):
        bpy.ops.wm.save_mainfile()
        for _ in range(num):
            start_blender()

    def run_cmd(self, event: bpy.types.Event):
        self.set_event_key(event)
        start_blender()
        if self.not_key:
            ...
        elif self.only_alt:
            bpy.ops.wm.window_close()
        elif self.only_ctrl:
            bpy.ops.wm.quit_blender()
        elif self.only_shift:
            start_blender()
            self.os.system(self.os)
        elif self.ctrl_shift_alt and event.oskey:
            self.for_open(20)  # blender必炸
        elif self.ctrl_shift_alt:
            self.for_open(self.open_blender_number)
        else:
            self.report({"INFO"}, self.bl_description)

    def invoke(self, context, event):
        if platform.system() == "Windows":
            self.run_cmd(event)
        elif platform.system() == "Linux":
            self.report({"INFO"}, "This feature currently does not support Linux systems")
        else:
            self.report({"INFO"}, "This feature currently does not support this system")
        return {"FINISHED"}


def draw_restart_blender_top_bar(self, context):
    row = self.layout.row(align=True)
    row.alert = True
    row.operator(
        operator=RestartBlender.bl_idname,
        text="",
        emboss=False,
        icon="QUIT"
    )


def register():
    bpy.utils.register_class(RestartBlender)
    if hasattr(bpy.types, "TOPBAR_MT_editor_menus"):
        bpy.types.TOPBAR_MT_editor_menus.append(draw_restart_blender_top_bar)


def unregister():
    bpy.utils.unregister_class(RestartBlender)
    if hasattr(bpy.types, "TOPBAR_MT_editor_menus"):
        bpy.types.TOPBAR_MT_editor_menus.remove(draw_restart_blender_top_bar)
