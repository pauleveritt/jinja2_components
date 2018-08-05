"""

Register with Jinja2 Environment

Components have environment-related information, such as the
registered Jinja2 extension and the list of known components.
Make it easy to register with a new or existing environment. Also,
provide helpers on the environment, which acts as the central state
for various component-related stuff.

"""
from dataclasses import dataclass
from typing import Dict, List

from jinja2 import Environment, Template

from jinja2_component.extension import ComponentExtension
from jinja2_component.resolver import resolve_path_string


class ComponentEnvironment(Environment):
    components: Dict[str, dataclass] = {}
    templates: Dict[str, Template] = {}

    def __init__(self, components: List[dataclass] = []):
        super().__init__()
        self.add_extension(ComponentExtension)
        ComponentExtension.tags = {
            c.__name__
            for c in components
        }
        self.register_components(components)

    def register_components(self, components: List[dataclass]):
        """ Add known components to tags """
        for component in components:
            tag_name = component.__name__
            self.components[tag_name] = component
            ComponentExtension.tags.add(tag_name)

    def load_template(self, component):
        # Return the template if it exists, if not, make it and store it
        component_name = component.__class__.__name__
        if component_name in self.templates:
            # Template is already loaded, so return it
            return self.templates[component_name]
        else:
            # This template not yet loaded.
            # First, if the component has a "template string" field,
            # use it.
            template_string = None
            if hasattr(component, 'template_string'):
                template_string = component.template_string
            elif hasattr(component, 'template'):
                # The template field is a path, call the resolver
                template_string = resolve_path_string(
                    component.template,
                    component
                )
            if template_string:
                template = self.from_string(template_string)
                self.templates[component_name] = template
                return template

            # If we get here, it means this is a non-Jinja2
            # component that should be rendered via the
            # component's render method.
            return
