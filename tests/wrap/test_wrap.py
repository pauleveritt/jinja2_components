def test_wrap_prop_reference_body(rootenv):
    ts = '''\
<h1>Wrapping</h1>
{% wrap template='wrapper.html' %}
        im wrapped content
{% endwrap %}    
    '''
    template = rootenv.from_string(ts)
    context = dict(reference_value='REFERENCE_VALUE')
    result = template.render(context)
    assert 'Hello REFERENCE_VALUE' == result
