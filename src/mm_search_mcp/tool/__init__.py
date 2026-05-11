import importlib
import pkgutil

__all__ = []

for _, module_name, _ in pkgutil.iter_modules(__path__):
    if module_name.startswith("_"):
        continue
    module = importlib.import_module(f".{module_name}", package=__name__)
    for name in dir(module):
        obj = getattr(module, name)
        if callable(obj) and hasattr(obj, "_mcp_tool"):
            globals()[name] = obj
            __all__.append(name)
