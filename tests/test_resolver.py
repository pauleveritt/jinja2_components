from dataclasses import dataclass

import pytest

from jinja2_component.resolver import resolve_path_string


@dataclass
class Hello:
    pass


def test_import():
    assert 'resolve_path_string' == resolve_path_string.__name__


@pytest.mark.parametrize(
    'path_string, expected',
    [
        ('jinja2_component.test:/t1.html', '<div>t1.html</div>'),
        ('./templates/t2.html', '<div>t2.html</div>'),
    ]
)
def test_content(path_string, expected):
    hello = Hello()
    result = resolve_path_string(path_string, hello)
    assert expected == result
