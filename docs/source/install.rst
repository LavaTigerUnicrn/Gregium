Installation
============

Gregium must be installed using pip::

    python3 -m pip install --upgrade gregium

.. note::
    
    Gregium should support python versions at least 3.9+ (and may support older versions too), but is primarily tested on 3.12, some modules may have unexpected behavior on different versions, or require specific library installations

Gregium automatically will install some dependencies, but not all are installed due to size. To fix this issue you can either run::

    python3 -m gregium --verify

Which will scan for all missing libraries that don't come pre-installed

Alternatively, whenever a module attempts to import a library that might not exist, it will check and inform the user if it is missing