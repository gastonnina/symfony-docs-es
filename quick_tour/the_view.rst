La Vista
========

Después de ver la primera parte de este tutorial, has decidido que vale la pena 
otros 10 minutos con Symfony2. ¡Excelente!. En esta segunda parte, aprenderás 
más sobre el motor de plantillas de Symfony2, `Twig`_. Twig es un flexible, 
rápido y seguro motor de plantillas para PHP que hace a tus plantillas más 
legibles y concisas, haciéndolas también más amigables para los diseñadores web.

.. note::

    En la lugar de Tiwig, también puedes usar :doc:`PHP </cookbook/templating/PHP>` 
    para tus plantillas. Ambos motores son soportados por Symfony2 y tienen el 
    mismo nivel de soporte.

Un vistazo rápido a Twig
----------------------

.. tip::

    Si quieres aprender a usar Twig, recomendamos leer su 
    `documentation`_ oficial. Esta sección es solo una vista general de los conceptos 
    principales.

Una plantilla Twig es un archivo de texto que puede generar cualquier formato 
basado en texto (HTML, XML, CSV, LaTeX, ...). Existen dos tipos de delimitadores:

* ``{{ ... }}``: Imprime una variable o el resultado de una expresión;

* ``{% ... %}``: Controla la lógica de la plantilla; es usado para ejecutar ciclos de tipo ``for`` o sentencias condicionales como el ``if``.

Abajo puedes encontrar una plantilla bien simple para mostrar las características básicas:

.. code-block:: html+jinja

    <!DOCTYPE html>
    <html>
        <head>
            <title>My Webpage</title>
        </head>
        <body>
            <h1>{{ page_title }}</h1>

            <ul id="navigation">
                {% for item in navigation %}
                    <li><a href="{{ item.href }}">{{ item.caption }}</a></li>
                {% endfor %}
            </ul>
        </body>
    </html>


.. tip::

   Se pueden comentarios dentro de las plantillas usando los delimitadores ``{# ... #}``.

Para mostrar una plantilla, puedes usar el método ``render`` desde dentro del controlador
y pasarle las variables necesarios para la plantilla::

    $this->render('AcmeDemoBundle:Demo:hello.html.twig', array(
        'name' => $name,
    ));

Las variables pasadas a la plantilla pueden ser cadenas, matrices o incluso 
objetos. Twig abstrae las diferencias entre ellos y permite acceder a "atributos" 
de una variable por medio del operador punto (``.``):

.. code-block:: jinja

    {# array('name' => 'Fabien') #}
    {{ name }}

    {# array('user' => array('name' => 'Fabien')) #}
    {{ user.name }}

    {# force array lookup #}
    {{ user['name'] }}

    {# array('user' => new User('Fabien')) #}
    {{ user.name }}
    {{ user.getName }}

    {# force method name lookup #}
    {{ user.name() }}
    {{ user.getName() }}

    {# pass arguments to a method #}
    {{ user.date('Y-m-d') }}

.. note::

    Es importante notar que las llaves no forman parte de la variable sino de 
    la impresión de la misma. Si necesitas acceder a variables dentro de 
    etiquetas, no uses las llaves.

Decorar plantillas
--------------------

Por lo general, las plantillas de un proyecto comparten elementos comunes, como 
las conocidas cabeceras y pies de página. Con Symfony2 nos gusta pensar en 
forma diferente sobre este problema: una plantilla puede ser decorada por otra. Esto 
funciona de la misma manera que las clases PHP: La herencia de plantillas permite 
construir una plantilla base denominada "layout" que contiene todos los elementos 
comunes del sitio y que define bloques para que los hijos los puedan sobrescribir.

La plantilla ``hello.html.twig`` hereda de ``layout.html.twig`` gracias a la etiqueta ``extends``:

.. code-block:: html+jinja

    {# src/Acme/DemoBundle/Resources/views/Demo/hello.html.twig #}
    {% extends "AcmeDemoBundle::layout.html.twig" %}

    {% block title "Hello " ~ name %}

    {% block content %}
        <h1>Hello {{ name }}!</h1>
    {% endblock %}

La notación ``AcmeDemoBundle::layout.html.twig`` suena familiar cierto? Es la misma 
notación utilizada para referenciar plantillas regulares. Los ``::`` significan que 
el elemento controlador esta vacío, por lo que el archivo correspondiente se 
encuentra almacenado dentro de ``views/``.

Demos una mirada a nuestro layout ``layout.html.twig``:

.. code-block:: jinja

    {# src/Acme/DemoBundle/Resources/views/layout.html.twig #}
    {% extends "::base.html.twig" %}

    {% block body %}
        <h1>Demo Bundle</h1>

        {% block content %}{% endblock %}
    {% endblock %}

La etiqueta ``{% block %}`` define dos bloques(``body`` y ``content``) para que los hijos 
lo puedan sobrescribir. Todo lo que hace esta etiqueta de tipo bloque es decirle al motor 
de plantillas que un hijo puede sobrescribir esa sección. La plantilla 
``hello.html.twig`` sobrescribe el bloque con nombre ``content``. El otro está definido en 
el layout ya que la propia plantilla se encuentra decorada por otra.. Cuando la parte 
del bundle del nombre del template está vacía (``::base.html.twig``), las vistas son buscadas 
dentro de la carpeta ``app/Resources/``. Esta carpeta almacena vistas globales para el proyecto completo.

.. code-block:: jinja

    {# app/Resources/views/base.html.twig #}
    <!DOCTYPE html>
    <html>
        <head>
            <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
            <title>{% block title %}Welcome!{% endblock %}</title>
            {% block stylesheets %}{% endblock %}
            <link rel="shortcut icon" href="{{ asset('favicon.ico') }}" />
        </head>
        <body>
            {% block body %}{% endblock %}
            {% block javascripts %}{% endblock %}
        </body>
    </html>

Usar Etiquetas, Filtros y Funciones
----------------------------

Una de las mejores funcionalidades de Twig es la extensibilidad a través de
etiquetas, filtros y funciones. Symfony2 contiene ya varias de estas para facilitar 
el trabajo del diseñador

Incluir otros templates
~~~~~~~~~~~~~~~~~~~~~~~~~

La mejor forma de compartir un fragmento de código entre varias plantillas 
diferentes es definir una plantilla que luego pueda ser incluida dentro de otra.

Crea una plantilla con el nombre ``embedded.html.twig``:

.. code-block:: jinja

    {# src/Acme/DemoBundle/Resources/views/Demo/embedded.html.twig #}
    Hello {{ name }}

And change the ``index.html.twig`` template to include it:

.. code-block:: jinja

    {# src/Acme/DemoBundle/Resources/views/Demo/hello.html.twig #}
    {% extends "AcmeDemoBundle::layout.html.twig" %}

    {# override the body block from embedded.html.twig #}
    {% block body %}
        {% include "AcmeDemoBundle:Hello:embedded.html.twig" %}
    {% endblock %}

Incluir otros controladores
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Y si la necesidad es incluir el resultado de otro controlador dentro de la 
plantilla? Esto es muy útil cuando trabajamos con Ajax o cuando la plantilla 
incluida necesita algunas variables que no existen en la plantilla principal.

Supongamos que hemos creado una acción con nombre ``fancy``, y quieres utilizarlo dentro de la 
plantilla ``index``, para esto, puedes usar la etiqueta ``render``:

.. code-block:: jinja

    {# src/Acme/DemoBundle/Resources/views/Hello/index.html.twig #}
    {% render "AcmeDemoBundle:Demo:fancy" with { 'name': name, 'color': 'green' } %}

La cadena ``AcmeDemoBundle:Demo:fancy`` hace referencia a la acción ``fancy``
del controlador ``Demo``. Los argumentos (``name`` and ``color``) actúan como variables
enviadas por la petición (como si fuera que ``fancyAction`` fuera manejado como una nueva 
petición) y de esta manera estarán habilitadas para el controlador::

    // src/Acme/DemoBundle/Controller/DemoController.php

    class DemoController extends Controller
    {
        public function fancyAction($name, $color)
        {
            // create some object, based on the $color variable
            $object = ...;

            return $this->render('AcmeDemoBundle:Demo:fancy.html.twig', array('name' => $name, 'object' => $object));
        }

        // ...
    }

Crear vínculos entre páginas
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Cuando hablamos de aplicaciones web, la creación de vínculos entre páginas 
es una necesidad. En lugar de escribir URLs en duro dentro de las plantillas, 
la función ``path`` sabe como generar URLs de acuerdo a la configuración de 
ruteo, haciendo que todas las URLs puedan ser fácilmente actualizadas con solo
modificar la configuración:

.. code-block:: html+jinja

    <a href="{{ path('_demo_hello', { 'name': 'Thomas' }) }}">Greet Thomas!</a>

La función ``path`` toma el nombre de la ruta y un array de parámetros 
como argumentos.El nombre de la ruta es la clave principal bajo las rutas que están referenciadas y los parámetros son los valores de los placeholders definidos en los patrones de las rutas::

    // src/Acme/DemoBundle/Controller/DemoController.php
    /**
     * @extra:Route("/hello/{name}", name="_demo_hello")
     * @extra:Template()
     */
    public function helloAction($name)
    {
        return array('name' => $name);
    }

.. tip::

    La función ``url`` genera URLs *absolutas* ``{{ url('_demo_hello', {
    'name': 'Thomas' }) }}``

Incluir Recursos: imágenes, JavaScripts, y hojas de estilo
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

¿Qué sería Internet sin imágenes, JavaScripts, y hojas de estilo? Symfony2 
provee la función ``asset`` para lidiar con esto fácilmente:

.. code-block:: jinja

    <link href="{{ asset('css/blog.css') }}" rel="stylesheet" type="text/css" />

    <img src="{{ asset('images/logo.png') }}" />

El principal propósito de la función ``asset`` es hacer la aplicación más 
portable. Gracias a esta función puedes mover el directorio raíz de tu aplicación 
a cualquier lugar dentro del directorio raíz de tu servidor web sin tener que 
cambiar nada en el código de tu plantilla.

Escapar salidas
---------------

Twig está configurado para escapar automáticamente todas las salidas por 
omisión. Lee la `documentation`_ de Twig para aprender más sobre como escapar 
salidas y sobre la extensión Escaper.

Pensamientos finales
--------------

Twig es simple pero poderoso. Gracias a los layouts, bloques, 
plantillas y la inclusión de acciones, es muy sencillo organizar 
tus plantillas de una forma lógica y extensible.

Haz trabajado con Symfony2 por nada más que 20 minutos y ya puedes crear 
varias cosas interensates. Este es el poder de Symfony2. Aprender la parte 
básica es sencilla y pronto te darás cuenta que la simplicidad esta escondida bajo 
una arquitectura muy flexible.

Pero estoy yendo demasiado rápido. Primero necesitas aprender más sobre los 
controladores y es exactamente de esto de lo que hablamos en la próxima parte 
de este tutorial. Preparado para otros 10 minutos con Symfony2?

.. _Twig:          http://www.twig-project.org/
.. _documentation: http://www.twig-project.org/documentation