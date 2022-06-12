init -5 python:
    class BaseCharCallback(AutofocusBase):
        """
        Base class for callbacks classes.
        Should not be applied to the displayable.

        Attributes
        ----------
        `begin_parameter`: Any
            Parameter passed to the `do_stuff()` method when the Character speaks.

        `end_parameter`: Any
            Parameter passed to the `do_stuff()` method when the Character doesn't speak.

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
            super(BaseCharCallback, self).__init__(name=name)
            self.begin_parameter = begin_parameter
            self.end_parameter = end_parameter

        def condition(self):
            raise NotImplementedError("<%s %s>.condition not implemented" % (type(self).__name__, self.name))
        
        def do_stuff(self, arg):
            raise NotImplementedError("<%s %s>.do_stuff not implemented" % (type(self).__name__, self.name))

        def __call__(self, event, interact=True, **kwargs):
            if not interact: return

            self.set_attributes()

            if not self.attributes: return

            if self.condition():
                if event == "begin":
                    return self.do_stuff(self.begin_parameter)

                elif event == "end":
                    return self.do_stuff(self.end_parameter)
        
        @staticmethod
        def is_allowed():
            return True
