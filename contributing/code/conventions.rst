Convenciones
============

The :doc:`standards` describe el estándar de codificación para el proyecto
Symfony2 y los paquetes internos y de terceras partes. Este documento describe
los estándares de codificación y las convenciones utilizadas en el framework
principal para hacerlo más consistente y predictible. Puedes seguir éstos
estándares en tu propio código, aunque ello no es nesesario.

Nombre de los Métodos
---------------------

Cuando un objeto tiene una relación "principal" múltiple con "cosas"
relacionadas (objetos, parámetros, ...), los nombres de los métodos son
normalizados:

  * ``get()``
  * ``set()``
  * ``has()``
  * ``all()``
  * ``replace()``
  * ``remove()``
  * ``clear()``
  * ``isEmpty()``
  * ``add()``
  * ``register()``
  * ``count()``
  * ``keys()``

La utilización de éstos métodos esta permitido únicamente cuando está claro
que existe una relacion principal:

* un ``Tarro de Galletita`` tiene muchos objetos ``Galletita``;

* un ``Contenedor`` de Servicios tiene muchos servicios y muchos parámetros
  (como servicios es la relación principal, utilizamos la convención de nombres
  para esta relación);

* una ``Entrada`` de Consola tiene muchos argumentos y muchas opciones. No
  existe una relación principal, y por ello la convención de nombres no aplica.

Para muchas relaciones donde la convención de nombres no aplica, los siguientes
métodos deben ser utlizados (donde ``XXX`` es el nombre de la cosa relacionada):

================== =================
Relación Principal  Otras Relaciones
================== =================
``get()``          ``getXXX()``
``set()``          ``setXXX()``
``has()``          ``hasXXX()``
``all()``          ``getXXXs()``
``replace()``      ``setXXXs()``
``remove()``       ``removeXXX()``
``clear()``        ``clearXXX()``
``isEmpty()``      ``isEmptyXXX()``
``add()``          ``addXXX()``
``register()``     ``registerXXX()``
``count()``        ``countXXX()``
``keys()``         n/a
================== =================
