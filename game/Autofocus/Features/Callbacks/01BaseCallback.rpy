init -5 python:
    class BaseCharCallback(AutofocusDisplayable):
        """
        Base class for callbacks classes.
        Should not be applied to the displayable.

        Attributes
        ----------
        `begin_parameter`: Any
            Parameter passed to the `do_stuff()` function when the Character speaks.

        `end_parameter`: Any
            Parameter passed to the `do_stuff()` function when the Character doesn't speak.

        Methods
        -------
        `condition()` -> bool
            Logic check. To be overriden.
        
        `do_stuff(arg: Any)`
            Does something. To be overriden.
        """
        
        allowed_args = (
            "begin_parameter",
            "end_parameter"
        )

        def __init__(self, name, begin_parameter, end_parameter, **kwargs):
            super(BaseCharCallback, self).__init__()
            self.name = name
            self.begin_parameter = begin_parameter
            self.end_parameter = end_parameter

        def condition(self):
            raise NotImplementedError("%s.condition not implemented" % self)
        
        def do_stuff(self, arg):
            raise NotImplementedError("%s.do_stuff not implemented" % self)

        def __call__(self, event, interact=True, **kwargs):
            if not interact: return

            self.set_attributes()
            if not self.attributes: return

            if self.condition():
                if event == "begin":
                    self.do_stuff(self.begin_parameter)

                elif event == "end":
                    self.do_stuff(self.end_parameter)
        
        @staticmethod
        def can_be_used():
            return True

        def __repr__(self):
            return "<{} on {} at {}> | begin_parameter: {}, end_parameter: {}".format(type(self).__name__, self.name, hex(id(self)), self.begin_parameter, self.end_parameter)
