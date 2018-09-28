"""

This example comes from

https://stackoverflow.com/questions/34021437/how-do-you-parse-and-inject
-additional-nodes-in-a-jinja-extension


"""
import jinja2
import pytest
from jinja2 import nodes, Environment
from jinja2.ext import Extension


class WrapExtension(Extension):
    tags = {'wrap'}
    template = None

    def parse(self, parser):
        tag = parser.stream.current.value
        lineno = parser.stream.next().lineno
        args, kwargs = self.parse_args(parser)
        body = parser.parse_statements(['name:end{}'.format(tag)],
                                       drop_needle=True)

        return nodes.CallBlock(
            self.call_method('wrap', args, kwargs),
            [], [], body).set_lineno(lineno)

    def parse_args(self, parser):
        args = []
        kwargs = []
        require_comma = False

        while parser.stream.current.type != 'block_end':
            if require_comma:
                parser.stream.expect('comma')

            if parser.stream.current.type == 'name' and parser.stream.look(

            ).type == 'assign':
                key = parser.stream.current.value
                parser.stream.skip(2)
                value = parser.parse_expression()
                kwargs.append(nodes.Keyword(key, value, lineno=value.lineno))
            else:
                if kwargs:
                    parser.fail(
                        'Invalid argument syntax for WrapExtension tag',
                        parser.stream.current.lineno)
                args.append(parser.parse_expression())

            require_comma = True

        return args, kwargs

    @jinja2.contextfunction
    def wrap(self, context, caller, template=None, *args, **kwargs):
        return self.environment.get_template(template or self.template).render(
            dict(context, content=caller(), **kwargs))


@pytest.fixture
def rootenv():
    env = Environment(WrapExtension)

    return env
