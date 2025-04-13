"""

Generic Jinja2 extension for all components

Jinja2 has extensions. Though our components act like Jinja2 extensions,
in that they have different tag names, they are really all the same
thing, extension wise.

Thus, we have one kind of extension which knows how to handle all
registered "components" and dispatch correctly.

"""
import dataclasses
from typing import Set

from jinja2 import nodes
from jinja2.ext import Extension

from jinja2_components.context import make_context


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
            # args.append(value.value)

        # context = ContextReference()
        # args.append(context)
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
            children=children
        )

        # Now render
        template = env.load_template(component)
        if template is None:
            # No Jinja2 template, this component should implement render
            result = component.render()
        else:
            d = dataclasses.asdict(component)
            result = template.render(**d)
        return result
