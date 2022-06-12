# Autofocus
A Ren'Py tool that aims at making character dialogues less of a chore to write.





As of now the tool contains 5 features (and only works for Ren'Py 7):

`Autozoom`
-zooms the character in when they are speaking.

`Autozorder`
-changes the character's zorder when they are speaking.

`Autofilter`
-darkens the character when they are not speaking.

`Automouth`
-changes the character's mouth when they are speaking.

`Coloring`
-colors the character.

`DropShadow`
-adds a drop shadow effect to the character sprites

a more in-depth guide of each feature is included in the package.
each feature can be enabled / disabled thanks to the corresponding variable found in `01AutofocusStore.rpy`

-
-
-
-

(taking ddlc modding as an example)
using this tool allows this
```
show monika forward neut at t21 zorder 2
show sayori turned neut om at f22 zorder 3
s "Sayori is talking!"
show sayori cm at t22 zorder 2
show monika om at f21 zorder 3
m "Now Monika is talking."
show monika cm at t21 zorder 2
show sayori om at f22 zorder 3
s "Now Sayori is talking."
show sayori cm at t22 zorder 2
show monika om at f21 zorder 3
m "Now Monika is talking."
show monika cm at t21 zorder 2
show sayori om at f22 zorder 3
s "Now Sayori is talking."
show sayori cm at t22 zorder 2
show monika om at f21 zorder 3
m "Now Monika is talking."
show monika cm at t21 zorder 2
show sayori om at f22 zorder 3
s "Now Sayori is talking."
```

to be shortened to this

```
show monika forward neut at t21 zorder 2
show sayori turned neut at t22 zorder 2
s "Sayori is talking!"
m "Now Monika is talking."
s "Now Sayori is talking."
m "Now Monika is talking."
s "Now Sayori is talking."
m "Now Monika is talking."
s "Now Sayori is talking."
```
