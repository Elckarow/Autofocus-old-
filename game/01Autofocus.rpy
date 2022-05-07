init -5 python:
    """
    Make sure to credit the authors:
        Pseurae#6758 was the one that made this entire system.
        Elckarow#8399 (me) who polished some things, wrote both `AutofocusZorder` and `AutofocusMouth` as they were originally one single class, added the two character definition functions and made the substore.
    """
    from __future__ import print_function # for logging purposes


    def AutofocusCharacter(name=renpy.character.NotSet, kind=None, **kwargs):
        """
        Creates and returns a `Character` object that allows, if image is given, features such as auto-zoom or coloring to be used.
        See the `Character` function for more details.
        """
        char = renpy.character.Character(name, kind=kind, **kwargs)
        image = kwargs.get("image", None)

        if image is not None:
            AutofocusDisplayable.characters[image] = char
        
        return char
    
    def AutofocusDynamicCharacter(name_expr, **kwargs):
        """
        Creates and returns an `AutofocusCharacter` with the `dynamic` property set to `True`.
        See the `DynamicCharacter` function for more details.
        """
        return AutofocusCharacter(name_expr, dynamic=True, **kwargs)
    

    def get_all_subclasses(cls):
        for subclass in cls.__subclasses__():
            yield subclass
            for subclass in get_all_subclasses(subclass):
                yield subclass


    class AutofocusDisplayable(renpy.display.core.Displayable, renpy.python.NoRollback):
        """
        Apply it like:
        ```
        layeredimage ayaya stuff boizhfcsxl ee:
            at AutofocusDisplayable(name="ayaya")
        ```

        Base class for all the AutofocusDisplayable subclasses.

        Attributes
        ----------
        `name`: str
            Name of the image tag.
            Needed for gettings the current attributes.

        `layer`: str
            The layer in which the image is shown. This variable is periodically updated. 
            Needed for gettings the current attributes.

        `attributes`: list[str]
            Stores the current image attributes.
        
        `characters`: dict[str, Character] [Class Variable]
            Stores the Characters created.

        Methods
        -------
        `is_allowed()` -> bool [Static Method]
            A static method that should be overriden to allow the warper to be applied.

        `is_on()` -> bool [Static Method]
            A static method that should be overriden to control the status of the Wrapper.

        `set_attributes()`
            Populates the `attributes` variable and updates the `layer` variable if needed.
            To be called from the render method.
        
        `get_subclasses()` -> set[type] [Class Method]
            Returns all subclasses of the current class.

        `character_visible_num()` -> int [Static Method]
            Returns the number of Characters that are showing and that are defined
            using `AutofocusCharacter` or `AutofocusDynamicCharacter`.
        """

        characters = { }

        def __init__(self, name=None, **kwargs):
            super(AutofocusDisplayable, self).__init__(**kwargs)

            self.name = name
            self.attributes = [ ]
            self.layer = "master"

        @staticmethod
        def is_allowed():
            return False

        @staticmethod
        def is_on():
            return False

        def __call__(self, child):
            if not self.name: raise Exception("Character name isn't specified.")

            child = Flatten(child)

            for cls in self.get_subclasses():
                if not cls.is_allowed(): continue

                child = cls(child=child, name=self.name)
            
            return child

        def set_attributes(self):
            if not self.name in renpy.get_showing_tags(self.layer):
                self.layer = None

                for layer in config.layers:
                    if self.name not in renpy.get_showing_tags(layer): continue

                    self.layer = layer
                    break

            if self.layer is None:
                self.attributes = [ ]
                return

            self.attributes = list(renpy.get_attributes(self.name, self.layer) or [ ])

        @classmethod
        def get_subclasses(cls):
            return set(get_all_subclasses(cls))
        
        @staticmethod # static to ensure we use AutofocusDisplayable.characters and not SomeSubclass.characters
        def character_visible_num():
            return len(filter(renpy.showing, AutofocusDisplayable.characters.keys()))


    class AutofocusColoring(AutofocusDisplayable):
        """
        A class used for implementing image coloring using colormatrices. 

        Attributes
        ----------
        `child`: renpy.Displayable
            The displayable to color.

        `matrix_map`: dict[str, ColorMatrix] [Class Variable]
            Maps image attributes to the respective colormatrices.

        `matrix`: ColorMatrix [Property]
            The colormatrix to be applied to the image.
            Raise ValueError if set to any other type.

        Methods
        -------
        `set_current_matrix()`
            Sets the `matrix` variable according to the current image attributes and values in `matrix_map`.
        """

        matrix_map = {
            "dawn": TintMatrix((102, 76, 127)) * SaturationMatrix(0.8),
            "day": IdentityMatrix(),
            "sunset": TintMatrix((255, 202, 202)),
            "evening": TintMatrix((131, 102, 127)) * BrightnessMatrix(0.25),
            "night": SaturationMatrix(0.8) * TintMatrix((115, 115, 165))
        }

        def __init__(self, child, name, **kwargs):
            super(AutofocusColoring, self).__init__(**kwargs)

            self.name = name
            self.child = Transform(child)

            self.matrix = IdentityMatrix()

        @staticmethod
        def is_allowed():
            if not renpy.version(tuple=True) >= (7, 4, 0):
                print("---[INCOMPATIBLE VERSION - %s - EXPECTED Ren'Py 7.4.0 OR ABOVE]--- AutofocusColoring disabled" % renpy.version())
                return False

            return config.gl2

        @staticmethod
        def is_on():
            return AutofocusStore.autofocus_coloring

        @property
        def matrix(self):
            return self.__matrix

        @matrix.setter
        def matrix(self, value):
            if not isinstance(value, ColorMatrix): raise ValueError("matrix is not a ColorMatrix instance.")

            self.__matrix = value

        def set_current_matrix(self):
            self.matrix = IdentityMatrix()

            for tag, matrix in self.matrix_map.items():
                if tag not in self.attributes: continue 

                self.matrix = matrix
                break

        def render(self, width, height, st, at):
            self.set_attributes()
            self.set_current_matrix()

            if not self.is_on():
                return renpy.render(self.child, width, height, st, at)
            
            self.child.matrixcolor = self.matrix
            rv = renpy.render(self.child, width, height, st, at)

            return rv


    class AutofocusInterpolation(AutofocusDisplayable):
        """
        A subclass of `AutofocusDisplayable` used as a base for classes that should change a displayable over a period of time.
        This interpolates between two values with a specified amount of duration.

        Attributes
        ----------
        `focused`: dict[str, bool] [Class Variable]
            A dictionary containing character focused bools.
            To be redefined as a class variable again in other subclasses.

        `focused_level`: float | int
            The value to be interpolated to if focused.

        `unfocused_level`: float | int
            The value to be interpolated to if unfocused.

        `duration`: float | int
            The amount of time taken for the interpolation.

        `current_time`: float
            Elapsed time after a state change, i.e. time when a sprite when 
            from a focused state -> unfocused and vice versa.

        `overlimit_behavior`: str
            The state to switch to when the number of on-screen characters
            is below the limit.

        `warper`: function -> float
            A function that will control how the interpolated value will change.

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

        focused = {}

        def __init__(self, name, focused_level, unfocused_level, warper=None, **kwargs):
            super(AutofocusInterpolation, self).__init__(**kwargs)

            self.name = name
            self.focused_level = focused_level
            self.unfocused_level = unfocused_level

            self.duration = 0.0
            self.warper = warper or _warper.easein

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
            if self.character_visible_num() >= AutofocusStore.autofocus_zoom_zorder_minimum_char_requirement:
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

                else: raise ValueError("unkown overlimit_behavior %r for %r" % (self.overlimit_behavior, self))

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


    class AutofocusFilter(AutofocusInterpolation):
        """
        A subclass of `AutofocusInterpolation` used to automatically darken Characters when they are not speaking.

        Attributes
        ----------
        `child`: renpy.Displayable
            The image to darken.
        
        `duration`: float | int
            How long the darkening will take.
        """

        focused = {}

        def __init__(self, child, name, **kwargs):
            super(AutofocusFilter, self).__init__(name=name, focused_level=0.0, unfocused_level=-0.1, **kwargs)
            self.name = name
            self.child = Transform(child)

            self.duration = 0.25

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


    class AutofocusZoom(AutofocusInterpolation):
        """
        A subclass of `AutofocusInterpolation` used to automatically zoom Characters when they are speaking.

        Attributes
        ----------
        `child`: renpy.Displayable
            The image to zoom / unzoom.
        
        `duration`: float | int
            How long the zoom will take.
        """

        focused = {}

        def __init__(self, child, name, **kwargs):
            super(AutofocusZoom, self).__init__(name=name, focused_level=1.05, unfocused_level=1.0, **kwargs)
            self.child = Transform(child, subpixel=True)

            self.duration = 0.5
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


    class BaseCharCallback(AutofocusDisplayable):
        """
        Base class for callbacks classes.
        Should not be applied to the displayable.

        Attributes
        ----------
        `begin_parameter`: str | int
            Parameter passed to the `do_stuff()` function when the Character speaks.

        `end_parameter`: str | int
            Parameter passed to the `do_stuff()` function when the Character doesn't speak.

        Methods
        -------
        `condition()` -> bool
            Logic check. To be overriden.
        
        `do_stuff(arg: str | int)`
            Does something. To be overriden.
        """

        def __init__(self, name, begin_parameter, end_parameter, **kwargs):
            super(BaseCharCallback, self).__init__(**kwargs)
            self.name = name
            self.begin_parameter = begin_parameter
            self.end_parameter = end_parameter

        def condition(self):
            raise AttributeError("%s.condition not implemented" % self)
        
        def do_stuff(self, arg):
            """
            `arg`
                Passed at the beginning / end of each callbacks.
            """
            raise AttributeError("%s.do_stuff not implemented" % self)

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


    class AutofocusZorder(BaseCharCallback):
        """
        A class used to automatically change zorder.
        """
        def __init__(self, name, **kwargs):
            super(AutofocusZorder, self).__init__(name=name, begin_parameter=3, end_parameter=2, **kwargs)

        def condition(self):
            return AutofocusStore.autofocus_zorder and self.character_visible_num() >= AutofocusStore.autofocus_zoom_zorder_minimum_char_requirement

        def do_stuff(self, zorder):
            if "change_zorder" in dir(renpy):
                renpy.change_zorder(self.layer, self.name, zorder)
            else:
                renpy.show(self.name, layer=self.layer, zorder=zorder)


    class AutofocusMouth(BaseCharCallback):
        """
        A class used to automatically change mouths.
        Only works if moods are used, if the mouth attributes `om` and `cm` are defined, and if the mouth attributes are defined within the `mouth` group.

        Attributes
        ----------
        `mouth_tags`: set[str]
            The different mouth tags used. Takes into account every image defined with `name` as image tag.
        """

        def __init__(self, name, **kwargs):
            super(AutofocusMouth, self).__init__(name=name, begin_parameter="om", end_parameter="cm", **kwargs)

            layeredimages = [
                layeredimage
                for tags, layeredimage in renpy.display.image.images.items()
                if tags[0] == self.name
                and isinstance(layeredimage, LayeredImage)
            ]

            self.mouth_tags = set(
                attr.attribute
                for layeredimage in layeredimages
                for attr in layeredimage.attributes
                if attr.group == "mouth"
                and attr.attribute not in ["om", "cm"]
            )

        def condition(self):
            other_mouth_applied = bool(self.mouth_tags & set(self.attributes))
            return AutofocusStore.autofocus_mouth and not other_mouth_applied

        def do_stuff(self, mouth):
            renpy.show("%s %s" % (self.name, mouth), layer=self.layer)
        
        @staticmethod
        def can_be_used():
            if not renpy.version(tuple=True) >= (7, 0):
                print("---[INCOMPATIBLE VERSION - %s - EXPECTED Ren'Py 7.0 OR ABOVE]--- AutofocusMouth disabled" % renpy.version())
                return False

            return True


init -100 python in AutofocusStore:
    """
    This substore contains variables needed for controlling whether these features can be used or not, as well as informations about the project.
    """
    __author__ = "Pseurae#6758", "Elckarow#8399"
    __version__ = (1, 1, 0) # 1.0.0 was Pseurae's

    autofocus_coloring = True
    autofocus_filter = True
    autofocus_zoom = True
    autofocus_zoom_zorder_minimum_char_requirement = 2
    autofocus_zorder = True
    autofocus_mouth = False

    def version(tuple=False):
        """
        If `tuple` is `False`, returns a string containing "Autofocus ", followed by the current version of the project.
        If `tuple` is `True`, returns a tuple giving each component of the version as an integer.
        """
        global __version__

        if tuple: return __version__
        return "Autofocus " + ".".join([str(x) for x in __version__])
    
    def authors(tuple=False):
        """
        If `tuple` is `False`, returns a string containing every authors separated by ", ".
        If `tuple` is `True`, returns a tuple containing each author as a string.
        """
        global __author__

        if tuple: return __author__
        return ", ".join(__author__)


init 999 python hide:
    for name, char in AutofocusDisplayable.characters.items():
        char.display_args["callback"] = [ _class(name) for _class in BaseCharCallback.get_subclasses() if _class.can_be_used() ]
