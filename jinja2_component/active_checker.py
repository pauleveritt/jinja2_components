from jinja2 import Markup
from jinja2.ext import Extension
from jinja2.nodes import ContextReference, CallBlock


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
        d = dict(x=1)
        node = self.call_method('_render_tag', [ctx_ref, d], lineno=lineno)
        return CallBlock(node, [], [], [], lineno=lineno)
