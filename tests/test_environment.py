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


def test_good_extension():
    template_string = '{% Simple %}'
    template = Template(template_string, extensions=[Simple])
    output = template.render()
    assert 'Simple' == output


def test_one_extension_instance():
    pass
