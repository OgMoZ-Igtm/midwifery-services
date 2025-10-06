import importlib
import os


def get_form_functions(role):
    form_funcs = {}
    module_path = f"modules.forms.forms_{role}"
    try:
        for filename in os.listdir(module_path):
            if filename.endswith(".py") and filename != "__init__.py":
                module_name = f"{module_path}.{filename[:-3]}"
                module = importlib.import_module(module_name)
                for attr in dir(module):
                    if attr.startswith("render_"):
                        func = getattr(module, attr)
                        form_funcs[attr] = func
    except Exception:
        pass
    return form_funcs
