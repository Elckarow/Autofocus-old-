init -5 python:
    from __future__ import print_function
    
    class AutofocusFilter(AutofocusInterpolation):
        """
        A subclass of `AutofocusInterpolation` used to automatically darken Characters when they are not speaking.

        Attributes
        ----------
        `child`: renpy.Displayable
            The image to darken.
        """

        focused = {}

        def __init__(self, child, name, duration=0.25, focused_level=0.0, unfocused_level=-0.1, warper=None, **kwargs):
            super(AutofocusFilter, self).__init__(name=name, duration=duration, focused_level=focused_level, unfocused_level=unfocused_level, warper=warper, child=child)
            self.child = Transform(child)

        @staticmethod
        def is_allowed():
            if not renpy.version(tuple=True) >= (7, 4, 0):
                print("---[INCOMPATIBLE VERSION - %s - EXPECTED Ren'Py 7.4.0 OR ABOVE]--- AutofocusFilter disabled" % renpy.version())
                return False

            return config.gl2

        @staticmethod
        def is_on():
            return AutofocusStore.autofocus_filter

        def render(self, width, height, st, at):
            self.process_logic(st)

            if not self.is_on():
                return renpy.render(self.child, width, height, st, at)

            self.child.matrixcolor = BrightnessMatrix(self.current)
            rv = renpy.render(self.child, width, height, st, at)

            return rv
