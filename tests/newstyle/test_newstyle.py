def test_env(rootenv):
    e = 'jinja2_component.active_checker.ActiveCheckerExtension'
    assert e in rootenv.extensions


def test_simplest_active(rootenv):
    ts = "{% set active = True %}{% check_active %}"
    template = rootenv.from_string(ts)
    context = dict()
    result = template.render(context)
    assert 'Active is : True' == result


def test_simplest_with(rootenv):
    ts = "{% coco %}Hello{% endcoco %}"
    template = rootenv.from_string(ts)
    context = dict()
    result = template.render(context)
    assert 'Hello' == result
