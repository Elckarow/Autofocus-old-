init -4 python:
    class AutofocusCallbackHandler(BaseCharCallback):
        """
        Passed as character callback.

        Attributes
        ----------
        `callbacks`: dict[tuple[str], list[BaseCharCallback]]
             A dictionnary mapping an image tag to callback features.

        `current_showing`: str | None
            Current tag showing of `name`, ie `sayori turned` or `sayori tap`, or None if not found.
        
        `callback_kwargs`: dict[tuple[str], dict[str, dict[str, Any]]] [Class Variable]
            Stores kwargs for callbacks. Fetched by the `add_callback` method.

            This dict has three layers.
            `full image tag as tuple` -> `("sayori", "turned")`
            `callback class name` -> `"AutofocusMouth"`
            `kwargs` -> `"begin_parameter"`
        
            So by the above example, to get `begin_parameter` for `AutofocusMouth`, you'd do `AutofocusCallbackHandler.callback_kwargs[("sayori", "turned")]["AutofocusMouth"]["begin_parameter"]`
        """

        allowed_args = None

        callback_kwargs = { }
        common_callback = { }

        def __init__(self, name):
            AutofocusBase.__init__(self, name=name)
            self.callbacks = { }
            self.current_showing = None
            
            callbacks = BaseCharCallback.get_subclasses(exclude=AutofocusCallbackHandler, exclude_subclasses=True)

            for name, cls_and_kwargs in self.callback_kwargs.items():
                if name[0] == self.name:
                    self.callbacks[name] = [ ]

                    for cls in callbacks:
                        if not cls.is_allowed(): continue
                        self.callbacks[name].append(cls(name=self.name, **cls_and_kwargs.setdefault(cls.__name__, {})))

        def __call__(self, event, interact=True, **kwargs):
            self.handle_showing()

            if self.current_showing is None: return
            
            for c in self.callbacks[self.current_showing]:
                c(event, interact, **kwargs)

        def handle_showing(self):
            self.set_attributes()

            for char in self.callbacks:
                if renpy.showing(char, self.layer):
                    self.current_showing = char
                    break

            else:
                self.current_showing = None

        @classmethod
        def add_callback(cls, name, kwargs, common=False):
            tag = name[0]

            if common:
                if tag not in cls.common_callback:
                    cls.common_callback[tag] = kwargs
                
                for k, v in cls.callback_kwargs.items():
                    if k[0] == tag and v != cls.common_callback[tag]:
                        cls.callback_kwargs[k] = cls.common_callback[tag]

                cls.callback_kwargs[name] = cls.common_callback[tag]

            else:
                if tag in cls.common_callback:
                    cls.callback_kwargs[name] = cls.common_callback[tag]
                
                else:
                    cls.callback_kwargs[name] = kwargs

