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
        template_string: str = '<div>Hello</div>'

    return Hello


@pytest.fixture
def helloworld_component():
    @dataclass
    class HelloWorld:
        name: str = 'World'
        template_string: str = '<div>Hello {{name}}</div>'

    return HelloWorld


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
    tag_name = hello_component.__name__
    extensions = list(env.extensions.values())
    assert tag_name in extensions[0].tags


def test_load_template(env, hello_component):
    env.register_components([hello_component])
    hc = hello_component()
    env.load_template(hc)
    assert hello_component.__name__ in env.templates


def test_render_component(helloworld_component):
    env = ComponentEnvironment([helloworld_component])
    result = env.render_component(helloworld_component)
    assert '<div>Hello World</div>' == result


def test_render_component_extra(helloworld_component):
    env = ComponentEnvironment([helloworld_component])
    extra_context = dict(name='extra')
    result = env.render_component(helloworld_component,
                                  extra_context=extra_context)
    assert '<div>Hello extra</div>' == result


def test_render_string(env, helloworld_component):
    env.register_components([helloworld_component])
    ts = '{% HelloWorld %}'
    result = env.render_string(ts)
    assert '<div>Hello World</div>' == result


# This is the problematic one
def test_render_string_context(env, helloworld_component):
    env.register_components([helloworld_component])
    ts = '{% HelloWorld name=context_name %}'
    context = dict(context_name='CONTEXTBABY')
    result = env.render_string(ts, context=context)
    assert '<div>Hello CONTEXTBABY</div>' == result
