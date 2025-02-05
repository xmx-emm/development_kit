import os

import bpy

from ..utils import get_pref


class UnlinkAllScript(bpy.types.Operator):
    bl_idname = "script.unlink_all"
    bl_label = "Unlink All Script"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        while bpy.data.texts:
            bpy.ops.text.unlink()
        return {"FINISHED"}


def draw_text_header(self, context):
    pref = get_pref()

    row = self.layout.row(align=True)

    text = context.space_data.text

    if text:
        if not text.library:
            row.prop(
                pref,
                "auto_reload_script",
                text="",
                toggle=True,
                icon="FILE_REFRESH")
            row.prop(
                pref,
                "auto_run_script",
                text="",
                toggle=True,
                icon="PLAY")

            path_file = text.filepath
            path_folder = os.path.dirname(path_file)

            row.operator("wm.path_open", text="", icon="FILE_SCRIPT").filepath = fr"{path_file}"
            row.operator("wm.path_open", text="", icon="FILE_FOLDER").filepath = fr"{path_folder}"

            alert_row = row.row(align=True)
            alert_row.alert = True
            alert_row.operator(UnlinkAllScript.bl_idname, text="", icon="PANEL_CLOSE")

            if pref.auto_reload_script and text and text.is_modified:
                # Judging whether the text has been modified through UI drawing
                pref.reload_script_number += 1
    else:
        row.label(text="Not Load or Select Script")


class AutoReloadScriptPreferences:
    def update_reload_script(self, context):
        text = context.space_data.text
        try:
            bpy.ops.text.reload()
            if self.auto_run_script:
                try:
                    bpy.ops.text.run_script()
                    print(f"Reload Script {text.name},and Run Script!!!")
                except Exception as e:
                    import traceback
                    traceback.print_exc()
                    traceback.print_stack()
                    print("Run Error!!", e.args)
        except Exception as e:
            print(f"Reload Script {text.name} Error,Perhaps this script does not exist", e.args)
            self.auto_reload_script = False

    reload_script_number: bpy.props.IntProperty(default=-1, update=update_reload_script)
    auto_run_script: bpy.props.BoolProperty(
        name="Auto Run Script",
        description="Auto run script switch, only when auto reload script is turned on can it run",
        options={"SKIP_SAVE"},
        default=False)

    auto_reload_script: bpy.props.BoolProperty(
        name="Auto Reload Script",
        description="Whether to automatically reload scripts",
        default=True,
    )


def register():
    bpy.utils.register_class(UnlinkAllScript)
    bpy.types.TEXT_HT_footer.prepend(draw_text_header)


def unregister():
    bpy.types.TEXT_HT_footer.remove(draw_text_header)
    bpy.utils.unregister_class(UnlinkAllScript)
