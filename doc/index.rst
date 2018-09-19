Requirements
============

Simplest Example
================

A view with a template field. Doesn't have to be named ``template``. But
can only have one of type ``Template``.

@dataclass
class Header(Component):
    template: Template = '<div>Hello</div>'

<div>{% Header %}</div>

Template as Property
====================

The template doesn't have to be a field. It can be a property, to allow
some computation.

@dataclass
class Header(Component):
    def template(self):
        return '<div>Hello</div>'

<div>{% Header %}{% endHeader %}</div>

Template File as Property
=========================

Or use template_file which returns a filename, using an
``importlib.resources`` capable string (package, './', etc.)

@dataclass
class Header(Component):
    @property
    def template_file(self):
        return 'bs4_jinja2:templates/header.html'

<div>{% Header %}{% endHeader %}</div>


Simplest Error
==============

View doesn't have ``children``, so body is ignored, so no closing tag
allowed.

@dataclass
class Header(Component):
    template: Template = '<div>Hello</div>'

<div>{% Header %}{% endHeader %}</div>

Basic Expression
================

The component template can have Jinja2 expressions.

@dataclass
class Header(Component):
    template: Template = '<div>Sum: {{ 2 + 2 }}</div>'

<div>{% Header %}</div>

Expression Value from View Field
================================

Fields in the view are available in the template.

@dataclass
class Header(Component):
    name: str = 'Jill'
    template: Template = '<div>Hello: {{ name }}</div>'

<div>{% Header %}</div>


Expression Value from View Property/Method
==========================================

Fields in the view are available in the template.

@dataclass
class Header(Component):
    name: str = 'Jill'
    template: Template = '<div>{{ view.prefix }}: {{ view.greet('Hello') }}</div>'

    @property
    def prefix(self):
        return 'Greeting: '

    def greet(self, msg):
        return f'{msg}, {self.name}'

<div>{% Header %}</div>


View Template Asks For Missing Field
====================================

The view's template inserts ``resources`` but no field on view.

@dataclass
class Header(Component):
    template: Template = '<div>R1: {{ resources[0].name }}</div>'

<div>{% Header %}</div>


Outside Context
===============

Get a value made available from the outside system.

@dataclass
class Header(Component):
    resources: List[Resource]
    template: Template = '<div>R1: {{ resources[0].name }}</div>'

<div>{% Header %}</div>


Props Passed In
================

Components can have props that are passed in from the caller.

@dataclass
class Header(Component):
    template: Template = '<div>R1: {{ resources[0].name }}</div>'

<div>{% Header resources={{ site.resources}} %}</div>

Error When Missing Prop
=======================

The view demands ``resources`` but it isn't provided.

@dataclass
class Header(Component):
    resources: List[Resource]
    template: Template = '<div>R1: {{ resources[0].name }}</div>'

<div>{% Header %}</div>

Error When Providing Prop
=========================

The view demands ``resources`` but it isn't provided.

@dataclass
class Header(Component):
    resources: List[Resource]
    template: Template = '<div>R1: {{ resources[0].name }}</div>'

<div>{% Header %}</div>


Prop Overrides DI
=================

If the outside system has ``resources`` but a particular caller uses a
different list in a prop, the prop has precedence.


Children
========

- View template references but not on view

- View template references, on view but None

- View asks for children, but no end block

- Child block asks for view field

- Child block contains simple subcomponent

- Simple subcomponent has prop

- Simple subcomponent has DI

- Simple subcomponent accesses parent view's field

Other
=====

- Component asks for static resource to be injected

    - Head vs. foot

    - Before vs. after

    - De-dupe

- Cache

    - Decorator which indicates policy

    - Specifies what fields are used for hash

    - Might have to recurse into children

- Non-Jinja2 component with ``render`` as f-string

- View validation: None, simple, pydantic

- Isolation: total vs. shared

- skipIf and looping view fields

- Optional ``customize_context`` lets you add/subtract/modify the context
  dictionary

- Subclass to specialize a component

- Predicate registry to override a view or a view template

Also
====

- Line numbers work correctly

- The view has to state which extensions are available in its templates

- Does the parent context automatically extend to children?

References
==========

https://stackoverflow.com/questions/34021437/how-do-you-parse-and-inject-additional-nodes-in-a-jinja-extension

https://stackoverflow.com/questions/29378468/how-can-a-custom-jinja2-tag-interface-with-the-context-of-a-flask-request

https://stackoverflow.com/questions/12139029/how-to-access-context-variables-from-the-jinjas-extension

https://stackoverflow.com/questions/23170013/jinja-extension-that-has-access-to-context

https://github.com/pallets/jinja/blob/2.8/jinja2/ext.py#L413-L431