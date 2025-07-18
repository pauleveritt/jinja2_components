from dataclasses import dataclass

import pytest

from jinja2_components.environment import ComponentEnvironment


@dataclass
class Root01:
    children: str = None
    name: str = 'World'
    template: str = './templates/root01.html'


@dataclass
class Root02:
    children: str = None
    name: str = 'World'
    template_string: str = '<div class="root">children={{children}}</div>'


@dataclass
class Child01:
    child_name: str = 'Child'
    template_string: str = '<div class="child">{{child_name}}</div>'


@dataclass
class Root03:
    children: str = None
    name: str = 'World'
    template_string: str = '''\
<div class="root">
    <h1>Name: {{name}}</h1>
    {% Child01 child_name='Some Child Name'%}
</div>
'''


# Isolation from global context
@dataclass
class Root04:
    name: str = 'World'
    template_string: str = '<div class="root">g: {{g}}</div>'


@dataclass
class Root05:
    name: str = 'world'

    def render(self):
        return f'Hello {self.name.upper()}'


@dataclass
class Root06:
    name: str = 'World'
    template_string: str = '''
<div class="root"
>{% Root05 name="Child" %}</div>'''


@pytest.fixture
def rootenv():
    components = [
        Root01, Root02, Root03, Child01, Root04, Root05,
        Root06,
    ]
    env = ComponentEnvironment(components)

    return env
