init -5 python:
    from __future__ import print_function
    
    class AutofocusDropShadow(AutofocusDisplayable):
        """
        A class used to add a drop shadow effect. 

        Attributes
        ----------
        `child`: renpy.Displayable
            The base displayable.
        
        `child_ds`: Fixed
            The displayable with the drop shadow effect on.

        `xoffset`: int | float
            How far on the x axis the drop shadow effect will be set.
        
        `yoffset`: int | float
            How far on the y axis the drop shadow effect will be set.
        
        `offset`: tuple[int | float]
            If passed, should be a 2-element tuple contanining the `xoffset` and `yoffset` values.

        `blur`: int | float
            How much blur the drop shadow effect will have. Stored as attribute to prevent resizing issues when rendering.
        
        `color`: tuple[int | float] | str
            A value passed to the ColorMatrix `TintMatrix` that will change the color of the `transform_child`.
        
        `brightness`: int | float
            A value passed to the ColorMatrix `BrightnessMatrix` that will change the brightness of the `transform_child`.
        """

       allowed_args = (
            "xoffset",
            "yoffset",
            "offset",
            "blur",
            "color",
            "brightness"
        )

        def __init__(self, child, name, xoffset=0, yoffset=0, blur=10, color="#000", brightness=1.0, **kwargs):
            super(AutofocusDropShadow, self).__init__()
           
            offset = kwargs.get("offset", None)

            if offset is not None:
                xoffset, yoffset = offset
            
            self.child = child
            self.blur = blur

            self.transform_child = Transform(
                                        child,
                                        anchor=(0.0, 0.0),
                                        xoffset=xoffset,
                                        yoffset=yoffset,
                                        matrixcolor=TintMatrix(color) * BrightnessMatrix(brightness),
                                        subpixel=True
                                    )

            self.child_ds = Flatten(
                                Fixed(
                                    self.transform_child,
                                    child,
                                    fit_first=True
                                )
                            )
        
        @staticmethod
        def is_allowed():
            if not renpy.version(tuple=True) >= (7, 4, 0):
                print("---[INCOMPATIBLE VERSION - %r - EXPECTED Ren'Py 7.4.0 OR ABOVE]--- AutofocusDropShadow disabled" % renpy.version())
                return False

            return config.gl2

        @staticmethod
        def is_on():
            return AutofocusStore.autofocus_dropshadow
        
        def render(self, w, h, st, at):
            if not self.is_on():
                rv = renpy.render(self.child, w, h, st, at)
            else:
                rv = renpy.render(self.child_ds, w, h, st, at)

            return rv
