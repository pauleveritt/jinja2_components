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


class ComponentEnvironment(Environment):
    components: Dict[str, dataclass] = {}
    templates: Dict[str, Template] = {}

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.add_extension(ComponentExtension)

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
            return self.templates[component_name]
        else:
            template_string = component.template
            template = self.from_string(template_string)
            self.templates[component_name] = template
            return template
