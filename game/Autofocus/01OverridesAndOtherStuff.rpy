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
        """
        Returns all subclasses of `cls`.
        
        `cls`: type
            The class that should return the subclasses from.
        
        `exclude`: set[type] | tuple[type] | list[type] | type
            A class / list of classes we should exclude from the returned value.
           
        `exclude_subclasses`: bool
            If `True`, will exclude all subclasses of the classes passed in `exclude`.
        """
        
        def get_subclasses(cls, exclude=()):
            for subclass in cls.__subclasses__():
                if subclass not in exclude:
                    yield subclass

                for subclass in get_subclasses(subclass, exclude):
                    yield subclass
                ### if you're using Ren'Py 8, remove the 2 lines above and uncomment the following line ###
                ### both ways work but this one is better / faster ###

                #yield from get_subclasses(subclass, exclude)

        if not isinstance(exclude, (list, tuple, set)): exclude = [ exclude ]

        if exclude_subclasses:
            for cls_to_exclude in exclude:
                exclude.extend(get_subclasses(cls_to_exclude))

        return get_subclasses(cls, exclude)
    

    def get_layer(name):
        """
        Gets the layer `name` is showing on, or `None` if not found.
        
        `name`: str
            The tag of the image.
        """
        
        for layer in config.layers:
            if name not in renpy.get_showing_tags(layer): continue
            break
        else:
            layer = None
            
        return layer
    

    def filter_autofocus_kwargs(kwargs, mode="both", error=True):
        """
        Given a dictionnary, will filter the dictionnary and return a new one.
        
        `kwargs`: dict[Any, Any]
            The dictionnary to filter.
        
        `mode`: str
            Will dictate the returned value.
            `"both"` will return a tuple containing Features kwargs and Callbacks kwargs.
            `"features"` will only return Features kwargs.
            `"callbacks"` will only return Callbacks kwargs.
            `"all"` will return a dictionnary containing both Features kwargs and Callbacks kwargs.
            `"filter"` will return a dictionnary containing everything but Features kwargs and Callbacks kwargs.
            `"class_names_true"` will return a dictionnary where each key is a feature name, ie `"AutofocusZorder": value`, if `bool(value)` is True.
            `"class_names_false"` will return a dictionnary where each key is a feature name, ie `"AutofocusZorder": value`, if `bool(value)` is False.
            
            Will raise an error if not any of the above.
        
        `error`: bool
            If `True`, will raise an error if needed.
        """
        
        subclasses_name = [
            cls.__name__
            for cls in AutofocusBase.get_subclasses(exclude=BaseCharCallback, exclude_subclasses=True)
        ]

        callbacks = [
            cls.__name__
            for cls in BaseCharCallback.get_subclasses(exclude=AutofocusCallbackHandler, exclude_subclasses=True)
        ]

        filtered_kw = { }
        features_kw = { }
        callbacks_kw = { }
        all_kw = { }
        class_names_true = { }
        class_names_false = { }

        for cls, v in kwargs.items():
            # checking for non-allowed features          
            # at AutofocusDisplayable(AutofocusDropShadow=False)
            if cls in callbacks or cls in subclasses_name:
                if v is True:
                    class_names_true[cls] = v
                elif v is False:
                    class_names_false[cls] = v
                elif error:
                    raise Exception("""'"Feature_Name": Value' - Value must either be `True` or `False`, not %s""" % v)
                continue
            
            # checking for user arguments
            # at AutofocusDisplayable(AutofocusDropShadow_blur=20)
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
                filtered_kw[cls + _ + k] = v
                continue

            if error: raise Exception("Unknown -> %r" % cls)
        
        if   mode == "filter":            return filtered_kw
        elif mode == "all":               return all_kw
        elif mode == "callbacks":         return callbacks_kw
        elif mode == "features":          return features_kw
        elif mode == "both":              return features_kw, callbacks_kw
        elif mode == "class_names_true":  return class_names_true
        elif mode == "class_names_false": return class_names_false

        else: raise Exception("Unknown mode -> %r" % mode)


init 999 python hide:
    for name, char in AutofocusDisplayable.characters.items():
        char.display_args["callback"] = AutofocusCallbackHandler(name)
