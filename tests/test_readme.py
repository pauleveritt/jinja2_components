"""Provide an example that can be included in the README."""

from dataclasses import dataclass

from jinja2_components.environment import ComponentEnvironment


def test_environment():
    # Make a component
    @dataclass
    class HelloWorld:
        name: str = "World"
        template_string: str = "<div>Hello {{name}}</div>"

    # Make a Jinja2 environment and register the components
    env = ComponentEnvironment()
    env.register_components([HelloWorld])

    # Render a template usage of this component
    usage_template = '{% HelloWorld %}'
    result = env.render_string(usage_template)
    assert '<div>Hello World</div>' == result

    # Pass an argument
    usage_template = '{% HelloWorld name="Jinja2" %}'
    result = env.render_string(usage_template)
    assert '<div>Hello Jinja2</div>' == result
