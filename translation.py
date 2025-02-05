import ast
import re

import bpy

zh_HANS = {
    "Automatically reload scripts and run them": "自动重载脚本并运行",
    "ReLoad Script": "重载脚本",
    "Development Keymap": "开发快捷键",
    "Commonly used Keymaps to speed up the development process": "常用可以加快开发流程的快捷键",
    "Addon Open": "打开插件",
    "Rewrite the drawing method of the addon section, and display it in the expansion of the addon": "重写插件部分的绘制方法,并在插件的扩展是显示打开脚本文件与文件夹按钮",
    "Remember addon expanded": "记住插件展开",
    "Record the expanded Addon and restore it the next time you open Blender": "将已展开的插件记录下来,在下次打开Blender时恢复",
    "Remember addon search": "记住插件搜索",
    "Record the Addon search and restore it the next time you start Blender": "将插件搜索记录下来,在下次启动Blender时恢复",
    "Restart Blender": "重启Blender",
    "Enable multiple Blenders or restart Blender, please be careful to save the edit file!!!!": "启用多个Blender或重启Blender,请注意保存编辑文件!!!!",
    "Keymap": "快捷键",
    "Click           Open a New Blender": "左键         打开一个新的Blender",
    "Alt         Prompt to save file, Restart Blender": "Alt          提示保存文件,重启Blender",
    "Ctrl         Do not prompt to save files, Restart Blender": "Ctrl         不提示保存文件,重启Blender",
    "Shift       Open Tow Blender": "Shift       打开两个Blender",
    "Ctrl+Alt+Shift Loop Open Blender, dedicated for explosion": "Ctrl+Alt+Shift 循环打开Blender,爆炸专用",
}


def translate_lines_text(*args, split="\n"):
    from bpy.app.translations import pgettext_iface
    return split.join([pgettext_iface(line) for line in args])


def get_language_list() -> list:
    """
    Traceback (most recent call last):
  File "<blender_console>", line 1, in <module>
TypeError: bpy_struct: item.attr = val: enum "a" not found in ("DEFAULT", "en_US", "es", "ja_JP", "sk_SK", "vi_VN", "zh_HANS", "ar_EG", "de_DE", "fr_FR", "it_IT", "ko_KR", "pt_BR", "pt_PT", "ru_RU", "uk_UA", "zh_TW", "ab", "ca_AD", "cs_CZ", "eo", "eu_EU", "fa_IR", "ha", "he_IL", "hi_IN", "hr_HR", "hu_HU", "id_ID", "ky_KG", "nl_NL", "pl_PL", "sr_RS", "sr_RS@latin", "sv_SE", "th_TH", "tr_TR")
    """
    try:
        bpy.context.preferences.view.language = ""
    except TypeError as e:
        matches = re.findall(r"\(([^()]*)\)", e.args[-1])
        return ast.literal_eval(f"({matches[-1]})")


class TranslationHelper:
    def __init__(self, name: str, data: dict, lang='zh_CN'):
        self.name = name
        self.translations_dict = dict()

        for src, src_trans in data.items():
            key = ("Operator", src)
            self.translations_dict.setdefault(lang, {})[key] = src_trans
            key = ("*", src)
            self.translations_dict.setdefault(lang, {})[key] = src_trans
            key = (name, src)
            self.translations_dict.setdefault(lang, {})[key] = src_trans

    def register(self):
        try:
            bpy.app.translations.register(self.name, self.translations_dict)
        except(ValueError):
            pass

    def unregister(self):
        bpy.app.translations.unregister(self.name)


# Set
############

all_language = get_language_list()

zh_CN = None


def register():
    global zh_CN

    language = "zh_CN"
    if language not in all_language:
        if language in ("zh_CN", "zh_HANS"):
            if "zh_CN" in all_language:
                language = "zh_CN"
            elif "zh_HANS" in all_language:
                language = "zh_HANS"
    zh_CN = TranslationHelper('development_kit_zh_CN', zh_HANS, lang=language)
    zh_CN.register()


def unregister():
    zh_CN.unregister()
