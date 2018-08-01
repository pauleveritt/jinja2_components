from typing import Dict

import pytest
from bs4 import BeautifulSoup
from jinja2 import TemplateSyntaxError

from jinja2_component.environment import ComponentEnvironment


def get_soup(env: ComponentEnvironment, ts: str, context: Dict):
    template = env.from_string(ts)
    r = template.render(context)
    soup = BeautifulSoup(r, 'html5lib')
    return soup


def test_root_environment(rootenv_simplest: ComponentEnvironment):
    assert 'ComponentEnvironment' == rootenv_simplest.__class__.__name__


def test_Root_multiple(rootenv_simplest: ComponentEnvironment):
    ts = """
<body>{% Root %}x={{ x }}{% endRoot %}</body>
    """
    context = dict(x=99)
    soup = get_soup(rootenv_simplest, ts, context)
    result = soup.find(id='root').string

    # Now assert
    expected = 'Root World children: x=99'
    assert expected == result

    # Second
    context = dict(x=89)
    soup = get_soup(rootenv_simplest, ts, context)
    result = soup.find(id='root').string
    expected = 'Root World children: x=89'
    assert expected == result


@pytest.mark.parametrize(
    'template_string, expected',
    [
        ('{% Root "one %}{% endRoot %}', TemplateSyntaxError),
        ('{% Root "one %}', TemplateSyntaxError),
    ]
)
def test_Root_fail(rootenv_simplest, template_string, expected):
    with pytest.raises(expected):
        rootenv_simplest.from_string(template_string)


def test_Root_args(rootenv_simplest):
    ts = """
<body>{% Root %}x={{ x }}{% endRoot %}</body>
    """
    context = dict(x=99)
    soup = get_soup(rootenv_simplest, ts, context)
    result = soup.find(id='root').string

    # Now assert
    expected = 'Root World children: x=99'
    assert expected == result
