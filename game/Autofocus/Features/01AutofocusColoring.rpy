init -5 python:
    from __future__ import print_function
    
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

        def __init__(self, child, **kwargs):
            super(AutofocusColoring, self).__init__()
            self.child = Transform(child)

            self.matrix = IdentityMatrix()

        @staticmethod
        def is_allowed():
            if not renpy.version(tuple=True) >= (7, 4, 0):
                print("---[INCOMPATIBLE VERSION - %r - EXPECTED Ren'Py 7.4.0 OR ABOVE]--- AutofocusColoring disabled" % renpy.version())
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
