"""

Generic Jinja2 extension for all components

Jinja2 has extensions. Though our components act like Jinja2 extensions,
in that they have different tag names, they are really all the same
thing, extension wise.

Thus, we have one kind of extension which knows how to handle all
registered "components" and dispatch correctly.

"""
from dataclasses import asdict

from jinja2 import nodes
from jinja2.ext import Extension


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

        if True:
            targets = []
            while parser.stream.current.type != 'block_end':
                lineno = parser.stream.current.lineno
                if targets:
                    parser.stream.expect('comma')
                target = parser.parse_assign_target()
                target.set_ctx('param')
                targets.append(target)
                parser.stream.expect('assign')
                args.append(parser.parse_expression())
                self.props['outer'] = 123
        else:
            while parser.stream.current.type != 'block_end':
                args.append(parser.parse_expression())
                parser.stream.skip_if('comma')

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
