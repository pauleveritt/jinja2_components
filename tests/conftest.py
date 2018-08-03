import pytest

from dataclasses import dataclass

from jinja2_component.environment import ComponentEnvironment
from jinja2_component.extension import ComponentExtension


@dataclass
class Root01:
    children: str = None
    name: str = 'World'
    template: str = '<div class="root">name={{ name }}</div>'


@dataclass
class Root02:
    children: str = None
    name: str = 'World'
    template: str = '<div class="root">children={{children}}</div>'


@dataclass
class Child01:
    child_name: str = 'Child'
    template: str = '<div class="child">{{child_name}}</div>'


@dataclass
class Root03:
    children: str = None
    name: str = 'World'
    template: str = '''\
<div class="root">
    <h1>Name: {{name}}</h1>
    {% Child01 child_name='Some Child Name'%}{% endChild01 %}
</div>
'''


# Isolation from global context
@dataclass
class Root04:
    name: str = 'World'
    template: str = '<div class="root">g: {{g}}</div>'


@pytest.fixture
def rootenv():
    env = ComponentEnvironment()
    env.add_extension(ComponentExtension)

    # Register all the components
    ComponentExtension.tags = {
        'Root01', 'Root02', 'Root03', 'Child01', 'Root04',
    }
    env.register_components([Root01, Root02, Root03, Child01, Root04])
    # for r in (Root01, Root02, Root03, Child01, Root04):
    #     env.components[r.__name__] = r

    return env
