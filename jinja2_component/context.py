"""

Inspect dataclasses and provide constructor values from sources.

"""
from dataclasses import (
    dataclass,
    fields
)
from typing import Dict


# Notes on what is getting passed in:
# - component_class is a dataclass *class*, thing being made instance of
# - props are the args coming from the tag usage in HTML
# - request is a Request object, e.g. SphinxRequest
# - extra_context comes from standalone usage to pass in arbitrary stuff
# - children are when a component contains a (rendered) child
def make_context(
        component_class: dataclass,
        props: Dict = None,  # Passed into a component in HTML
        di: Dict = None,
        request: Dict = None,
        extra_context: Dict = None,
        children: str = None
):
    """ Merge passed-in props, defaults, DI props, children """

    context = dict()

    dataclass_field_names = [
        field.name
        for field in fields(component_class)
    ]

    # Do a quick sanity check to see if the tag usage passed in
    # anything not defined on the component.
    if props:
        for passed_in_key in props.keys():
            if passed_in_key not in dataclass_field_names:
                raise ValueError(f'{passed_in_key} not in component dataclass')

    for field in fields(component_class):
        field_name = field.name

        # 1: First priority, assign children if asked for
        if field_name == 'children':
            # This component wants to use the subnodes of this
            # component
            # TODO use types annotation instead of magic names
            context['children'] = children

        # 2: Next priority, props passed into component tag
        elif props and field_name in props:
            context[field_name] = props[field_name]

        # 3: Next priority, extra context
        elif extra_context and field_name in extra_context:
            context[field_name] = extra_context[field_name]

        # 4: Next priority, DI
        elif 'di' in field.metadata:  # Do the DI dance
            # - Is this a DI field?
            #   * If so, and not available, raise an exception
            di_value = di.get(field.type)
            if di_value is None:
                t = field.type.__name__
                msg = f'Dependency injector cannot find type "{t}"'
                raise KeyError(msg)
            context[field_name] = di_value
        else:
            # Get the default value. If there isn't one, raise an
            # exception
            context[field_name] = field.default

    # Later, have a global flag offering validation.
    return component_class(**context)
