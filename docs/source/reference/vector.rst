gregium.vector
==============

Standard vectors for math

.. note::

    When performing operations on Vectors, each value of the Vector will run on the same placed other one.

    If one is a Vector and another is a number (float/int), the operation will be applied on all values of the Vector.

    When performing operations on two Vectors, the shorter length Vector is used as the length of the new Vector, truncating as required.

    .. code-block:: python3

        >>> from gregium.vector import Vector
        >>> Vector(3,5) + 5
        Vector(8, 10)
        >>> Vector(3,5) + Vector(2,9)
        Vector(5, 14)
        >>> Vector(3,9) + Vector(5,5,5) # Higher dimensions ignored
        Vector(8, 14)

.. important::

    Vectors are strictly typed as either being an integer or float Vector to keep easier track of; however, this will make linters call out incorrect typing if you attempt to run operations on them, but has no real danger.

    .. code-block:: python3

        from gregium.vector import Vector

        vec1:Vector[int] = Vector(3)
        vec2:Vector[float] = Vector(3.5)

        vec3:Vector[float] = vec1 + vec2 # Linters may warn you on this line, just be mindful of typing

.. autoclass:: gregium.vector.Vector
    :members:

    .. note::

        Only a 2D vector have the functions `as_polar`, `angle`, and `from_polar`

.. autofunction:: gregium.vector.Vector2
.. autofunction:: gregium.vector.Vector3
.. autofunction:: gregium.vector.Vector4