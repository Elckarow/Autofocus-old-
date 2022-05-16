init -5 python:
    class AutofocusZoom(AutofocusInterpolation):
        """
        A subclass of `AutofocusInterpolation` used to automatically zoom Characters when they are speaking.

        Attributes
        ----------
        `child`: renpy.Displayable
            The image to zoom / unzoom.
        """

        focused = { }

        def __init__(self, child, name, duration=0.5, focused_level=1.05, unfocused_level=1.0, warper=None, **kwargs):
            super(AutofocusZoom, self).__init__(name=name, duration=duration, focused_level=focused_level, unfocused_level=unfocused_level, warper=warper)
            self.child = Transform(child, subpixel=True)

            self.overlimit_behavior = "unfocused"

        @staticmethod
        def is_allowed():
            return True

        @staticmethod
        def is_on():
            return AutofocusStore.autofocus_zoom

        def render(self, width, height, st, at):
            self.process_logic(st)

            if not self.is_on():
                return renpy.render(self.child, width, height, st, at)

            self.child.zoom = self.current
            rv = renpy.render(self.child, width, height, st, at)

            return rv