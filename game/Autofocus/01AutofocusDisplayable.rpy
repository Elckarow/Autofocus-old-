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

        `allowed_args`: None | list[str] | tuple[str] | set[type] [Class Variable]
            Arguments the user is allowed to pass.
            If `None`, no argument is allowed, and will raise an error in case an argument is passed.
            Else, should be a `list` / `tuple` / `set` that contains the arguments allowed, and will raise an error in case a non-allowed argument is passed.

        `callback_kwargs`: dict[str, dict[str, dict[str, Any]]] [Class Variable]
            Stores arguments passed to features using callbacks.
        
        `repr_dict`: dict[str, str]
            A dictionnary containing every representaion of features used by a certain character.
        
        If you need to know the different parameters of a character, say `eileen`, do
            ```
            $ print(AutofocusDisplayable.repr_dict["eileen"])
            ```
        and for callbacks do
            ```
            $ print(AutofocusDisplayable.characters["eileen"].display_args["callback"])
            ```
        
        then look into `log.txt`.
        
        
        If you ever read through the features' doc, you might encounter a `self.raw_child`. It's used for representation purposes so don't worry about it.

        Methods
        -------
        `is_allowed()` -> bool [Static Method]
            A static method that should be overriden to allow the warper to be applied.

        `is_on()` -> bool [Static Method]
            A static method that should be overriden to control the status of the Wrapper.

        `set_attributes()`
            Populates the `attributes` variable and updates the `layer` variable if needed.
            To be called from the render method.
        
        `get_subclasses(exclude: list[type] | tuple[type] | set[type], exclude_subclasses: bool)` -> set[type] [Class Method]
            Returns all subclasses of the current class.

        `character_visible_num()` -> int [Static Method]
            Returns the number of Characters that are showing and that use Autofocus features.
        
        `get_repr(obj: Any)` -> str [Static Method]
            If `obj` is a feature, returns `repr(obj)`, else retruns an empty string.
        """

        characters = { }
        allowed_args = None
        callback_kwargs = { }
        repr_dict = { }

        def __init__(self, name=None, **kwargs):
            super(AutofocusDisplayable, self).__init__()

            self.name = name
            self.attributes = [ ]
            self.layer = "master"
            self.kwargs, callback_kwargs = filter_autofocus_kwargs(kwargs)

            AutofocusDisplayable.callback_kwargs.setdefault(self.name, callback_kwargs)
            
        @staticmethod
        def is_allowed():
            return False                       

        @staticmethod
        def is_on():
            return False

        def __call__(self, child):
            if not self.name: raise Exception("Character name isn't specified.")

            child = Flatten(child) 

            for cls in self.get_subclasses(exclude=BaseCharCallback, exclude_subclasses=True):
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
            
            AutofocusDisplayable.repr_dict[self.name] = repr(child)
                                                
            return child

        def set_attributes(self):
            self.layer = get_layer(self.name)

            if self.layer is None:
                self.attributes = [ ]
                return

            self.attributes = list(renpy.get_attributes(self.name, self.layer) or [ ])
        
        @staticmethod
        def character_visible_num(): # static to ensure we use AutofocusDisplayable.characters and not SomeSubclass.characters
            return len(list(filter(renpy.showing, AutofocusDisplayable.characters.keys())))

        @classmethod
        def get_subclasses(cls, exclude=(), exclude_subclasses=False):
            return set(get_all_subclasses(cls, exclude, exclude_subclasses))

        @staticmethod
        def get_repr(obj):
            if isinstance(obj, AutofocusDisplayable): return repr(obj)
            return ""

        def __repr__(self):
            return "<AutofocusDisplayable {} at {}>".format(self.name, hex(id(self)))
        
        __str__ = __repr__
