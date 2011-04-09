El Controlador
==============

¿ Aún con nosotros después de las primeras dos partes ? Ya te estás 
volviendo un adicto a Symfony2. Sin más preámbulos, descubramos lo que
los controladores pueden hacer por tí. 

Uso de formatos de salida
--------------------------

En la actualidad, una aplicación web debería estar en capacidad de
generar respuestas no sólo como páginas HTML. Desde XML para fuentes RSS o
servicios Web, hasta JSON para peticiones AJAX, hay variedad de formatos de
donde escoger. El soporte para estos formatos en Symfony2 es realmente
sencillo. Se debe ajustar la ruta añadiendo un valor por omisión como
``xml`` para la variable ``_format``::  

    // src/Acme/DemoBundle/Controller/DemoController.php
    /**
     * @extra:Route("/hello/{name}", defaults={"_format"="xml"}, name="_demo_hello")
     * @extra:Template()
     */
    public function helloAction($name)
    {
        return array('name' => $name);
    }

De acuerdo al formato de respuesta (definido por el valor de ``_format``)
Symfony2 selecciona automáticamente la plantilla correcta, en este caso 
``hello.xml.twig``:

.. code-block:: xml+php

    <!-- src/Acme/DemoBundle/Resources/views/Demo/hello.xml.twig -->
    <hello>
        <name>{{ name }}</name>
    </hello>

Es todo lo que hay que hacer. Para formatos estándar, Symfony2 también 
selecciona la cabecera ``Content-Type`` adecuada para la respuesta. Si quieres
soportar diferentes formatos para una sola acción, usa el marcador de posición
``{_format}`` en el patrón que define la ruta::

    // src/Acme/DemoBundle/Controller/DemoController.php
    /**
     * @extra:Route("/hello/{name}.{_format}", defaults={"_format"="html"}, requirements={"_format"="html|xml|json"}, name="_demo_hello")
     * @extra:Template()
     */
    public function helloAction($name)
    {
        return array('name' => $name);
    }

El controlador será llamado por urls como: ``/demo/hello/Fabien.xml`` o
``/demo/hello/Fabien.json``.

El parámetro ``requirements`` define una expresión regular que el marcador
de posición debe cumplir. En este caso, si intentas hacer una petición al
recurso ``/demo/hello/Fabien.js``, obtendrás un error de tipo 404, debido 
a que no se cumple la expresión establecida en ``_format``. 

Redirección y reenvío
----------------------

Si quieres redirigir al usuario a otra página, usa la clase ``RedirectResponse``::

    return new RedirectResponse($this->generateUrl('_demo_hello', array('name' => 'Lucas')));

El método ``generateUrl()`` es el mismo que la función ``path()`` usada en
las plantillas. Este toma el nombre de la ruta y un arreglo de parámetros como
argumentos y retorna la url asociada.     

También puedes fácilmente pasar de una acción a otra con el método ``forward()``. 
Para los helpers asociados a las ``acciones``, este realiza una sub-petición interna, 
pero retorna un objeto ``Response`` que permite modificaciones posteriores::


    $response = $this->forward('AcmeDemo:Hello:fancy', array('name' => $name, 'color' => 'green'));

    // hacer algo con el objeto respose o retornarlo 

Obtener información de la petición
------------------------------------

Además de los valores de los marcadores de posición (placeholders) del
sistema de enrutamiento, el controlador también tiene acceso a el objeto
``Request``::

    $request = $this->get('request');

    $request->isXmlHttpRequest(); // ¿ es una petición Ajax ?

    $request->getPreferredLanguage(array('en', 'fr'));

    $request->query->get('page'); // obtiene un parámetro del arreglo $_GET

    $request->request->get('page'); // obtiene un parámetro del arreglo $_POST

En una plantilla, tienes acceso a el objeto ``Request`` a través de la 
variable ``app.request``:

.. code-block:: html+php

    {{ app.request.query.get('page') }}

    {{ app.request.parameter('page') }}


Persistencia de datos en la sesión
----------------------------------

Aún cuando el protocolo HTTP no almacena estados, Symfony2 provee un elegante
objeto de sesión que representa el cliente (puede ser una persona real usando
un navegador, un bot o un servicio web). Entre dos peticiones, Symfony2 almacena
los atributos en una cookie usando sesiones nativas de PHP. 

El almacenamiento y la recuperación de información de la sesión se logra
fácilmente desde cualquier controlador::

    $session = $this->get('request')->getSession();

    // se almacena un atributo para reuso en una próxima petición
    $session->set('foo', 'bar');

    // se recupera en otro controlador para otra petición
    $foo = $session->get('foo');

    // establece la localización del usuario
    $session->setLocale('fr');

También puedes almacenar pequeños mensajes que solamente estarán disponibles
en la próxima petición::

    // almacenar un mensaje para la próxima petición (en un controlador)
    $session->setFlash('notice', 'Felicitaciones, proceso realizado!');

    // mostrar el mensaje anterior en la próxima petición (en una plantilla)
    {{ app.session.flash('notice') }}

Asegurando los recursos
-----------------------

La edición estándar de Symfony viene con un configuración de seguridad 
sencilla que se ajusta a las necesidades más comúnes:

.. code-block:: yaml

    # app/config/security.yml
    security:
        encoders:
            Symfony\Component\Security\Core\User\User: plaintext

        role_hierarchy:
            ROLE_ADMIN:       ROLE_USER
            ROLE_SUPER_ADMIN: [ROLE_USER, ROLE_ADMIN, ROLE_ALLOWED_TO_SWITCH]

        providers:
            in_memory:
                users:
                    user:  { password: userpass, roles: [ 'ROLE_USER' ] }
                    admin: { password: adminpass, roles: [ 'ROLE_ADMIN' ] }

        firewalls:
            login:
                pattern:  /demo/secured/login
                security: false

            secured_area:
                pattern:    /demo/secured/.*
                form_login:
                    check_path: /demo/secured/login_check
                    login_path: /demo/secured/login
                logout:
                    path:   /demo/secured/logout
                    target: /demo/

Con esta configuración un usuario debe iniciar sesión para ingresar en cualquiera
de las urls que inician con ``/demo/secured/`` y se definem dos usuarios válidos: 
``user`` y ``admin``. Además el usuario ``admin`` tiene el rol ``ROLE_ADMIN``,
el cual incluye el rol ``ROLE_USER`` también. (ver el parámetro ``role_hierarchy``).  


.. tip::

    Por legibilidad, las claves se almacenan en texto plano para esta
    configuración, para el uso de algoritmos de hash es necesario ajustar
    la sección ``encoders``.  

Al entrar en la url: ``http://localhost/Symfony/web/app_dev.php/demo/secured/hello``
serás automáticamente redireccionado al formulario de login ya que este recurso
se encuentra protegido por un firewall (via el formulario de login). 

También puedes forzar para que un rol determinado sea requerido usando
la anotación ``@extra:Secure`` en el controlador::

    /**
     * @extra:Route("/hello/admin/{name}", name="_demo_secured_hello_admin")
     * @extra:Secure(roles="ROLE_ADMIN")
     * @extra:Template()
     */
    public function helloAdminAction($name)
    {
        return array('name' => $name);
    }

Inicia sesión con el usuario ``user`` y desde la página de bienvenida que
se encuentra protegida, haz click en el enlace: "Hello resource secured";
Symfony2 deberia retornar un error HTTP de tipo 403. 


.. note::

    La capa de seguridad de Symfony2 es muy flexible e integra varios formas
    para manejo de usuarios (como una para el ORM Doctrine) y para autenticación
    (por HTTP básica, HTTP digest o certificados X509). Lee el capítulo del libro
    sobre "`Seguridad`_" para más información sobre cómo usarlas y configurarlas.      


Utilizando cache para los recursos
----------------------------------

Tan pronto como tu sitio web empiece a generar más tráfico, querás evitar la
generación del mismo recurso con cada petición. Symfony2 usa las cabeceras
HTTP de cache para manejar los recursos en cache. Para una sencilla estrategia
de cacheo, usa la anotación ``@extra:Cache()``::

    /**
     * @extra:Route("/hello/{name}", name="_demo_hello")
     * @extra:Template()
     * @extra:Cache(maxage="86400")
     */
    public function helloAction($name)
    {
        return array('name' => $name);
    }

En este ejemplo, el recurso será almacenado en cache por un día. Puedes
usar también la validación en vez de la expiración o una combinación de ambas
si esto se ajusta más a tus necesidades. 


Resource caching is managed by the Symfony2 built-in reverse. But as caching
is only managed by regular HTTP cache headers, you can also replace it with
Varnish or Squid and easily scale your application.

.. note::

    But what if you cannot cache whole pages? Symfony2 still has the solution
    via Edge Side Includes (ESI) that are supported natively. Learn more by
    reading the "`HTTP Cache`_" chapter of the book.

Final Thoughts
--------------

That's all there is to it, and I'm not even sure we have spent the allocated
10 minutes. We briefly introduced bundles in the first part; and all the
features we've learned about until now are part of the core framework bundle.
But thanks to bundles, everything can be extended or replaced in Symfony2.
That's the topic of the next part of this tutorial.

.. _Security:   http://symfony.com/doc/2.0/book/security/index.html
.. _HTTP Cache: http://symfony.com/doc/2.0/book/http_cache.html
