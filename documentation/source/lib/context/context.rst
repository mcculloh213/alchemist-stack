Alchemist Stack: Context Class
---------------------------------------------

.. py:class:: Context(settings : dict)

    A class containing the context used to connect to a database.

    .. py:method:: __init__(settings: dict)

        The :class:`Context` constructor. It takes in a `dict` of String keys and values to create the
        :class:`sqlalchemy.engine.base.Engine` and :class:`sqlalchemy.orm.session.Session` used to interact with a
        database.

    .. py:method:: __call__() -> sqlalchemy.orm.session.Session

        Calling an instance of :class:`Context` will return a :class:`sqlalchemy.orm.session.Session`