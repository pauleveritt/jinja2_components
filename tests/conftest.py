import pytest

from jinja2 import Environment, nodes, Template
from jinja2.ext import Extension


class Simple(Extension):
    tags = {'Simple'}

    def parse(self, parser):
        lineno = next(parser.stream).lineno
        call = self.call_method('_render', )
        return nodes.Output([call], lineno=lineno)

    def _render(self):
        return self.__class__.__name__


class Heading(Simple):
    tags = {'Heading'}


class Logo1(Simple):
    tags = {'Logo1'}


class Logo2(Simple):
    tags = {'Logo2'}


class Args(Extension):
    tags = {'Args'}

    def parse(self, parser):
        lineno = next(parser.stream).lineno
        args = []
        while parser.stream.current.type != 'block_end':
            args.append(parser.parse_expression())
            parser.stream.skip_if('comma')

        body = parser.parse_statements(['name:endArgs'], drop_needle=True)
        call = self.call_method('_render', args=args)
        result = nodes.CallBlock(call, [], [], [])
        result.set_lineno(lineno)
        return result

    def _render(self, *args, caller):
        cn = self.__class__.__name__
        a = str(args)
        return f'{cn}-{a}'


class Root(Extension):
    tags = {'Root'}

    def parse(self, parser):
        lineno = next(parser.stream).lineno
        args = []
        while parser.stream.current.type != 'block_end':
            args.append(parser.parse_expression())
            parser.stream.skip_if('comma')

        body = parser.parse_statements(['name:endRoot'], drop_needle=True)
        call = self.call_method('_render', args=args)
        result = nodes.CallBlock(call, [], [], [])
        result.set_lineno(lineno)
        return result

    def _render(self, *args, caller):
        cn = self.__class__.__name__
        a = str(args)
        return f'{cn}-{a}'


@pytest.fixture
def environment():
    env = Environment()
    return env


@pytest.fixture
def simple_template(environment):
    template_string = '{% Simple %}'
    template = Template(template_string, extensions=[Simple])
    return template


@pytest.fixture
def args_environment(environment):
    environment.add_extension(Args)
    return environment


@pytest.fixture
def root_environment(environment):
    environment.add_extension(Root)
    environment.add_extension(Heading)
    environment.add_extension(Logo1)
    environment.add_extension(Logo2)

    return environment