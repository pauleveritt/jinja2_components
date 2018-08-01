from dataclasses import dataclass
from typing import Dict

import pytest
from bs4 import BeautifulSoup
from jinja2 import TemplateSyntaxError


def get_soup(ts: str, context: Dict):
    template = root_environment.from_string(ts)
    r = template.render(context)
    soup = BeautifulSoup(r, 'html5lib')
    return soup


@dataclass
class Root:
    name: str = 'World'
    template: str = '<div id="root">Root {{name}} children: {{children}}</div>'


@pytest.fixture
def root_environment():
    from jinja2_component.environment import ComponentEnvironment
    from jinja2_component.extension import ComponentExtension
    env = ComponentEnvironment()
    env.components['Root'] = Root
    ComponentExtension.tags = {'Root'}
    env.add_extension(ComponentExtension)

    return env


def test_root_environment(root_environment):
    assert 'ComponentEnvironment' == root_environment.__class__.__name__


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

    # Second
    r = template.render(dict(x=89))
    soup = BeautifulSoup(r, 'html5lib')
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
def test_Root_fail(root_environment, template_string, expected):
    with pytest.raises(expected):
        root_environment.from_string(template_string)


def test_Root_args(root_environment):
    ts = """
<body>{% Root z=1 %}x={{ x }}{% endRoot %}</body>
    """
    template = root_environment.from_string(ts)
    r = template.render(dict(x=99))
    soup = BeautifulSoup(r, 'html5lib')
    result = soup.find(id='root').string

    # Now assert
    expected = 'Root World children: x=99'
    assert expected == result

    # Second
    r = template.render(dict(x=89))
    soup = BeautifulSoup(r, 'html5lib')
    result = soup.find(id='root').string
    expected = 'Root World children: x=89'
    assert expected == result
