import pytest

from dataclasses import dataclass

from jinja2_component.environment import ComponentEnvironment
from jinja2_component.extension import ComponentExtension


@dataclass
class Root01:
    children: str = None
    name: str = 'World'
    template: str = '''\
<div class="root">Root {{name}} children: {{children}} name: {{ name }}</div>'''


@pytest.fixture
def rootenv():
    env = ComponentEnvironment()
    env.add_extension(ComponentExtension)

    # Register all the components
    ComponentExtension.tags = {'Root01'}
    for r in (Root01,):
        env.components[r.__name__] = r

    return env

