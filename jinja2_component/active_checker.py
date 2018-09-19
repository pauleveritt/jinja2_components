from jinja2 import Markup
from jinja2.ext import Extension
from jinja2.nodes import ContextReference, CallBlock, Assign, Scope


class ActiveCheckerExtension(Extension):
    """
    This will give us a {% check_active %} tag.
    """

    template = 'Active is : %s'
    tags = {'check_active'}

    def _render_tag(self, context, caller):
        return Markup(self.template % context['active'])

    def parse(self, parser):
        ctx_ref = ContextReference()
        lineno = next(parser.stream).lineno
        node = self.call_method('_render_tag', [ctx_ref, ], lineno=lineno)
        return CallBlock(node, [], [], [], lineno=lineno)


class WithComponentExtension(Extension):
    """
    Use the With component as a basis
    """

    tags = {'coco'}

    def parse(self, parser):
        node = Scope(lineno=next(parser.stream).lineno)
        assignments = []
        while parser.stream.current.type != 'block_end':
            lineno = parser.stream.current.lineno
            if assignments:
                parser.stream.expect('comma')
            target = parser.parse_assign_target()
            parser.stream.expect('assign')
            expr = parser.parse_expression()
            assignments.append(Assign(target, expr, lineno=lineno))
        node.body = assignments + \
                    list(parser.parse_statements(
                        ('name:end' + 'coco',),
                        drop_needle=True)
                    )
        return node
