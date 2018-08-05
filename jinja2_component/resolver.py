"""
Resolve flavors of strings into Path objects and return contents

"""
from importlib.resources import read_text
from inspect import getsourcefile
from pathlib import Path

MISSING_COMPONENT = 'Must supply a component to resolve template'


def resolve_path_string(path_string, component=None):
    if ':/' in path_string:
        # Package version
        package, path = path_string.split(':/')
        template_string = read_text(package, path)
    else:
        # Relative path, relative to the component. If the
        # component is omitted, raise an exception
        if component is None:
            raise ValueError(MISSING_COMPONENT)
        p = Path(getsourcefile(component)).parent / path_string
        with open(p, 'r') as f:
            template_string = f.read()

    return template_string
