"""
mesclan.attributes
~~~~~~~~~~~~~~~~~~~
"""


class AttributeDict(dict):
    def __init__(self, *args, **kwargs):
        super(AttributeDict, self).__init__()
        self.update(*args, **kwargs)

    def __getattr__(self, key):
        try:
            return self[key]
        except KeyError:
            # to conform with __getattr__ spec
            raise AttributeError(key)

    def __setattr__(self, key, value):
        self[key] = value

    def __setitem__(self, key, value):
        super(AttributeDict, self).__setitem__(key, self._to_attribute(value))

    def update(self, *args, **kwargs):
        if args:
            # Assumes dictionary style input for args
            for key in args[0]:
                self[key] = args[0][key]

        for key in kwargs:
            self[key] = kwargs[key]

    def _to_attribute(self, value):
        if isinstance(value, dict) and not isinstance(value, AttributeDict):
            return AttributeDict(value)
        return value
