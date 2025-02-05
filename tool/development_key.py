from ..utils import get_keymap

register_keymap_items = []


def register():
    global register_keymap_items

    from ..registration import DEVELOPMENT_KEY_MAPS

    for keymap_name, keymap_items in DEVELOPMENT_KEY_MAPS.items():
        km = get_keymap(keymap_name)
        for item in keymap_items:
            idname = item.get("idname")
            key_type = item.get("type")
            value = item.get("value")

            shift = item.get("shift", False)
            ctrl = item.get("ctrl", False)
            alt = item.get("alt", False)

            kmi = km.keymap_items.new(idname, key_type, value, shift=shift, ctrl=ctrl, alt=alt)

            if kmi:
                properties = item.get("properties")
                if properties:
                    for name, value in properties.items():
                        setattr(kmi.properties, name, value)
            register_keymap_items.append((km, kmi))


def unregister():
    global register_keymap_items
    for keymap, kmi in register_keymap_items:
        try:
            keymap.keymap_items.remove(kmi)
        except ReferenceError as e:
            print(e.area)
            import traceback
            traceback.print_exc()
            traceback.print_stack()
    register_keymap_items.clear()
