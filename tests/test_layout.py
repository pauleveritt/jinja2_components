from dataclasses import dataclass

from bs4 import BeautifulSoup

from jinja2_component.environment import ComponentEnvironment


@dataclass
class Root01:
    name: str = 'World'
    template: str = './templates/root01.html'


components = [Root01, ]


def get_soup(component_class: dataclass):
    env = ComponentEnvironment(components)
    context = dict(
        request=dict(docname='articles/index'),
        name='CONTEXT',
    )
    root = component_class(**context)
    result = env.render(component=root, context=context)
    soup = BeautifulSoup(result, 'html5lib')
    return soup


# def test_layout():
#     # TODO
#     # - Have this "env" somewhere "in the system"
#     # - Have "the system" create the Root instance
#     result = get_soup(Root01).find(class_='root').string
#     assert 'World' == result
