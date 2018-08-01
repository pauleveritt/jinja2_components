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
        while parser.stream.current.type != 'block_end':
            args.append(parser.parse_expression())
            parser.stream.skip_if('comma')

        end_tag_name = f'name:end{self.tag_name}'
        body = parser.parse_statements([end_tag_name], drop_needle=True)
        call = self.call_method('_callblock', args=args)
        result = nodes.CallBlock(call, args, [], body)
        result.set_lineno(lineno)
        return result

    def _callblock(self, *args, caller):
        children = caller()
        env = self.environment
        component_class = env.components[self.tag_name]
        template = env.from_string(component_class.template)
        component = component_class()
        context = asdict(component)
        context['children'] = children
        result_one = template.render(context)
        return result_one