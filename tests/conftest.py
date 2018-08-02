import pytest

from dataclasses import dataclass

from jinja2_component.environment import ComponentEnvironment
from jinja2_component.extension import ComponentExtension


@pytest.fixture
def env():
    env = ComponentEnvironment()
    env.add_extension(ComponentExtension)

    return env


@pytest.fixture
def rootenv_simplest(env):
    @dataclass
    class Root:
        children: str = None
        name: str = 'World'
        template: str = '''\
<div id="root">Root {{name}} children: {{children}} name: {{ name }}</div>'''

    env.components['Root'] = Root
    ComponentExtension.tags = {'Root'}

    return env
