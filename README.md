# Components for Jinja2

Frontend-style components as Jinja2 Jinja2 extensions.

## Features

- Reusable components for Jinja
- Better developer experience

## jinja2_components development setup

Let's get `jinja2_components` setup for development, using `uv`. Clone this repo and make a virtual environment there:

```shell
$ git clone https://github.com/pauleveritt/jinja2_components.git
$ cd jinja2_components
$ uv run pytest
```

If you are using an IDE with testing support (PyCharm, VS Code) and it doesn't have `uv run` support, you'll need
another step. Whenever you change dependencies, run `uv sync`, since the IDE is likely running `pytest` directly.

## Using `jinja2_components`

Let's write a component. It can be developed and tested in isolation:

```python
@dataclass
class HelloWorld:
    name: str = "World"
    template_string: str = "<div>Hello {{name}}</div>"
```

The component's template can be inline or point to a path on disk.

In your application setup, use `ComponentEnvironment` as a custom
[Jinja2 environment](https://tedboy.github.io/jinja2/generated/generated/jinja2.environment.Environment.html). Then,
start registering components.

```python
env = ComponentEnvironment()
env.register_components([HelloWorld])
```

During an operation (e.g. a web request), build up some context and render a template that uses the component.

```python
usage_template = '{% HelloWorld %}'
result = env.render_string(usage_template)
assert '<div>Hello World</div>' == result
```

Components can be passed args, get values from a DI system, etc.:

```python
usage_template = '{% HelloWorld name="Jinja2" %}'
result = env.render_string(usage_template)
assert '<div>Hello Jinja2</div>' == result
```

## How it works

Jinja2 has extensions. Though our components act like Jinja2 extensions,
in that they have different tag names, they are really all the same
thing, extension wise.

Thus, we have *one* kind of extension which knows how to handle all
registered "components" and dispatch correctly. This extension, and the registered components, are part of a custom
`ComponentEnvironment`.

This environment sits between the usage template and the component, providing all the machinery:

- Component lookup
- Gathering "props" from the usage
- Inspecting the component to find what props it requires
- Calling the component with the inputs (props, injection, etc.)
- Throwing useful errors when missing props or type mismatch

Along the way, `jinja2_components` can provide extra facilities:

- A context-like API
- Dependency injector

Since components declare their props as type information, smarter tooling can inspect the component and match TSX
authoring:

- Component name autocomplete and autoimport
- Prop name autocomplete
- Prop value autocomplete and type checking
- Missing required props

## TODO

- Update from Sasha's branch for better Jinja extension
- Switch to tdom
- Bring in Hopscotch for DI

## References

https://stackoverflow.com/questions/34021437/how-do-you-parse-and-inject-additional-nodes-in-a-jinja-extension

https://medium.com/horlu/my-experience-of-writing-a-jinja-extension-f8eed5fe3ef5

https://stackoverflow.com/questions/16635145/jinja2-extension-multiple-keyword-arguments

