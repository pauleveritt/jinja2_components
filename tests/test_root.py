import pytest
from jinja2 import TemplateSyntaxError


def test_root_environment(environment):
    assert 'ComponentEnvironment' == environment.__class__.__name__


# @pytest.mark.parametrize(
#     'template_string, expected',
#     [
#         ('{% Root %}{% endRoot %}',
#          "Root-()"),
#         ('{% Root "one" %}{% endRoot %}',
#          "Root-('one',)"),
#         (
#                 '{% with foo = 42 %}{% Root "one", "two" %}{% endRoot %}{% '
#                 'endwith %}',
#                 "Root-('one', 'two')"),
#     ]
# )
# def test_Root_pass(root_environment, template_string, expected):
#     template = root_environment.from_string(template_string)
#     result = template.render(dict())
#     assert expected == result


def test_Root_multiple(root_environment):
    ts = """
<b>{% Root %}x={{ x }}{% endRoot %}</b>
    """
    template = root_environment.from_string(ts)
    result_one = template.render(dict(x=99))
    expected = '<b><d>Root World</d></b>'
    assert expected == str.strip(result_one)
    result_two = template.render(dict(x=88))
    # expected = 'Root-()-\n<div>x=88</div>'
    # assert expected == str.strip(result_two)


@pytest.mark.parametrize(
    'template_string, expected',
    [
        ('{% Root "one %}{% endRoot %}', TemplateSyntaxError),
    ]
)
def test_Root_fail(root_environment, template_string, expected):
    with pytest.raises(expected):
        root_environment.from_string(template_string)
