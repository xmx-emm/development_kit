import os

"""TODO
This feature seems to be unused and will not be used temporarily
And as Blender iterates, unpredictable errors may occur
"""

import addon_utils
import bpy
from bl_ui.space_userpref import USERPREF_PT_addons

from ..utils import get_addon_user_dirs


def draw_addon_add_item(layout, user_addon, mod):
    row = layout.row(align=True)
    # 添加打开文件夹按钮
    if user_addon:
        row.operator(
            "preferences.addon_remove", text="Remove", icon='CANCEL',
        ).module = mod.__name__
    row.alert = True
    row.operator('wm.path_open',
                 text='Open Script').filepath = mod.__file__
    folder_path, file_path = os.path.split(mod.__file__)
    row.operator('wm.path_open', icon='FILEBROWSER',
                 text='').filepath = folder_path


def draw_addon_4_1_or_below(self, context):
    layout = self.layout

    wm = context.window_manager
    prefs = context.preferences
    used_ext = {ext.module for ext in prefs.addons}

    addon_user_dirs = get_addon_user_dirs()
    # Development option for 2.8x, don't show users bundled addons
    # unless they have been updated for 2.8x.
    # Developers can turn them on with '--debug'
    show_official_27x_addons = bpy.app.debug

    # collect the categories that can be filtered on
    addons = [
        (mod, addon_utils.module_bl_info(mod))
        for mod in addon_utils.modules(refresh=False)
    ]

    split = layout.split(factor=0.6)

    row = split.row()
    row.prop(wm, "addon_support", expand=True)

    row = split.row(align=True)
    row.operator("preferences.addon_install",
                 icon='IMPORT', text="Install...")
    row.operator("preferences.addon_refresh",
                 icon='FILE_REFRESH', text="Refresh")

    row = layout.row()
    row.prop(prefs.view, "show_addons_enabled_only")
    row.prop(wm, "addon_filter", text="")
    row.prop(wm, "addon_search", text="", icon='VIEWZOOM')

    col = layout.column()

    # set in addon_utils.modules_refresh()
    if addon_utils.error_duplicates:
        box = col.box()
        row = box.row()
        row.label(text="Multiple add-ons with the same name found!")
        row.label(icon='ERROR')
        box.label(text="Delete one of each pair to resolve:")
        for (addon_name, addon_file, addon_path) in addon_utils.error_duplicates:
            box.separator()
            sub_col = box.column(align=True)
            sub_col.label(text=addon_name + ":")
            sub_col.label(text="    " + addon_file)
            sub_col.label(text="    " + addon_path)

    if addon_utils.error_encoding:
        self.draw_error(
            col,
            "One or more addons do not have UTF-8 encoding\n"
            "(see console for details)",
        )

    show_enabled_only = prefs.view.show_addons_enabled_only
    addon_filter = wm.addon_filter
    search = wm.addon_search.lower()
    support = wm.addon_support

    # initialized on demand
    user_addon_paths = []

    for mod, info in addons:
        module_name = mod.__name__

        is_enabled = module_name in used_ext

        if info["support"] not in support:
            continue

        # check if addon should be visible with current filters
        is_visible = (
                (addon_filter == "All") or
                (addon_filter == info["category"]) or
                (addon_filter == "User" and (mod.__file__.startswith(addon_user_dirs)))
        )
        if show_enabled_only:
            is_visible = is_visible and is_enabled

        if is_visible:
            if search and not (
                    (search in info["name"].lower()) or
                    (info["author"] and (search in info["author"].lower())) or
                    ((addon_filter == "All") and (
                            search in info["category"].lower()))
            ):
                continue

            # Skip 2.7x add-ons included with Blender, unless in debug mode.
            is_addon_27x = info.get("blender", (0,)) < (2, 80)
            if (
                    is_addon_27x and
                    (not show_official_27x_addons) and
                    (not mod.__file__.startswith(addon_user_dirs))
            ):
                continue

            # Addon UI Code
            col_box = col.column()
            box = col_box.box()
            colsub = box.column()
            row = colsub.row(align=True)

            row.operator(
                "preferences.addon_expand",
                icon='DISCLOSURE_TRI_DOWN' if info["show_expanded"] else 'DISCLOSURE_TRI_RIGHT',
                emboss=False,
            ).module = module_name

            row.operator(
                "preferences.addon_disable" if is_enabled else "preferences.addon_enable",
                icon='CHECKBOX_HLT' if is_enabled else 'CHECKBOX_DEHLT', text="",
                emboss=False,
            ).module = module_name

            sub = row.row()
            sub.active = is_enabled
            sub.label(text="%s: %s" % (info["category"], info["name"]))

            # use disabled state for old add-ons, chances are they are broken.
            if is_addon_27x:
                sub.label(text="Upgrade to 2.8x required")
                sub.label(icon='ERROR')
            # Remove code above after 2.8x migration is complete.
            elif info["warning"]:
                sub.label(icon='ERROR')

            # icon showing support level.
            sub.label(icon=self._support_icon_mapping.get(
                info["support"], 'QUESTION'))

            # Expanded UI (only if additional info is available)
            if info["show_expanded"]:
                if info["description"]:
                    split = colsub.row().split(factor=0.15)
                    split.label(text="Description:")
                    split.label(text=info["description"])
                if info["location"]:
                    split = colsub.row().split(factor=0.15)
                    split.label(text="Location:")
                    split.label(text=info["location"])
                if mod:
                    split = colsub.row().split(factor=0.15)
                    split.label(text="File:")
                    split.label(text=mod.__file__, translate=False)
                if info["author"]:
                    split = colsub.row().split(factor=0.15)
                    split.label(text="Author:")
                    split.label(text=info["author"], translate=False)
                if info["version"]:
                    split = colsub.row().split(factor=0.15)
                    split.label(text="Version:")
                    split.label(text=".".join(str(x)
                                              for x in info["version"]), translate=False)
                if info["warning"]:
                    split = colsub.row().split(factor=0.15)
                    split.label(text="Warning:")
                    split.label(text="  " + info["warning"], icon='ERROR')

                user_addon = USERPREF_PT_addons.is_user_addon(mod, user_addon_paths)
                tot_row = bool(info["doc_url"]) + bool(user_addon)

                if tot_row:
                    split = colsub.row().split(factor=0.15)
                    split.label(text="Internet:")
                    sub = split.row()
                    if info["doc_url"]:
                        sub.operator(
                            "wm.url_open", text="Documentation", icon='HELP',
                        ).url = info["doc_url"]
                    # Only add "Report a Bug" button if tracker_url is set
                    # or the add-on is bundled (use official tracker then).
                    if info.get("tracker_url"):
                        sub.operator(
                            "wm.url_open", text="Report a Bug", icon='URL',
                        ).url = info["tracker_url"]
                    elif not user_addon:
                        addon_info = (
                                         "Name: %s %s\n"
                                         "Author: %s\n"
                                     ) % (info["name"], str(info["version"]), info["author"])
                        props = sub.operator(
                            "wm.url_open_preset", text="Report a Bug", icon='URL',
                        )
                        props.type = 'BUG_ADDON'
                        props.id = addon_info

                draw_addon_add_item(sub, user_addon, mod)
                # Show addon user preferences
                if is_enabled:
                    addon_preferences = prefs.addons[module_name].preferences
                    if addon_preferences is not None:
                        draw = getattr(addon_preferences, "draw", None)
                        if draw is not None:
                            addon_preferences_class = type(
                                addon_preferences)
                            box_prefs = col_box.box()
                            box_prefs.label(text="Preferences:")
                            addon_preferences_class.layout = box_prefs
                            try:
                                draw(context)
                            except:
                                import traceback
                                traceback.print_exc()
                                box_prefs.label(
                                    text="Error (see console)", icon='ERROR')
                            del addon_preferences_class.layout

    # Append missing scripts
    # First collect scripts that are used but have no script file.
    module_names = {mod.__name__ for mod, info in addons}
    missing_modules = {ext for ext in used_ext if ext not in module_names}

    if missing_modules and addon_filter in {"All", "Enabled"}:
        col.column().separator()
        col.column().label(text="Missing script files")

        module_names = {mod.__name__ for mod, info in addons}
        for module_name in sorted(missing_modules):
            is_enabled = module_name in used_ext
            # Addon UI Code
            box = col.column().box()
            colsub = box.column()
            row = colsub.row(align=True)

            row.label(text="", icon='ERROR')

            if is_enabled:
                row.operator(
                    "preferences.addon_disable", icon='CHECKBOX_HLT', text="", emboss=False,
                ).module = module_name

            row.label(text=module_name, translate=False)


# scripts/addons_core/bl_pkg/bl_extension_ui.py l:212
def draw_addon_4_2_or_above(
        *,
        layout,  # `bpy.types.UILayout`
        mod,  # `ModuleType`
        addon_type,  # `int`
        is_enabled,  # `bool`
        # Expanded from both legacy add-ons & extensions.
        # item_name,  # `str`  # UNUSED.
        item_description,  # `str`
        item_maintainer,  # `str`
        item_version,  # `str`
        item_warnings,  # `list[str]`
        item_doc_url,  # `str`
        item_tracker_url,  # `str`
):
    from bl_pkg.bl_extension_ui import (
        ADDON_TYPE_LEGACY_USER, ADDON_TYPE_LEGACY_CORE, ADDON_TYPE_LEGACY_OTHER, ADDON_TYPE_EXTENSION,
        USE_SHOW_ADDON_TYPE_AS_TEXT,addon_type_name,
    )

    from bpy.app.translations import (
        contexts as i18n_contexts,
    )

    split = layout.split(factor=0.8)
    col_a = split.column()
    col_b = split.column()

    if item_description:
        col_a.label(
            text=" {:s}.".format(item_description),
            translate=False,
        )

    rowsub = col_b.row()
    rowsub.alignment = 'RIGHT'
    if addon_type == ADDON_TYPE_LEGACY_CORE:
        rowsub.active = False
        rowsub.label(text="Built-in")
        rowsub.separator()
    elif addon_type == ADDON_TYPE_LEGACY_USER:
        rowsub.operator("preferences.addon_remove", text="Uninstall").module = mod.__name__
    del rowsub

    layout.separator(type='LINE')

    sub = layout.column()
    sub.active = is_enabled
    split = sub.split(factor=0.15)
    col_a = split.column()
    col_b = split.column()

    col_a.alignment = 'RIGHT'

    if item_doc_url:
        col_a.label(text="Website")
        col_b.split(factor=0.5).operator(
            "wm.url_open",
            text=domain_extract_from_url(item_doc_url),
            icon='HELP' if addon_type in {ADDON_TYPE_LEGACY_CORE, ADDON_TYPE_LEGACY_USER} else 'URL',
        ).url = item_doc_url
    # Only add "Report a Bug" button if tracker_url is set.
    # None of the core add-ons are expected to have tracker info (glTF is the exception).
    if item_tracker_url:
        col_a.label(text="Feedback", text_ctxt=i18n_contexts.editor_preferences)
        col_b.split(factor=0.5).operator(
            "wm.url_open", text="Report a Bug", icon='URL',
        ).url = item_tracker_url

    if USE_SHOW_ADDON_TYPE_AS_TEXT:
        col_a.label(text="Type")
        col_b.label(text=addon_type_name[addon_type])
    if item_maintainer:
        col_a.label(text="Maintainer")
        col_b.label(text=item_maintainer, translate=False)
    if item_version:
        col_a.label(text="Version")
        col_b.label(text=item_version, translate=False)
    if item_warnings:
        # Only for legacy add-ons.
        col_a.label(text="Warning")
        col_b.label(text=item_warnings[0], icon='ERROR')
        if len(item_warnings) > 1:
            for value in item_warnings[1:]:
                col_a.label(text="")
                col_b.label(text=value, icon='BLANK1')
            # pylint: disable-next=undefined-loop-variable
            del value

    if addon_type != ADDON_TYPE_LEGACY_CORE:
        col_a.label(text="File")
        col_b.label(text=mod.__file__, translate=False)

        draw_addon_add_item(col_b, False, mod)


is_4_2_or_above = bpy.app.version[:2] >= (4, 2)
source_draw_func = None


def register():
    global source_draw_func

    if is_4_2_or_above:
        import bl_pkg
        source_draw_func = bl_pkg.bl_extension_ui.addon_draw_item_expanded
        bl_pkg.bl_extension_ui.addon_draw_item_expanded = draw_addon_4_2_or_above
    else:
        source_func = bpy.types.USERPREF_PT_addons.draw
        if source_func != draw_addon_4_1_or_below:
            source_draw_func = source_func

        if source_draw_func is None:
            source_draw_func = source_func

        bpy.types.USERPREF_PT_addons.draw = draw_addon_4_1_or_below


def unregister():
    global source_draw_func

    if is_4_2_or_above:
        import bl_pkg
        if bl_pkg.bl_extension_ui.addon_draw_item_expanded == draw_addon_4_2_or_above:
            bl_pkg.bl_extension_ui.addon_draw_item_expanded = source_draw_func
    else:
        source_func = bpy.types.USERPREF_PT_addons.draw
        if source_func == draw_addon_4_1_or_below:
            bpy.types.USERPREF_PT_addons.draw = source_draw_func
    source_draw_func = None
