init -100 python in AutofocusStore:
    """
    This substore contains variables needed for controlling whether these features can be used or not, as well as informations about the project.
    """
    
    __author__ = "Pseurae#6758", "Elckarow#8399"
    __version__ = (1, 5, 0)

    autofocus_coloring = True
    autofocus_dropshadow = True
    autofocus_minimum_char_requirement = 2
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
        


init 1 python in AutofocusStore:
    from store import AutofocusDisplayable, get_layer

    def redraw_autofocus(f):
        """
        Calls `f`, then redraws all characters that are using `Autofocus`.
        """

        def redraw(*args, **kwargs):
            rv = f(*args, **kwargs)
            
            for img in AutofocusDisplayable.characters:
                renpy.redraw(img, 0.0)
            
            return rv
                
        return redraw
    
    #####
    # The following functions are used to enable / disable features dynamically,
    # which means that instead of doing
    #
    # $ AutofocusStore.autofocus_dropshadow = False
    #
    # you should do
    #
    # $ AutofocusStore.disable_dropshadow()
    #
    #
    #
    # If you want to make a function that will redraw the characters in the same way,
    # just decorate your function with @AutofocusStore.redraw_autofocus
    
    @redraw_autofocus
    def enable_coloring():
        global autofocus_coloring
        autofocus_coloring = True
        
    @redraw_autofocus
    def enable_dropshadow():
        global autofocus_dropshadow
        autofocus_dropshadow = True
    
    @redraw_autofocus
    def enable_filter():
        global autofocus_filter
        autofocus_filter = True
        
    @redraw_autofocus
    def enable_zoom():
        global autofocus_zoom
        autofocus_zoom = True
    
    @redraw_autofocus
    def enable_zorder():
        global autofocus_zorder
        autofocus_zorder = True
        
    @redraw_autofocus
    def enable_mouth():
        global autofocus_mouth
        autofocus_mouth = True
    
    ##########################################
    
    @redraw_autofocus
    def disable_coloring():
        global autofocus_coloring
        autofocus_coloring = False
        
    @redraw_autofocus
    def disable_dropshadow():
        global autofocus_dropshadow
        autofocus_dropshadow = False
    
    @redraw_autofocus
    def disable_filter():
        global autofocus_filter
        autofocus_filter = False
        
    @redraw_autofocus
    def disable_zoom():
        global autofocus_zoom
        autofocus_zoom = False
    
    @redraw_autofocus
    def disable_zorder():
        global autofocus_zorder
        autofocus_zorder = False
        
    @redraw_autofocus
    def disable_mouth():
        global autofocus_mouth
        autofocus_mouth = False
