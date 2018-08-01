from dataclasses import asdict, dataclass

import pytest

from jinja2 import Environment, nodes, Template
from jinja2.ext import Extension


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
def root_environment(environment):
    ComponentExtension.tags = {'Root'}
    environment.add_extension(ComponentExtension)

    return environment
