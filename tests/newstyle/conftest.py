import pytest
from jinja2 import Environment

from jinja2_component.active_checker import ActiveCheckerExtension


@pytest.fixture
def rootenv():
    env = Environment(extensions=[ActiveCheckerExtension])

    return env
