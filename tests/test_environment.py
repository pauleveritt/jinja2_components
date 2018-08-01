import pytest
from jinja2 import TemplateSyntaxError


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


def test_args_no_close(args_environment):
    template_string = '{% Args %}'
    with pytest.raises(TemplateSyntaxError):
        args_environment.from_string(template_string)


@pytest.mark.parametrize(
    'template_string, expected',
    [
        ('{% Args %}{% endArgs %}',
         "Args-()"),
        ('{% Args "one" %}{% endArgs %}',
         "Args-('one',)"),
        ('{% with foo = 42 %}{% Args "one", "two" %}{% endArgs %}{% endwith %}',
         "Args-('one', 'two')"),
    ]
)
def test_args_pass(args_environment, template_string, expected):
    template = args_environment.from_string(template_string)
    result = template.render(dict())
    assert expected == result


@pytest.mark.parametrize(
    'template_string, expected',
    [
        ('{% Args "one %}{% endArgs %}',TemplateSyntaxError),
    ]
)
def test_args_fail(args_environment, template_string, expected):
    with pytest.raises(expected):
        args_environment.from_string(template_string)
