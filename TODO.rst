- template source: package file, relative file, string
    - resolver.py
    - detects 3 modes
    - first two, returns full path, otherwise, string
    - get type information right
    - change template loader to handle file or string

- non-jinja callable
    - make template field optional
    - don't parse template if field is none
    - at render time
        - try to get template
        - if no template, try to get render method

- Get self.props off instance, onto fragment-cache-style data

- Real DI

- request

- view

- layout

- path resolvers

- if/loop handlers

- predicate registry