"""

Generic Jinja2 extension for all components

Jinja2 has extensions. Though our components act like Jinja2 extensions,
in that they have different tag names, they are really all the same
thing, extension wise.

Thus, we have one kind of extension which knows how to handle all
registered "components" and dispatch correctly.

"""
import dataclasses
from typing import Dict, Set

from jinja2 import nodes
from jinja2.ext import Extension


def make_context(component_class, passed_in, di: Dict, children: str = None):
    """ Merge passed-in props, defaults, DI props, children """

    props = dict()

    dataclass_field_names = [
        field.name
        for field in dataclasses.fields(component_class)
    ]
    for passed_in_key in passed_in.keys():
        if passed_in_key not in dataclass_field_names:
            raise ValueError(f'{passed_in_key} not in component dataclass')

    for field in dataclasses.fields(component_class):
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


class ComponentExtension(Extension):
    tags: Set
    tag_name: str

    def parse(self, parser):
        # Get the component for the tag name that we matched on
        self.tag_name = parser.stream.current[2]
        component_class = self.environment.components[self.tag_name]
        field_names = [f.name for f in dataclasses.fields(component_class)]
        has_children = 'children' in field_names

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
            self.props[target.name] = value.value

        if has_children:
            end_tag_name = f'name:end{self.tag_name}'
            body = parser.parse_statements([end_tag_name], drop_needle=True)
        else:
            body = ''

        call = self.call_method('_callblock', args=args)
        result = nodes.CallBlock(call, [], [], body)
        result.set_lineno(lineno)
        return result

    def _callblock(self, *args, caller):
        env = self.environment
        component_class = env.components[self.tag_name]

        # Render any child nodes inside the "tags" for this
        # component's usage.
        # TODO Find a way for this to not get access to the
        # global context
        children = caller()

        # Make an instance of this component, to be used as the
        # template context
        di = dict()
        component = make_context(
            component_class,
            self.props,
            di,
            children
        )

        # Now render
        template = env.load_template(component)
        if template is None:
            # No Jinja2 template, this component should implement render
            result = component.render()
        else:
            result = template.render(dataclasses.asdict(component))
        return result
