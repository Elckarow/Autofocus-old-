init -100 python in AutofocusStore:
    """
    This substore contains variables needed for controlling whether these features can be used or not, as well as informations about the project.
    """
    
    __author__ = "Pseurae#6758", "Elckarow#8399"
    __version__ = (1, 3, 0)

    autofocus_coloring = True
    autofocus_dropshadow = True
    autofocus_interpolation_minimum_char_requirement = 2
    autofocus_filter = True
    autofocus_zoom = True
    autofocus_zorder = True
    autofocus_mouth = True

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
        


init -99 python in AutofocusStore:
    def redraw_char(f):
        def redraw():
            f()
            
            for img in AutofocusDisplayable.characters:
                if not renpy.showing(None, img): continue
                renpy.redraw(img, 0.0)
                
        return redraw
    
    
    @redraw_char
    def enable_coloring():
        global autofocus_coloring
        autofocus_coloring = True
        
    @redraw_char
    def enable_dropshadow():
        global autofocus_dropshadow
        autofocus_dropshadow = True
    
    @redraw_char
    def enable_filter():
        global autofocus_filter
        autofocus_filter = True
        
    @redraw_char
    def enable_zoom():
        global autofocus_zoom
        autofocus_zoom = True
    
    @redraw_char
    def enable_zorder():
        global autofocus_zorder
        autofocus_zorder = True
        
    @redraw_char
    def enable_mouth():
        global autofocus_mouth
        autofocus_mouth = True
    
    
    
    @redraw_char
    def disable_coloring():
        global autofocus_coloring
        autofocus_coloring = False
        
    @redraw_char
    def disable_dropshadow():
        global autofocus_dropshadow
        autofocus_dropshadow = False
    
    @redraw_char
    def disable_filter():
        global autofocus_filter
        autofocus_filter = False
        
    @redraw_char
    def disable_zoom():
        global autofocus_zoom
        autofocus_zoom = False
    
    @redraw_char
    def disable_zorder():
        global autofocus_zorder
        autofocus_zorder = False
        
    @redraw_char
    def disable_mouth():
        global autofocus_mouth
        autofocus_mouth = False
