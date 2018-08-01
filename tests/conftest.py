from dataclasses import asdict, dataclass

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


@dataclass
class RootComponent:
    name: str = 'World'
    template: str = '<d>Root {{name}}</d>'


class ComponentExtension(Extension):
    tags = {'Root'}

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
        component_class = env.get_component_class(self.tag_name)
        ts = RootComponent.template
        template = env.from_string(ts)
        component = component_class()
        result_one = template.render(asdict(component))
        return result_one


class ComponentEnvironment(Environment):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def get_component_class(self, class_name: str):
        return RootComponent


@pytest.fixture
def environment():
    env = ComponentEnvironment()
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
    ComponentExtension.tags = {'Root'}
    environment.add_extension(ComponentExtension)

    return environment
