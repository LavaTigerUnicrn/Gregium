gregium.misc
============

Miscellaneous helper functions

.. autoclass:: gregium.misc.ProgressBar

    .. warning::
        
        Most terminals used monospaced fonts, but for fonts that aren't monospaced, the progress bar will change size if the width of `completed_char` differs from `empty_char`.

    .. automethod:: __call__

.. autofunction:: gregium.misc.colorAscii
.. autofunction:: gregium.misc.format_time
.. autofunction:: gregium.misc.import_absolute
.. autofunction:: gregium.misc.load_audio
.. autofunction:: gregium.misc.interpolate
    
    .. note::
        
        The generator can start an iterator multiple times and will not preserve data between one another.

        .. code-block:: python3

            from gregium.misc import interpolate

            interpolate_obj = interpolate((255,0,0),(0,255,0),50)

            iter1 = iter(interpolate_obj)
            iter2 = iter(interpolate_obj)
            # Both iter1 and iter2 are unique and can be iterated through separately to move from red to green

            for color in iter1: # red to green

                print(color)

            for color in iter2: # red to green

                print(color)

.. autofunction:: gregium.misc.listdir_recurse
.. autofunction:: gregium.misc.format_md