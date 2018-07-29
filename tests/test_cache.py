from jinja2 import Environment
import pytest

from jinja2_component.cache import FragmentCacheExtension

template_string = """\
{% cache 'sidebar', 300 %}
<div class="sidebar">
    ...
</div>
{% endcache %}
"""


@pytest.fixture
def environment():
    env = Environment(extensions=[FragmentCacheExtension])
    return env


@pytest.fixture
def first_context():
    class A:
        def complicated_value(self):
            return 999

    return dict(a=A())


def test_run(environment, first_context):
    template = environment.from_string(template_string)
    result = template.render(first_context)
    assert '<h1>Hello</h1>' == result
