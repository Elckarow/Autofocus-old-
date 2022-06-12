init -5 python:
    from __future__ import division

    class RedefineFocused(type):
        """
        Metaclass used to redefine the `focused` attribute automatically.
        """

        def __new__(cls, *args, **kwargs):
            _class = type.__new__(cls, *args, **kwargs)
            _class.focused = { }
            return _class

    @renpy.six.add_metaclass(RedefineFocused)
    class AutofocusInterpolation(AutofocusBase):
        """
        A subclass of `AutofocusBase` used as a base for classes that should change a displayable over a period of time.
        This interpolates between two values with a specified amount of duration.

        Attributes
        ----------
        `focused`: dict[str, bool] [Class Variable]
            A dictionary containing character focused bools.
            Defined as a class variable automatically for each subclass.

        `focused_level`: float | int
            The value to be interpolated to if focused.

        `unfocused_level`: float | int
            The value to be interpolated to if unfocused.

        `duration`: float | int
            The amount of time taken for the interpolation.

        `current_time`: float
            Elapsed time after a state change, i.e. time when a sprite changes
            from a focused state -> unfocused and vice versa.

        `overlimit_behavior`: str
            The state to switch to when the number of on-screen characters
            is below the limit.

        `warper`: function
            A function that will control how the interpolated value will change. Can be passed as a string `warper="linear"` and if did so,
            the value is first looked up in the `_warper` substore, then in the global store if not found. `TypeError` is raised if the value found isn't a callable.

        Methods
        -------
        `set_defaults()`
            Sets the default values for the variables needed for interpolation.

        `handle_logic()`
            Triggers an event for interpolation and resets `current_time` if needed.
            To be called in the render method. 

        `lerp_value(st: float)`
            Interpolates the value and clamps it if over bounds.
            To be called in the render method.

        `process_logic()`
            Calls a redraw event along with the aforementioned two methods.
        """

        allowed_args = (
            "focused_level",
            "unfocused_level",
            "warper",
            "duration"
        )

        def __init__(self, name, duration, focused_level, unfocused_level, warper, **kwargs):
            super(AutofocusInterpolation, self).__init__(name=name)

            if isinstance(warper, basestring):
                func = getattr(_warper, warper, None)

                if func is None:
                    func = getattr(store, warper, None)
                
                warper = func

            self.focused_level = focused_level
            self.unfocused_level = unfocused_level
            self.duration = duration

            if warper is None:
                self.warper = _warper.easein
            else:
                if not callable(warper): raise TypeError("warper must be a function, not %r" % warper)
                self.warper = warper

            self.set_defaults()

        def set_defaults(self):
            self.current = 0.0
            self.current_time = 0.0
            self.last_st = 0.0

            self.overlimit_behavior = "focused"

            if self.focused.setdefault(self.name, renpy.get_say_image_tag() == self.name):
                self.target = self.focused_level
            else:
                self.target = self.unfocused_level

            self.current = self.target

        def handle_logic(self):
            if self.character_visible_num() >= AutofocusStore.autofocus_interpolation_minimum_char_requirement:
                if renpy.get_say_image_tag() == self.name:
                    if not self.focused[self.name]:
                        self.current_time = 0.0
                        self.target = self.focused_level

                    self.focused[self.name] = True

                else:
                    if self.focused[self.name]:
                        self.current_time = 0.0
                        self.target = self.unfocused_level

                    self.focused[self.name] = False

            else:
                if self.overlimit_behavior == "focused" and not renpy.game.interface.ongoing_transition:
                    if not self.focused[self.name]:
                        self.target = self.focused_level
                        self.current_time = 0.0

                    self.focused[self.name] = True

                elif self.overlimit_behavior == "unfocused":
                    if self.focused[self.name]:
                        self.target = self.unfocused_level
                        self.current_time = 0.0

                    self.focused[self.name] = False

        def process_logic(self, st):
            self.handle_logic()
            self.lerp_value(st)
            renpy.redraw(self, 0.0)

        def lerp_value(self, st):
            """
            `st`
                Time since displayable was first shown. To be supplied through the render method.
            """

            delta = st - self.last_st
            self.last_st = st

            self.current_time += delta

            if self.duration > 0.0:
                complete = min( (self.current_time / self.duration), 1.0 )
            else:
                complete = 1.0

            self.current = self.current + ((self.target - self.current) * self.warper(complete))

            levels = [ self.focused_level, self.unfocused_level ]
            levels.sort()

            self.current = max(self.current, levels[0])
            self.current = min(self.current, levels[1])
