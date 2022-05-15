init -100 python in AutofocusStore:
    """
    This substore contains variables needed for controlling whether these features can be used or not, as well as informations about the project.
    """
    
    __author__ = "Pseurae#6758", "Elckarow#8399"
    __version__ = (1, 3, 0)

    autofocus_coloring = True
    autofocus_dropshadow = False
    autofocus_interpolation_minimum_char_requirement = 2
    autofocus_filter = True
    autofocus_zoom = True
    autofocus_zorder = True
    autofocus_mouth = False

    def version(tuple=False):
        """
        If `tuple` is `False`, returns a string containing "Autofocus ", followed by the current version of the project.
        If `tuple` is `True`, returns a tuple giving each component of the version as an integer.
        """
        global __version__

        if tuple: return __version__
        return "Autofocus " + ".".join([str(x) for x in __version__])
    
    def authors(tuple=False):
        """
        If `tuple` is `False`, returns a string containing every authors separated by ", ".
        If `tuple` is `True`, returns a tuple containing each author as a string.
        """
        global __author__

        if tuple: return __author__
        return ", ".join(__author__)
