init -5 python:
    from __future__ import print_function
    
    class AutofocusMouth(BaseCharCallback):
        """
        A class used to automatically change mouths.
        Only works if the mouth attributes are defined within the `mouth` group.

        Attributes
        ----------
        `mouth_tags`: set[str]
            The different mouth tags used. Takes into account every image defined with `name` as image tag.
        """

        def __init__(self, name, begin_parameter="om", end_parameter="cm", **kwargs):
            super(AutofocusMouth, self).__init__(name=name, begin_parameter=begin_parameter, end_parameter=end_parameter)

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
                and attr.attribute not in [begin_parameter, end_parameter]
            )

        def condition(self):
            other_mouth_applied = bool(self.mouth_tags & self.attributes)
            return AutofocusStore.autofocus_mouth and not other_mouth_applied

        def do_stuff(self, mouth):
            renpy.show("%s %s" % (self.name, mouth), layer=self.layer, zorder=None)
        
        def set_attributes(self):
            super(AutofocusMouth, self).set_attributes()
            self.attributes = set(self.attributes)
        
        @staticmethod
        def is_allowed():
            if not renpy.version(tuple=True) >= (7, 0):
                print("---[INCOMPATIBLE VERSION - %s - EXPECTED Ren'Py 7.0 OR ABOVE]--- AutofocusMouth disabled" % renpy.version())
                return False

            return True

