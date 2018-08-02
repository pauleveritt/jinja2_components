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


def test_root_01_no_prop(rootenv: ComponentEnvironment):
    ts = "<body>{% Root01 %}{% endRoot01 %}</body>"
    context = dict()
    soup = get_soup(rootenv, ts, context)
    result = soup.find(class_='root').string
    assert 'name=World' == result


def test_root_01_prop(rootenv: ComponentEnvironment):
    ts = "<body>{% Root01 name='prop' %}{% endRoot01 %}</body>"
    context = dict()
    soup = get_soup(rootenv, ts, context)
    result = soup.find(class_='root').string
    assert 'name=prop' == result


def test_root_01_prop_multiple(rootenv: ComponentEnvironment):
    for i in ('prop1', 'prop2'):
        ts = "<body>{% Root01 name='" + i + "' %}{% endRoot01 %}</body>"
        context = dict()
        soup = get_soup(rootenv, ts, context)
        result = soup.find(class_='root').string
        assert 'name=' + i == result


def test_root_02_children(rootenv: ComponentEnvironment):
    ts = "<body>{% Root02 %}inner={{inner}}{% endRoot02 %}</body>"
    context = dict(inner='inner')
    soup = get_soup(rootenv, ts, context)
    result = soup.find(class_='root').string
    assert 'children=inner=inner' == result


def test_root_03_nested_children(rootenv: ComponentEnvironment):
    ts = "<body>{% Root03 name='Root 3' %}{% endRoot03 %}</body>"
    context = dict()
    soup = get_soup(rootenv, ts, context)
    result = soup.find(class_='child').string
    assert 'Some Child Name' == result


#   Failures
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
