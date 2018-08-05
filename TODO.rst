- view

- Real DI

- request

- layout

- path resolvers

- if/loop handlers

- predicate registry

# Later

- Get self.props off instance, onto fragment-cache-style data. This
  didn't work the first time. Child nodes were getting the parent's
  data passed in (which failed when the dataclass didn't define what
  was being passed in.)

- doctests didn't work the first time. Storing the list of components
  on the class means per-run doctests are weird. Also, dataclasses
  defined inline don't seem to have a correct file path.
