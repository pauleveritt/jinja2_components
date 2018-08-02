import dataclasses
from dataclasses import dataclass

import pytest

from jinja2_component.extension import get_props


def test_import():
    assert 'get_props' == get_props.__name__


def test_simplest():
    @dataclass
    class Root:
        pass

    actual = get_props(Root, dict())
    assert dict() == dataclasses.asdict(actual)


def test_passed_in_not_field():
    @dataclass
    class Root:
        pass

    with pytest.raises(ValueError):
        get_props(Root, dict(xxx=111))


def test_passed_in_is_field():
    @dataclass
    class Root:
        name: str

    d = dict(name='hello')
    component = get_props(Root, d)
    assert 'hello' == component.name


def test_field_default():
    @dataclass
    class Root:
        name: str = 'DEFAULT'

    component = get_props(Root, dict())
    assert 'DEFAULT' == component.name


def test_field_passed_in_and_default():
    @dataclass
    class Root:
        name: str = 'DEFAULT'

    d = dict(name='hello')
    component = get_props(Root, d)
    assert 'hello' == component.name

#
# -------  REMINDER
# Simplify algorithm. Dataclasses already handles passing in
# an invalid value to the constructor. Basically, for any
# field that is NOT in passed_in, see if it is a DI. If so,
# add it to passed_in, then pass in passed_in to dataclass
# constructor.
