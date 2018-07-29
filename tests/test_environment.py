import pytest
from jinja2 import Template

from tests.conftest import Simple


def test_basic_environment(environment):
    assert 'Environment' == environment.__class__.__name__


def test_no_extensions(environment):
    assert dict() == environment.extensions


def test_fail_bad_extension(environment):
    class Foo:
        pass

    with pytest.raises(TypeError):
        environment.add_extension(Foo)


def test_good_extension(simple_template):
    ext = simple_template.environment.extensions['conftest.Simple']
    assert 'conftest.Simple' == ext.identifier


def test_good_render(simple_template):
    output = simple_template.render()
    assert 'Simple' == output


def test_args_zero(args_environment):
    template_string = '{% Args %}'
    template = args_environment.from_string(template_string)
    result = template.render(dict())
    assert 'Args' == result
