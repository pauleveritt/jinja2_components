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


def test_root_environment(rootenv: ComponentEnvironment):
    assert 'ComponentEnvironment' == rootenv.__class__.__name__


def test_root_multiple(rootenv: ComponentEnvironment):
    ts = """
<body>{% Root01 %}x={{ x }}{% endRoot01 %}</body>
    """
    context = dict(x=99)
    soup = get_soup(rootenv, ts, context)
    result = soup.find(class_='root').string

    # Now assert
    expected = 'Root World children: x=99 name: World'
    assert expected == result

    # Second
    context = dict(x=89)
    soup = get_soup(rootenv, ts, context)
    result = soup.find(class_='root').string
    expected = 'Root World children: x=89 name: World'
    assert expected == result


@pytest.mark.parametrize(
    'template_string, expected',
    [
        ('{% Root01 "one %}{% endRoot01 %}', TemplateSyntaxError),
        ('{% Root01 "one %}', TemplateSyntaxError),
    ]
)
def test_root_fail(rootenv, template_string, expected):
    with pytest.raises(expected):
        rootenv.from_string(template_string)


def test_root_args(rootenv):
    ts = """
<body>{% Root01 name=123 %}x={{ x }}{% endRoot01 %}</body>
    """
    context = dict(x=99)
    soup = get_soup(rootenv, ts, context)
    result = soup.find(class_='root').string

    # Now assert
    expected = 'Root 123 children: x=99 name: 123'
    assert expected == result
