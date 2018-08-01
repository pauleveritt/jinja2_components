import pytest

from dataclasses import dataclass


@pytest.fixture
def rootenv_simplest():
    from jinja2_component.environment import ComponentEnvironment
    from jinja2_component.extension import ComponentExtension

    @dataclass
    class Root:
        name: str = 'World'
        template: str = '<div id="root">Root {{name}} children: {{' \
                        'children}}</div>'

    env = ComponentEnvironment()
    env.components['Root'] = Root
    ComponentExtension.tags = {'Root'}
    env.add_extension(ComponentExtension)

    return env
