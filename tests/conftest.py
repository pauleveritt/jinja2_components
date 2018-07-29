from random import randint

import pytest

from jinja2 import Environment, nodes, Template
from jinja2.ext import Extension


class Simple(Extension):
    tags = {'Simple'}

    def parse(self, parser):
        lineno = next(parser.stream).lineno
        call = self.call_method('_render', )
        return nodes.Output([call], lineno=lineno)

    def _render(self):
        return self.__class__.__name__


class Args(Extension):
    tags = {'Args'}

    def parse(self, parser):
        lineno = next(parser.stream).lineno
        call = self.call_method('_render', )
        return nodes.Output([call], lineno=lineno)

    def _render(self):
        return self.__class__.__name__


@pytest.fixture
def environment():
    env = Environment()
    return env


@pytest.fixture
def simple_template(environment):
    template_string = '{% Simple %}'
    template = Template(template_string, extensions=[Simple])
    return template


@pytest.fixture
def args_environment(environment):
    environment.add_extension(Args)
    return environment
