from os.path import dirname

import bpy
from bpy.types import Operator, Text, TEXT_HT_footer

from ..public import PublicClass


class UnlinkText(Operator):
    bl_idname = 'script.unlink_all'
    bl_label = 'Unlink All Script'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        while bpy.data.texts:
            for text in bpy.data.texts:
                print(text.name)
                bpy.ops.text.unlink()
        return {'FINISHED'}


class ScriptingTools(Text):
    text: Text = None

    @classmethod
    def register(cls):
        TEXT_HT_footer.prepend(cls.draw_text_header)
        bpy.utils.register_class(UnlinkText)

    @classmethod
    def unregister(cls):
        TEXT_HT_footer.remove(cls.draw_text_header)
        bpy.utils.unregister_class(UnlinkText)

    def draw_text_header(self, context):
        pref = PublicClass.pref_()
        layout = self.layout
        text = context.space_data.text
        row = layout.row(align=True)
        if text:
            if not text.library:
                row.prop(pref, 'auto_reload_script',
                         text='',
                         toggle=True,
                         icon='FILE_REFRESH')
                row.prop(pref, 'auto_run_script',
                         text='',
                         toggle=True,
                         icon='PLAY')

                file_path = text.filepath
                folder_path = dirname(file_path)

                row.operator('wm.path_open', text='', icon='FILE_SCRIPT').filepath = fr'{file_path}'
                row.operator('wm.path_open', text='', icon='FILE_FOLDER').filepath = fr'{folder_path}'

                alert_row = row.row(align=True)
                alert_row.alert = True
                alert_row.operator(UnlinkText.bl_idname, text='', icon='PANEL_CLOSE')

                if pref.auto_reload_script and text and text.is_modified:
                    pref.reload_script_number += 1
        else:
            row.label(text='Not Load or Select Script')


def register():
    ScriptingTools.register()


def unregister():
    ScriptingTools.unregister()
