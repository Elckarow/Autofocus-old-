init -5 python:
    """
    Make sure to credit the authors:
        Pseurae#6758 was the one that made this entire system.
        Q™#9999 for the drop shadow effect.
        Elckarow#8399 (me), who is maintaining this thing and for making it usable and available.
    """
    
    class AutofocusDisplayable(object):
        """
        Apply it like:
        ```
        layeredimage ayaya stuff boizhfcsxl ee:
            at AutofocusDisplayable(name="ayaya stuff boizhfcsxl ee")
        ```

        Should NOT serve as base for subclasses. See `AutofocusBase` at the end of the `01AutofocusDisplayable.rpy`.

        Attributes
        ----------
        `name`: str
            Name of the image tag.
            Needed for gettings the current attributes.
        
        `kwargs`: dict[str, Any]
            Filtered user arguments.
        
        `unallowed_features`: list[str]
            Explicitly disabled features for this Displayable.
        
        `characters`: dict[str, Character] [Class Variable]
            Stores the Characters created.

        `allowed_args`: None | list[str] | tuple[str] | set[type] [Class Variable]
            Arguments the user is allowed to pass.
            If `None`, no argument is allowed, and will raise an error in case an argument is passed.
            Else, should be a `list` / `tuple` / `set` that contains the arguments allowed, and will raise an error in case a non-allowed argument is passed.
        
        Methods
        -------
        `is_allowed()` -> bool [Static Method]
            A static method that should be overriden to allow the warper to be applied.

        `is_on()` -> bool [Static Method]
            A static method that should be overriden to control the status of the Wrapper.

        `set_attributes()`
            Populates the `attributes` variable and updates the `layer` variable if needed.
            To be called from the render method.
        
        `get_subclasses(exclude: list[type] | tuple[type] | set[type] | type, exclude_subclasses: bool)` -> set[type] [Class Method]
            Returns all subclasses of the current class.

        `character_visible_num()` -> int [Static Method]
            Returns the number of Characters that are showing and that use Autofocus features.
        """

        characters = { }
        allowed_args = None

        def __init__(self, name=None, **kwargs):
            if not name: raise Exception("Character name isn't specified.")

            name = tuple(name.split())
            commmon_callback = kwargs.pop("common_callback", False)

            self.name = name[0]
            self.kwargs, callback_kwargs = filter_autofocus_kwargs(kwargs)
            self.unallowed_features = list(filter_autofocus_kwargs(kwargs, mode="class_names_false").keys())

            AutofocusCallbackHandler.add_callback(name, callback_kwargs, commmon_callback)
            
        @staticmethod
        def is_allowed():
            return False                       

        @staticmethod
        def is_on():
            return False

        def __call__(self, child):
            child = Flatten(child) 

            for cls in self.get_subclasses(exclude=BaseCharCallback, exclude_subclasses=True):
                if not cls.is_allowed(): continue

                # for speed purposes
                cls_name = cls.__name__

                if cls_name in self.unallowed_features: continue

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

        def __repr__(self):
            return "<{} on {} at {}>".format(type(self).__name__, self.name, hex(id(self)))
        
        __str__ = __repr__

###########################################################################################################
                    
    class AutofocusBase(AutofocusDisplayable, renpy.display.core.Displayable, renpy.python.NoRollback):
        """
        This class should be the base for new features.
        
        Attributes
        ----------
        `name`: str
            Image tag.

        `layer`: str
            The layer in which the image is shown. This variable is periodically updated. 
            Needed for gettings the current attributes.

        `attributes`: list[str]
            Stores the current image attributes.
        """

        def __init__(self, name, **kwargs):
            # manual __init__ so that `super(AutofocusBase, self).__init__` doens't call `AutofocusDisplayable.__init__`,
            # otherwise it'll throw an error since `name` defaults to `None`(and it'll prevent unwanted attributes from spawning).
            renpy.display.core.Displayable.__init__(self)

            self.name = name
            self.layer = "master"
            self.attributes = [ ]
