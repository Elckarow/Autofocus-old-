init -5 python:
    """
    Make sure to credit the authors:
        Pseurae#6758 was the one that made this entire system.
        Q™#9999 for the drop shadow effect.
        Elckarow#8399 (me), who is maintaining this thing and for making it usable and available.
    """
    
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

        `allowed_args`: None | list[str] | tuple[str] [Class Variable]
            Arguments the user is allowed to pass.
            If `None`, no argument is allowed, and will log a message in case an argument is passed.
            Else, should be a `list` / `tuple` that contains the arguments allowed, and will log a message in case a non-allowed argument is passed.

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
        allowed_args = None

        def __init__(self, name=None, **kwargs):
            super(AutofocusDisplayable, self).__init__()

            self.name = name
            self.attributes = [ ]
            self.layer = "master"
            self.kwargs = { }

            subclasses_name = [
                cls.__name__
                for cls in self.get_subclasses()
            ]

            for cls, v in kwargs.items():
                og_cls = cls
                cls, _, k = cls.partition("_")

                if cls not in subclasses_name: raise Exception("Unknown subclass -> %r" % og_cls)

                if cls not in self.kwargs:
                    self.kwargs[cls] = { }

                self.kwargs[cls][k] = v
            
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

                cls_name = cls.__name__
                kwargs = { }

                if cls.allowed_args is not None:
                    for k, v in self.kwargs.get(cls_name, {}).items():
                        if k not in cls.allowed_args: raise Exception("Argument %r isn't allowed for the class %r" % (k, cls_name))
                            
                        kwargs[k] = v

                else:
                    if cls_name in self.kwargs: raise Exception("Arguments passed to %r, but this class doesn't allow user arguments." % cls_name)
                
                child = cls(child=child, name=self.name, **kwargs)
                                                
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
