init -5 python:
    def Character(name=renpy.character.NotSet, kind=None, **kwargs):
        """
        Creates and returns a `Character` object that allows, if image is given, features such as auto-zoom or coloring to be used.
        """

        char = renpy.character.Character(name, kind=kind, **kwargs)
        image = kwargs.get("image", None)

        if image is not None:
            AutofocusDisplayable.characters[image] = char
        
        return char
    
    def DynamicCharacter(name_expr, **kwargs):
        return Character(name_expr, dynamic=True, **kwargs)
    

    def AutofocusCharacter(name=renpy.character.NotSet, kind=None, **kwargs):
        """
        Needed for backwards comptability.
        """
        return Character(name=name, kind=kind, **kwargs)
    
    def AutofocusDynamicCharacter(name_expr, **kwargs):
        """
        Needed for backwards comptability.
        """
        return DynamicCharacter(name_expr, **kwargs)
    

    def get_all_subclasses(cls):
        for subclass in cls.__subclasses__():
            yield subclass
            for subclass in get_all_subclasses(subclass):
                yield subclass


init 999 python hide:
    for name, char in AutofocusDisplayable.characters.items():
        char.display_args["callback"] = [ cls(name) for cls in BaseCharCallback.get_subclasses() if cls.can_be_used() ]
