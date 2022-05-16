init -5 python:
    class AutofocusZorder(BaseCharCallback):
        """
        A class used to automatically change zorder.
        """

        def __init__(self, name, begin_parameter=3, end_parameter=2, **kwargs):
            super(AutofocusZorder, self).__init__(name=name, begin_parameter=begin_parameter, end_parameter=end_parameter)

        def condition(self):
            return AutofocusStore.autofocus_zorder and self.character_visible_num() >= AutofocusStore.autofocus_interpolation_minimum_char_requirement

        def do_stuff(self, zorder):
            if hasattr(renpy, "change_zorder"):
                renpy.change_zorder(self.layer, self.name, zorder)
            else:
                renpy.show(self.name, layer=self.layer, zorder=zorder)