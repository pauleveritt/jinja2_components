import pytest
from bs4 import BeautifulSoup
from jinja2 import TemplateSyntaxError


def test_root_environment(root_environment):
    assert 'ComponentEnvironment' == root_environment.__class__.__name__


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
<body>{% Root %}x={{ x }}{% endRoot %}</body>
    """
    template = root_environment.from_string(ts)
    r = template.render(dict(x=99))
    soup = BeautifulSoup(r, 'html5lib')
    result = soup.find(id='root').string

    # Now assert
    expected = 'Root World children: x=99'
    assert expected == result
    # result_two = template.render(dict(x=88))
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
