Estándar de Codificación
========================

Cuando contribuyes código a Symfony2, debes seguir su estándar de
codificación. Para hacer corta la historia, esta es la regla de oro:
*Imita el código existente de Symfony2*.

Estructura
----------

* Nunca utilices las etiquetas cortas (`<?`);

* No finalices las clases con la etiqueta usual de cierre (`?>`);

* La indentación se realiza utilizando cuatro espacios (tabulaciones no
  están permitidas);

* Utiliza el caracter de salto de línea (`0x0A`) para finalizar las líneas;

* Agrega un único espacio después de cada delimitador coma;

* No pongas espacios después de la apertura de un paréntesis y antes del
  cierre del mismo;

* Agrega un único espacio alrededor de operadores (`==`, `&&`, ...);

* Agrega un único espacio antes de los paréntesis de apertura de una palabra
  clave de control (`if`, `else`, `for`, `while`, ...);

* Agrega una línea en blanco antes de la sentencia `return`;

* No agregues espacios al final de las líneas;

* Utiliza llaves para indicar el cuerpo de las estructuras de control sin
  importar el número de sentencias que éstas contengan;

* Coloca las llaves en sus propias líneas para clases, métodos y declaración
  de funciones;

* Separa las sentencias condicionales y las llaves de apertura con un único
  espacio sin dejar una línea en blanco;

* Declara explícitamente la visibilidad de clases, métodos y propiedades (el
  uso de `var` está prohibido);

* Utiliza constantes de tipo PHP nativas en minúsculas: `false`, `true` y `null`.
  Lo mismo aplica para `array()`;

* Utiliza letras mayúsculas para constantes, con palabras separadas por guiónes
  bajos;

* Define una clase por archivo;

* Declara las propiedades de las clases antes de los métodos;

* Declara los métodos públicos primero, luego los protegidos y finalmente
  los privados.

Convención de Nombres
---------------------

* Utiliza camelCase y no guiones bajos, para variables, funciones y nombres de
  métodos;

* Utiliza guiones bajos para definir opciones, argumentos y nombres de
  parámetros;

* Utiliza los `namespace` para todas las clases;

* Utiliza `Symfony` como el `namespace` de primer nivel;

* Añade como sufijo `Interface` a las interfaces;

* Utiliza caractéres alfanuméricos y guiones bajos para nombres de archivos;

Documentación
-------------

* Agrega los bloques PHPDoc para todas las clases, métodos y funciones;

* Las anotaciones `@package` y `@subpackage` no son utilizadas.
