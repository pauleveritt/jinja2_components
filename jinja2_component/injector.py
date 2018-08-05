"""

Dependency Injection for the component system.

The injector is a dictionary-like object which can be used
to fetch values. When asking for a value, though, it looks it
up in the predicate registry. This allows multiple values to be
registered for one key, and thus context-sensitive lookups.

Things a component might want dependency-injected:

- The current request
- The layout
- The context resource
- The resolver service

Internally, the component system uses the injector

"""


class Injector:
    pass
