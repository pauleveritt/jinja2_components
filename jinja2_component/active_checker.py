from jinja2 import Markup
from jinja2.ext import Extension
from jinja2.nodes import (
    ContextReference, CallBlock, Assign, Scope, Name
)


class ActiveCheckerExtension(Extension):
    """
    This will give us a {% check_active %} tag.
    """

    template = 'Active is : %s'
    tags = {'check_active'}

    def _render_tag(self, context, caller):
        assert 99 == context.get('foo', False)
        return Markup(self.template % context['active'])

    def parse(self, parser):
        ctx_ref = ContextReference()

        var = Assign(Name('foo', 'store'), 99)
        lineno = next(parser.stream).lineno
        node = self.call_method('_render_tag', [ctx_ref, ], lineno=lineno)
        return CallBlock(node, [], [], [], lineno=lineno)


class WithComponentExtension(Extension):
    """
    Use the With component as a basis
    """

    tags = {'coco'}

    def parse(self, parser):
        lineno = next(parser.stream).lineno
        node = Scope(lineno=lineno)
        assignments = []
        while parser.stream.current.type != 'block_end':
            lineno = parser.stream.current.lineno
            if assignments:
                parser.stream.expect('comma')
            target = parser.parse_assign_target()
            parser.stream.expect('assign')
            expr = parser.parse_expression()
            assignments.append(Assign(target, expr, lineno=lineno))

        children = list(parser.parse_statements(
            ('name:end' + 'coco',),
            drop_needle=True)
        )

        node.body = assignments + children

        return node
