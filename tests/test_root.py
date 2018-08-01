import pytest
from jinja2 import TemplateSyntaxError


def test_root_environment(environment):
    assert 'Environment' == environment.__class__.__name__


@pytest.mark.parametrize(
    'template_string, expected',
    [
        ('{% Root %}{% endRoot %}',
         "Root-()"),
        ('{% Root "one" %}{% endRoot %}',
         "Root-('one',)"),
        (
                '{% with foo = 42 %}{% Root "one", "two" %}{% endRoot %}{% '
                'endwith %}',
                "Root-('one', 'two')"),
    ]
)
def test_Root_pass(root_environment, template_string, expected):
    template = root_environment.from_string(template_string)
    result = template.render(dict())
    assert expected == result


@pytest.mark.parametrize(
    'template_string, expected',
    [
        ('{% Root "one %}{% endRoot %}', TemplateSyntaxError),
    ]
)
def test_Root_fail(root_environment, template_string, expected):
    with pytest.raises(expected):
        root_environment.from_string(template_string)
