from jinja2 import Environment
from jinja2.ext import Extension
from jinja2.nodes import Scope, Assign, Output


class CocoExtension(Extension):
    tags = {'coco'}

    def parse(self, parser):
        lineno = next(parser.stream).lineno
        node = Scope(lineno=lineno)
        assignments = []
        while parser.stream.current.type != 'block_end':
            lineno = parser.stream.current.lineno
            if assignments:
                parser.stream.expect('comma')
            target = parser.parse_assign_target()
            parser.stream.expect('assign')
            expr = parser.parse_expression()
            assignments.append(Assign(target, expr, lineno=lineno))

        inner_block = list(parser.parse_statements(
            ('name:end' + 'coco',),
            drop_needle=True)
        )
        # Grab the Output node's child nodes
        children = inner_block[0].nodes[:]

        # Make the extension's template
        ts = '''\
<div class="extension">
Coco {{msg}} {{children}}
{% with x=1 %}
    x: {{x}}
{% endwith %}
</div>
'''
        template = self.environment.parse(ts)

        # Grab the templates's Output child nodes
        template_output_nodes = template.body[0].nodes[:]

        # Replace the {{ children }} node with the child template
        template.body[1] = children

        # Make a new Output node
        output = Output(template_output_nodes + children)

        node.body = assignments + [output, ]

        return node


def test_template_simple():
    env = Environment(extensions=[CocoExtension])
    ts = '<p>Hello {{msg}}</p>'
    template = env.parse(ts)

    body = template.body
    assert 'list' == body.__class__.__name__
    output = body[0]
    assert 'Output' == output.__class__.__name__
    output_nodes = output.nodes
    assert 'list' == output_nodes.__class__.__name__
    assert 3 == len(output_nodes)
    output_name = output_nodes[1]
    assert 'Name' == output_name.__class__.__name__
    assert 'msg' == output_name.name
    assert 'load' == output_name.ctx


def test_coco_simplest(rootenv):
    rootenv = Environment(extensions=[CocoExtension])
    ts = "{% coco %}Inner{% endcoco %}"
    template = rootenv.parse(ts)

    # Make sure there is a body
    body = template.body
    assert 'list' == body.__class__.__name__

    # Get the Output node
    output = body[0].body[0]
    assert 'Output' == output.__class__.__name__

    # Children of Output
    # First, stuff from extension's template
    coco = output.nodes[0]
    assert 'TemplateData' == coco.__class__.__name__
    assert '<div class="extension">Coco' == coco.data.strip()

    # The arguments that ts passed to the extension
    # output_nodes = output.nodes
    # assert 'list' == output_nodes.__class__.__name__
    # assert 1 == len(output_nodes)
    # assert 'TemplateData' == output_nodes[0].__class__.__name__

    # Now the children
    pass
    # Render it, see if you like it
    pass
