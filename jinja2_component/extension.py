"""

Generic Jinja2 extension for all components

Jinja2 has extensions. Though our components act like Jinja2 extensions,
in that they have different tag names, they are really all the same
thing, extension wise.

Thus, we have one kind of extension which knows how to handle all
registered "components" and dispatch correctly.

"""
import dataclasses
from dataclasses import asdict
from typing import Dict

from jinja2 import nodes
from jinja2.ext import Extension


def make_context(component_class, passed_in, di: Dict):
    """ Merge passed-in props, defaults, and DI props """

    # Iterate over what the component_class has for fields
    #   * Otherwise, use it.
    # Add this field/value to props
    # Construct the dataclass instance and return it, which will raise
    # an exception if something required isn't available.
    # Later, have a global flag offering validation.

    props = dict()

    dataclass_field_names = [
        field.name
        for field in dataclasses.fields(component_class)
    ]
    for passed_in_key in passed_in.keys():
        if passed_in_key not in dataclass_field_names:
            raise ValueError(f'{passed_in_key} not in component dataclass')

    for field in dataclasses.fields(component_class):
        fn = field.name

        # First priority: passed in
        if fn in passed_in:
            props[fn] = passed_in[fn]

        # Second priority: DI
        elif 'di' in field.metadata:  # Do the DI dance
            # - Is this a DI field?
            #   * If so, and not available, raise an exception
            di_value = di.get(field.type)
            if di_value is None:
                t = field.type.__name__
                msg = f'Dependency injector cannot find type "{t}"'
                raise KeyError(msg)
            props[fn] = di_value
        else:
            # Get the default value. If there isn't one, raise an
            # exception
            props[fn] = field.default

    return component_class(**props)


class ComponentExtension(Extension):
    tags = {'Root'}
    tag_name: str

    def parse(self, parser):
        # Which tag did we match on?
        self.tag_name = parser.stream.current[2]

        lineno = next(parser.stream).lineno

        args = []

        # Parse the key/value pairs out of the AST structure into
        # a regular dict.
        self.props = dict()

        targets = []
        while parser.stream.current.type != 'block_end':
            lineno = parser.stream.current.lineno
            if targets:
                parser.stream.expect('comma')
            target = parser.parse_assign_target()
            target.set_ctx('param')
            targets.append(target)
            parser.stream.expect('assign')
            value = parser.parse_expression()
            args.append(value)
            self.props['outer'] = value.value

        end_tag_name = f'name:end{self.tag_name}'
        body = parser.parse_statements([end_tag_name], drop_needle=True)

        call = self.call_method('_callblock', args=args)
        result = nodes.CallBlock(call, [], [], body)
        result.set_lineno(lineno)
        return result

    def _callblock(self, *args, caller):
        children = caller()
        env = self.environment
        component_class = env.components[self.tag_name]
        template = env.from_string(component_class.template)
        component = component_class()

        context = {**self.props, **asdict(component)}
        context['children'] = children
        result = template.render(context)
        return result
