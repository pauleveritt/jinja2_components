import dataclasses
from dataclasses import dataclass

import pytest

from jinja2_component.context import make_context


def test_import():
    assert 'make_context' == make_context.__name__


def test_simplest():
    @dataclass
    class Root:
        pass

    passed_in = dict()
    di = dict()
    actual = make_context(Root, passed_in, di)
    assert dict() == dataclasses.asdict(actual)


def test_passed_in_not_field():
    @dataclass
    class Root:
        pass

    passed_in = dict(xxx=111)
    di = dict()
    with pytest.raises(ValueError):
        make_context(Root, passed_in, di)


def test_passed_in_is_field():
    @dataclass
    class Root:
        name: str

    passed_in = dict(name='hello')
    di = dict()
    component = make_context(Root, passed_in, di)
    assert 'hello' == component.name


def test_field_default():
    @dataclass
    class Root:
        name: str = 'DEFAULT'

    passed_in = dict()
    di = dict()
    component = make_context(Root, passed_in, di)
    assert 'DEFAULT' == component.name


def test_field_missing_di():
    @dataclass
    class Root:
        name: str = dataclasses.field(metadata=dict(di=True))

    passed_in = dict()
    di = dict()
    with pytest.raises(KeyError) as excinfo:
        make_context(Root, passed_in, di)
    expected = 'Dependency injector cannot find type "str"'
    assert expected in str(excinfo.value)


def test_field_di():
    @dataclass
    class Root:
        name: str = dataclasses.field(metadata=dict(di=True))

    passed_in = dict()
    di = {str: 'DI Forever'}
    component = make_context(Root, passed_in, di)
    assert 'DI Forever' == component.name


def test_field_passed_in_and_default():
    @dataclass
    class Root:
        name: str = 'DEFAULT'

    passed_in = dict(name='hello')
    di = dict()
    component = make_context(Root, passed_in, di)
    assert 'hello' == component.name


def test_field_passed_in_and_di():
    @dataclass
    class Root:
        name: str = dataclasses.field(metadata=dict(di=True))

    passed_in = dict(name='hello')
    di = dict()
    component = make_context(Root, passed_in, di)
    assert 'hello' == component.name
