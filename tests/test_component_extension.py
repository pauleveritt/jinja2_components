import pytest

from jinja2 import TemplateSyntaxError, Template, nodes, Environment
from jinja2.ext import Extension

from jinja2_components.environment import ComponentExtension


@pytest.fixture
def environment():
    env = Environment()
    return env


@pytest.fixture
def args_environment(environment):
    environment.add_extension(Args)
    return environment


class Simple(Extension):
    tags = {'Simple'}

    def parse(self, parser):
        lineno = next(parser.stream).lineno
        call = self.call_method('_render', )
        return nodes.Output([call], lineno=lineno)

    def _render(self):
        return self.__class__.__name__


@pytest.fixture
def simple_template(environment):
    template_string = '{% Simple %}'
    template = Template(template_string, extensions=[Simple])
    return template


class Args(Extension):
    tags = {'Args'}

    def parse(self, parser):
        lineno = next(parser.stream).lineno
        args = []
        while parser.stream.current.type != 'block_end':
            args.append(parser.parse_expression())
            parser.stream.skip_if('comma')

        body = parser.parse_statements(['name:endArgs'],
                                       drop_needle=True)
        call = self.call_method('_render', args=args)
        result = nodes.CallBlock(call, [], [], [])
        result.set_lineno(lineno)
        return result

    def _render(self, *args, caller):
        cn = self.__class__.__name__
        a = str(args)
        return f'{cn}-{a}'


def test_import():
    assert 'ComponentExtension' == ComponentExtension.__name__


def test_basic_environment(environment):
    assert 'Environment' == environment.__class__.__name__


def test_no_extensions(environment):
    assert dict() == environment.extensions


def test_fail_bad_extension(environment):
    class Foo:
        pass

    with pytest.raises(TypeError):
        environment.add_extension(Foo)


def test_good_extension(simple_template):
    ext = simple_template.environment.extensions[
        'test_component_extension.Simple']
    assert 'test_component_extension.Simple' == ext.identifier


def test_good_render(simple_template):
    output = simple_template.render()
    assert 'Simple' == output


def test_args_no_close(args_environment):
    template_string = '{% Args %}'
    with pytest.raises(TemplateSyntaxError):
        args_environment.from_string(template_string)


@pytest.mark.parametrize(
    'template_string, expected',
    [
        ('{% Args %}{% endArgs %}',
         "Args-()"),
        ('{% Args "one" %}{% endArgs %}',
         "Args-('one',)"),
    ]
)
def test_args_pass(args_environment, template_string, expected):
    template = args_environment.from_string(template_string)
    result = template.render(dict())
    assert expected == result


def test_component_no_jinja(rootenv):
    template_string = '{% Root05 %}'
    template = rootenv.from_string(template_string)
    result = template.render(dict())
    assert 'Hello WORLD' == result


@pytest.mark.parametrize(
    'template_string, expected',
    [
        ('{% Args "one %}{% endArgs %}', TemplateSyntaxError),
    ]
)
def test_args_fail(args_environment, template_string, expected):
    with pytest.raises(expected):
        args_environment.from_string(template_string)
