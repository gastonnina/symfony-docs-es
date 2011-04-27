Enviar un Parche
================

Los parches son la mejor manera de proveer una corrección a un error o
proponer mejoas a Symfony2.

Configuración Inicial
---------------------

Antes de trabajar en Symfony2, configura un entorno amigable con los
siguientes programas:

* Git;

* PHP versión 5.3.2 o superior;

* PHPUnit 3.5.11 o superior.

Establece tu información de usuario con tu nombre real y tu una dirección
de correo electrónico de trabajo:

.. code-block:: bash

    $ git config --global user.name "Tu Nombre"
    $ git config --global user.email tu.email@ejemplo.com

.. tip::

    Si eres nuevo en Git, te recomendamos que leas el libro exelente y
    gratuito `ProGit`_.

Obtener el código fuente de Symfony2:

* Crea una cuenta `GitHub`_ e ingresa;

* Has una copia del `repositorio de Symfony2`_ (click en el boton "Copiar");

* Después que la "acción de copiado duro" se ha completado, clona
  tu copia localmente (esto creará un directorio `symfony`):

.. code-block:: bash

      $ git clone git@github.com:TU-NOMBRE/symfony.git

* Agrega el repositorio principal como ``remote``:

.. code-block:: bash

      $ cd symfony
      $ git remote add upstream git://github.com/symfony/symfony.git

Ahora que Symfony2 está instalado, comprueba que todas las pruebas unitarias
se ejecutan con éxito para tu entorno, como se explica en el
:doc:`documento <tests>` dedicado.

Trabajar en un Parche
---------------------

Cada vez que desees trabajar en un parche para un error o una mejora, crea una
rama del tema:

.. code-block:: bash

    $ git checkout -b NOMBRE_DE_RAMA

.. tip::

    Usa un nombre descriptivo para tu rama (`ticket_XXX` en donde `XXX` es el
    número del ticket, es una buena convención para corrección de errores).

El comando anterior cambia automaticamente el código a la rama recientemente
creada (comprueba la rama en la que estas trabajando con `git branch`).

Trabaja en el código tanto como desees y has tantos commits como desees; pero
mantén en mente lo siguiente:

* Sigue los :doc:`estándares <standards>` de código (usa `git diff --check`
  para verifcar los espacios finales);

* Agrega pruebas unitarias para demostrar que el error está corregido o que la
  nueva característica realmente funciona;

* Has commits separados logica y atómicamente (usa el poder de `git rebase`
  para tener un historial limpio y lógico);

* Escribe buenos mensajes de commit.

.. tip::

    Un buen mensaje de commit está compuesto de un sumario (la primera línea),
    seguido opcionalmente por una línea en blanco y una descripción más
    detallada. El sumario debería comenzar con el Componente en el que estas
    trabajando, señalado en corchetes (``[DependencyInjection]``,
    ``[FrameworkBundle]``, ...). Usa un verbo (``fixed ...``, ``added ...``,
    ...) para iniciar el sumario y no agregues un punto al final.

Enviar un Parche
----------------

Antes de enviar tu parche, actualiza tu rama (es necesario si te toma un tiempo
mientras terminas tus cambios):

.. code-block:: bash

    $ git checkout master
    $ git fetch upstream
    $ git merge upstream/master
    $ git checkout NOMBRE_RAMA
    $ git rebase master

Cuando se ejecuta el comando `rebase`, es posible que tengas que corregir y
combinar conflictos. `git st` indica los archivos *sin combinar*. Resuelve
todos los conflictos y continúa con el `rebase`:

.. code-block:: bash

    $ git add ... # agrega los archivos resueltos
    $ git rebase --continue

Verifica que todos las pruebas siguen ejecutandose existosamente y empuja tu
rama remotamente:

.. code-block:: bash

    $ git push origin NOMBRE_RAMA

Ahora puedes discutir tu parche en la `lista de correos dev`_ o envía una
solicitud (debe estar hecho sobre el repositorio ``symfony/symfony``). Para
facilitar el trabajo del equipo principal, incluye siempre el nombre de los
componentes modificados en tu solicitud, como en:

.. code-block:: text

    [Yaml] un cambio
    [Form] [Validator] [FrameworkBundle] otro cambio

Si envías un email a la lista de correo, no olvides referenciar a la url de tu
rama (``https://github.com/NOMBRE_USUARIO/symfony.git NOMBRE_RAMA``) o la url de la
solicitud.

Basado en la retroalimentación de la lista de correos o a travéz de la solititud
en GitHub, es posible que necesites reveer tu parche. Antes de reenviar el parche,
reajusta con `master`, sin combinar; y obliga el empuje a `origin`:

.. code-block:: bash

    $ git rebase -f upstream/master
    $ git push -f origin NOMBRE_RAMA

.. note::

    Todos los parches que envíes deben ser publicados bajo la licencia MIT, a
    menos que sea explícitamente indicado en el código.

.. _ProGit:               http://progit.org/
.. _GitHub:               https://github.com/signup/free
.. _repositorio Symfony2: https://github.com/symfony/symfony
.. _lista de correos dev: http://groups.google.com/group/symfony-devs
