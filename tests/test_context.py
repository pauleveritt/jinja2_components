"""
Different ways to construct a component

System
- Make a request
-

Standalone
- kwargs
- component

"""

import dataclasses
from dataclasses import dataclass

import pytest

from jinja2_components.context import make_context


def test_import():
    assert 'make_context' == make_context.__name__


def test_simplest():
    @dataclass
    class Root:
        pass

    passed_in = dict()
    di = dict()
    actual = make_context(Root, props=passed_in, di=di)
    assert dict() == dataclasses.asdict(actual)


def test_none_di_props():
    @dataclass
    class Root:
        name: str = 'default'

    component = make_context(Root)
    assert 'default' == component.name


def test_passed_in_not_field():
    @dataclass
    class Root:
        pass

    passed_in = dict(xxx=111)
    di = dict()
    with pytest.raises(ValueError):
        make_context(Root, props=passed_in, di=di)


def test_passed_in_is_field():
    @dataclass
    class Root:
        name: str

    passed_in = dict(name='hello')
    di = dict()
    component = make_context(Root, props=passed_in, di=di)
    assert 'hello' == component.name


def test_field_default():
    @dataclass
    class Root:
        name: str = 'DEFAULT'

    passed_in = dict()
    di = dict()
    component = make_context(Root, props=passed_in, di=di)
    assert 'DEFAULT' == component.name


def test_field_missing_di():
    @dataclass
    class Root:
        name: str = dataclasses.field(metadata=dict(di=True))

    passed_in = dict()
    di = dict()
    with pytest.raises(KeyError) as excinfo:
        make_context(Root, props=passed_in, di=di)
    expected = 'Dependency injector cannot find type "str"'
    assert expected in str(excinfo.value)


def test_field_di():
    @dataclass
    class Root:
        name: str = dataclasses.field(metadata=dict(di=True))

    passed_in = dict()
    di = {str: 'DI Forever'}
    component = make_context(Root, props=passed_in, di=di)
    assert 'DI Forever' == component.name


def test_field_extra_context():
    @dataclass
    class Root:
        name: str

    extra_context = dict(name='extra stuff')
    component = make_context(Root, extra_context=extra_context)
    assert 'extra stuff' == component.name


def test_field_passed_in_and_default():
    @dataclass
    class Root:
        name: str = 'DEFAULT'

    passed_in = dict(name='hello')
    di = dict()
    component = make_context(Root, props=passed_in, di=di)
    assert 'hello' == component.name


def test_field_passed_in_and_di():
    @dataclass
    class Root:
        name: str = dataclasses.field(metadata=dict(di=True))

    passed_in = dict(name='hello')
    di = dict()
    component = make_context(Root, props=passed_in, di=di)
    assert 'hello' == component.name


def test_props_extra_context_di():
    @dataclass
    class Root:
        name: str = dataclasses.field(metadata=dict(di=True))

    passed_in = dict(name='hello')
    extra_context = dict(name='extra stuff')
    di = dict()
    component = make_context(Root,
                             props=passed_in,
                             extra_context=extra_context,
                             di=di)
    assert 'hello' == component.name
