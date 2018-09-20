def test_env(rootenv):
    e = 'jinja2_component.active_checker.ActiveCheckerExtension'
    assert e in rootenv.extensions


def test_simplest_active(rootenv):
    ts = "{% set active = True %}{% check_active %}"
    template = rootenv.from_string(ts)
    context = dict()
    result = template.render(context)
    assert 'Active is : True' == result


def test_coco_simplest(rootenv):
    ts = "{% coco %}Hello{% endcoco %}"
    template = rootenv.from_string(ts)
    context = dict()
    result = template.render(context)
    assert 'Hello' == result


def test_coco_external(rootenv):
    ts = "{% coco %}Hello {{ name }}{% endcoco %}"
    template = rootenv.from_string(ts)
    context = dict(name='External')
    result = template.render(context)
    assert 'Hello External' == result


def test_coco_prop(rootenv):
    ts1 = "{% coco name='prop1' %}Hello {{ name }}{% endcoco %}"
    template1 = rootenv.from_string(ts1)
    context = dict()
    result1 = template1.render(context)
    assert 'Hello prop1' == result1

    # Make sure another usage of the component doesn't stash values
    ts2 = "{% coco name='prop2' %}Hello {{ name }}{% endcoco %}"
    template2 = rootenv.from_string(ts2)
    context = dict()
    result2 = template2.render(context)
    assert 'Hello prop2' == result2


def test_coco_prop_reference(rootenv):
    ts = "{% coco name=reference_value %}Hello {{ name }}{% endcoco %}"
    template = rootenv.from_string(ts)
    context = dict(reference_value='REFERENCE_VALUE')
    result = template.render(context)
    assert 'Hello REFERENCE_VALUE' == result


def test_coco_prop_reference_body(rootenv):
    ts = "{% coco name=reference_value %}Hello {{ name }}{% endcoco %}"
    template = rootenv.from_string(ts)
    context = dict(reference_value='REFERENCE_VALUE')
    result = template.render(context)
    assert 'Hello REFERENCE_VALUE' == result
