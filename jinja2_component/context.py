"""

Inspect dataclasses and provide constructor values from sources.

"""
from dataclasses import (
    dataclass,
    fields
)
from typing import Dict


def make_context(
        component_class: dataclass,
        passed_in: Dict,
        di: Dict,
        children: str = None
):
    """ Merge passed-in props, defaults, DI props, children """

    props = dict()

    dataclass_field_names = [
        field.name
        for field in fields(component_class)
    ]
    for passed_in_key in passed_in.keys():
        if passed_in_key not in dataclass_field_names:
            raise ValueError(f'{passed_in_key} not in component dataclass')

    for field in fields(component_class):
        field_name = field.name

        if field_name == 'children':
            # This component wants to use the subnodes of this
            # component
            # TODO use types annotation instead of magic names
            props['children'] = children
        # Next priority: passed in
        elif field_name in passed_in:
            props[field_name] = passed_in[field_name]

        # Second priority: DI
        elif 'di' in field.metadata:  # Do the DI dance
            # - Is this a DI field?
            #   * If so, and not available, raise an exception
            di_value = di.get(field.type)
            if di_value is None:
                t = field.type.__name__
                msg = f'Dependency injector cannot find type "{t}"'
                raise KeyError(msg)
            props[field_name] = di_value
        else:
            # Get the default value. If there isn't one, raise an
            # exception
            props[field_name] = field.default

    # Later, have a global flag offering validation.
    return component_class(**props)
