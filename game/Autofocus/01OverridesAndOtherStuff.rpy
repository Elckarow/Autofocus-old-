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
    
    # Needed for backwards comptability
    AutofocusCharacter = Character
    AutofocusDynamicCharacter = DynamicCharacter
    

init -6 python:
    """
    Contains useful functions.
    """

    def get_all_subclasses(cls, exclude=(), exclude_subclasses=False):
        def get_subclasses(cls, exclude=()):
            for subclass in cls.__subclasses__():
                if subclass not in exclude:
                    yield subclass

                for subclass in get_subclasses(subclass, exclude):
                    yield subclass
                ### if you're using Ren'Py 8, remove the 2 lines above and uncomment the following line ###
                ### both ways work but this all is better / faster ###

                #yield from get_subclasses(subclass, exclude)

        if not isinstance(exclude, (list, tuple, set)): exclude = [ exclude ]

        if exclude_subclasses:
            for cls_to_exclude in exclude:
                exclude.extend(get_subclasses(cls_to_exclude))

        return get_subclasses(cls, exclude)
    

    def get_layer(name):
        for layer in config.layers:
            if name not in renpy.get_showing_tags(layer): continue
            break
        else:
            layer = None
            
        return layer
    

    def filter_autofocus_kwargs(kwargs, mode="both", error=True):
        subclasses_name = [
            cls.__name__
            for cls in AutofocusDisplayable.get_subclasses(exclude=BaseCharCallback, exclude_subclasses=True)
        ]

        callbacks = [
            cls.__name__
            for cls in BaseCharCallback.get_subclasses()
        ]

        filtered_kw = { }
        features_kw = { }
        callbacks_kw = { }
        all_kw = { }

        for cls, v in kwargs.items():
            og_cls = cls
            cls, _, k = cls.partition("_")

            if cls in callbacks:
                all_kw.setdefault(cls, { })
                all_kw[cls][k] = v

                callbacks_kw.setdefault(cls, { })
                callbacks_kw[cls][k] = v
                continue

            elif cls in subclasses_name:
                all_kw.setdefault(cls, { })
                all_kw[cls][k] = v
                
                features_kw.setdefault(cls, { })
                features_kw[cls][k] = v
                continue

            elif mode == "filter":
                filtered_kw[og_cls] = v
                continue

            if error: raise Exception("Unknown subclass -> %r" % og_cls)
        
        if mode == "filter": return filtered_kw
        elif mode == "all": return all_kw
        elif mode == "callbacks": return callbacks_kw
        elif mode == "features": return features_kw
        elif mode == "both": return features_kw, callbacks_kw
        else: raise Exception("Unknown mode -> '%s'" % mode)


init 999 python hide:
    for name, char in AutofocusDisplayable.characters.items():
        char.display_args["callback"] = [
                                            cls(name, **AutofocusDisplayable.callback_kwargs[name].setdefault(cls.__name__, { }))
                                            for cls in BaseCharCallback.get_subclasses()
                                            if cls.can_be_used()
                                        ]
