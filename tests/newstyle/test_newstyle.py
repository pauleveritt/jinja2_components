from jinja2_component.active_checker import ActiveCheckerExtension


def test_env(rootenv):
    e = 'jinja2_component.active_checker.ActiveCheckerExtension'
    assert e in rootenv.extensions


def test_simplest(rootenv, mocker):
    mocker.spy(ActiveCheckerExtension, '_render_tag')
    ts = "{% set active = True %}{% check_active %}"
    template = rootenv.from_string(ts)
    context = dict()
    result = template.render(context)
    art = ActiveCheckerExtension._render_tag
    call_context = art.call_args_list[0][0]
    assert 9 == call_context
