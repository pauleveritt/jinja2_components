from dataclasses import dataclass

import pytest

from jinja2_component.environment import ComponentEnvironment


@pytest.fixture
def env():
    return ComponentEnvironment()


@pytest.fixture
def hello_component():
    @dataclass
    class Hello:
        template: str = '<div>Hello</div>'

    return Hello


def test_import():
    assert 'ComponentEnvironment' == ComponentEnvironment.__name__


def test_construction(env):
    k = 'jinja2_component.extension.ComponentExtension'
    ext = env.extensions
    assert 'ComponentEnvironment' == env.__class__.__name__
    assert {} == env.components
    assert k in ext.keys()
    assert 1 == len(ext.keys())


def test_register_components(env, hello_component):
    assert {} == env.components
    env.register_components([hello_component])
    tag_name = hello_component.__class__.__name__
    extensions = list(env.extensions.values())
    assert tag_name in extensions[0].tags
